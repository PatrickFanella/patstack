#!/usr/bin/env python3
"""Export the public patstack edition into a generic-skills checkout.

Copies the skills listed in catalog/public-edition.json, applies the listed
substitutions, rewrites Blacktower notices to the public attribution, keeps each
skill's license from the existing public copy, refreshes provenance.json and the
README skill list, and refuses the export if a forbidden pattern remains.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.md', '.txt', '.py', '.sh', '.json', '.yaml', '.yml', '.mjs', '.js', '.ts', '.toml', '.csv', ''}
NOTICE = ('# Blacktower attribution\n\n'
          'Derived Blacktower procedures retain MIT terms. The complete notice is\n'
          'in the repository-level `notices/blacktower-MIT.txt`. The exported skill\n'
          'inputs and licenses are recorded in `provenance.json`.\n')


def move_to_metadata(text, fields):
    # Public frontmatter allows name, description, license, metadata and allowed-tools.
    if not text.startswith('---\n') or not fields:
        return text
    end = text.index('\n---\n', 4)
    lines = text[4:end].split('\n')
    moved, kept = [], []
    for line in lines:
        key = line.split(':', 1)[0]
        (moved if key in fields and not line.startswith(' ') else kept).append(line)
    if not moved:
        return text
    if 'metadata:' not in kept:
        kept.append('metadata:')
    at = kept.index('metadata:') + 1
    while at < len(kept) and kept[at].startswith('  '):
        at += 1
    kept[at:at] = ['  ' + line for line in moved]
    return '---\n' + '\n'.join(kept) + text[end:]


def source_dir(name):
    for base in ('skills', 'shared'):
        if (ROOT / base / name / 'SKILL.md').is_file():
            return ROOT / base / name
    raise SystemExit('Missing source skill: ' + name)


def export(target, check_only=False):
    config = json.loads((ROOT / 'catalog/public-edition.json').read_text())
    retired = json.loads((ROOT / 'catalog/retired-names.json').read_text())
    previous = {row['owner']: old for old, row in retired.items() if row.get('owner')}
    forbidden = [re.compile(p) for p in config['forbidden']]
    out = target / 'skills'
    staged = target / '.skills-export'
    if staged.exists():
        shutil.rmtree(staged)
    errors = []
    for name in config['skills']:
        src = source_dir(name)
        dest = staged / name
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'), symlinks=True)
        # Licenses come from the published copy, under its current or pre-rename name.
        if not any((dest / f).is_file() for f in ('LICENSE', 'LICENSE.txt')):
            found = [d / f for d in (out / name, out / previous.get(name, name))
                     for f in ('LICENSE', 'LICENSE.txt') if (d / f).is_file()]
            if found:
                shutil.copy2(found[0], dest / found[0].name)
            else:
                errors.append('No license for ' + name)
        for path in sorted(dest.rglob('*')):
            if path.is_symlink():
                errors.append('Symlink in export: ' + str(path.relative_to(staged)))
                continue
            if not path.is_file():
                continue
            if path.name == 'blacktower-mit.md' and path.parent.name == 'notices':
                path.write_text(NOTICE)
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue  # binary assets carry no text to substitute or leak-check
            new = text
            if path.name == 'SKILL.md' and path.parent == dest:
                new = move_to_metadata(new, config.get('metadataFields', []))
            if path.suffix in TEXT:
                for before, after in config['substitutions']:
                    new = new.replace(before, after)
            if new != text:
                path.write_text(new)
            for pattern in forbidden:
                for match in pattern.finditer(new):
                    line = new.count('\n', 0, match.start()) + 1
                    errors.append(f'{path.relative_to(staged)}:{line}: forbidden {match.group(0)!r}')
    if errors:
        shutil.rmtree(staged)
        print('\n'.join(errors), file=sys.stderr)
        raise SystemExit(1)
    if check_only:
        shutil.rmtree(staged)
        print(f'Public edition check passed for {len(config["skills"])} skills')
        return
    shutil.rmtree(out)
    staged.rename(out)
    readme = target / 'README.md'
    text = readme.read_text()
    listing = '\n'.join(f'- [`{n}`](skills/{n}/SKILL.md)' for n in sorted(config['skills']))
    text = re.sub(r'(## Included skills\n\n)(?:- \[.*\n)+', lambda m: m.group(1) + listing + '\n', text)
    readme.write_text(text)
    provenance = target / 'provenance.json'
    manifest = json.loads(provenance.read_text())
    rows = {row['name']: row for row in manifest['skills']}
    manifest['skills'] = [{**rows.get(previous.get(n, n), {'origin': 'curated', 'inputs': [n], 'licenses': []}), 'name': n}
                          for n in config['skills']]
    manifest['source_snapshot'] = __import__('subprocess').check_output(
        ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    files = {}
    for path in sorted(target.rglob('*')):
        rel = path.relative_to(target)
        if path.is_file() and rel.parts[0] not in ('.git',) and '__pycache__' not in rel.parts \
                and path.suffix != '.pyc' and path != provenance and rel.parts[0] != 'node_modules':
            files[str(rel)] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest['files'] = files
    provenance.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Exported {len(config["skills"])} skills to {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path, help='generic-skills checkout')
    parser.add_argument('--check', action='store_true', help='stage and leak-check only')
    args = parser.parse_args()
    if not (args.target / 'provenance.json').is_file():
        raise SystemExit('Target is not a generic-skills checkout')
    export(args.target.resolve(), args.check)


if __name__ == '__main__':
    main()
