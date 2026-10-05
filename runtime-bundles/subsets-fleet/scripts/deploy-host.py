#!/usr/bin/env python3
"""Install a reviewed Subsets fleet source and record recoverable host changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import time

import install


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', required=True)
    parser.add_argument('--python', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    home = Path.home()
    metadata = install.read(source / 'deployment-source.json')
    for relative, expected in metadata['files'].items():
        if install.snapshot(source / relative) != expected:
            raise RuntimeError('Source manifest mismatch: ' + relative)
    app = home / '.local/share/subsets-fleet/npm/node_modules/@subcult/subsets/dist/cli.js'
    version = subprocess.check_output([args.node, str(app), '--version'], text=True).strip()
    if version != '0.2.0-alpha.3':
        raise RuntimeError('Unexpected app version: ' + version)
    state = home / '.local/state/subsets-fleet'
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    run = state / ('deploy-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
    run.mkdir(mode=0o700)
    # Preserve every pre-existing shared skill, not only category collisions.
    active = home / '.agents/skills'
    existing = {str(p): install.snapshot(p) for p in active.iterdir()} if active.is_dir() else {}
    profile_cmd = [args.python, str(source / 'scripts/skill-profile')]
    plans = {}
    for profile in sorted(p.stem for p in (source / 'profiles').glob('*.txt')):
        plan = json.loads(subprocess.check_output(profile_cmd + ['plan', profile], text=True))
        plans[profile] = {'selected': len(plan['skills']), 'preserved': list(plan['protected']),
                          'claudeExcluded': plan['claudeExcluded']}
    (run / 'category-plans.json').write_text(json.dumps(plans, indent=2) + '\n')
    subprocess.run(profile_cmd + ['activate', 'core'], check=True, stdout=subprocess.DEVNULL)
    for path, before in existing.items():
        if install.snapshot(path) != before:
            raise RuntimeError('Existing shared skill changed: ' + path)
    operations = []
    def replace(path, *, content=None, target=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        before = install.snapshot(path)
        if target and path.is_symlink() and path.readlink() == target:
            return
        if content is not None and path.is_file() and path.read_text() == content:
            return
        backup = run / ('before-' + str(len(operations)))
        if before is not None:
            install.copy(path, backup)
            if install.snapshot(backup) != before:
                raise RuntimeError('Backup mismatch')
        if install.snapshot(path) != before:
            raise RuntimeError('Concurrent edit: ' + str(path))
        install.remove(path)
        if target:
            path.symlink_to(target)
        else:
            path.write_text(content)
            path.chmod(0o755 if path.name == 'subsets' else before['mode'] if before else 0o644)
        operations.append({'path': str(path), 'before': before, 'backup': str(backup),
                           'after': install.snapshot(path)})
        install.save(run / 'changes.json', operations)
    launcher = '#!/bin/sh\nexport SUBSETS_PYTHON=' + shlex.quote(args.python) + '\nexec ' + shlex.quote(args.node) + ' ' + shlex.quote(str(app)) + ' "$@"\n'
    replace(home / '.local/bin/subsets', content=launcher)
    replace(home / '.agents/bin/skill-profile', target=source / 'scripts/skill-profile')
    # Both interactive and login shells need the user launcher directory.
    shell = Path(os.environ.get('SHELL', '/bin/bash')).name
    rc_files = ['.zshrc', '.zprofile'] if shell == 'zsh' else ['.bashrc', '.bash_profile']
    addition = '\n# Subsets user executables\ncase ":$PATH:" in\n  *":$HOME/.local/bin:"*) ;;\n  *) export PATH="$HOME/.local/bin:$PATH" ;;\nesac\n'
    for name in rc_files:
        rc = home / name
        if rc.is_symlink():
            raise RuntimeError('Shell configuration has another source owner: ' + str(rc))
        content = rc.read_text() if rc.exists() else ''
        if '# Subsets user executables' not in content:
            replace(rc, content=content + addition)
    env = {**os.environ, 'SUBSETS_PYTHON': args.python}
    groups = json.loads(subprocess.check_output([args.node, str(app), 'groups', '--json'], env=env, text=True))
    if set(groups['existingProfiles']) != set(plans):
        raise RuntimeError('Subsets category readback mismatch')
    inventory = json.loads(subprocess.check_output([args.node, str(app), 'discover', '--json'], env=env, text=True))
    subprocess.run(profile_cmd + ['verify', 'core'], check=True, stdout=subprocess.DEVNULL)
    install.save(run / 'receipt.json', {'host': subprocess.check_output(['hostname'], text=True).strip(),
        'source': str(source), 'sourceRevision': metadata['sourceRevision'], 'version': version,
        'categories': sorted(plans), 'discoveredSkills': len(inventory['skills']),
        'discoveryWarnings': inventory['warnings'], 'preservedExistingSharedEntries': len(existing),
        'changes': operations, 'categoryPlans': str(run / 'category-plans.json')})
    print(json.dumps({'receipt': str(run / 'receipt.json'), 'version': version,
                      'categories': len(plans), 'skills': len(inventory['skills']),
                      'warnings': len(inventory['warnings'])}))


if __name__ == '__main__':
    main()
