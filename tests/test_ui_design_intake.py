"""Keep the pinned upstream scanner executable and its provenance intact."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UIDesignIntakeTests(unittest.TestCase):
    def test_pinned_resources_match_the_intake_ledger(self):
        ledger = json.loads((ROOT / 'catalog/avoid-ai-design-intake-2026-11-04.json').read_text())
        for record in ledger['files']:
            for field in ['archivePath', 'installedPath']:
                if record[field]:
                    with self.subTest(path=record[field]):
                        actual = hashlib.sha256((ROOT / record[field]).read_bytes()).hexdigest()
                        self.assertEqual(actual, record['sha256'])

    @unittest.skipUnless(shutil.which('node'), 'Node 18+ required for scanner behavior checks')
    def test_upstream_scanner_positive_and_near_miss_cases(self):
        result = subprocess.run(
            ['node', '--test', '--test-reporter=tap', 'skills/ui-cliche-audit/scripts/detect.test.mjs'],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('# pass 11', result.stdout)


if __name__ == '__main__':
    unittest.main()
