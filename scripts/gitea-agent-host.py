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
import sys
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


def run(args, *, data=None, env=None, cwd=None, allowed=(0,), timeout=45):
    p = subprocess.run(args, input=data, env=env, text=True,
                       cwd=cwd, capture_output=True, timeout=timeout)
    if p.returncode not in allowed:
        # Responses and argv may contain credentials; never print either.
        raise RuntimeError(f"{Path(args[0]).name} operation failed ({p.returncode})")
    return p.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def api(tea, path, explicit=True, cwd=None):
    args = [tea, "api"]
    if explicit:
        args += ["--login", LOGIN]
    result = json.loads(run(args + [path], cwd=cwd))
    if isinstance(result, dict) and "message" in result and "url" in result:
        raise RuntimeError("Gitea API rejected the request")
    return result


def verify(tea, require_repository_context=True):
    me = api(tea, "/user", explicit=False)
    assert me["login"] == LOGIN
    credential = run(["git", "credential", "fill"],
                     data="protocol=https\nhost=git.subcult.tv\n\n")
    values = dict(line.split("=", 1) for line in credential.splitlines() if "=" in line)
    assert values.get("username") == LOGIN and values.get("password")
    with tempfile.TemporaryDirectory(prefix="gitea-agent-proof-") as td:
        run(["git", "init", "--quiet", td])
        run(["git", "-C", td, "remote", "add", "origin",
             URL + "/subculture-collective/project-template.git"])
        context_identity = api(tea, "/user", explicit=False, cwd=td)
        if require_repository_context:
            assert context_identity["login"] == LOGIN
        author = run(["git", "-C", td, "var", "GIT_AUTHOR_IDENT"]).strip()
        assert author.startswith("SUBCULT Agent <info@subcult.tv>")
        transport = run(["git", "-C", td, "remote", "get-url", "origin"]).strip()
        assert transport.startswith(URL + "/")
        run(["git", "-C", td, "fetch", "--quiet", "--depth=1", "origin", "HEAD"])
        run(["git", "-C", td, "push", "--dry-run", "origin",
             "FETCH_HEAD:refs/heads/agent-identity-verification"], timeout=60)
    return {"api_login": me["login"], "site_admin": me["is_admin"],
            "credential_login": values["username"], "author": author,
            "repository_context_login": context_identity["login"],
            "https_transport": True, "receive_pack_dry_run": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["apply", "normalize", "verify"])
    parser.add_argument("--tea", required=True)
    args = parser.parse_args()
    os.umask(0o077)
    if args.mode == "verify":
        print(json.dumps(verify(args.tea)))
        return
    payload = json.load(sys.stdin)
    home = Path.home()
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(home / ".config")))
    tea_config = config_home / "tea/config.yml"
    if sys.platform == "darwin" and not os.environ.get("XDG_CONFIG_HOME"):
        tea_config = home / "Library/Application Support/tea/config.yml"
    state = home / ".local/state/gitea-agent" / ("fleet-" + payload["run_id"])
    state.mkdir(parents=True, exist_ok=True)
    receipt_path = state / "receipt.json"
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {
        "token_id": payload["token_id"], "host": payload["host"], "files": []}
    if args.mode == "normalize":
        assert digest(tea_config) == payload["expected_config_sha256"]
        config = payload["tea_config"]
        assert config["logins"][0]["name"] == LOGIN and config["logins"][0]["default"]
        snapshot = state / "before-context-normalization.yml"
        if not snapshot.exists():
            shutil.copyfile(tea_config, snapshot)
        tea_config.write_text(json.dumps(config, indent=2))
        tea_config.chmod(0o600)
        for entry in receipt["files"]:
            if entry["path"] == str(tea_config):
                entry["after_sha256"] = digest(tea_config)
        receipt["verification"] = verify(args.tea)
        receipt["context_verification_pending"] = False
        receipt["context_normalization_completed_at"] = time.time()
        receipt_path.write_text(json.dumps(receipt, indent=2))
        print(json.dumps({"host": payload["host"], "verification": receipt["verification"]}))
        return
    if receipt.get("completed_at"):
        raise RuntimeError("Deployment already completed; use verify")

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
    identity = config_home / "agent-identity"
    identity.mkdir(parents=True, exist_ok=True)
    isolated = identity / "tea"
    isolated.mkdir(parents=True, exist_ok=True)
    isolated_config = isolated / "config.yml"
    backup(isolated_config)
    # JSON is valid YAML; no additional parser dependency is needed on the host.
    isolated_config.write_text(json.dumps({"logins": [{"name": LOGIN, "url": URL,
        "token": payload["token"], "default": True, "user": LOGIN,
        "ssh_host": "git.subcult.tv"}], "preferences": {}}))
    isolated_config.chmod(0o600)
    helper_key = f"credential.{URL}.helper"
    run(["git", "config", "--global", "--replace-all", helper_key, ""])
    run(["git", "config", "--global", "--add", helper_key,
         "!XDG_CONFIG_HOME=" + shlex.quote(str(identity)) + " " +
         shlex.quote(args.tea) + " login helper"])
    run(["git", "config", "--global", f"credential.{URL}.username", LOGIN])
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
    receipt["verification"] = verify(args.tea, require_repository_context=False)
    receipt["context_verification_pending"] = (
        receipt["verification"]["repository_context_login"] != LOGIN)
    receipt["completed_at"] = time.time()
    (state / "receipt.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps({"host": payload["host"], "receipt": str(state / "receipt.json"),
                      "verification": receipt["verification"]}))


if __name__ == "__main__":
    main()
