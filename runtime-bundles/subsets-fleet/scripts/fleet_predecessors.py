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
    return proven, protected, sorted(edited)
