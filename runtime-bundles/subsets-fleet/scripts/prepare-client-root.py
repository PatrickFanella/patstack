#!/usr/bin/env python3
"""Detach a legacy generated Claude view without changing its backing sources."""
import argparse
import fcntl
import json
import os
import sys
from pathlib import Path

import install


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify', 'rollback'])
    parser.add_argument('--run', type=Path)
    args = parser.parse_args()
    home = Path.home()
    state = home / '.local/state/subsets-fleet/client-root-migration'
    root = home / '.claude/skills'
    if args.command == 'rollback':
        if not args.run or args.run.resolve().parent != state.resolve():
            parser.error('--run must name a client-root migration')
        with (state / 'installer.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            install.rollback(args.run, state)
        print(json.dumps({'rolledBack': str(args.run)}))
        return
    if not root.is_symlink():
        print(json.dumps({'needed': False, 'root': str(root)}))
        return
    target = root.resolve()
    allowed = home / '.agents/.generated/skill-profiles'
    if not target.is_relative_to(allowed) or target.name != 'skills' or not target.is_dir():
        raise RuntimeError('Unrecognized linked client root; retain its owner: ' + str(root))
    expected = install.snapshot(root)
    mask = os.umask(0)
    os.umask(mask)
    link_mode = 0o777 & ~mask if sys.platform == 'darwin' else 0o777
    entries = {}
    for child in target.iterdir():
        # Preserve the first-hop destination, including dangling links and
        # package-owned sources, without following arbitrary link chains.
        destination = os.path.abspath(child.parent / os.readlink(child)) if child.is_symlink() else str(child)
        entries[child.name] = {'type': 'symlink', 'target': destination, 'mode': link_mode}
    desired = {'type': 'directory', 'mode': 0o755, 'entries': entries}
    source = Path(__file__).resolve().parents[1]
    plan = {'sourceRoot': str(source), 'sourceRevision': install.read(source / 'deployment-source.json')['sourceRevision'],
            'operations': [{'destination': str(root), 'expected': expected, 'desired': desired,
                            'source': None, 'payload': None, 'group': 1, 'action': 'detach-generated-view'}],
            'protected': {str(target): install.snapshot(target)},
            'previousInstalled': install.read(install.statefile(state), {'paths': {}})}
    if args.command == 'plan':
        print(json.dumps({'needed': True, 'root': str(root), 'backingSource': str(target), 'entriesPreserved': len(entries)}))
        return
    if args.command == 'verify':
        raise RuntimeError('Generated root is still linked; apply the reviewed migration first')
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state / 'installer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if any(install.read(p)['status'] in {'applying', 'partial', 'rolling-back'} for p in state.glob('run-*/journal.json')):
            raise RuntimeError('Recover the pending client-root transaction first')
        stage = state / 'view-source'
        if stage.exists():
            raise RuntimeError('Review the existing client-root staging directory')
        stage.mkdir(mode=0o755)
        for name, value in entries.items():
            (stage / name).symlink_to(value['target'])
        plan['operations'][0]['source'] = str(stage)
        run = install.apply(plan, state)
        install.verify(plan, state)
        print(json.dumps({'run': str(run), 'root': str(root), 'entriesPreserved': len(entries)}))


if __name__ == '__main__':
    main()
