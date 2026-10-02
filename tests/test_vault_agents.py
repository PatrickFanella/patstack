import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('vault_agents', Path(__file__).parents[1] / 'scripts/vault-agents.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class DeploymentGuardTests(unittest.TestCase):
    def test_modified_destination_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, target = root / 'source', root / 'target'
            source.write_text('new')
            target.write_text('original')
            row = {'source': str(source), 'destination': str(target), 'previous_sha256': module.digest(target)}
            self.assertEqual(len(module.plan([row])[0]), 1)
            target.write_text('concurrent edit')
            changes, errors = module.plan([row])
            self.assertFalse(changes)
            self.assertTrue(errors)
            self.assertEqual(target.read_text(), 'concurrent edit')

    def test_current_copy_is_noop(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, target = root / 'source', root / 'target'
            source.write_text('same')
            target.write_text('same')
            self.assertEqual(module.plan([{'source': str(source), 'destination': str(target), 'previous_sha256': None}]), ([], []))

    def test_symlink_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            source.write_text('new')
            (root / 'outside').mkdir()
            (root / 'linked').symlink_to(root / 'outside', target_is_directory=True)
            changes, errors = module.plan([{'source': str(source), 'destination': str(root / 'linked/target'), 'previous_sha256': None}])
            self.assertFalse(changes)
            self.assertTrue(errors)


if __name__ == '__main__':
    unittest.main()
