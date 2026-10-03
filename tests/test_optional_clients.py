import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('optional_clients', ROOT / 'scripts/optional-clients.py')
clients = importlib.util.module_from_spec(spec); spec.loader.exec_module(clients)


class OptionalClientTests(unittest.TestCase):
    def test_reviewed_selection_and_unsupported_contract_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / 'catalog').mkdir(); active = root / 'active'; active.mkdir()
            target = root / 'claude'; target.mkdir(); state = root / 'state'
            (root / 'catalog/qualification.json').write_text(json.dumps({'skills': {
                'specialist': {'status': 'structure-reviewed', 'supportedClients': ['codex', 'claude']}}}))
            (root / 'catalog/workstation-links.json').write_text(json.dumps({'links': {}, 'baseline': {}}))
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@invalid', 'commit', '--allow-empty', '-qm', 'fixture'], check=True)
            manager = {'preview': lambda profiles: {'skills': ['specialist']}, 'ACTIVE': active}
            proposal = clients.plan(['profile'], root, state, target, manager)
            self.assertEqual(proposal['selection'], ['specialist'])
            self.assertEqual(proposal['operations'][0]['desired']['target'], str(active / 'specialist'))
            (target / 'specialist').write_text('user-owned')
            with self.assertRaisesRegex(RuntimeError, 'drift'): clients.plan(['profile'], root, state, target, manager)
            self.assertEqual((target / 'specialist').read_text(), 'user-owned')
            (root / 'catalog/qualification.json').write_text(json.dumps({'skills': {'specialist': {
                'status': 'unreviewed', 'supportedClients': []}}}))
            with self.assertRaisesRegex(RuntimeError, 'not qualified'): clients.plan(['profile'], root, state, target, manager)
