import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('global_instructions', ROOT / 'scripts/global-instructions.py')
gi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gi)


class RenderTests(unittest.TestCase):
    def test_every_host_and_client_renders_with_its_own_home(self):
        hosts = json.loads((ROOT / 'instructions/hosts.json').read_text())['hosts']
        for host, info in hosts.items():
            for client in gi.CLIENTS:
                text = gi.render(host, client, 'f' * 40)
                self.assertIn('@' + info['home'] + '/.homelab/HOMELAB.md', text)
                # gitea-agent-host.py appends this reference when missing; keep it present.
                self.assertIn('@' + info['home'] + '/.config/agent-identity/GITEA.md', text)
                self.assertIn('### Keep going until it is done', text)
                self.assertEqual(('rtk proxy' in text), bool(info.get('rtk')), host)
                other = '/Users/onnwee' if info['home'] == '/home/onnwee' else '/home/onnwee/.homelab'
                self.assertNotIn(other + '/.homelab', text)

    def test_client_specific_lines(self):
        self.assertIn('does not expand `@`', gi.render('sputnik', 'codex', 'x' * 40))
        self.assertNotIn('does not expand `@`', gi.render('sputnik', 'claude', 'x' * 40))
        self.assertIn('blacktower', gi.render('soyuz', 'codex', 'x' * 40))
        self.assertNotIn('blacktower', gi.render('soyuz', 'claude', 'x' * 40))
        self.assertNotIn('blacktower', gi.render('kvant', 'codex', 'x' * 40))

    def test_context_and_rtk_files_follow_host_facts(self):
        soyuz = gi.render_all('soyuz', 'x' * 40)
        self.assertIn('AGENTS.md', soyuz)
        self.assertIn('@/Users/onnwee/.homelab/HOMELAB.md', soyuz['.agents/AGENTS.md'])
        self.assertEqual(soyuz['.claude/RTK.md'], (ROOT / 'instructions/RTK.md').read_text())
        nuc = gi.render_all('nuc', 'x' * 40)
        self.assertNotIn('.codex/RTK.md', nuc)
        self.assertNotIn('AGENTS.md', nuc)
        self.assertIn('.agents/AGENTS.md', nuc)
        almaz = gi.render_all('almaz', 'x' * 40)
        self.assertIn('Agent Hub repository', almaz['.agents/CLAUDE.md'])
        self.assertEqual(almaz['.agents/CLAUDE.md'], almaz['.agents/AGENTS.md'])
        self.assertNotIn('Agent Hub', nuc['.agents/AGENTS.md'])

    def test_remote_script_compiles(self):
        compile(gi.remote_source(), 'remote-script', 'exec')


class DeployTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.patch = patch.object(gi.Path, 'home', return_value=self.home)
        self.patch.start()
        self.payload = gi.payload_for('sputnik', 'a' * 40)
        self.codex = self.home / '.codex/AGENTS.md'

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def deploy(self, payload=None):
        gi.remote('plan', payload or self.payload)
        gi.remote('apply', payload or self.payload)

    def test_adopts_existing_file_and_symlink_with_backups(self):
        self.codex.parent.mkdir(parents=True)
        self.codex.write_text('hand written\n')
        self.codex.chmod(0o600)
        source = self.home / 'repo-claude.md'
        source.write_text('linked\n')
        claude = self.home / '.claude/CLAUDE.md'
        claude.parent.mkdir(parents=True)
        claude.symlink_to(source)
        self.deploy()
        self.assertEqual(self.codex.read_text(), self.payload['files']['.codex/AGENTS.md'])
        self.assertEqual(self.codex.stat().st_mode & 0o777, 0o600)
        self.assertFalse(claude.is_symlink())
        self.assertEqual(source.read_text(), 'linked\n')
        gi.remote('verify', self.payload)
        gi.remote('rollback', self.payload)
        self.assertEqual(self.codex.read_text(), 'hand written\n')
        self.assertEqual(claude.resolve(), source.resolve())
        self.assertFalse((self.home / '.config/opencode/AGENTS.md').exists())

    def test_hand_edit_after_deploy_is_refused(self):
        self.deploy()
        self.codex.write_text(self.codex.read_text() + 'local tweak\n')
        with self.assertRaisesRegex(RuntimeError, 'Hand-edited'):
            gi.remote('plan', self.payload)

    def test_apply_refuses_change_after_plan(self):
        gi.remote('plan', self.payload)
        self.codex.parent.mkdir(parents=True)
        self.codex.write_text('new edit\n')
        with self.assertRaisesRegex(RuntimeError, 'State changed'):
            gi.remote('apply', self.payload)
        self.assertEqual(self.codex.read_text(), 'new edit\n')

    def test_update_and_rollback_refusal(self):
        self.deploy()
        newer = dict(self.payload)
        newer['files'] = {c: t + '\n- extra\n' for c, t in self.payload['files'].items()}
        newer['hashes'] = {r: gi.digest(t.encode()) for r, t in newer['files'].items()}
        self.deploy(newer)
        self.assertTrue(self.codex.read_text().endswith('- extra\n'))
        self.codex.write_text('later edit\n')
        with self.assertRaisesRegex(RuntimeError, 'Changed since deployment'):
            gi.remote('rollback', newer)

    def test_retired_working_copy_removed_only_when_unedited(self):
        dest = self.home / gi.RETIRED[0]
        dest.parent.mkdir(parents=True)
        dest.write_text('old working style\n')
        dest.chmod(0o644)
        receipt = self.home / gi.RETIRED[1]
        receipt.parent.mkdir(parents=True)
        receipt.write_text(json.dumps({'dest': gi.state(dest)}))
        dest.write_text('edited by hand\n')
        self.deploy()
        self.assertTrue(dest.exists())
        gi.remote('rollback', self.payload)
        dest.write_text('old working style\n')
        dest.chmod(0o644)
        self.deploy()
        self.assertFalse(dest.exists())


if __name__ == '__main__':
    unittest.main()
