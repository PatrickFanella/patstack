#!/usr/bin/env python3
"""Deploy a reviewed project skill selection with guarded backups and rollback."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import install

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- managed-project-skills:start -->'
END = '<!-- managed-project-skills:end -->'


def common_dir(root):
    return Path(subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
        text=True).strip()).resolve()


def state_for(root):
    key = hashlib.sha256(str(Path(root).resolve()).encode()).hexdigest()[:20]
    return Path.home() / '.codex/skill-installations/project-selections' / key


def instruction_text(actual, snippet):
    block = START + '\n' + snippet.rstrip() + '\n' + END
    if START in actual or END in actual:
        if actual.count(START) != 1 or actual.count(END) != 1:
            raise RuntimeError('Malformed managed instruction block')
        before, rest = actual.split(START, 1)
        old, after = rest.split(END, 1)
        return before + block + after
    return actual.rstrip() + '\n\n' + block + '\n'


def plan(project, target, source_root=ROOT, state=None):
    source_root = Path(source_root).resolve()
    target = Path(target).absolute()
    if target.is_symlink() or any(p.is_symlink() for p in target.parents):
        raise RuntimeError('Project root must not traverse symlinks')
    config = install.read(source_root / 'catalog/project-selections.json')['projects'][project]
    if common_dir(target) != common_dir(config['canonicalRoot']):
        raise RuntimeError('Target is not a checkout of the registered repository')
    state = Path(state) if state else state_for(target)
    previous = install.read(install.statefile(state), {'paths': {}})
    qualification = install.read(source_root / 'catalog/qualification.json', {'skills': {}})['skills']
    desired = {}
    hashes = {}
    for relative in config['sources']:
        raw_source = source_root / relative
        source = raw_source.resolve()
        if source_root not in source.parents or raw_source.is_symlink() or not (source / 'SKILL.md').is_file():
            raise RuntimeError('Invalid canonical skill source: ' + relative)
        name = source.name
        record = qualification.get(name, {})
        if record.get('status') == 'blocked':
            raise RuntimeError('Blocked skill: ' + name)
        if not set(config['clients']) <= set(record.get('supportedClients', [])):
            raise RuntimeError('Client contract not declared for ' + name)
        destination = target / '.agents/skills' / name
        desired[str(destination)] = {'source': str(source), 'desired': install.snapshot(source)}
        hashes[name] = hashlib.sha256(json.dumps(install.snapshot(source), sort_keys=True).encode()).hexdigest()
        for client, folder in [('claude', '.claude'), ('opencode', '.opencode')]:
            if client in config['clients']:
                desired[str(target / folder / 'skills' / name)] = {
                    'source': None, 'desired': {'type': 'symlink',
                    'target': '../../.agents/skills/' + name, 'mode': 0o777}}
    manifest = {'schemaVersion': 1, 'project': project,
                'authoringSource': str(source_root), 'sources': config['sources'],
                'clients': config['clients'], 'sourceHashes': hashes}
    desired[str(target / '.agent-skills.json')] = {
        'source': None, 'payload': json.dumps(manifest, indent=2) + '\n'}
    agents = target / 'AGENTS.md'
    actual = agents.read_text() if agents.is_file() and not agents.is_symlink() else ''
    snippet = (source_root / config['instructions']).read_text()
    desired[str(agents)] = {'source': None, 'payload': instruction_text(actual, snippet)}
    # Only remove paths previously managed by this project's transaction.
    for destination in previous['paths']:
        if destination not in desired:
            desired[destination] = {'source': None, 'desired': None}
    operations = []
    for destination, item in desired.items():
        path = Path(destination)
        if target not in path.parents or any(p.is_symlink() for p in path.parents):
            raise RuntimeError('Destination escapes project or traverses a symlink: ' + destination)
        relative = str(path.relative_to(target))
        baseline = config.get('rootBaselines', {}).get(str(target), {})
        old = previous['paths'].get(destination,
                    baseline.get(relative, config.get('baseline', {}).get(relative)))
        actual = install.snapshot(path)
        payload = item.get('payload')
        wanted = item.get('desired')
        if payload is not None:
            wanted = {'type': 'file', 'sha256': hashlib.sha256(payload.encode()).hexdigest(),
                      'mode': actual['mode'] if actual and actual['type'] == 'file' else 0o644}
        if actual not in [old, wanted]:
            raise RuntimeError('Project destination drift: ' + destination)
        operations.append({'destination': destination, 'source': item['source'],
            'expected': old, 'desired': wanted, 'payload': payload, 'group': 1,
            'action': 'unchanged' if actual == wanted else 'retire' if wanted is None else 'install'})
    revision = subprocess.check_output(['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True).strip()
    return {'sourceRoot': str(source_root), 'sourceRevision': revision,
            'operations': operations, 'protected': {}, 'previousInstalled': previous}


def summary(proposal):
    return {'sourceRevision': proposal['sourceRevision'], 'operations': [
        {'destination': op['destination'], 'action': op['action']} for op in proposal['operations']]}


def stage_links(proposal, state):
    stage = Path(state) / 'link-sources'; stage.mkdir(parents=True, exist_ok=True)
    for index, op in enumerate(proposal['operations']):
        if op['desired'] and op['desired']['type'] == 'symlink':
            link = stage / str(index)
            if link.is_symlink(): link.unlink()
            elif link.exists(): raise RuntimeError('Unexpected link staging content')
            link.symlink_to(op['desired']['target']); op['source'] = str(link)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify', 'rollback'])
    parser.add_argument('--project', required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--run', type=Path)
    args = parser.parse_args()
    state = state_for(args.root)
    if args.command == 'plan':
        print(json.dumps(summary(plan(args.project, args.root)), indent=2)); return
    if args.command == 'verify':
        print(json.dumps(install.verify(plan(args.project, args.root), state))); return
    state.mkdir(parents=True, exist_ok=True)
    with (state / 'installer.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.command == 'rollback':
            if not args.run or args.run.resolve().parent != state.resolve():
                parser.error('--run must identify this project root\'s transaction')
            install.rollback(args.run, state); return
        pending = [p for p in state.glob('run-*/journal.json') if
                   install.read(p)['status'] in {'applying', 'partial', 'rolling-back'}]
        if pending:
            raise RuntimeError('Roll back unfinished project transaction: ' + str(pending[0].parent))
        proposal = plan(args.project, args.root)
        # Every deployed source and the deployment code must match committed bytes.
        config = install.read(ROOT / 'catalog/project-selections.json')['projects'][args.project]
        paths = ['catalog/project-selections.json', 'catalog/qualification.json',
                 'scripts/project-skills.py', 'scripts/install.py', config['instructions']]
        for relative in config['sources']:
            paths += [str(p.relative_to(ROOT)) for p in (ROOT / relative).rglob('*') if p.is_file()]
        for relative in paths:
            committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'HEAD:' + relative])
            if (ROOT / relative).read_bytes() != committed:
                raise RuntimeError('Commit reviewed source: ' + relative)
        stage_links(proposal, state)
        print(install.apply(proposal, state))


if __name__ == '__main__':
    main()
