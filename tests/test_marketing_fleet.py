import importlib.util
import base64
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('marketing_fleet', ROOT/'scripts/marketing-fleet.py')
fleet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fleet)


class MarketingFleetTests(unittest.TestCase):
    def payload(self):
        return {'sourceRoot': str(ROOT), 'sourceRevision': 'fixture',
                'installer': (ROOT/'scripts/install.py').read_text(),
                'destinations': {'.agents/skills/prepare-product-launch': {'files': {
                    'SKILL.md': base64.b64encode(b'fixture skill').decode()}},
                    '.claude/skills/prepare-product-launch': {'link': '.agents/skills/prepare-product-launch'},
                    'Work/Research/Marketing-Packets/2026-10-19': {'files': {
                        'README.md': base64.b64encode(b'fixture packet').decode()}}}}

    def test_apply_verify_idempotency_and_rollback_preserve_unrelated(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            sentinel = home/'unrelated'; sentinel.write_text('keep')
            payload = self.payload()
            fleet.receive('plan', payload, home)
            fleet.receive('apply', payload, home)
            self.assertEqual(fleet.receive('verify', payload, home)['verified'], 3)
            repeat = fleet.receive('plan', payload, home)
            self.assertTrue(all(o['action']=='unchanged' for o in repeat['operations']))
            fleet.receive('rollback', payload, home)
            self.assertFalse((home/'.agents/skills/prepare-product-launch').exists())
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_drift_between_preview_and_apply_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); payload = self.payload()
            fleet.receive('plan', payload, home)
            dest = home/'.agents/skills/prepare-product-launch'
            dest.mkdir(parents=True); (dest/'SKILL.md').write_text('user edit')
            with self.assertRaisesRegex(RuntimeError, 'Drift'):
                fleet.receive('apply', payload, home)
            self.assertEqual((dest/'SKILL.md').read_text(), 'user edit')
            self.assertFalse((home/'Work/Research/Marketing-Packets/2026-10-19').exists())

    def test_unmanaged_root_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); payload = self.payload()
            dest = home/'.agents/skills/prepare-product-launch'
            dest.mkdir(parents=True); (dest/'SKILL.md').write_text('other owner')
            with self.assertRaisesRegex(RuntimeError, 'retains its owner'):
                fleet.receive('plan', payload, home)
            self.assertEqual((dest/'SKILL.md').read_text(), 'other owner')

    def test_subsets_owned_skill_roots_are_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); payload = self.payload()
            marker = home/'.local/state/subsets-fleet/profiles/ownership.json'
            marker.parent.mkdir(parents=True)
            marker.write_text(json.dumps({'owner': 'subsets', 'roots': {
                'shared': str(home/'.agents/skills'), 'claude': str(home/'.claude/skills')}}))
            result = fleet.receive('plan', payload, home)
            self.assertEqual([o['destination'] for o in result['operations']],
                             [str(home/'Work/Research/Marketing-Packets/2026-10-19')])
            fleet.receive('apply', payload, home)
            self.assertFalse((home/'.agents/skills/prepare-product-launch').exists())
            self.assertFalse((home/'.claude/skills/prepare-product-launch').is_symlink())
            self.assertTrue((home/'Work/Research/Marketing-Packets/2026-10-19/README.md').exists())


if __name__ == '__main__':
    unittest.main()
