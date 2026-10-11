import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tadooer_host', ROOT / 'scripts/tadooer-assistant-host.py')
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)

class TadooerGuardTests(unittest.TestCase):
    def test_client_json_preserves_wrapper_status_and_parses_native_result(self):
        self.assertEqual(host.client_json('mise status\n[{"version":"1.0.1"}]\n'), [{"version":"1.0.1"}])

    def test_remote_script_compiles_without_truncating_its_own_strings(self):
        compile(host.remote_source(), "remote-script", "exec")

    def test_conflicting_claude_registration_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config = home / '.claude.json'
            original = json.dumps({'mcpServers': {'tadooer': {'command': '/other/adapter'}}})
            config.write_text(original)
            with self.assertRaisesRegex(RuntimeError, 'differs'):
                host.existing_mcp(home, home / '.local/bin/tadooer-mcp')
            self.assertEqual(config.read_text(), original)

    def test_plan_refuses_changed_config_before_application(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            payload = host.payload_for(Path(__file__), '/usr/bin/node', 'https://example.test', 'fixture')
            def client(args, check=True):
                if 'marketplace' in args:
                    return SimpleNamespace(returncode=0, stdout='{"marketplaces":[]}', stderr='')
                if args[-1] == '--version':
                    return SimpleNamespace(returncode=0, stdout='v24.1.0', stderr='')
                return SimpleNamespace(returncode=1, stdout='', stderr='absent')
            with patch.object(host.Path, 'home', return_value=home), patch.object(host.shutil, 'which', return_value='/client'), patch.object(host, 'run', side_effect=client):
                host.remote('plan', payload)
                config = home / '.codex/config.toml'
                config.parent.mkdir()
                config.write_text('model = "owner-choice"')
                with self.assertRaisesRegex(RuntimeError, 'State changed'):
                    host.remote('apply', payload)
                self.assertEqual(config.read_text(), 'model = "owner-choice"')
                self.assertFalse((home / '.local/bin/tadooer-mcp').exists())

    def test_private_receipt_mode_and_symlink_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'receipt.json'
            host.write(path, b'{}')
            self.assertEqual(host.state(path)['mode'], 0o600)
            link = Path(directory) / 'link'
            link.symlink_to(path)
            self.assertEqual(host.state(link), {'link': str(path)})
