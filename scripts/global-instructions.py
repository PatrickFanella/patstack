#!/usr/bin/env python3
"""Render and deploy each host's global agent instructions from instructions/.

One source, three clients: ~/.codex/AGENTS.md, ~/.claude/CLAUDE.md and
~/.config/opencode/AGENTS.md are generated per host from WORKING.md and
hosts.json, along with directory context files (~/.agents/AGENTS.md and any
listed in hosts.json) and, on RTK hosts, ~/.codex/RTK.md and ~/.claude/RTK.md. Deployment is guarded: plan records the current state, apply
refuses anything that changed since, backups and receipts stay on the host,
and rollback restores only files nobody edited after the deploy.
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
CLIENTS = {'codex': '.codex/AGENTS.md', 'claude': '.claude/CLAUDE.md',
           'opencode': '.config/opencode/AGENTS.md'}
# Directory-scoped context files: they apply only to sessions started in that folder.
CONTEXT_FILES = ('.agents/AGENTS.md',)
RTK_FILES = ('.codex/RTK.md', '.claude/RTK.md')
STATE = '.local/state/agent-global-instructions'
# Superseded by inlining WORKING.md; removed only if still the unedited deployed copy.
RETIRED = ('.config/agent-instructions/WORKING.md', '.local/state/agent-working-style/latest.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def render(host, client, revision, source=ROOT / 'instructions'):
    facts = json.loads((source / 'hosts.json').read_text())
    info = facts['hosts'][host]
    home = info['home']
    authoring = facts['authoring']
    expands = client == 'claude'
    homelab = '@' + home + '/.homelab/HOMELAB.md'
    gitea = '@' + home + '/.config/agent-identity/GITEA.md'
    lines = [
        '<!-- Generated for ' + host + ' by codex-skills scripts/global-instructions.py at ' + revision[:12] + '.',
        '     Edit instructions/ in ' + authoring + ' on Kvant and redeploy; hand edits here are refused. -->',
        '# Global agent context (' + host + ')', '']
    if expands:
        lines += [homelab, gitea, '',
                  'HOMELAB above carries the fleet map, this host\'s role and the documentation policy. '
                  'GITEA selects the agent identity for git.subcult.tv.']
    else:
        lines += ['This client does not expand `@` references, so open these files yourself:', '',
                  '- ' + homelab + ' before workspace work: the fleet map, this host\'s role and the documentation policy.',
                  '- ' + gitea + ' before any Gitea write: the agent identity for git.subcult.tv.', '']
    lines += ['Then read the nearest project AGENTS.md.', '']
    host_lines = []
    if info.get('rtk'):
        host_lines.append('Prefix shell commands with `rtk` (`rtk git status`, `rtk pytest -q`). '
                          'Use `rtk proxy <cmd>` when you need raw, unfiltered output.')
    if info.get('vaults'):
        host_lines.append('Vault roots: ' + info['vaults'] + '. Read the target vault\'s root AGENTS.md; '
                          'Machinum\'s `20-operations/Four Vault Setup.md` records ownership.')
    if info.get('blacktowerCodex') and client == 'codex':
        host_lines.append('Use `blacktower-codex:blacktower` at the start of each substantive coding task, '
                          'follow its routing guidance, and prefer Blacktower plugin skills when an equivalent exists.')
    host_lines += info.get('notes', [])
    where = '' if info.get('authoringCheckout') else ' on Kvant'
    host_lines.append('Skill, profile and global-instruction changes are authored in codex-skills (`' + authoring +
                      '`' + where + '); read its AGENTS.md and `docs/OPERATING-MODEL.md`. '
                      'Installed skills and this file are deployment targets.')
    host_lines.append('Load the `unslop` skill once per session and apply it to user-facing prose and documentation edits.')
    host_lines.append('For a requested `grill-me` or `grill-with-docs`, use the matching mode of `requirements-interview`.')
    if client == 'claude':
        host_lines.append('Many fleet skills were written for Codex. When a skill needs a tool Claude Code lacks, '
                          'say so and use a supported equivalent; reading a skill does not install its tools.')
    if client == 'codex':
        host_lines.append('Keep harness or memory markup such as `<oai-mem-citation>` out of replies.')
    lines += ['## This host', ''] + ['- ' + line for line in host_lines] + ['']
    working = (source / 'WORKING.md').read_text().strip().splitlines()
    lines += ['#' + line if line.startswith('#') else line for line in working]
    return '\n'.join(lines).rstrip() + '\n'


def render_context(host, revision, source=ROOT / 'instructions'):
    info = json.loads((source / 'hosts.json').read_text())['hosts'][host]
    lines = [
        '<!-- Generated for ' + host + ' by codex-skills scripts/global-instructions.py at ' + revision[:12] + '. -->',
        '# Homelab infrastructure context', '',
        '@' + info['home'] + '/.homelab/HOMELAB.md', '',
        'If your client does not expand `@` references, open that file yourself. '
        'Your global client file carries the working rules; this file only adds directory context. '
        'Read the nearest more-specific `AGENTS.md` when one exists. Live state overrides documentation.', '']
    if info.get('contextNote'):
        lines += [info['contextNote'], '']
    return '\n'.join(lines)


def render_all(host, revision, source=ROOT / 'instructions'):
    """Every managed file for a host, keyed by path relative to its home."""
    info = json.loads((source / 'hosts.json').read_text())['hosts'][host]
    files = {CLIENTS[c]: render(host, c, revision, source) for c in CLIENTS}
    for relative in CONTEXT_FILES + tuple(info.get('contextFiles', [])):
        files[relative] = render_context(host, revision, source)
    if info.get('rtk'):
        for relative in RTK_FILES:
            files[relative] = (source / 'RTK.md').read_text()
    return files


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
    temp = path.with_name(path.name + '.global-new')
    if temp.exists():
        temp.unlink()
    with open(temp, 'xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temp.chmod(mode)
    os.replace(temp, path)


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}


def retired_targets(home):
    """Old working-style copies that are still exactly what was deployed."""
    receipt = read_json(home / RETIRED[1])
    dest = home / RETIRED[0]
    if dest.is_file() and not dest.is_symlink() and receipt.get('dest') == state(dest):
        return [dest, home / RETIRED[1]]
    return []


def remote(mode, payload, run_dir=None):
    home = Path.home()
    files = {home / relative: text.encode() for relative, text in payload['files'].items()}
    for path, data in files.items():
        if digest(data) != payload['hashes'][str(path.relative_to(home))]:
            raise RuntimeError('Invalid deployment payload.')
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
            path, before = Path(entry['path']), entry['before']
            if path.exists() or path.is_symlink():
                path.unlink()
            if before and 'link' in before:
                path.symlink_to(before['link'])
            elif before:
                shutil.copy2(run / entry['backup'], path)
                path.chmod(before['mode'])
        (receipts / 'latest.json').unlink()
        print(json.dumps({'host': payload['host'], 'rolledBack': str(run)}))
        return

    managed = latest.get('after', {})
    actions = {}
    for path, data in files.items():
        current = state(path)
        if current == {'sha256': digest(data), 'mode': (current or {}).get('mode')}:
            actions[str(path)] = 'unchanged'
        elif str(path) in managed and current != managed[str(path)]:
            raise RuntimeError('Hand-edited since last deploy; move the change into instructions/ first: ' + str(path))
        elif str(path) in managed:
            actions[str(path)] = 'update'
        else:
            actions[str(path)] = 'adopt (replace ' + ('symlink' if current and 'link' in current
                                                      else 'file' if current else 'nothing') + ')'
    for path in retired_targets(home):
        actions[str(path)] = 'remove retired copy'
    before = {p: state(Path(p)) for p in actions}
    summary = {'host': payload['host'], 'sourceRevision': payload['revision'], 'actions': actions}

    if mode == 'plan':
        write(plan_path, json.dumps({'before': before, 'hashes': payload['hashes']}, indent=2).encode(), 0o600)
        print(json.dumps(summary, indent=2))
        return

    if mode == 'apply':
        plan = read_json(plan_path)
        if plan.get('before') != before or plan.get('hashes') != payload['hashes']:
            raise RuntimeError('State changed since plan; re-plan and review.')
        run = receipts / (time.strftime('%Y%m%dT%H%M%S') + '-' + str(time.time_ns() % 10**9))
        run.mkdir(mode=0o700)
        entries = []
        for index, (name, action) in enumerate(actions.items()):
            if action == 'unchanged':
                continue
            path = Path(name)
            entry = {'path': name, 'before': before[name], 'backup': None}
            if path.is_file() and not path.is_symlink():
                entry['backup'] = str(index) + '.private'
                shutil.copy2(path, run / entry['backup'])
                (run / entry['backup']).chmod(0o600)
            if action == 'remove retired copy':
                path.unlink()
            else:
                if path.is_symlink():
                    path.unlink()
                mode_bits = before[name]['mode'] if before[name] and 'mode' in before[name] else 0o644
                write(path, files[path], mode_bits)
            entry['after'] = state(path)
            entries.append(entry)
        write(run / 'receipt.json', json.dumps({'summary': summary, 'files': entries}, indent=2).encode(), 0o600)
        after = {str(p): state(p) for p in files}
        write(receipts / 'latest.json', json.dumps({'run': str(run), 'after': after}, indent=2).encode(), 0o600)
        plan_path.unlink()
        summary['receipt'] = str(run / 'receipt.json')

    if mode in ('apply', 'verify'):
        for path, data in files.items():
            if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
                raise RuntimeError('Deployed file does not match the source: ' + str(path))
        summary['verification'] = 'passed'
        print(json.dumps(summary, indent=2))


def payload_for(host, revision):
    files = render_all(host, revision)
    return {'host': host, 'revision': revision, 'files': files,
            'hashes': {relative: digest(t.encode()) for relative, t in files.items()}}


def remote_source():
    body = Path(__file__).read_text().rsplit('\nif __name__ ==', 1)[0]
    return "__file__='/tmp/global-instructions.py'\n" + body + \
        "\nremote(sys.argv[1], json.load(sys.stdin), sys.argv[2] if len(sys.argv) > 2 else None)\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('mode', choices=('render', 'plan', 'apply', 'verify', 'rollback'))
    p.add_argument('--host', required=True)
    p.add_argument('--file', help='render: one managed path relative to home, such as .codex/AGENTS.md')
    p.add_argument('--run', help='rollback: receipt directory (default: latest)')
    p.add_argument('--python', default='python3')
    args = p.parse_args()
    revision = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True, check=True).stdout.strip()
    if args.mode == 'apply' and subprocess.run(
            ['git', '-C', str(ROOT), 'status', '--porcelain', '--', 'instructions', 'scripts/global-instructions.py'],
            capture_output=True, text=True, check=True).stdout.strip():
        raise RuntimeError('Commit instructions/ and the deploy script before applying.')
    payload = payload_for(args.host, revision)
    if args.mode == 'render':
        for relative, text in payload['files'].items():
            if not args.file or args.file == relative:
                print('===== ' + relative + '\n' + text)
        return
    if args.host == 'kvant' and Path.home() == Path('/home/onnwee') and os.uname().nodename.startswith('kvant'):
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
