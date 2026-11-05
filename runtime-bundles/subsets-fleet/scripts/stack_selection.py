"""One Subsets owner for portable user skills and generated client views."""
import hashlib
import json
from pathlib import Path

import install


def available(source):
    registry = install.read(source / 'catalog/qualification.json')['skills']
    retired = install.read(source / 'catalog/retired-names.json', {})
    local = set(install.read(source / 'catalog/local-owners.json', {}))
    for row in install.read(source / 'catalog/vault-agents.json', {'files': []})['files']:
        path = Path(row['source'])
        if path.name == 'SKILL.md' and 'skills' in path.parts:
            local.add(path.parent.name)
    sources = {}
    for name, record in registry.items():
        scope = record['scope']
        prefix = {'personal': 'skills', 'shared': 'shared', 'optional': 'library/skills'}.get(scope)
        if not prefix or name in retired or name in local:
            continue
        if record['status'] in {'archived', 'blocked', 'unreviewed'}:
            continue
        relative = prefix + '/' + name
        path = (source / relative).resolve()
        if record['canonicalSource'] != relative or not path.is_relative_to(source.resolve()):
            continue
        if (path / 'SKILL.md').is_file():
            sources[name] = path
    return sources


def selection(source, profiles):
    sources = available(source)
    selected = set()
    for name in ['core', *profiles]:
        if not name.replace('-', '').isalnum():
            raise RuntimeError('Invalid stack name: ' + name)
        path = source / 'profiles' / (name + '.txt')
        if not path.is_file():
            raise RuntimeError('Unknown stack: ' + name)
        selected.update(s.strip() for s in path.read_text().splitlines()
                        if s.strip() and not s.lstrip().startswith('#'))
    missing = selected - sources.keys()
    if missing:
        raise RuntimeError('Stack has unavailable owners: ' + ', '.join(sorted(missing)))
    return sorted(selected), sources


def text_op(path, actual, payload, action):
    payload = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    desired = {'type': 'file', 'mode': actual['mode'] if actual else 0o600,
               'sha256': hashlib.sha256(payload.encode()).hexdigest()}
    return {'destination': str(path), 'expected': actual, 'desired': desired,
            'source': None, 'payload': payload, 'group': 1,
            'action': 'unchanged' if actual == desired else action}


