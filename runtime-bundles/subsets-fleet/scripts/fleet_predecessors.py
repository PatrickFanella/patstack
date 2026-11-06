"""Validate historical fleet rename evidence against pinned source trees."""
import hashlib
import json
from pathlib import Path

import install


def fingerprint(tree):
    if tree is None:
        return None
    normalized = dict(tree)
    if tree['type'] != 'symlink':
        # The recorded fleet recipe inherited umask 0002 on some hosts. Preserve
        # full current modes in the transaction; this source-identity check only
        # tolerates that known group-write difference, never executable changes.
        normalized['mode'] &= ~0o020
    if tree['type'] == 'directory':
        normalized['entries'] = {k: normalized_tree(v) for k, v in tree['entries'].items()}
    return hashlib.sha256(json.dumps(normalized, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def normalized_tree(tree):
    result = dict(tree)
    if tree['type'] != 'symlink':
        result['mode'] &= ~0o020
    if tree['type'] == 'directory':
        result['entries'] = {k: normalized_tree(v) for k, v in tree['entries'].items()}
    return result


def managed_entries_match(current, expected):
    """Compare only the entries a detach receipt manages; later additions stay foreign."""
    return (current is not None and current['type'] == 'directory' and current['mode'] == expected['mode']
            and all(current['entries'].get(name) == entry for name, entry in expected['entries'].items()))


def generated_views(home, roots, sources):
    """Use custody from the completed, backed-up root-detachment transaction."""
    state = home / '.local/state/subsets-fleet/client-root-migration'
    receipt = state / 'installed.json'
    if not receipt.exists():
        return {}, {}
    if any(p.is_symlink() for p in [receipt, *receipt.parents]):
        raise RuntimeError('Linked client-root receipt retains its owner')
    data = install.read(receipt)
    if not data.get('run'):
        return {}, {}  # The detachment was rolled back.
    run = Path(data['run'])
    if run.parent != state or any(p.is_symlink() for p in [run, *run.parents]):
        raise RuntimeError('Unexpected client-root migration transaction')
    journal_path = run / 'journal.json'
    journal = install.read(journal_path)
    root = roots['claude']
    expected = data['paths'].get(str(root))
    operations = journal['plan']['operations']
    if (journal['status'] != 'complete' or len(operations) != 1
            or operations[0]['destination'] != str(root)
            or operations[0]['action'] != 'detach-generated-view'
            or operations[0]['desired'] != expected
            or not expected or expected['type'] != 'directory'
            or not managed_entries_match(install.snapshot(root), expected)):
        raise RuntimeError('Client-root migration receipt or view drift; recover it first')
    original = operations[0]['expected']
    backup = run / 'backups/0'
    if (original['type'] != 'symlink' or install.snapshot(backup) != original
            or not (root.parent / original['target']).resolve().is_relative_to(
                home / '.agents/.generated/skill-profiles')):
        raise RuntimeError('Client-root migration backup or predecessor changed')
    proven = {str(root / name): snapshot for name, snapshot in expected['entries'].items()
              if name in sources and snapshot['type'] == 'symlink'}
    return proven, {str(p): install.snapshot(p) for p in [receipt, journal_path, backup]}


def evidence(source, home, roots, sources):
    ledger = install.read(source / 'catalog/fleet-skill-predecessors.json', {'revisions': {}})
    candidates = {}
    links = {}
    protected = {}
    for receipt in sorted((home / '.local/state/skill-review-20261103').glob('*/receipt.json')):
        data = install.read(receipt)
        revision = data.get('revision')
        if revision not in ledger['revisions']:
            continue
        protected[str(receipt)] = install.snapshot(receipt)
        for row in data.get('renamed', []) + data.get('updated', []):
            candidates[row['to']] = revision
        for dest in data.get('current', []):
            candidates[dest] = revision
        for row in data.get('links', []):
            if 'from' in row and 'to' in row:
                target = Path(row['to'])
                links[str(Path(row['from']).parent / target.name)] = str(target)
    proven = {}
    edited = []
    for dest, revision in candidates.items():
        path = Path(dest)
        if path.parent not in roots.values() or path.name not in sources:
            continue
        relative = sources[path.name].relative_to(source).as_posix()
        expected = ledger['revisions'][revision].get(relative)
        actual = install.snapshot(path)
        if expected and actual and actual['type'] == 'directory':
            if fingerprint(actual) == expected:
                proven[dest] = actual
            else:
                edited.append(dest)
    for dest, target in links.items():
        path = Path(dest)
        actual = install.snapshot(path)
        if (path.parent in roots.values() and str(Path(target)) in proven and actual
                and actual['type'] == 'symlink' and actual['target'] == target):
            proven[dest] = actual
    generated, custody = generated_views(home, roots, sources)
    proven.update(generated)
    protected.update(custody)
    return proven, protected, sorted(edited)
