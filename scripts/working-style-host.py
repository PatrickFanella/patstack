#!/usr/bin/env python3
"""Guarded per-host deployment of instructions/WORKING.md.

Writes ~/.config/agent-instructions/WORKING.md and appends one import line to
each user-controlled client file (Codex, Claude Code, OpenCode). Client files
that are symlinks belong to their source repository and are left alone.
"""
import argparse
import hashlib
import json
import os
import shlex
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'instructions/WORKING.md'
CLIENT_FILES = ('.codex/AGENTS.md', '.claude/CLAUDE.md', '.config/opencode/AGENTS.md')
DEST = '.config/agent-instructions/WORKING.md'
STATE = '.local/state/agent-working-style'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def state(path):
    if path.is_symlink():
        return {'link': os.readlink(path)}
    if not path.exists():
        return None
    if not path.is_file():
        raise RuntimeError('Expected regular file: ' + str(path))
    return {'sha256': digest(path.read_bytes()), 'mode': stat.S_IMODE(path.stat().st_mode)}


def write(path, data, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.working-style-new')
    with open(temp, 'xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temp.chmod(mode)
    os.replace(temp, path)


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}


def remote(mode, payload, run_dir=None):
    home = Path.home()
    content = payload['content'].encode()
    if digest(content) != payload['sha256']:
        raise RuntimeError('Invalid deployment payload.')
    dest = home / DEST
    reference = '@' + str(dest)
    clients = [home / relative for relative in CLIENT_FILES]
    receipts = home / STATE
    receipts.mkdir(parents=True, exist_ok=True, mode=0o700)
    receipts.chmod(0o700)
    plan_path = receipts / 'plan.json'
    latest = read_json(receipts / 'latest.json')

    if mode == 'rollback':
        run = Path(run_dir) if run_dir else Path(latest.get('run', '/nonexistent'))
        receipt = read_json(run / 'receipt.json')
        if not receipt:
            raise RuntimeError('No receipt at ' + str(run))
        for entry in receipt['files']:
            if state(Path(entry['path'])) != entry['after']:
                raise RuntimeError('Changed since deployment; preserve it: ' + entry['path'])
        for entry in receipt['files']:
            path = Path(entry['path'])
            if entry['before'] is None:
                path.unlink()
            elif entry['changed']:
                shutil.copy2(run / entry['backup'], path)
                path.chmod(entry['before']['mode'])
        print(json.dumps({'host': payload['host'], 'rolledBack': str(run)}))
        return

    # A destination that differs from what we last deployed is someone else's edit.
    current = state(dest)
    if current and current.get('sha256') != digest(content):
        if current != latest.get('dest'):
            raise RuntimeError('Unmanaged or drifted ' + str(dest) + '; reconcile it into the source first.')
    actions = {}
    for path in clients:
        s = state(path)
        if s and 'link' in s:
            actions[str(path)] = 'source-managed symlink; skipped'
        elif s and reference in path.read_text():
            actions[str(path)] = 'import present'
        else:
            actions[str(path)] = 'append import' if s else 'create with import'
    before = {str(p): state(p) for p in [dest, *clients]}
    summary = {'host': payload['host'], 'sourceRevision': payload['revision'],
               'sha256': payload['sha256'], 'dest': str(dest),
               'destAction': 'unchanged' if current == {'sha256': payload['sha256'], 'mode': 0o644} else 'write',
               'clients': actions}

    if mode == 'plan':
        write(plan_path, json.dumps({'before': before, 'summary': summary}, indent=2).encode(), 0o600)
        print(json.dumps(summary, indent=2))
        return

    if mode == 'apply':
        plan = read_json(plan_path)
        if plan.get('before') != before or plan.get('summary', {}).get('sha256') != payload['sha256']:
            raise RuntimeError('State changed since plan; re-plan and review.')
        run = receipts / (time.strftime('%Y%m%dT%H%M%S') + '-' + str(time.time_ns() % 10**9))
        run.mkdir(mode=0o700)
        files = []
        targets = [(dest, None)] + [(p, actions[str(p)]) for p in clients]
        for index, (path, action) in enumerate(targets):
            if action in ('source-managed symlink; skipped', 'import present'):
                continue
            entry = {'path': str(path), 'before': state(path), 'backup': None}
            if path.is_file():
                entry['backup'] = str(index) + '.private'
                shutil.copy2(path, run / entry['backup'])
                (run / entry['backup']).chmod(0o600)
            if action is None:
                write(path, content, 0o644)
            else:
                text = path.read_text() if path.exists() else ''
                mode_bits = entry['before']['mode'] if entry['before'] else 0o644
                write(path, (text.rstrip() + '\n\n' + reference + '\n').lstrip('\n').encode(), mode_bits)
            entry['after'] = state(path)
            entry['changed'] = entry['before'] != entry['after']
            files.append(entry)
        receipt = {'summary': summary, 'files': files, 'completedAt': time.time()}
        write(run / 'receipt.json', json.dumps(receipt, indent=2).encode(), 0o600)
        write(receipts / 'latest.json', json.dumps({'run': str(run), 'dest': state(dest)}, indent=2).encode(), 0o600)
        plan_path.unlink()
        summary['receipt'] = str(run / 'receipt.json')

    if mode in ('apply', 'verify'):
        if dest.read_bytes() != content:
            raise RuntimeError('Deployed WORKING.md does not match the source.')
        for path in clients:
            if path.is_symlink():
                continue
            if not path.exists() or reference not in path.read_text():
                raise RuntimeError('Import missing from ' + str(path))
        summary['verification'] = 'passed'
        print(json.dumps(summary, indent=2))


def remote_source():
    body = Path(__file__).read_text().rsplit('\nif __name__ ==', 1)[0]
    return "__file__='/tmp/working-style-host.py'\n" + body + \
        "\nremote(sys.argv[1], json.load(sys.stdin), sys.argv[2] if len(sys.argv) > 2 else None)\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('mode', choices=('plan', 'apply', 'verify', 'rollback'))
    p.add_argument('--host', required=True)
    p.add_argument('--run', help='rollback: receipt directory (default: latest)')
    p.add_argument('--python', default='python3')
    args = p.parse_args()
    revision = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', str(ROOT), 'status', '--porcelain', '--', str(SOURCE)],
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty and args.mode == 'apply':
        raise RuntimeError('Commit instructions/WORKING.md before applying.')
    content = SOURCE.read_text()
    payload = {'host': args.host, 'revision': revision, 'content': content,
               'sha256': digest(content.encode())}
    if args.host == 'kvant':
        remote(args.mode, payload, args.run)
        return
    command = ' '.join(shlex.quote(x) for x in
                       [args.python, '-c', remote_source(), args.mode] + ([args.run] if args.run else []))
    result = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8', args.host, command],
                            input=json.dumps(payload), text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    print(result.stdout)


if __name__ == '__main__':
    main()
