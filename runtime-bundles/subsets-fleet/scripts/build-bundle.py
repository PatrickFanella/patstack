#!/usr/bin/env python3
"""Build the Subsets fleet deployment folder from a clean codex-skills commit.

The folder holds this adapter's scripts and README, the source installer and
profile selector, and the catalog, library, profiles and shared trees, with a
manifest of every file's snapshot. Copy it to a host and run its
scripts/deploy-host.py there.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
import install  # noqa: E402

TREES = ('catalog', 'library', 'profiles', 'shared')


def build(out):
    if subprocess.check_output(['git', 'status', '--porcelain', '--', *TREES, 'scripts', 'runtime-bundles'],
                               cwd=ROOT, text=True).strip():
        raise RuntimeError('Commit the source before building a deployment bundle.')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    out = Path(out) if out else Path.home() / '.local/share/subsets-fleet' / ('source-' + revision[:12])
    if out.exists():
        raise RuntimeError('Bundle already exists: ' + str(out))
    ignore = shutil.ignore_patterns('__pycache__', '*.pyc')
    adapter = ROOT / 'runtime-bundles/subsets-fleet'
    (out / 'scripts').mkdir(parents=True)
    shutil.copy2(adapter / 'README.md', out / 'README.md')
    for script in (adapter / 'scripts').iterdir():
        if script.is_file() and script.name != 'build-bundle.py':
            shutil.copy2(script, out / 'scripts' / script.name)
    shutil.copy2(ROOT / 'scripts/install.py', out / 'scripts/install.py')
    shutil.copy2(ROOT / 'scripts/skill-profile', out / 'scripts/profile-selector')
    for tree in TREES:
        shutil.copytree(ROOT / tree, out / tree, ignore=ignore)
    files = {str(p.relative_to(out)): install.snapshot(p) for p in sorted(out.rglob('*')) if p.is_file()}
    install.save(out / 'deployment-source.json', {'sourceRevision': revision, 'sourceOwner': str(ROOT), 'files': files})
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', help='destination folder (default ~/.local/share/subsets-fleet/source-<rev12>)')
    print(build(parser.parse_args().out))
