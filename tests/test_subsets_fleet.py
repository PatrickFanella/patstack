import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FleetProfilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.source = self.home / 'source'
        shutil.copytree(ROOT / 'runtime-bundles/subsets-fleet', self.source)
        shutil.copy2(ROOT / 'scripts/install.py', self.source / 'scripts/install.py')
        shutil.copy2(ROOT / 'scripts/skill-profile', self.source / 'scripts/profile-selector')
        for folder in ['shared/base', 'library/skills/optional', 'profiles', 'catalog']:
            (self.source / folder).mkdir(parents=True, exist_ok=True)
        (self.source / 'shared/base/SKILL.md').write_text('canonical base')
        (self.source / 'library/skills/optional/SKILL.md').write_text('optional')
        for name, content in [('core', 'base'), ('extra', 'optional')]:
            (self.source / 'profiles' / (name + '.txt')).write_text(content + '\n')
        for name, data in [('proposed-catalog', []), ('retired-names', {}),
                           ('qualification', {'skills': {'base': {'status': 'selection-tested', 'supportedClients': ['codex', 'claude']},
                                                        'optional': {'status': 'selection-tested', 'supportedClients': ['codex', 'claude']}}})]:
            (self.source / 'catalog' / (name + '.json')).write_text(json.dumps(data))
        (self.source / 'deployment-source.json').write_text(json.dumps({'sourceRevision': 'fixture'}))
        active = self.home / '.agents/skills'
        (active / 'base').mkdir(parents=True)
        (active / 'base/SKILL.md').write_text('local edited base')
        (active / 'foreign').mkdir()
        (active / 'foreign/SKILL.md').write_text('foreign package')

    def run_cli(self, *args, success=True):
        import os
        result = subprocess.run(['python3', str(self.source / 'scripts/skill-profile'), *args],
                                env={**os.environ, 'HOME': str(self.home)}, text=True,
                                capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def test_preserve_foreign_and_edited_core_select_deactivate_and_rollback(self):
        preview = self.run_cli('plan', 'extra')
        self.assertIn(str(self.home / '.agents/skills/base'), preview['protected'])
        receipt = self.run_cli('activate', 'extra')
        self.assertTrue((self.home / '.agents/skills/optional/SKILL.md').is_file())
        self.assertTrue((self.home / '.claude/skills/optional').is_symlink())
        self.run_cli('verify', 'extra')
        self.assertEqual((self.home / '.agents/skills/base/SKILL.md').read_text(), 'local edited base')
        self.assertEqual((self.home / '.agents/skills/foreign/SKILL.md').read_text(), 'foreign package')
        deactivated = self.run_cli('deactivate')
        self.assertFalse((self.home / '.agents/skills/optional').exists())
        self.assertFalse((self.home / '.claude/skills/optional').is_symlink())
        self.run_cli('rollback', '--run', deactivated['run'])
        self.run_cli('verify', 'extra')
        self.run_cli('rollback', '--run', receipt['run'])
        self.assertFalse((self.home / '.agents/skills/optional').exists())

    def test_drift_blocks_switch_and_rollback_without_partial_changes(self):
        receipt = self.run_cli('activate', 'extra')
        path = self.home / '.agents/skills/optional/SKILL.md'
        path.write_text('later user edit')
        self.run_cli('deactivate', success=False)
        self.run_cli('rollback', '--run', receipt['run'], success=False)
        self.assertEqual(path.read_text(), 'later user edit')
        self.assertTrue((self.home / '.claude/skills/optional').is_symlink())

    def test_unknown_category_and_symlink_parent_are_refused(self):
        self.run_cli('activate', 'unknown', success=False)
        elsewhere = self.home / 'elsewhere'
        elsewhere.mkdir()
        (self.home / '.claude').symlink_to(elsewhere)
        self.run_cli('activate', 'extra', success=False)
        self.assertFalse((self.home / '.agents/skills/optional').exists())
