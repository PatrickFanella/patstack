#!/usr/bin/env python3
"""Preview, deploy or verify vault-local agent files without overwriting drift."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def plan(rows):
    changes, errors = [], []
    for row in rows:
        source = ROOT / row['source']
        target = Path(row['destination'])
        if not source.is_file() or source.is_symlink():
            errors.append(f'Invalid source: {source}')
            continue
        if target.is_symlink() or any(p.is_symlink() for p in target.parents):
            errors.append(f'Symlink destination: {target}')
            continue
        wanted, actual = digest(source), digest(target)
        if actual == wanted:
            continue
        if actual != row['previous_sha256'] or (target.exists() and not target.is_file()):
            errors.append(f'Local drift: {target}')
            continue
        changes.append((source, target, actual, wanted))
    return changes, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['plan', 'apply', 'verify'])
    parser.add_argument('--only-destination', action='append', help='Deploy only exact registered paths; preserve normal drift checks')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'catalog/vault-agents.json').read_text())
    if args.only_destination:
        unknown = set(args.only_destination) - {row['destination'] for row in manifest['files']}
        if unknown:
            parser.error('Unknown destinations: ' + ', '.join(sorted(unknown)))
        manifest['files'] = [row for row in manifest['files'] if row['destination'] in args.only_destination]
    changes, errors = plan(manifest['files'])
    print(json.dumps({'mode': args.mode, 'changes': len(changes), 'errors': errors}, indent=2))
    if errors:
        return 1
    if args.mode == 'verify':
        return int(bool(changes))
    if args.mode == 'plan':
        for _, target, _, _ in changes:
            print(target)
        return 0
    if not changes:
        return 0
    backup = Path.home() / '.local/state/vault-agent-deployments' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup.mkdir(parents=True, mode=0o700)
    receipts = []
    for index, (source, target, before, wanted) in enumerate(changes):
        if digest(target) != before or digest(source) != wanted:
            raise SystemExit('Concurrent change; previous writes and backups are in ' + str(backup))
        saved = backup / str(index)
        if before is not None:
            shutil.copy2(target, saved)
            if digest(saved) != before:
                raise SystemExit('Backup verification failed')
        receipts.append({'target': str(target), 'backup': str(saved) if before else None,
                         'before': before, 'after': wanted})
        (backup / 'receipt.json').write_text(json.dumps(receipts, indent=2) + '\n')
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + '.vault-agents-next')
        with temporary.open('xb') as stream:
            stream.write(source.read_bytes())
        temporary.chmod(source.stat().st_mode & 0o777)
        if digest(target) != before:
            temporary.unlink()
            raise SystemExit('Concurrent destination change; backup retained')
        temporary.replace(target)
        if digest(target) != wanted:
            raise SystemExit('Readback verification failed')
    print('Verified backup and deployment receipt: ' + str(backup))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
