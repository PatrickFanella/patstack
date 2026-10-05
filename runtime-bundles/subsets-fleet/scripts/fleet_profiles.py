"""Subsets fleet adapter: manage additions while preserving other skill owners."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

import install

SOURCE = Path(__file__).resolve().parents[1]
HOME = Path.home()
STATE = HOME / '.local/state/subsets-fleet/profiles'


def manager():
    # The original profile selector supplies ownership and qualification filters.
    result = runpy.run_path(str(SOURCE / 'scripts/profile-selector'))
    result.update(SOURCE=SOURCE, LIBRARY=SOURCE / 'library/skills',
                  PROFILES=SOURCE / 'profiles', ACTIVE=HOME / '.agents/skills')
    # Functions retain the runpy namespace, so update their globals too.
    result['selection_for'].__globals__.update(result)
    return result


def proposal(profiles):
    m = manager()
    selected = sorted(m['selection_for'](profiles, False))
    sources = m['sources']()
    previous = install.read(install.statefile(STATE), {'paths': {}})
    desired = {}
    preserved = {}
    excluded = []
    qualification = install.read(SOURCE / 'catalog/qualification.json')['skills']
    active = HOME / '.agents/skills'
    for name in selected:
        dest = str(active / name)
        desired[dest] = (install.snapshot(sources[name]), str(sources[name]))
        if 'claude' in qualification.get(name, {}).get('supportedClients', []):
            link = str(HOME / '.claude/skills' / name)
            desired[link] = ({'type': 'symlink', 'target': dest, 'mode': 0o777}, None)
        else:
            excluded.append(name)
    for dest in previous['paths']:
        if dest == str(STATE / 'selection.json'):
            continue
        desired.setdefault(dest, (None, None))
    ops = []
    for dest, (wanted, source) in sorted(desired.items()):
        path = Path(dest)
        if path.parent not in [active, HOME / '.claude/skills']:
            raise RuntimeError('Unexpected managed destination: ' + dest)
        if any(p.is_symlink() for p in path.parents):
            raise RuntimeError('Linked parent retains its owner: ' + dest)
        actual = install.snapshot(path)
        old = previous['paths'].get(dest)
        if dest not in previous['paths'] and actual is not None:
            # Never claim an existing installation, even when bytes match.
            preserved[dest] = actual
            continue
        if actual != old:
            raise RuntimeError('Preserve local edits before switching: ' + dest)
        ops.append({'destination': dest, 'expected': old, 'desired': wanted,
                    'source': source, 'payload': None, 'group': 1,
                    'action': 'unchanged' if actual == wanted else
                    'retire' if wanted is None else 'link' if source is None else 'install'})
    # Profile state participates in the same transaction and rollback.
    state_path = STATE / 'selection.json'
    payload = json.dumps({'profiles': profiles or ['core'], 'skills': selected},
                         indent=2, sort_keys=True) + '\n'
    import hashlib
    wanted = {'type': 'file', 'mode': 0o600,
              'sha256': hashlib.sha256(payload.encode()).hexdigest()}
    actual = install.snapshot(state_path)
    if str(state_path) in previous['paths'] and actual != previous['paths'][str(state_path)]:
        raise RuntimeError('Selection state changed; preserve it before switching')
    ops.append({'destination': str(state_path), 'expected': actual, 'desired': wanted,
                'source': None, 'payload': payload, 'group': 1,
                'action': 'unchanged' if actual == wanted else 'select'})
    revision = install.read(SOURCE / 'deployment-source.json')['sourceRevision']
    return {'sourceRoot': str(SOURCE), 'sourceRevision': revision,
            'operations': ops, 'protected': preserved, 'previousInstalled': previous,
            'profiles': profiles or ['core'], 'skills': selected,
            'claudeExcluded': excluded, 'restart_session': True}


def activate(profiles):
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (STATE / 'installer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        unfinished = [p for p in STATE.glob('run-*/journal.json')
                      if install.read(p)['status'] in {'applying', 'partial', 'rolling-back'}]
        if unfinished:
            raise RuntimeError('Roll back unfinished transaction: ' + str(unfinished[0].parent))
        plan = proposal(profiles)
        staging = STATE / 'link-sources'
        staging.mkdir(exist_ok=True)
        for i, op in enumerate(plan['operations']):
            if op['desired'] and op['desired']['type'] == 'symlink':
                link = staging / str(i)
                if link.is_symlink():
                    link.unlink()
                elif link.exists():
                    raise RuntimeError('Unexpected link staging content')
                link.symlink_to(op['desired']['target'])
                op['source'] = str(link)
        run = install.apply(plan, STATE)
        install.verify(plan, STATE)
        print(json.dumps({'run': str(run), 'profiles': plan['profiles'],
                          'skills': len(plan['skills']), 'preserved': list(plan['protected']),
                          'restart_session': True}))


def main(client=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'activate', 'apply', 'verify',
                                          'deactivate', 'list', 'status', 'rollback'])
    parser.add_argument('profiles', nargs='*')
    parser.add_argument('--profile', action='append', default=[])
    parser.add_argument('--run', type=Path)
    args = parser.parse_args()
    profiles = sorted(set(args.profiles + args.profile))
    if args.command == 'list':
        print('\n'.join(p.stem for p in sorted((SOURCE / 'profiles').glob('*.txt'))))
    elif args.command == 'status':
        print(json.dumps(install.read(STATE / 'selection.json', {'profiles': ['core']}), indent=2))
    elif args.command == 'rollback':
        if not args.run or args.run.resolve().parent != STATE.resolve():
            parser.error('--run must name a fleet profile transaction')
        with (STATE / 'installer.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            install.rollback(args.run, STATE)
        print(json.dumps({'rolledBack': str(args.run)}))
    elif args.command == 'plan':
        print(json.dumps(proposal(profiles), indent=2))
    elif args.command == 'verify' or (client and args.command == 'apply'):
        plan = proposal(profiles)
        if install.read(STATE / 'selection.json', {}).get('profiles') != (profiles or ['core']):
            raise RuntimeError('Activate the same profile before client verification')
        print(json.dumps(install.verify(plan, STATE)))
    else:
        activate([] if args.command == 'deactivate' else profiles)


if __name__ == '__main__':
    main()