def plan(source, home, state, profiles, link_mode):
    config = install.read(source / 'catalog/skill-stacks.json')
    selected, sources = selection(source, profiles)
    qualification = install.read(source / 'catalog/qualification.json')['skills']
    previous = install.read(install.statefile(state), {'paths': {}})
    for row in config['clients'].values():
        relative = Path(row['root'])
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Client root must stay under the user home')
    roots = {client: home / row['root'] for client, row in config['clients'].items()}
    if len(set(roots.values())) != len(roots):
        raise RuntimeError('Client roots must be distinct')
    for root in roots.values():
        if not root.is_relative_to(home) or any(p.is_symlink() for p in [root, *root.parents]):
            raise RuntimeError('Linked or escaping client root retains its owner: ' + str(root))
    # Historical installers supply evidence for a one-time ownership transfer.
    # Their exact before-state and the released manifests participate in rollback.
    marker = state / 'ownership.json'
    migrated = marker.exists()
    prior_owners = {}
    manifests = {}
    historical_protected = {}
    preserved_edits = []
    if not migrated:
        for relative in config['migrationReceipts']:
            path = home / relative
            if Path(relative).is_absolute() or '..' in Path(relative).parts or any(p.is_symlink() for p in [path, *path.parents]):
                raise RuntimeError('Predecessor receipt has an external owner: ' + str(path))
            data = install.read(path)
            if data is not None:
                manifests[path] = data
                for dest, expected in data['paths'].items():
                    if expected is not None:
                        prior_owners.setdefault(dest, []).append(expected)
        if (source / 'catalog/fleet-skill-predecessors.json').exists():
            from fleet_predecessors import evidence
            proven, historical_protected, preserved_edits = evidence(source, home, roots, sources)
            for dest, expected in proven.items():
                prior_owners.setdefault(dest, []).append(expected)
    wanted = {}
    excluded = {}
    for name in selected:
        supported = qualification[name]['supportedClients']
        for client, root in roots.items():
            contract = config['clients'][client]['contract']
            if contract == 'shared':
                eligible = 'codex' in supported and 'claude' in supported
            else:
                eligible = contract in supported
            if eligible:
                wanted[str(root / name)] = {'type': 'symlink', 'target': str(sources[name]), 'mode': link_mode}
            else:
                excluded.setdefault(client, []).append(name)
    # Retire recorded views for deselected skills, and migrate only known source
    # names with matching predecessor receipts. Unknown/app-owned entries stay put.
    candidates = set(wanted)
    for dest in previous['paths']:
        if Path(dest).parent in roots.values():
            candidates.add(dest)
    if not migrated:
        for dest in prior_owners:
            if Path(dest).parent in roots.values() and Path(dest).name in sources:
                candidates.add(dest)
    operations = []
    transferred = set()
    for dest in sorted(candidates):
        path = Path(dest)
        if path.parent not in roots.values() or path.name.startswith('.'):
            raise RuntimeError('Unexpected managed destination: ' + dest)
        actual = install.snapshot(path)
        if dest in previous['paths']:
            expected = previous['paths'][dest]
            if actual != expected:
                raise RuntimeError('Preserve local edits before switching: ' + dest)
        elif actual is None:
            expected = None
        elif not migrated and actual in prior_owners.get(dest, []):
            expected = actual
            transferred.add(dest)
        else:
            raise RuntimeError('Unmanaged collision; preserve and review before adoption: ' + dest)
        desired = wanted.get(dest)
        operations.append({'destination': dest, 'expected': expected, 'desired': desired,
                           'source': None, 'payload': None, 'group': 1,
                           'action': 'unchanged' if actual == desired else 'retire' if desired is None else 'link'})
    protected = dict(historical_protected)
    metadata = install.read(source / 'deployment-source.json')
    for relative, expected in metadata.get('files', {}).items():
        path = source / relative
        if any(path.is_relative_to(sources[name]) for name in selected):
            if install.snapshot(path) != expected:
                raise RuntimeError('Selected source drift: ' + relative)
            protected[str(path)] = expected
    for root in roots.values():
        if root.is_dir():
            for path in root.iterdir():
                if str(path) not in candidates:
                    protected[str(path)] = install.snapshot(path)
    if not migrated:
        # A path recorded by the old fleet adapter is already owned by Subsets;
        # transfer its other predecessor records too, when their bytes match.
        transferred.update(dest for dest in candidates if dest in prior_owners)
        for path, data in manifests.items():
            released = sorted(set(data['paths']) & transferred)
            if released:
                for dest in released:
                    if data['paths'][dest] is not None and install.snapshot(dest) != data['paths'][dest]:
                        raise RuntimeError('Predecessor receipt drift: ' + dest)
                replacement = {**data, 'paths': {k: v for k, v in data['paths'].items() if k not in released},
                               'releasedTo': str(marker)}
                operations.append(text_op(path, install.snapshot(path), replacement, 'release-owner'))
        operations.append(text_op(marker, None, {'owner': 'subsets', 'schemaVersion': 1,
            'roots': {k: str(v) for k, v in roots.items()}, 'transferredPaths': sorted(transferred),
            'preservedLocalEdits': preserved_edits}, 'take-ownership'))
    else:
        ownership = install.read(marker)
        if ownership.get('owner') != 'subsets' or ownership['roots'] != {k: str(v) for k, v in roots.items()}:
            raise RuntimeError('Subsets ownership mapping changed; migrate it explicitly')
        if install.snapshot(marker) != previous['paths'].get(str(marker)):
            raise RuntimeError('Subsets ownership receipt changed; preserve it before switching')
        protected[str(marker)] = install.snapshot(marker)
    selection_path = state / 'selection.json'
    actual = install.snapshot(selection_path)
    if str(selection_path) in previous['paths'] and actual != previous['paths'][str(selection_path)]:
        raise RuntimeError('Selection state changed; preserve it before switching')
    operations.append(text_op(selection_path, actual,
                              {'profiles': profiles or ['core'], 'skills': selected}, 'select'))
    return {'sourceRoot': str(source), 'sourceRevision': install.read(source / 'deployment-source.json')['sourceRevision'],
            'operations': operations, 'protected': protected, 'previousInstalled': previous,
            'profiles': profiles or ['core'], 'skills': selected, 'clientExcluded': excluded,
            'claudeExcluded': excluded.get('claude', []), 'transferredPaths': sorted(transferred),
            'managedClients': list(roots), 'restart_session': True}
