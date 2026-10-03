import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location('source_link_installer', ROOT / 'scripts/link-workstation.py')
links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(links)


class SourceLinkScopeTests(unittest.TestCase):
    def test_retired_link_is_backed_up_and_rollback_preserves_later_edits(self):
        old_root, old_state = links.ROOT, links.STATE
        self.addCleanup(setattr, links, 'ROOT', old_root)
        self.addCleanup(setattr, links, 'STATE', old_state)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            links.ROOT, links.STATE = root, root / 'state'
            (root / 'catalog').mkdir()
            source = root / 'source'; source.mkdir()
            dest = root / 'retired'; dest.symlink_to(source)
            before = links.install.snapshot(dest)
            (root / 'catalog/workstation-links.json').write_text(json.dumps({
                'links': {}, 'retiredLinks': [str(dest)], 'baseline': {str(dest): before}}))
            import subprocess
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@invalid',
                            'commit', '--allow-empty', '-qm', 'fixture'], check=True)
            plan = links.plan([str(dest)])
            self.assertEqual(plan['operations'][0]['action'], 'retire')
            run = links.install.apply(plan, links.STATE)
            self.assertFalse(dest.is_symlink())
            links.install.verify(links.plan([str(dest)]), links.STATE)
            dest.write_text('later content')
            with self.assertRaisesRegex(RuntimeError, 'intervening edits'):
                links.install.rollback(run, links.STATE)
            self.assertEqual(dest.read_text(), 'later content')
            dest.unlink()
            links.install.rollback(run, links.STATE)
            self.assertEqual(links.install.snapshot(dest), before)
    def test_selected_link_preserves_unrelated_destination_drift(self):
        old_root, old_state = links.ROOT, links.STATE
        self.addCleanup(setattr, links, 'ROOT', old_root)
        self.addCleanup(setattr, links, 'STATE', old_state)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            links.ROOT, links.STATE = root, root / 'state'
            (root / 'catalog').mkdir()
            source = root / 'source'
            source.mkdir()
            selected, unrelated = root / 'selected', root / 'unrelated'
            unrelated.write_text('user content')
            manifest = {'links': {str(selected): str(source), str(unrelated): str(source)},
                        'baseline': {str(selected): None, str(unrelated): None}}
            (root / 'catalog/workstation-links.json').write_text(json.dumps(manifest))
            import subprocess
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@invalid',
                            'commit', '--allow-empty', '-qm', 'fixture'], check=True)
            with self.assertRaisesRegex(RuntimeError, 'Drift'):
                links.plan()
            plan = links.plan([str(selected)])
            self.assertEqual([op['destination'] for op in plan['operations']], [str(selected)])
            self.assertIsNone(plan['operations'][0]['expected'])
            self.assertEqual(unrelated.read_text(), 'user content')
            with self.assertRaisesRegex(RuntimeError, 'Unknown source links'):
                links.plan([str(root / 'missing')])
