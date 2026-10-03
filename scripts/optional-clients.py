#!/usr/bin/env python3
"""Preview/apply Claude links for the reviewed Codex optional profile selection."""
import argparse
import fcntl
import json
from pathlib import Path
import runpy
import subprocess
import install

ROOT = Path(__file__).resolve().parents[1]
STATE = Path.home() / '.codex/skill-installations/optional-client-links'


def plan(profiles, root=ROOT, state=STATE, claude_root=None, manager=None):
    manager = manager or runpy.run_path(str(root / 'scripts/skill-profile'))
    selection = manager['preview'](profiles)['skills']
    qualifications = install.read(root / 'catalog/qualification.json')['skills']
    active = manager['ACTIVE']
    claude_root = claude_root or Path.home() / '.claude/skills'
    previous = install.read(install.statefile(state), {'paths': {}})
    workstation = install.read(root / 'catalog/workstation-links.json')
    desired = {}
    for name in selection:
        record = qualifications.get(name, {})
        if record.get('status') == 'blocked' or 'claude' not in record.get('supportedClients', []):
            raise RuntimeError('Claude contract not qualified: ' + name)
        desired[str(claude_root / name)] = {'type': 'symlink', 'target': str(active / name), 'mode': 0o777}
    for dest in previous['paths']:
        desired.setdefault(dest, None)
    operations = []
    for dest, wanted in desired.items():
        if Path(dest).parent != claude_root or any(p.is_symlink() for p in Path(dest).parents):
            raise RuntimeError('Invalid Claude destination: ' + dest)
        baseline = workstation['baseline'].get(dest)
        if dest in workstation['links']:
            baseline = {'type': 'symlink', 'target': workstation['links'][dest], 'mode': 0o777}
        # Retired global links were explicitly removed by the source-link installer.
        if dest in workstation.get('retiredLinks', []): baseline = None
        old = previous['paths'].get(dest, baseline)
        actual = install.snapshot(dest)
        if actual not in [old, wanted]: raise RuntimeError('Claude destination drift: ' + dest)
        operations.append({'destination': dest, 'expected': old, 'desired': wanted,
            'source': None, 'payload': None, 'group': 1,
            'action': 'unchanged' if actual == wanted else 'retire' if wanted is None else 'link'})
    return {'sourceRoot': str(root), 'sourceRevision': subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
        'selection': selection, 'operations': operations, 'protected': {}, 'previousInstalled': previous}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify', 'rollback'])
    parser.add_argument('--profile', action='append', default=[])
    parser.add_argument('--run', type=Path)
    args = parser.parse_args()
    if args.command == 'plan':
        proposal = plan(args.profile)
        print(json.dumps({'selection': proposal['selection'], 'operations': [
            {'destination': x['destination'], 'action': x['action']} for x in proposal['operations']]}, indent=2)); return
    if args.command == 'verify':
        proposal = plan(args.profile)
        manager = runpy.run_path(str(ROOT / 'scripts/skill-profile'))
        if set(manager['skill_dirs'](manager['ACTIVE'])) != set(proposal['selection']):
            raise RuntimeError('Activate the same Codex profile before verification')
        print(json.dumps(install.verify(proposal, STATE))); return
    STATE.mkdir(parents=True, exist_ok=True)
    with (STATE / 'installer.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.command == 'rollback':
            if not args.run or args.run.resolve().parent != STATE.resolve(): parser.error('--run must be this client transaction')
            install.rollback(args.run, STATE); return
        if any(install.read(p)['status'] in {'partial', 'applying', 'rolling-back'} for p in STATE.glob('run-*/journal.json')):
            raise RuntimeError('Roll back unfinished client transaction first')
        proposal = plan(args.profile)
        for relative in ['catalog/qualification.json', 'catalog/workstation-links.json',
                         'scripts/optional-clients.py', 'scripts/install.py']:
            committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'HEAD:' + relative])
            if (ROOT / relative).read_bytes() != committed:
                raise RuntimeError('Commit reviewed client source: ' + relative)
        manager = runpy.run_path(str(ROOT / 'scripts/skill-profile'))
        if set(manager['skill_dirs'](manager['ACTIVE'])) != set(proposal['selection']):
            raise RuntimeError('Activate the same Codex profile before applying Claude links')
        stage = STATE / 'link-sources'; stage.mkdir(exist_ok=True)
        for i, op in enumerate(proposal['operations']):
            if op['desired'] is None: continue
            link = stage / str(i)
            if link.is_symlink(): link.unlink()
            elif link.exists(): raise RuntimeError('Unexpected staging content')
            link.symlink_to(op['desired']['target']); op['source'] = str(link)
        print(install.apply(proposal, STATE))


if __name__ == '__main__': main()
