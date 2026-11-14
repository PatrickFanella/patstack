import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'vault-agents/ars-malefica/skills/coding-challenge-coach/scripts/validate-coding-challenge-system.py'
PRACTICE = Path('001 Projects/Threads/Programming/Practice')
BLOCK = PRACTICE / 'Blocks/Block 00.md'


def note(fields, body=''):
    lines = '\n'.join(f'{k}: {v}' for k, v in fields.items())
    return f'---\n{lines}\n---\n\n{body}\n'


BLOCK_FIELDS = {'block-id': 'b0', 'status': 'active', 'phase': 'baseline', 'started': '2026-01-01',
                'target-attempt-count': '3', 'target-language': 'Go', 'workspace': '/w'}
TRACK_BODY = '## Current state\n\n## Dimensions\n\n## Next instruction\n'
SET_BODY = '## Puzzles\n\n## Review\n\n## Next set guidance\n'


class CodingChallengeValidatorTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        files = {
            PRACTICE / 'Coding Challenge Practice System.md': note({'title': 'x'}),
            PRACTICE / 'Learner Profile.md': note({'title': 'x'}, '## Learning target\n## Evidence-based baseline\n## Coaching contract\n'),
            PRACTICE / 'Current Challenge Block.md': note({'active-block': str(BLOCK)}),
            PRACTICE / 'Challenge Progress Ledger.md': note({'title': 'x'}, '## Current state\n## Baseline dimensions\n## Attempt history\n## Attempt review schema\n## Block review schema\n'),
            PRACTICE / 'Challenge Library.md': note({'title': 'x'}),
            PRACTICE / 'Challenge Attempt Template.md': note({'title': 'x'}),
            Path('001 Projects/Threads/Programming/Programming MOC.md'): note({'title': 'x'}),
            BLOCK: note(BLOCK_FIELDS),
            PRACTICE / 'Puzzle Sets/Puzzle Sets.md': note({'active-set': ''}),
            PRACTICE / 'Puzzle Sets/Puzzle Set 01.md': note({'set-id': 'set-01', 'status': 'active', 'workspace': '/w/puzzles/set-01'}, SET_BODY),
        }
        for lang in ('typescript', 'go', 'python'):
            files[PRACTICE / f'Tracks/{lang} Track.md'] = note(
                {'track-id': lang, 'language': lang, 'toolchain': 't', 'workspace': f'/w/{lang}',
                 'active-challenge': 'cc-1', 'phase': 'baseline'}, TRACK_BODY)
        (self.root / '001 Projects/Works').mkdir(parents=True)
        for rel, text in files.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text)

    def run_validator(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, '-I', str(VALIDATOR), '--root', str(self.root)],
                              capture_output=True, text=True, env=env)

    def edit(self, rel, old, new):
        path = self.root / rel
        path.write_text(path.read_text().replace(old, new))

    def test_tracks_and_puzzle_sets_pass(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('3 tracks, 1 puzzle sets', result.stdout)

    def test_empty_pointer_needs_every_track_block(self):
        self.edit(PRACTICE / 'Current Challenge Block.md', f'active-block: {BLOCK}', 'active-block:')
        self.assertIn('lacks active-block', self.run_validator().stdout)
        for lang in ('typescript', 'go', 'python'):
            self.edit(PRACTICE / f'Tracks/{lang} Track.md', 'phase: baseline', f'phase: practice\nactive-block: {BLOCK}')
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_broken_track_and_set_notes_fail(self):
        self.edit(PRACTICE / 'Tracks/go Track.md', '## Dimensions', '## Levels')
        self.edit(PRACTICE / 'Puzzle Sets/Puzzle Set 01.md', 'status: active', 'status: done')
        out = self.run_validator().stdout
        self.assertIn('track note lacks heading ## Dimensions', out)
        self.assertIn('puzzle set status must be active or complete', out)

    def test_track_block_must_exist_and_be_active(self):
        self.edit(PRACTICE / 'Tracks/go Track.md', 'phase: baseline', 'phase: practice\nactive-block: missing.md')
        self.assertIn('names a block that does not exist', self.run_validator().stdout)


if __name__ == '__main__':
    unittest.main()
