import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gitea_agent_host', ROOT / 'scripts/gitea-agent-host.py')
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)


class GiteaAgentHostTests(unittest.TestCase):
    def test_identity_guard_raises_without_assert(self):
        with patch.object(host, 'api', return_value={'login': 'human'}):
            with self.assertRaisesRegex(RuntimeError, 'not subcult-agent'):
                host.verify('tea')

    def test_backs_up_the_file_git_global_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); config_home = home / '.config'
            self.assertEqual(host.global_gitconfig(home, config_home), home / '.gitconfig')
            (config_home / 'git').mkdir(parents=True)
            (config_home / 'git/config').write_text('[user]\n')
            self.assertEqual(host.global_gitconfig(home, config_home), config_home / 'git/config')
            (home / '.gitconfig').write_text('[core]\n')
            self.assertEqual(host.global_gitconfig(home, config_home), home / '.gitconfig')


if __name__ == '__main__':
    unittest.main()
