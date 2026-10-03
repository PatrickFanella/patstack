#!/usr/bin/env python3
"""Apply a Gitea agent default on one host; receive its token only over stdin."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import time


URL = "https://git.subcult.tv"
LOGIN = "subcult-agent"
PATTERNS = [
    "https://git.subcult.tv/**", "git@git.subcult.tv:**",
    "git@ssh.git.subcult.tv:**", "ssh://git@git.subcult.tv/**",
    "ssh://git@git.subcult.tv:*/**", "ssh://git@ssh.git.subcult.tv/**",
    "ssh://git@ssh.git.subcult.tv:*/**", "ssh://git@10.0.0.200:2223/**",
]
SSH_PREFIXES = [
    "git@git.subcult.tv:", "git@ssh.git.subcult.tv:",
    "ssh://git@git.subcult.tv/", "ssh://git@ssh.git.subcult.tv/",
    "ssh://git@10.0.0.200:2223/",
] + [f"ssh://git@{host}:{port}/" for host in
     ["git.subcult.tv", "ssh.git.subcult.tv"] for port in [2222, 2223]]


def run(args, *, data=None, env=None, allowed=(0,), timeout=45):
    p = subprocess.run(args, input=data, env=env, text=True,
                       capture_output=True, timeout=timeout)
    if p.returncode not in allowed:
        # Responses and argv may contain credentials; never print either.
        raise RuntimeError(f"{Path(args[0]).name} operation failed ({p.returncode})")
    return p.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def api(tea, path, explicit=True):
    args = [tea, "api"]
    if explicit:
        args += ["--login", LOGIN]
    result = json.loads(run(args + [path]))
    if isinstance(result, dict) and "message" in result and "url" in result:
        raise RuntimeError("Gitea API rejected the request")
    return result


def verify(tea):
    me = api(tea, "/user", explicit=False)
    assert me["login"] == LOGIN and not me["is_admin"]
    credential = run([tea, "login", "helper", "get"],
                     data="protocol=https\nhost=git.subcult.tv\n\n")
    values = dict(line.split("=", 1) for line in credential.splitlines() if "=" in line)
    assert values.get("username") == LOGIN and values.get("password")
    with tempfile.TemporaryDirectory(prefix="gitea-agent-proof-") as td:
        run(["git", "init", "--quiet", td])
        run(["git", "-C", td, "remote", "add", "origin",
             URL + "/subculture-collective/project-template.git"])
        author = run(["git", "-C", td, "var", "GIT_AUTHOR_IDENT"]).strip()
        assert author.startswith("SUBCULT Agent <info@subcult.tv>")
        transport = run(["git", "-C", td, "remote", "get-url", "origin"]).strip()
        assert transport.startswith(URL + "/")
        run(["git", "-C", td, "fetch", "--quiet", "--depth=1", "origin", "HEAD"])
        run(["git", "-C", td, "push", "--dry-run", "origin",
             "FETCH_HEAD:refs/heads/agent-identity-verification"], timeout=60)
    return {"api_login": me["login"], "site_admin": me["is_admin"],
            "credential_login": values["username"], "author": author,
            "https_transport": True, "receive_pack_dry_run": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["apply", "verify"])
    parser.add_argument("--tea", required=True)
    args = parser.parse_args()
    os.umask(0o077)
    if args.mode == "verify":
        print(json.dumps(verify(args.tea)))
        return
    payload = json.load(__import__("sys").stdin)
    home = Path.home()
    state = home / ".local/state/gitea-agent" / ("fleet-" + payload["run_id"])
    state.mkdir(parents=True, exist_ok=False)
    receipt = {"token_id": payload["token_id"], "host": payload["host"], "files": []}

    def backup(path):
        if any(f["path"] == str(path) for f in receipt["files"]):
            return
        entry = {"path": str(path), "before_sha256": digest(path), "backup": None}
        if path.exists():
            target = state / ("before-" + str(len(receipt["files"])))
            shutil.copyfile(path, target)
            entry["backup"] = str(target)
        receipt["files"].append(entry)
        (state / "receipt.json").write_text(json.dumps(receipt, indent=2))

    config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(home / ".config")))
    tea_config = config_home / "tea/config.yml"
    backup(tea_config)
    backup(home / ".gitconfig")
    has_login = False
    try:
        has_login = api(args.tea, "/user")["login"] == LOGIN
    except (RuntimeError, KeyError, json.JSONDecodeError):
        pass
    if not has_login:
        env = os.environ.copy()
        env["GITEA_SERVER_TOKEN"] = payload["token"]
        run([args.tea, "login", "add", "--name", LOGIN, "--url", URL], env=env)
    run([args.tea, "login", "default", LOGIN])
    tea_config.chmod(0o600)

    # Remove only Gitea redirects, retaining unrelated provider configuration.
    redirects = run(["git", "config", "--global", "--get-regexp",
                     r"^url\..*\.insteadof$"], allowed=(0, 1))
    for line in redirects.splitlines():
        key, value = line.split(" ", 1)
        if "git.subcult.tv" in value or value.startswith("ssh://git@10.0.0.200:2223/"):
            run(["git", "config", "--global", "--fixed-value", "--unset-all", key, value])
    for prefix in SSH_PREFIXES:
        run(["git", "config", "--global", "--add", f"url.{URL}/.insteadOf", prefix])
    helper_key = f"credential.{URL}.helper"
    run(["git", "config", "--global", "--replace-all", helper_key, ""])
    run(["git", "config", "--global", "--add", helper_key,
         "!" + shlex.quote(args.tea) + " login helper"])
    run(["git", "config", "--global", f"credential.{URL}.username", LOGIN])

    identity = config_home / "agent-identity"
    identity.mkdir(parents=True, exist_ok=True)
    include = identity / "gitea.gitconfig"
    guidance = identity / "GITEA.md"
    backup(include)
    backup(guidance)
    include.write_text('[user]\n\tname = SUBCULT Agent\n\temail = info@subcult.tv\n'
                       '[commit]\n\tgpgsign = false\n')
    guidance.write_text(payload["instructions"])
    for pattern in PATTERNS:
        run(["git", "config", "--global", "--replace-all",
             f"includeIf.hasconfig:remote.*.url:{pattern}.path", str(include)])
    for relative in [".codex/AGENTS.md", ".claude/CLAUDE.md", ".config/opencode/AGENTS.md"]:
        path = home / relative
        # Managed source links are updated by their owning repository.
        if path.is_symlink():
            continue
        backup(path)
        text = path.read_text() if path.exists() else ""
        reference = "@" + str(guidance)
        if reference not in text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text.rstrip() + "\n\n" + reference + "\n")
    for entry in receipt["files"]:
        entry["after_sha256"] = digest(Path(entry["path"]))
    receipt["verification"] = verify(args.tea)
    receipt["completed_at"] = time.time()
    (state / "receipt.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps({"host": payload["host"], "receipt": str(state / "receipt.json"),
                      "verification": receipt["verification"]}))


if __name__ == "__main__":
    main()
