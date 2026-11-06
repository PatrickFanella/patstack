#!/usr/bin/env python3
"""Audit Gitea package versions against container/Compose references.

This is deliberately a *planning* tool.  It never calls a destructive Gitea,
registry, Docker, database, or filesystem operation.  A version is eligible
only when all conservative gates are true; callers must separately approve and
execute any deletion from the generated JSON list.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
from typing import Any

HOSTS = ("kvant", "almaz", "dozor", "nuc", "soyuz", "sputnik")
GITEA_HOST = "almaz"
GITEA_REGISTRY = "git.subcult.tv"
DEFAULT_RETENTION_DAYS = 180
COMPOSE_REF_RE = r"git\.subcult\.tv/[A-Za-z0-9._/-]+(?::[A-Za-z0-9._-]+|@sha256:[0-9a-fA-F]{64})?"


def run(argv: list[str], *, input_text: str | None = None, timeout: int = 60) -> str:
    p = subprocess.run(argv, input=input_text, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=timeout)
    if p.returncode:
        raise RuntimeError("command failed (%s): %s" % (" ".join(argv[:3]), p.stderr.strip()[:400]))
    return p.stdout


def remote(host: str, program: str, timeout: int = 45) -> str:
    # ssh joins trailing arguments into a remote shell command.  Quote the
    # program ourselves so its newlines and parentheses never become shell.
    command = "python3 -c " + shlex.quote(program)
    return run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", host, command], timeout=timeout)


def package_rows() -> list[dict[str, Any]]:
    # Keep Docker manifests/labels but omit layers and blob paths: audit output
    # remains reviewable and does not duplicate the package store.
    sql = r"""
