#!/usr/bin/env python3
"""Inspect source qualification records without claiming runtime behavior."""
import argparse
from collections import Counter
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def inspect(root=ROOT):
    registry = json.loads((root / 'catalog/qualification.json').read_text())
    errors = []
    for name, record in registry['skills'].items():
        source = root / record['canonicalSource'] / 'SKILL.md'
        if not source.is_file():
            errors.append('Missing canonical source: ' + name); continue
        try:
            metadata = yaml.safe_load(source.read_text().split('---', 2)[1])
            if metadata['name'] != name: errors.append('Name mismatch: ' + name)
        except (ValueError, KeyError, yaml.YAMLError, TypeError):
            # Unreviewed reservoir defects are visible, not silently qualified.
            errors.append('Invalid source metadata: ' + name)
        for field in ['owner', 'scope', 'status', 'supportedClients', 'requiredTools',
                      'lastReviewed', 'evidence', 'positiveTask', 'nearMiss']:
            if field not in record: errors.append('Missing ' + field + ': ' + name)
        if record['status'] == 'blocked' and not record.get('blockedReason'):
            errors.append('Missing blocked reason: ' + name)
        if record['status'] not in ['unreviewed', 'archived', 'blocked'] and (
                not record['positiveTask'] or not record['nearMiss']):
            errors.append('Missing routing cases: ' + name)
        for relative in record['evidence']:
            if not (root / relative).exists(): errors.append('Missing evidence: ' + name + ': ' + relative)
    return {'counts': dict(Counter(x['status'] for x in registry['skills'].values())),
            'sourceFindings': errors, 'proofPolicy': registry['proofPolicy']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name')
    args = parser.parse_args()
    if args.name:
        print(json.dumps(json.loads((ROOT / 'catalog/qualification.json').read_text())['skills'][args.name], indent=2))
    else:
        print(json.dumps(inspect(), indent=2))


if __name__ == '__main__': main()
