"""Pin the council intake and the scored-loop contract that the new core skill adds."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/improve-to-a-target-score'


class ImproveToATargetScoreTests(unittest.TestCase):
    def test_pinned_resources_match_the_intake_ledger(self):
        ledger = json.loads((ROOT / 'catalog/tstack-council-intake-2026-11-11.json').read_text())
        self.assertEqual(ledger['license'], 'MIT')
        for record in ledger['files']:
            for field in ['archivePath', 'installedPath']:
                if record[field]:
                    with self.subTest(path=record[field]):
                        actual = hashlib.sha256((ROOT / record[field]).read_bytes()).hexdigest()
                        self.assertEqual(actual, record['sha256'])

    def test_skill_is_in_core(self):
        core = (ROOT / 'profiles/core.txt').read_text().split()
        self.assertIn('improve-to-a-target-score', core)

    def test_procedure_keeps_the_rules_the_video_found(self):
        body = (SKILL / 'SKILL.md').read_text()
        for rule in [
            'three providers',               # cross-provider panel
            'round 0',                       # baseline before changes
            'gap to the references',         # judge against comparable products
            'Do not tell members the target score',
            'never substitute a model silently',
            'revert it in full',             # program ruler: keep or revert
            'Never lower the target',
        ]:
            with self.subTest(rule=rule):
                self.assertIn(rule, body)

    def test_brief_withholds_the_target_and_stays_read_only(self):
        brief = (SKILL / 'references/panel-brief.md').read_text()
        self.assertIn('Review only. Do not edit files', brief)
        self.assertIn('Leave the target score out', brief)
        self.assertNotIn('9/10', brief)

    def test_near_miss_routes_one_off_review_elsewhere(self):
        front = (SKILL / 'SKILL.md').read_text().split('---', 2)[1]
        self.assertIn('Not for a one-off review (review-code-changes)', front)
        q = json.loads((ROOT / 'catalog/qualification.json').read_text())['skills']['improve-to-a-target-score']
        self.assertIn('review-code-changes', q['nearMiss'])


if __name__ == '__main__':
    unittest.main()
