#!/usr/bin/env python3
"""Resolve qualified skill sources and conditional companions without mutation."""
import argparse
import json
from pathlib import Path
import re


def read(path):
    return json.loads(path.read_text())


def source_root(explicit=None):
    candidates = [explicit] if explicit else [
        (Path.home() / '.agents/bin/skill-profile').resolve().parent.parent,
        (Path.home() / '.agents/skill-library').resolve().parent,
    ]
    for candidate in candidates:
        if candidate and (candidate / 'catalog/qualification.json').is_file():
            return candidate.resolve()
    raise ValueError('No managed skill source found; inspect the Subsets installation')


def memberships(root):
    return {p.stem: {s.strip() for s in p.read_text().splitlines()
                     if s.strip() and not s.lstrip().startswith('#')}
            for p in sorted((root / 'profiles').glob('*.txt'))}


def resolve(root, name, client):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid skill name: ' + name)
    records = read(root / 'catalog/qualification.json')['skills']
    record = records.get(name)
    if not record or record['status'] in {'blocked', 'archived', 'unreviewed'}:
        raise ValueError('Skill is not qualified for routing: ' + name)
    if client not in record['supportedClients']:
        raise ValueError('Skill does not support this client: ' + name)
    if name in read(root / 'catalog/retired-names.json'):
        raise ValueError('Retired skill: ' + name)
    scope = record['scope']
    expected = {'personal': 'skills', 'shared': 'shared', 'optional': 'library/skills'}
    if scope not in expected or record['canonicalSource'] != expected[scope] + '/' + name:
        raise ValueError('Skill has a project, vault, plugin or external owner: ' + name)
    groups = memberships(root)
    if scope == 'optional':
        catalog = read(root / 'catalog/proposed-catalog.json')
        reserved = {r['name'] for r in catalog if r['scope'] != 'optional'}
        reserved.update(read(root / 'catalog/local-owners.json'))
        for row in read(root / 'catalog/vault-agents.json')['files']:
            path = Path(row['source'])
            if path.name == 'SKILL.md' and 'skills' in path.parts:
                reserved.add(path.parent.name)
        if name in reserved or not any(name in names for names in groups.values()):
            raise ValueError('Skill is not an activatable optional owner: ' + name)
    source = root / record['canonicalSource'] / 'SKILL.md'
    boundary = root
    # Subsets bundles carry optional/shared sources; personal owners are installed
    # separately. Never fall back to a different optional or plugin owner.
    if scope == 'personal' and not source.exists():
        boundary = Path.home() / '.codex/skills'
        source = boundary / name / 'SKILL.md'
    path = source.resolve()
    if not path.is_relative_to(boundary.resolve()) or not path.is_file():
        raise ValueError('Missing or escaping source: ' + name)
    # The agent reads full metadata before use; expose common explicit-only flags.
    front = path.read_text().split('---', 2)[1]
    policy = path.parent / 'agents/openai.yaml'
    explicit = bool(re.search(r'^disable-model-invocation:\s*true\s*$', front, re.M))
    if policy.is_file():
        explicit |= bool(re.search(r'^\s*allow_implicit_invocation:\s*false\s*$', policy.read_text(), re.M))
    return {'name': name, 'path': str(path), 'scope': scope,
            'groups': sorted(g for g, names in groups.items() if name in names),
            'status': record['status'], 'explicitOnly': explicit,
            'requiredTools': record['requiredTools']}


def lookup(root, client, *, skill=None, group=None, origin=None):
    if skill:
        return [resolve(root, skill, client)]
    if origin:
        resolve(root, origin, client)
        graph = read(root / 'catalog/skill-routes.json')['skills']
        if origin not in graph:
            raise ValueError('No companion routes recorded for: ' + origin)
        edges = graph[origin]
    else:
        groups = memberships(root)
        if group not in groups:
            raise ValueError('Unknown group: ' + str(group))
        edges = [{'skill': n} for n in sorted(groups[group])]
    result = []
    for edge in edges:
        try:
            row = resolve(root, edge['skill'], client)
        except ValueError as error:
            row = {'name': edge['skill'], 'unavailable': str(error)}
        result.append({**row, **{k: v for k, v in edge.items() if k != 'skill'}})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument('--skill')
    selector.add_argument('--group')
    selector.add_argument('--from', dest='origin')
    parser.add_argument('--client', required=True, choices=['codex', 'claude', 'opencode'])
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    try:
        root = source_root(args.source)
        print(json.dumps({'source': str(root), 'routes': lookup(
            root, args.client, skill=args.skill, group=args.group, origin=args.origin)}, indent=2))
    except (ValueError, KeyError, IndexError, OSError) as error:
        parser.exit(1, 'skill-stack-router: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
