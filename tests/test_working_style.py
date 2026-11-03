import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('working_style', ROOT / 'scripts/working-style-host.py')
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)


def payload(text='# Working style\n'):
    return {'host': 'fixture', 'revision': 'fixture', 'content': text,
            'sha256': hashlib.sha256(text.encode()).hexdigest()}


class WorkingStyleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.patch = patch.object(host.Path, 'home', return_value=self.home)
        self.patch.start()
        self.ref = '@' + str(self.home / host.DEST)

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def deploy(self, data=None):
        data = data or payload()
        host.remote('plan', data)
        host.remote('apply', data)

    def test_remote_script_compiles(self):
        compile(host.remote_source(), 'remote-script', 'exec')

    def test_apply_appends_import_and_preserves_content_and_mode(self):
        codex = self.home / '.codex/AGENTS.md'
        codex.parent.mkdir(parents=True)
        codex.write_text('owner text\n')
        codex.chmod(0o600)
        self.deploy()
        self.assertEqual(codex.read_text(), 'owner text\n\n' + self.ref + '\n')
        self.assertEqual(codex.stat().st_mode & 0o777, 0o600)
        self.assertTrue((self.home / '.claude/CLAUDE.md').read_text().startswith(self.ref))
        host.remote('verify', payload())

    def test_symlinked_client_file_is_left_to_its_source(self):
        source = self.home / 'source.md'
        source.write_text('managed\n')
        link = self.home / '.claude/CLAUDE.md'
        link.parent.mkdir(parents=True)
        link.symlink_to(source)
        self.deploy()
        self.assertEqual(source.read_text(), 'managed\n')

    def test_apply_refuses_change_after_plan(self):
        host.remote('plan', payload())
        codex = self.home / '.codex/AGENTS.md'
        codex.parent.mkdir(parents=True)
        codex.write_text('new owner edit\n')
        with self.assertRaisesRegex(RuntimeError, 'State changed'):
            host.remote('apply', payload())
        self.assertEqual(codex.read_text(), 'new owner edit\n')

    def test_unmanaged_destination_is_refused(self):
        dest = self.home / host.DEST
        dest.parent.mkdir(parents=True)
        dest.write_text('hand edit\n')
        with self.assertRaisesRegex(RuntimeError, 'Unmanaged or drifted'):
            host.remote('plan', payload())

    def test_update_replaces_previously_deployed_copy(self):
        self.deploy()
        self.deploy(payload('# Working style v2\n'))
        self.assertEqual((self.home / host.DEST).read_text(), '# Working style v2\n')

    def test_rollback_restores_and_refuses_later_edits(self):
        codex = self.home / '.codex/AGENTS.md'
        codex.parent.mkdir(parents=True)
        codex.write_text('owner text\n')
        self.deploy()
        host.remote('rollback', payload())
        self.assertEqual(codex.read_text(), 'owner text\n')
        self.assertFalse((self.home / host.DEST).exists())
        self.assertFalse((self.home / '.claude/CLAUDE.md').exists())
        self.deploy()
        codex.write_text(codex.read_text() + 'later edit\n')
        with self.assertRaisesRegex(RuntimeError, 'Changed since deployment'):
            host.remote('rollback', payload())


if __name__ == '__main__':
    unittest.main()
