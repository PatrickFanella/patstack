import base64
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('t3_fleet', Path(__file__).parents[1] / 'scripts/t3-fleet.py')
fleet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fleet)


class FleetDeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.patch = patch.object(fleet.Path, 'home', return_value=self.home)
        self.patch.start()
        self.payload = {'revision': 'test', 'skills': {'.codex/skills/example': {
            'SKILL.md': {'content': base64.b64encode(b'new skill').decode(), 'mode': 0o644}}},
            'mcpServers': {'docs': {'url': 'https://example.com/mcp'}}}

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def run_stage(self, stage):
        with contextlib.redirect_stdout(io.StringIO()):
            fleet.remote(stage, self.payload)

    def test_preserves_unrelated_config_and_saves_replaced_skill(self):
        skill = self.home / '.codex/skills/example'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('old skill')
        config = self.home / '.codex/config.toml'
        config.write_text('model = "existing"\n[mcp_servers.host_only]\ncommand = "local-tool"\n')
        self.run_stage('plan'); self.run_stage('apply'); self.run_stage('verify')
        self.assertIn('host_only', config.read_text())
        self.assertIn('model = "existing"', config.read_text())
        self.assertEqual((skill / 'SKILL.md').read_text(), 'new skill')
        backups = list((self.home / '.local/state/t3-fleet').glob('*/before/.codex/skills/example/SKILL.md'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'old skill')

    def test_refuses_intervening_edit(self):
        self.run_stage('plan')
        skill = self.home / '.codex/skills/example'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('concurrent work')
        with self.assertRaisesRegex(RuntimeError, 'changed since preview'):
            self.run_stage('apply')
        self.assertEqual((skill / 'SKILL.md').read_text(), 'concurrent work')

    def test_refuses_conflicting_mcp(self):
        config = self.home / '.claude.json'
        config.write_text(json.dumps({'mcpServers': {'docs': {'type': 'http', 'url': 'https://other.example/mcp'}}}))
        with self.assertRaisesRegex(RuntimeError, 'conflicting claude MCP'):
            self.run_stage('plan')

    def test_preserves_symlink_in_backup(self):
        source = self.home / 'owned-skill'
        source.mkdir(); (source / 'SKILL.md').write_text('owned')
        target = self.home / '.codex/skills/example'
        target.parent.mkdir(parents=True);target.symlink_to(source)
        self.run_stage('plan'); self.run_stage('apply')
        self.assertEqual((source / 'SKILL.md').read_text(), 'owned')
        backups = list((self.home / '.local/state/t3-fleet').glob('*/before/.codex/skills/example'))
        self.assertTrue(backups[0].is_symlink())


if __name__ == '__main__':
    unittest.main()
