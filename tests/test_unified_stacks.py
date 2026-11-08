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

    def manifest(self):
        # The same file inventory build-bundle.py records for a deployed bundle.
        files = {str(p.relative_to(self.source)): installer.snapshot(p) for p in sorted(self.source.rglob('*'))
                 if p.is_file() and '__pycache__' not in p.parts and p.name != 'deployment-source.json'}
        self.write(self.source / 'deployment-source.json', {'sourceRevision': 'fixture', 'files': files})

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
            self.assertEqual(len(stack_selection.selection(ROOT, [])[0]), 41)
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
        (generated / 'shared').mkdir()
        (generated / 'shared/SKILL.md').write_text('older generated copy with local content')
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
        child = self.roots['claude'] / 'shared'
        child.unlink()
        child.symlink_to(generated / 'app-tool')
        self.cli('activate', success=False)
        child.unlink()
        child.symlink_to(generated / 'shared')
        selection = self.cli('activate')
        self.cli('verify', 'core')
        self.assertEqual((self.roots['claude'] / 'shared').resolve(), self.source / 'shared/shared')
        self.assertEqual(installer.snapshot(generated), before)
        self.cli('rollback', '--run', selection['run'])
        self.assertEqual((self.roots['claude'] / 'shared').resolve(), generated / 'shared')
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

    def test_deploy_preservation_check_recognizes_historical_ownership_transfer(self):
        from unittest.mock import patch
        module = ROOT / 'runtime-bundles/subsets-fleet/scripts'
        sys.path[:0] = [str(ROOT / 'scripts'), str(module)]
        try:
            from fleet_predecessors import fingerprint
            path = self.roots['shared'] / 'optional'
            shutil.copytree(self.source / 'library/skills/optional', path)
            self.write(self.source / 'catalog/fleet-skill-predecessors.json', {'revisions': {
                'pinned': {'library/skills/optional': fingerprint(installer.snapshot(path))}}})
            self.write(self.home / '.local/state/skill-review-20261103/run/receipt.json', {
                'revision': 'pinned', 'current': [str(path)]})
            self.manifest()
            spec = importlib.util.spec_from_file_location('fixture_deploy', self.source / 'scripts/deploy-host.py')
            deploy = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(deploy)
            check_output = subprocess.check_output
            def node_output(args, **kwargs):
                if args[0] != 'fixture-node':
                    return check_output(args, **kwargs)
                if args[-1] == '--version':
                    return '0.2.0-alpha.6\n'
                if args[-2:] == ['groups', '--json']:
                    return json.dumps({'existingProfiles': ['core', 'extra']})
                return json.dumps({'skills': [], 'warnings': []})
            env = {**os.environ, 'HOME': str(self.home)}
            with patch.object(Path, 'home', return_value=self.home), patch.dict(os.environ, env), \
                    patch.object(sys, 'argv', ['deploy-host.py', '--node', 'fixture-node', '--python', sys.executable]), \
                    patch.object(subprocess, 'check_output', side_effect=node_output):
                deploy.main()
            self.assertFalse(path.exists())
            self.assertIn(str(path), json.loads((self.state / 'ownership.json').read_text())['transferredPaths'])
            self.assertTrue((self.roots['copilot'] / 'app-tool').is_symlink())
        finally:
            sys.path.remove(str(ROOT / 'scripts'))
            sys.path.remove(str(module))

    # Recovery paths: later writers, interrupted transactions and reruns.
    def env(self):
        return {**os.environ, 'HOME': str(self.home)}

    def faulted_activate(self, action, phase, dest=None, profiles=()):
        """Run activation in-process and stop it at one installer fault boundary."""
        driver = '\n'.join([
            'import sys', f'sys.path.insert(0, {str(self.source / "scripts")!r})',
            'import install, fleet_profiles', 'real = install.apply',
            'def apply(plan, state, **kw):',
            f'    index = next(i for i, op in enumerate(plan["operations"]) if op["action"] == {action!r}'
            f' and ({dest!r} is None or op["destination"] == {dest!r}))',
            '    def fault(name, i):',
            f'        if name == {phase!r} and i == index: raise SystemExit("injected fault")',
            '    return real(plan, state, fault=fault)',
            'install.apply = apply', f'fleet_profiles.activate({list(profiles)!r})'])
        result = subprocess.run([sys.executable, '-c', driver], env=self.env(), capture_output=True, text=True)
        self.assertIn('injected fault', result.stderr)
        return next(self.state.glob('run-*'))

    def detach_helper(self, *args, umask=None):
        result = subprocess.run([sys.executable, str(self.source / 'scripts/prepare-client-root.py'), *args],
                                env=self.env(), capture_output=True, text=True,
                                preexec_fn=(lambda: os.umask(umask)) if umask is not None else None)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def generated_root(self):
        generated = self.home / '.agents/.generated/skill-profiles/full/skills'
        generated.mkdir(parents=True)
        (generated / 'base').symlink_to(self.roots['codex'] / 'base')
        (generated / 'shared').symlink_to(self.roots['shared'] / 'shared')
        shutil.rmtree(self.roots['claude'])
        self.roots['claude'].symlink_to(generated)
        return generated

    def test_unrelated_entry_in_detached_root_is_preserved_through_activation_and_rollback(self):
        generated = self.generated_root()
        before = installer.snapshot(generated)
        detach = self.detach_helper('apply')
        plugin = self.roots['claude'] / 'new-plugin-skill'
        plugin.mkdir()
        (plugin / 'SKILL.md').write_text('added by a plugin after detachment')
        selection = self.cli('activate')
        self.assertIn(str(plugin), selection['preserved'])
        self.cli('verify', 'core')
        refused = subprocess.run([sys.executable, str(self.source / 'scripts/prepare-client-root.py'),
                                  'rollback', '--run', detach['run']], env=self.env(), capture_output=True, text=True)
        self.assertIn('Subsets ownership transfer', refused.stderr)
        self.cli('rollback', '--run', selection['run'])
        restored = self.detach_helper('rollback', '--run', detach['run'])
        self.assertTrue(self.roots['claude'].is_symlink())
        self.assertEqual(installer.snapshot(generated), before)
        kept = Path(detach['run']) / 'preserved-entries/new-plugin-skill/SKILL.md'
        self.assertEqual(restored['preservedEntries'], [str(kept.parent)])
        self.assertEqual(kept.read_text(), 'added by a plugin after detachment')

    def test_detach_reruns_after_rollback_and_ignores_the_caller_umask(self):
        generated = self.generated_root()
        before = installer.snapshot(self.roots['claude'])
        stage = self.home / '.local/state/subsets-fleet/client-root-migration/view-source'
        for _ in range(2):
            run = self.detach_helper('apply', umask=0o027)['run']
            self.assertFalse(stage.exists())
            self.assertFalse(self.roots['claude'].is_symlink())
            self.detach_helper('rollback', '--run', run, umask=0o027)
            self.assertFalse(stage.exists())
            self.assertEqual(installer.snapshot(self.roots['claude']), before)
        self.assertTrue((generated / 'base').is_symlink())

    def test_takeover_rollback_restores_released_records_beside_later_link_records(self):
        receipt = self.cli('activate')
        later = {str(self.home / '.local/bin/tool'): {'type': 'symlink', 'target': '/elsewhere', 'mode': 0o777}}
        # link-workstation.py re-saves its manifest for its remaining non-skill links.
        installer.save(self.links, {'sourceRevision': 'later', 'run': str(self.links.parent / 'run-later'), 'paths': later})
        self.cli('rollback', '--run', receipt['run'])
        restored = json.loads(self.links.read_text())
        self.assertEqual(restored['paths'], {**later, str(self.roots['claude'] / 'base'): self.original[self.roots['claude'] / 'base']})
        self.assertNotIn('releasedTo', restored)
        for path in [self.personal, self.roots['codex'] / 'base', self.roots['claude'] / 'base']:
            self.assertEqual(installer.snapshot(path), self.original[path])
        # A later claim on a released record is real content: refuse, change nothing.
        receipt = self.cli('activate')
        released = self.links.read_bytes()
        claimed = json.loads(released)
        claimed['paths'][str(self.roots['claude'] / 'base')] = {'type': 'symlink', 'target': '/other', 'mode': 0o777}
        installer.save(self.links, claimed)
        view = installer.snapshot(self.roots['claude'] / 'base')
        self.cli('rollback', '--run', receipt['run'], success=False)
        self.assertEqual(installer.snapshot(self.roots['claude'] / 'base'), view)
        self.links.write_bytes(released)
        self.cli('rollback', '--run', receipt['run'])

    def test_predecessor_rollbacks_refuse_to_reclaim_released_paths(self):
        self.cli('activate')
        old = self.links.parent / 'run-before-takeover'
        self.write(old / 'journal.json', {'status': 'complete', 'progress': {}, 'plan': {
            'operations': [], 'previousInstalled': {'paths': {str(self.roots['claude'] / 'base'): self.original[self.roots['claude'] / 'base']}}}})
        manifest = installer.snapshot(self.links)
        for command in [[str(ROOT / 'scripts/link-workstation.py'), 'rollback', '--run', str(old)],
                        [str(ROOT / 'scripts/install.py'), 'rollback', '--state', str(self.links.parent), '--run', str(old)]]:
            result = subprocess.run([sys.executable, *command], env=self.env(), capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Subsets owns released skill paths', result.stderr)
        self.assertEqual(installer.snapshot(self.links), manifest)

    def test_retired_name_reused_by_another_owner_stays_foreign(self):
        self.cli('activate', 'extra')
        self.cli('deactivate')
        foreign = self.roots['cursor'] / 'optional'
        foreign.mkdir()
        (foreign / 'SKILL.md').write_text('another owner')
        result = self.cli('deactivate')
        self.assertIn(str(foreign), result['preserved'])
        refused = self.cli('activate', 'extra', success=False)
        self.assertIn('Unmanaged collision', refused.stderr)
        self.assertEqual((foreign / 'SKILL.md').read_text(), 'another owner')

    def test_rollback_rechecks_each_path_immediately_before_removal(self):
        from unittest.mock import patch
        target, source, state = self.home / 'target', self.home / 'new', self.home / 'toy-state'
        target.write_text('old')
        source.write_text('new')
        plan = {'sourceRoot': str(self.home), 'sourceRevision': 'toy', 'protected': {}, 'previousInstalled': {'paths': {}},
                'operations': [{'destination': str(target), 'source': str(source), 'expected': installer.snapshot(target),
                                'desired': installer.snapshot(source), 'group': 1, 'payload': None, 'action': 'install'}]}
        run = installer.apply(plan, state)
        save = installer.save
        def edit_after_preflight(path, value):
            save(path, value)
            if isinstance(value, dict) and value.get('rollbackProgress', {}).get('0') == 'restoring':
                target.write_text('user edit')
        with patch.object(installer, 'save', side_effect=edit_after_preflight):
            with self.assertRaisesRegex(RuntimeError, 'intervening edits'):
                installer.rollback(run, state)
        self.assertEqual(target.read_text(), 'user edit')

    def test_failed_staging_leaves_no_stage_and_rollback_removes_a_crashed_one(self):
        from unittest.mock import patch
        target, source, state = self.home / 'target', self.home / 'new', self.home / 'toy-state'
        target.write_text('old')
        source.write_text('new')
        plan = {'sourceRoot': str(self.home), 'sourceRevision': 'toy', 'protected': {}, 'previousInstalled': {'paths': {}},
                'operations': [{'destination': str(target), 'source': str(source), 'expected': installer.snapshot(target),
                                'desired': installer.snapshot(source), 'group': 1, 'payload': None, 'action': 'install'}]}
        copy = installer.copy
        def corrupt_stage(src, dst):
            copy(src, dst)
            if '.stage-' in Path(dst).name:
                Path(dst).write_text('corrupt')
        with patch.object(installer, 'copy', side_effect=corrupt_stage):
            with self.assertRaisesRegex(RuntimeError, 'Staging failed'):
                installer.apply(plan, state)
        self.assertEqual(list(self.home.glob('.target.stage-*')), [])
        run = next(state.glob('run-*'))
        installer.rollback(run, state)
        self.assertEqual(target.read_text(), 'old')
        # A hard crash after staging leaves an entry named for the run in a client root.
        shared = str(self.roots['shared'] / 'base')
        run = self.faulted_activate('link', 'after_remove', dest=shared)
        stage = self.roots['shared'] / ('.base.stage-' + run.name)
        stage.symlink_to(self.source / 'skills/base')
        self.assertNotIn(str(stage), self.cli('plan')['protected'])
        self.cli('rollback', '--run', str(run))
        self.assertFalse(stage.is_symlink())
        for path, before in self.original.items():
            self.assertEqual(installer.snapshot(path), before)

    def test_interrupted_takeover_between_release_and_marker_rolls_back(self):
        run = self.faulted_activate('take-ownership', 'after_backup')
        self.assertEqual(json.loads(self.links.read_text())['paths'], {})
        self.assertFalse((self.state / 'ownership.json').exists())
        refused = self.cli('activate', success=False)
        self.assertIn('Roll back unfinished transaction', refused.stderr)
        self.cli('rollback', '--run', str(run))
        for path, before in self.original.items():
            self.assertEqual(installer.snapshot(path), before)
        self.cli('activate')
        self.cli('verify', 'core')

    def test_older_run_rollback_refuses_while_a_newer_run_exists(self):
        first = self.cli('activate', 'extra')
        second = self.cli('activate', 'extra')
        refused = self.cli('rollback', '--run', first['run'], success=False)
        self.assertIn('newer transaction first', refused.stderr)
        self.cli('verify', 'extra')
        self.cli('rollback', '--run', second['run'])
        self.cli('rollback', '--run', first['run'])
        for path, before in self.original.items():
            self.assertEqual(installer.snapshot(path), before)

    def test_unreviewed_selected_file_and_catalog_or_profile_drift_refuse_activation(self):
        self.manifest()
        added = self.source / 'skills/base/scripts/run.sh'
        added.parent.mkdir()
        added.write_text('#!/bin/sh\necho unreviewed\n')
        self.assertIn('unreviewed file skills/base/scripts/run.sh', self.cli('activate', success=False).stderr)
        shutil.rmtree(added.parent)
        cache = self.source / 'skills/base/__pycache__/helper.cpython-311.pyc'
        cache.parent.mkdir()
        cache.write_bytes(b'bytecode written by running a bundled script')
        cached = self.cli('activate', 'core')
        self.cli('rollback', '--run', cached['run'])
        shutil.rmtree(cache.parent)
        core = self.source / 'profiles/core.txt'
        core.write_text('base\n')
        self.assertIn('profiles/core.txt', self.cli('activate', success=False).stderr)
        core.write_text('base\nshared\n')
        self.write(self.source / 'catalog/extra-owner.json', {})
        self.assertIn('catalog/extra-owner.json', self.cli('activate', success=False).stderr)
        (self.source / 'catalog/extra-owner.json').unlink()
        self.assertFalse((self.state / 'ownership.json').exists())
        self.cli('activate')

    def test_deploy_failure_after_core_activation_reruns_and_rolls_back(self):
        from unittest.mock import patch
        self.manifest()
        spec = importlib.util.spec_from_file_location('fixture_deploy_retry', self.source / 'scripts/deploy-host.py')
        deploy = importlib.util.module_from_spec(spec)
        sys.path[:0] = [str(self.source / 'scripts')]
        self.addCleanup(sys.path.remove, str(self.source / 'scripts'))
        spec.loader.exec_module(deploy)
        check_output = subprocess.check_output
        def run_deploy(groups, stamp):
            def node_output(args, **kwargs):
                if args[0] != 'fixture-node':
                    return check_output(args, **kwargs)
                if args[-1] == '--version':
                    return '0.2.0-alpha.6\n'
                if args[-2:] == ['groups', '--json']:
                    return json.dumps({'existingProfiles': groups})
                return json.dumps({'skills': [], 'warnings': []})
            with patch.object(Path, 'home', return_value=self.home), patch.dict(os.environ, self.env()), \
                    patch.object(sys, 'argv', ['deploy-host.py', '--node', 'fixture-node', '--python', sys.executable]), \
                    patch.object(subprocess, 'check_output', side_effect=node_output), \
                    patch.object(deploy.time, 'strftime', return_value=stamp):
                deploy.main()
        with self.assertRaisesRegex(RuntimeError, 'category readback mismatch'):
            run_deploy(['core'], '20261106T000000Z')
        self.assertTrue((self.state / 'ownership.json').exists())
        run_deploy(['core', 'extra'], '20261106T000001Z')
        self.cli('verify', 'core')
        while run := installer.read(installer.statefile(self.state), {}).get('run'):
            self.cli('rollback', '--run', run)
        for path, before in self.original.items():
            self.assertEqual(installer.snapshot(path), before)
