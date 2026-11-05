"""Prove receipt-backed migration, cross-client selection and recovery."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stack_installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class UnifiedStackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.source = self.home / 'source'
        shutil.copytree(ROOT / 'runtime-bundles/subsets-fleet', self.source)
        shutil.copy2(ROOT / 'scripts/install.py', self.source / 'scripts/install.py')
        config = json.loads((ROOT / 'catalog/skill-stacks.json').read_text())
        self.roots = {k: self.home / v['root'] for k, v in config['clients'].items()}
        self.state = self.home / '.local/state/subsets-fleet/profiles'
        self.records = {}
        for name, scope, prefix in [('base', 'personal', 'skills'), ('shared', 'shared', 'shared'),
                                    ('optional', 'optional', 'library/skills')]:
            path = self.source / prefix / name
            path.mkdir(parents=True)
            (path / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test {name}.\n---\n')
            self.records[name] = {'scope': scope, 'canonicalSource': prefix + '/' + name,
                                  'status': 'selection-tested', 'supportedClients': ['codex', 'claude']}
        (self.source / 'profiles').mkdir()
        (self.source / 'profiles/core.txt').write_text('base\nshared\n')
        (self.source / 'profiles/extra.txt').write_text('optional\n')
        (self.source / 'catalog').mkdir()
        for name, data in [('skill-stacks', config), ('qualification', {'skills': self.records}),
                           ('retired-names', {}), ('local-owners', {}), ('vault-agents', {'files': []})]:
            self.write(self.source / 'catalog' / (name + '.json'), data)
        self.write(self.source / 'deployment-source.json', {'sourceRevision': 'fixture'})
        for root in self.roots.values():
            root.mkdir(parents=True)
        shutil.copytree(self.source / 'skills/base', self.roots['codex'] / 'base')
        shutil.copytree(self.source / 'shared/shared', self.roots['shared'] / 'shared')
        (self.roots['claude'] / 'base').symlink_to(self.roots['codex'] / 'base')
        self.personal = self.home / config['migrationReceipts'][0]
        self.links = self.home / config['migrationReceipts'][1]
        self.write(self.personal, {'paths': {str(self.roots['codex'] / 'base'): installer.snapshot(self.roots['codex'] / 'base'),
                                             str(self.roots['shared'] / 'shared'): installer.snapshot(self.roots['shared'] / 'shared')}})
        self.write(self.links, {'paths': {str(self.roots['claude'] / 'base'): installer.snapshot(self.roots['claude'] / 'base')}})
        self.original = {p: installer.snapshot(p) for p in [self.personal, self.links,
            self.roots['codex'] / 'base', self.roots['shared'] / 'shared', self.roots['claude'] / 'base']}
        # App and system owners are deliberately outside the takeover.
        app = self.home / '.claude/plugins/cache/example/skills/app-tool'
        app.mkdir(parents=True)
        (app / 'SKILL.md').write_text('app-owned')
        (self.roots['copilot'] / 'app-tool').symlink_to(app)
        (self.roots['codex'] / '.system').mkdir()
        (self.roots['codex'] / '.system/marker').write_text('system owner')

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    def cli(self, *args, success=True):
        r = subprocess.run([sys.executable, str(self.source / 'scripts/skill-profile'), *args],
                           env={**os.environ, 'HOME': str(self.home)}, capture_output=True, text=True)
        if success:
            self.assertEqual(r.returncode, 0, r.stderr)
            return json.loads(r.stdout)
        self.assertNotEqual(r.returncode, 0)
        return r

    def test_migration_switch_and_reverse_rollback_restore_owners(self):
        preview = self.cli('plan', 'extra')
        self.assertEqual(len(preview['transferredPaths']), 3)
        self.assertEqual(installer.snapshot(self.personal), self.original[self.personal])
        receipt = self.cli('activate', 'extra')
        self.cli('verify', 'extra')
        for client in ['shared', 'codex', 'claude', 'copilot', 'cursor']:
            for name in ['base', 'shared', 'optional']:
                self.assertTrue((self.roots[client] / name).is_symlink())
        self.assertEqual(json.loads(self.personal.read_text())['paths'], {})
        core = self.cli('deactivate')
        for root in self.roots.values():
            self.assertFalse((root / 'optional').is_symlink())
        self.cli('rollback', '--run', core['run'])
        self.cli('verify', 'extra')
        self.cli('rollback', '--run', receipt['run'])
        for path, before in self.original.items():
            self.assertEqual(installer.snapshot(path), before)
        self.assertFalse((self.state / 'ownership.json').exists())
        self.assertTrue((self.roots['copilot'] / 'app-tool').is_symlink())
        self.assertEqual((self.roots['codex'] / '.system/marker').read_text(), 'system owner')

    def test_predecessor_drift_refuses_before_any_changes(self):
        path = self.roots['codex'] / 'base/SKILL.md'
        path.write_text('unpublished local edit')
        self.cli('activate', success=False)
        self.assertEqual(path.read_text(), 'unpublished local edit')
        self.assertFalse((self.state / 'ownership.json').exists())
        self.assertEqual(installer.snapshot(self.links), self.original[self.links])

    def test_collision_linked_root_and_unknown_stack_are_rejected(self):
        self.cli('activate', 'unknown', success=False)
        collision = self.roots['cursor'] / 'base'
        collision.mkdir()
        (collision / 'SKILL.md').write_text('foreign source')
        self.cli('activate', success=False)
        self.assertEqual((collision / 'SKILL.md').read_text(), 'foreign source')
        shutil.rmtree(collision)
        shutil.rmtree(self.roots['cursor'])
        self.roots['cursor'].symlink_to(self.home / 'elsewhere')
        self.cli('activate', success=False)
        self.assertFalse((self.home / 'elsewhere').exists())

    def test_post_migration_view_drift_blocks_switch_and_rollback(self):
        receipt = self.cli('activate', 'extra')
        link = self.roots['cursor'] / 'optional'
        link.unlink()
        link.mkdir()
        (link / 'SKILL.md').write_text('later user edit')
        self.cli('deactivate', success=False)
        self.cli('rollback', '--run', receipt['run'], success=False)
        self.assertEqual((link / 'SKILL.md').read_text(), 'later user edit')

    def test_receipt_root_escape_and_source_drift_are_rejected(self):
        config_path = self.source / 'catalog/skill-stacks.json'
        config = json.loads(config_path.read_text())
        original = json.loads(config_path.read_text())
        config['clients']['cursor']['root'] = '../outside/skills'
        self.write(config_path, config)
        self.cli('activate', success=False)
        self.write(config_path, original)
        path = self.source / 'skills/base/SKILL.md'
        self.write(self.source / 'deployment-source.json', {
            'sourceRevision': 'fixture', 'files': {'skills/base/SKILL.md': installer.snapshot(path)}})
        path.write_text('edited after review')
        self.cli('activate', success=False)
        self.assertFalse((self.state / 'ownership.json').exists())

    def test_legacy_installer_and_changed_ownership_receipt_are_guarded(self):
        from unittest.mock import patch
        self.cli('activate')
        self.write(self.source / 'catalog/installation.json', {'personalRoot': str(self.roots['codex'])})
        self.write(self.source / 'catalog/baseline.json', {})
        with patch.object(Path, 'home', return_value=self.home):
            with self.assertRaisesRegex(RuntimeError, 'Subsets owns'):
                installer.prepare(self.source, self.home / 'old-state')
        marker = self.state / 'ownership.json'
        data = json.loads(marker.read_text())
        data['transferredPaths'] = []
        self.write(marker, data)
        self.cli('deactivate', success=False)

    def test_all_task_members_are_available_and_every_owner_is_covered(self):
        module = ROOT / 'runtime-bundles/subsets-fleet/scripts'
        import sys
        sys.path.insert(0, str(module))
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import stack_selection
            all_sources = stack_selection.available(ROOT)
            coverage = set()
            for profile in (ROOT / 'profiles').glob('*.txt'):
                names, _ = stack_selection.selection(ROOT, [profile.stem])
                coverage.update(names)
            self.assertEqual(coverage, set(all_sources))
            self.assertEqual(len(stack_selection.selection(ROOT, [])[0]), 40)
        finally:
            sys.path.remove(str(ROOT / 'scripts'))
            sys.path.remove(str(module))

    def test_historical_source_evidence_and_native_links_transfer_without_a_fake_receipt(self):
        module = ROOT / 'runtime-bundles/subsets-fleet/scripts'
        sys.path[:0] = [str(ROOT / 'scripts'), str(module)]
        try:
            from fleet_predecessors import fingerprint
            expected = {prefix + '/' + name: fingerprint(installer.snapshot(self.source / prefix / name))
                        for prefix, name in [('skills', 'base'), ('shared', 'shared')]}
            self.write(self.source / 'catalog/fleet-skill-predecessors.json', {'revisions': {'pinned': expected}})
            receipt = self.home / '.local/state/skill-review-20261103/run/receipt.json'
            self.write(receipt, {'revision': 'pinned', 'current': [str(self.roots['codex'] / 'base'), str(self.roots['shared'] / 'shared')],
                                 'links': [{'from': str(self.roots['claude'] / 'old-base'), 'to': str(self.roots['codex'] / 'base')}]})
            self.personal.unlink()
            self.links.unlink()
            result = self.cli('plan')
            self.assertEqual(len(result['transferredPaths']), 3)
            self.assertTrue(receipt.exists())
            run = self.cli('activate')
            self.cli('verify', 'core')
            self.cli('rollback', '--run', run['run'])
            path = self.roots['codex'] / 'base/SKILL.md'
            path.write_text('later edit')
            self.cli('activate', success=False)
            self.assertEqual(path.read_text(), 'later edit')
        finally:
            sys.path.remove(str(ROOT / 'scripts'))
            sys.path.remove(str(module))

    def test_generated_claude_root_detaches_and_recovers_without_mutating_its_sources(self):
        generated = self.home / '.agents/.generated/skill-profiles/full/skills'
        generated.mkdir(parents=True)
        (generated / 'base').symlink_to(self.roots['codex'] / 'base')
        (generated / 'app-tool').mkdir()
        (generated / 'app-tool/SKILL.md').write_text('application-owned')
        shutil.rmtree(self.roots['claude'])
        self.roots['claude'].symlink_to(generated)
        before = installer.snapshot(generated)
        helper = self.source / 'scripts/prepare-client-root.py'
        def command(*args):
            result = subprocess.run([sys.executable, str(helper), *args], env={**os.environ, 'HOME': str(self.home)}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertTrue(command('plan')['needed'])
        receipt = command('apply')
        self.assertFalse(self.roots['claude'].is_symlink())
        self.assertTrue((self.roots['claude'] / 'app-tool').is_symlink())
        self.assertEqual(installer.snapshot(generated), before)
        command('rollback', '--run', receipt['run'])
        self.assertTrue(self.roots['claude'].is_symlink())
        self.assertEqual(installer.snapshot(generated), before)

    def test_source_fingerprint_accepts_only_the_documented_umask_difference(self):
        module = ROOT / 'runtime-bundles/subsets-fleet/scripts'
        sys.path[:0] = [str(ROOT / 'scripts'), str(module)]
        try:
            from fleet_predecessors import fingerprint
            base = {'type': 'file', 'mode': 0o644, 'sha256': 'same-bytes'}
            self.assertEqual(fingerprint(base), fingerprint({**base, 'mode': 0o664}))
            self.assertNotEqual(fingerprint(base), fingerprint({**base, 'mode': 0o744}))
            self.assertNotEqual(fingerprint(base), fingerprint({**base, 'mode': 0o646}))
            self.assertNotEqual(fingerprint(base), fingerprint({**base, 'sha256': 'different'}))
        finally:
            sys.path.remove(str(ROOT / 'scripts'))
            sys.path.remove(str(module))
