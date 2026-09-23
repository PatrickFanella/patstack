import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('claude_mcp', Path(__file__).resolve().parents[1] / 'scripts/claude-mcp.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ClaudeMcpTests(unittest.TestCase):
    def test_portable_transports(self):
        converted, skipped = module.convert({
            'stdio': {'command': 'server', 'args': ['--stdio'], 'env': {'DATA': '/tmp/data'}, 'startup_timeout_sec': 20},
            'http': {'url': 'https://example.test/mcp'},
        })
        self.assertFalse(skipped)
        self.assertEqual(converted['stdio'], {'type': 'stdio', 'command': 'server', 'args': ['--stdio'], 'env': {'DATA': '/tmp/data'}})
        self.assertEqual(converted['http'], {'type': 'http', 'url': 'https://example.test/mcp'})

    def test_unsupported_entries_are_excluded(self):
        converted, skipped = module.convert({
            'node_repl': {'command': 'desktop-bridge'},
            'disabled': {'command': 'server', 'enabled': False},
            'invalid': {'url': 'placeholder'},
            'auth': {'url': 'https://example.test/mcp', 'bearer_token_env_var': 'TOKEN'},
        })
        self.assertFalse(converted)
        self.assertEqual(len(skipped), 4)
