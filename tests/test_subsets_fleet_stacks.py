"""test_subsets_fleet scenarios against the stack plan a built bundle runs.

A built bundle always carries catalog/skill-stacks.json, so fleet_profiles.proposal
delegates to stack_selection.plan rather than the profile-selector fallback.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FleetStackProfilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.source = self.home / 'source'
        shutil.copytree(ROOT / 'runtime-bundles/subsets-fleet', self.source)
        shutil.copy2(ROOT / 'scripts/install.py', self.source / 'scripts/install.py')
        shutil.copy2(ROOT / 'scripts/skill-profile', self.source / 'scripts/profile-selector')
        records = {}
        for name, scope, prefix in [('base', 'shared', 'shared'), ('optional', 'optional', 'library/skills')]:
            (self.source / prefix / name).mkdir(parents=True)
            (self.source / prefix / name / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test.\n---\n')
            records[name] = {'scope': scope, 'canonicalSource': prefix + '/' + name,
                             'status': 'selection-tested', 'supportedClients': ['codex', 'claude']}
        (self.source / 'profiles').mkdir()
        for name, content in [('core', 'base'), ('extra', 'optional')]:
            (self.source / 'profiles' / (name + '.txt')).write_text(content + '\n')
        config = json.loads((ROOT / 'catalog/skill-stacks.json').read_text())
        self.roots = {k: self.home / v['root'] for k, v in config['clients'].items()}
        # The fixture skills declare codex/claude support, so OpenCode views are excluded.
        self.views = [root for client, root in self.roots.items() if config['clients'][client]['contract'] != 'opencode']
        (self.source / 'catalog').mkdir()
        for name, data in [('skill-stacks', config), ('qualification', {'skills': records}),
                           ('retired-names', {}), ('local-owners', {}), ('vault-agents', {'files': []})]:
            (self.source / 'catalog' / (name + '.json')).write_text(json.dumps(data))
        (self.source / 'deployment-source.json').write_text(json.dumps({'sourceRevision': 'fixture'}))
        self.active = self.roots['shared']
        (self.active / 'foreign').mkdir(parents=True)
        (self.active / 'foreign/SKILL.md').write_text('foreign package')
        self.state = self.home / '.local/state/subsets-fleet/profiles'

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(self.source / 'scripts/skill-profile'), *args],
                                env={**os.environ, 'HOME': str(self.home)}, text=True, capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def test_preserve_foreign_select_deactivate_and_rollback(self):
        preview = self.run_cli('plan', 'extra')
        self.assertIn(str(self.active / 'foreign'), preview['protected'])
        receipt = self.run_cli('activate', 'extra')
        for root in self.views:
            self.assertEqual((root / 'optional').resolve(), self.source / 'library/skills/optional')
        self.run_cli('verify', 'extra')
        self.assertEqual((self.active / 'foreign/SKILL.md').read_text(), 'foreign package')
        deactivated = self.run_cli('deactivate')
        for root in self.views:
            self.assertFalse((root / 'optional').is_symlink())
            self.assertTrue((root / 'base').is_symlink())
        self.run_cli('rollback', '--run', deactivated['run'])
        self.run_cli('verify', 'extra')
        self.run_cli('rollback', '--run', receipt['run'])
        for root in self.views:
            self.assertFalse((root / 'optional').exists())
        self.assertFalse((self.state / 'ownership.json').exists())
        self.assertEqual((self.active / 'foreign/SKILL.md').read_text(), 'foreign package')

    def test_edited_core_without_a_receipt_is_a_collision_and_nothing_changes(self):
        (self.active / 'base').mkdir()
        (self.active / 'base/SKILL.md').write_text('local edited base')
        result = self.run_cli('activate', 'extra', success=False)
        self.assertIn('Unmanaged collision', result.stderr)
        self.assertEqual((self.active / 'base/SKILL.md').read_text(), 'local edited base')
        self.assertFalse((self.roots['claude'] / 'optional').exists())
        self.assertFalse((self.state / 'ownership.json').exists())

    def test_drift_blocks_switch_and_rollback_without_partial_changes(self):
        receipt = self.run_cli('activate', 'extra')
        link = self.active / 'optional'
        link.unlink()
        link.mkdir()
        (link / 'SKILL.md').write_text('later user edit')
        self.run_cli('deactivate', success=False)
        self.run_cli('rollback', '--run', receipt['run'], success=False)
        self.assertEqual((link / 'SKILL.md').read_text(), 'later user edit')
        self.assertTrue((self.roots['claude'] / 'optional').is_symlink())

    def test_unknown_stack_and_linked_client_root_are_refused(self):
        self.run_cli('activate', 'unknown', success=False)
        elsewhere = self.home / 'elsewhere'
        elsewhere.mkdir()
        (self.home / '.claude').symlink_to(elsewhere)
        result = self.run_cli('activate', 'extra', success=False)
        self.assertIn('Linked or escaping client root', result.stderr)
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertFalse((self.active / 'optional').exists())

    def test_profile_naming_an_unavailable_owner_is_refused(self):
        (self.source / 'profiles/mixed.txt').write_text('curated-owner\noptional\n')
        result = self.run_cli('activate', 'mixed', success=False)
        self.assertIn('unavailable owners: curated-owner', result.stderr)
        self.assertFalse((self.active / 'optional').exists())

    def test_linked_shared_root_is_refused_without_writes(self):
        shutil.rmtree(self.active)
        elsewhere = self.home / 'elsewhere'
        elsewhere.mkdir()
        self.active.symlink_to(elsewhere)
        self.run_cli('activate', 'extra', success=False)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_bundle_modes_do_not_depend_on_checkout_modes_or_umask(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('fixture_build', ROOT / 'runtime-bundles/subsets-fleet/scripts/build-bundle.py')
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        out = self.home / 'bundle'
        (out / 'skills/tool/scripts').mkdir(parents=True)
        files = {'skills/tool/SKILL.md': 0o664, 'skills/tool/notes.md': 0o600, 'skills/tool/scripts/run.sh': 0o700}
        for relative, mode in files.items():
            (out / relative).write_text('x')
            (out / relative).chmod(mode)
        (out / 'skills/tool').chmod(0o750)
        (out / 'skills/tool/link').symlink_to('SKILL.md')
        build.normalize_modes(out)
        modes = {relative: (out / relative).stat().st_mode & 0o777 for relative in files}
        self.assertEqual(modes, {'skills/tool/SKILL.md': 0o644, 'skills/tool/notes.md': 0o644,
                                 'skills/tool/scripts/run.sh': 0o755})
        self.assertEqual((out / 'skills/tool').stat().st_mode & 0o777, 0o755)
        self.assertTrue((out / 'skills/tool/link').is_symlink())


if __name__ == '__main__':
    unittest.main()