SELECT json_build_object(
 'type',p.type,'owner',u.name,'name',p.name,'id',pv.id,'version',pv.version,
 'created_unix',pv.created_unix,
 'is_tagged',COALESCE((pv.metadata_json::jsonb->>'is_tagged')::boolean,false),
 'revision',COALESCE(pv.metadata_json::jsonb->'labels'->>'org.opencontainers.image.revision',''),
 'manifests',COALESCE(pv.metadata_json::jsonb->'manifests','[]'::jsonb),
 'manifest_sha256',COALESCE(m.hash_sha256,'')
)::text
FROM package_version pv JOIN package p ON p.id=pv.package_id
JOIN "user" u ON u.id=p.owner_id
LEFT JOIN LATERAL (
 SELECT pb.hash_sha256 FROM package_file pf JOIN package_blob pb ON pb.id=pf.blob_id
 WHERE pf.version_id=pv.id AND pf.name='manifest.json' ORDER BY pf.is_lead DESC LIMIT 1
) m ON true ORDER BY p.type,u.name,p.name,pv.created_unix,pv.id;
"""
    command = "sudo -n docker exec postgres psql -U onnwee -d gitea -At -c " + shlex.quote(sql)
    raw = run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", GITEA_HOST, command], timeout=120)
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


REMOTE_CONTAINERS = r'''
import json, os, re, shutil, subprocess, sys
def call(a):
    try:
        p=subprocess.run(a,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,timeout=20)
        return p.stdout if p.returncode == 0 else None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
docker_path=shutil.which("docker")
if not docker_path:
    for candidate in ("/opt/homebrew/bin/docker", "/usr/local/bin/docker", "/Applications/Docker.app/Contents/Resources/bin/docker"):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            docker_path=candidate; break
docker=[docker_path or "docker"]
if not call(docker+["info"]): docker=["sudo","-n",docker_path or "docker"]
if not call(docker+["info"]):
    raise SystemExit("Docker daemon unavailable or access denied")
raw=call(docker+["ps","-a","--no-trunc","--format","{{json .}}\x1f{{.Label \"com.docker.compose.project.working_dir\"}}\x1f{{.Label \"com.docker.compose.project.config_files\"}}"])
if raw is None: raise SystemExit("container inventory failed")
rows=[]
for line in raw.splitlines():
    encoded, working_dir, config_files = line.split("\x1f", 2)
    c=json.loads(encoded)
    rows.append({"name":c.get("Names",""),"image":c.get("Image", ""),
      "running":c.get("State", "") == "running", "status":c.get("State", ""),
      "image_id":c.get("ImageID", ""), "repo_tags":[], "repo_digests":[],
      "compose_working_dir":working_dir, "compose_config_files":config_files})
raw_images=call(docker+["image","ls","--no-trunc","--digests","--format","{{json .}}"])
if raw_images is None: raise SystemExit("cached image inventory failed")
cached=[]
for line in raw_images.splitlines():
    im=json.loads(line); repo=im.get("Repository", ""); tag=im.get("Tag", ""); digest=im.get("Digest", "")
    tags=[] if repo in ("", "<none>") or tag in ("", "<none>") else [repo+":"+tag]
    digests=[] if repo in ("", "<none>") or not digest.startswith("sha256:") else [repo+"@"+digest]
    cached.append({"image_id":im.get("ID", ""),"repo_tags":tags,"repo_digests":digests})
refs=set()
compose_errors=[]
for row in rows:
    for path in filter(None, row["compose_config_files"].split(",")):
        try:
            if not os.path.isfile(path) or os.path.getsize(path) > 1048576: raise OSError("not a bounded readable file")
            with open(path, errors="replace") as handle: refs.update(re.findall(r"git\.subcult\.tv/[A-Za-z0-9._/-]+(?::[A-Za-z0-9._-]+|@sha256:[0-9a-fA-F]{64})?", handle.read()))
        except OSError as exc: compose_errors.append(path+": "+str(exc))
print(json.dumps({"containers":rows,"cached_images":cached,"compose_refs":sorted(refs),
                  "compose_errors":sorted(set(compose_errors))}))
'''


def host_references(host: str) -> tuple[dict[str, Any], str | None]:
    try:
        value = json.loads(remote(host, REMOTE_CONTAINERS))
        errors = value.get("compose_errors", [])
        return value, ("Compose source unreadable: " + "; ".join(errors[:3])) if errors else None
    except Exception as exc:
        return {"containers": [], "cached_images": [], "compose_refs": []}, str(exc)


def recovery_receipt(path: str | None = None) -> dict[str, Any]:
    """Read only the verified drill receipt; failure is a preservation gate."""
    try:
        selector = ("import glob,json; items=[(p,json.load(open(p))) for p in glob.glob('/mnt/spektr/server/backups/gitea-restore-drills/*/receipt.json')]; "
                    "items=[x for x in items if x[1].get('result')=='passed']; p,x=max(items); x['_receipt_path']=p; print(json.dumps(x))")
        command = "sudo -n cat " + shlex.quote(path) if path else "sudo -n python3 -c " + shlex.quote(selector)
        raw = run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", GITEA_HOST, command], timeout=30)
        value = json.loads(raw)
        receipt_path = value.get("_receipt_path", path)
        restored_dump = str(pathlib.PurePosixPath(receipt_path).parent / "restore" / str(value.get("database_dump", "")).lstrip("/"))
        return {"path": receipt_path, "read": True, "result": value.get("result"),
                "snapshot": value.get("snapshot"), "database_dump": value.get("database_dump"),
                "restored_dump": restored_dump,
                "database_counts": value.get("database_counts")}
    except Exception as exc:
        return {"path": path, "read": False, "error": str(exc)[:400]}


def recovered_package_ids(receipt: dict[str, Any]) -> set[int]:
    """Extract only package_version IDs from the dump used by the passing drill.

    This runs an ephemeral, networkless postgres image with the dump mounted
    read-only. It never opens or modifies the production database.
    """
    dump = receipt.get("restored_dump")
    if not dump:
        return set()
    # A custom-format dump's --table filter can omit TABLE DATA on this
    # PostgreSQL/Gitea combination. Build a restore list selecting exactly the
    # package_version table-data entry instead; no user or credential rows are read.
    extractor = ("set -e; pg_restore -l /dump > /tmp/restore.list; "
                 "sed -i '/TABLE DATA public.package_version/! s/^/;/' /tmp/restore.list; "
                 "pg_restore -L /tmp/restore.list -f - /dump | awk '"
                 "BEGIN { in_copy=0 } /^COPY public.package_version / { in_copy=1; next } "
                 "in_copy && /^\\\\\\./ { exit } in_copy { split($0,a,\"\\t\"); print a[1] }'")
    command = ("sudo -n docker run --rm --network none -v " + shlex.quote(str(dump) + ":/dump:ro") +
               " postgres:17-alpine /bin/sh -c " + shlex.quote(extractor))
    try:
        raw = run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", GITEA_HOST, command], timeout=240)
        ids = {int(line) for line in raw.splitlines() if line.strip().isdigit()}
        expected = int(str(receipt.get("database_counts", "||")).split("|")[2])
        return ids if expected > 0 and len(ids) == expected else set()
    except Exception:
        return set()


def refs_for_version(row: dict[str, Any]) -> set[str]:
    base = f"{GITEA_REGISTRY}/{row['owner']}/{row['name']}"
    v = str(row["version"])
    digest = "sha256:" + v[len("sha256-"):] if v.startswith("sha256-") else v
    refs = {base + ":" + v, base + "@" + digest if digest.startswith("sha256:") else ""}
    for manifest in row.get("manifests") or []:
        if isinstance(manifest, dict):
            digest = manifest.get("digest") or manifest.get("Digest")
            if digest:
                refs.add(base + "@" + str(digest))
    if row.get("manifest_sha256"):
        refs.add(base + "@sha256:" + str(row["manifest_sha256"]))
    return {r.lower() for r in refs if r}


def preservation_reasons(row: dict[str, Any], refs: set[str], deployed_refs: set[str], cutoff: dt.datetime,
                         host_errors: dict[str, str], recovery_ok: bool, covered_ids: set[int]) -> tuple[list[str], list[str]]:
    """Return exact fail-closed reasons and matching retained runtime refs."""
    created = dt.datetime.fromtimestamp(int(row["created_unix"]), tz=dt.timezone.utc)
    matches = sorted(refs & deployed_refs)
    permanent = bool(row.get("is_tagged")) or bool(re.match(r"^(v?\d+\.\d+\.\d+|latest|stable|release)", str(row["version"]), re.I))
    reasons=[]
    if matches: reasons.append("referenced_by_container_or_compose_or_cached_image")
    if permanent: reasons.append("permanent_version_tag")
    if created >= cutoff: reasons.append("within_retention_window")
    if str(row["version"]).endswith((".sig", ".att", ".sbom")): reasons.append("signature_or_attestation_sidecar")
    if host_errors: reasons.append("host_inventory_incomplete")
    if not recovery_ok: reasons.append("recovery_gate_unverified")
    elif int(row["id"]) not in covered_ids:
        reasons.append("not_covered_by_verified_recovery_dump")
    return reasons, matches


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", default=os.path.expanduser("~/.local/state/gitea-package-retention"))
    ap.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)
    ap.add_argument("--recovery-receipt", help="override latest passing drill receipt for diagnosis")
    args = ap.parse_args()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = pathlib.Path(args.output_dir).expanduser() / stamp
    outdir.mkdir(parents=True, mode=0o700)
    os.chmod(outdir, 0o700)
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=args.retention_days)
    recovery = recovery_receipt(args.recovery_receipt)
    covered_ids = recovered_package_ids(recovery) if recovery.get("read") and recovery.get("result") == "passed" else set()
    recovery["covered_package_version_count"] = len(covered_ids)
    recovery_ok = bool(recovery.get("read") and recovery.get("result") == "passed" and
                       recovery.get("snapshot") and recovery.get("database_dump") and covered_ids)
    rows = package_rows()
    containers: dict[str, dict[str, Any]] = {}
    host_errors: dict[str, str] = {}
    deployed_refs: set[str] = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(HOSTS)) as pool:
        inventories = dict(zip(HOSTS, pool.map(host_references, HOSTS)))
    for host, (values, error) in inventories.items():
        containers[host] = values
        if error:
            host_errors[host] = error
        deployed_refs.update(x.lower() for x in values.get("compose_refs", []))
        for value in values.get("containers", []):
            deployed_refs.update(x.lower() for x in value.get("repo_tags", []) + value.get("repo_digests", []))
            # Config.Image preserves a Compose-pinned tag even when Docker did
            # not retain it as a RepoTag.
            deployed_refs.add(str(value.get("image", "")).lower())
        for value in values.get("cached_images", []):
            deployed_refs.update(x.lower() for x in value.get("repo_tags", []) + value.get("repo_digests", []))
    evaluated=[]
    candidates=[]
    for row in rows:
        created = dt.datetime.fromtimestamp(int(row["created_unix"]), tz=dt.timezone.utc)
        refs = refs_for_version(row)
        reasons, matches = preservation_reasons(row, refs, deployed_refs, cutoff, host_errors, recovery_ok, covered_ids)
        eligible = not reasons
        result={**row, "created_at": created.isoformat(), "references": sorted(refs),
                "host_matches": matches, "preservation_reasons": reasons,
                "eligible_for_review": eligible}
        evaluated.append(result)
        if eligible: candidates.append(result)
    report={
      "generated_at": now.isoformat(), "mode": "audit_only", "deletion_performed": False,
      "policy": {"registry": GITEA_REGISTRY, "retention_days": args.retention_days,
        "eligibility": "untagged, older than cutoff, no running or stopped container/Compose reference on every inventoried host, and not a signature/attestation sidecar; this output is still review-only"},
      "recovery_gate": {"required": "passing receipt plus package_version IDs extracted from its read-only database dump", "receipt": recovery, "passed": recovery_ok},
      "host_errors": host_errors, "containers": containers, "versions": evaluated,
      "proposed_deletion_candidates": candidates,
      "summary": {"versions":len(evaluated), "candidates":len(candidates), "protected":len(evaluated)-len(candidates), "hosts_with_errors":len(host_errors)}
    }
    path=outdir / "package-retention-audit.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.chmod(path, 0o600)
    print(json.dumps({"receipt":str(path), **report["summary"], "deletion_performed":False}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
