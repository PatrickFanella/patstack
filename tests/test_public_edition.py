import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('public_edition', ROOT / 'scripts/public-edition.py')
edition = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edition)


class PublicEditionTest(unittest.TestCase):
    def test_compatibility_moves_into_metadata(self):
        text = '---\nname: x\ndescription: d\ncompatibility: Needs Bun.\nmetadata:\n  a: b\n---\n# x\n'
        out = edition.move_to_metadata(text, ['compatibility'])
        self.assertIn('metadata:\n  a: b\n  compatibility: Needs Bun.\n---', out)
        self.assertNotIn('\ncompatibility:', out)

    def test_every_listed_skill_exists_and_check_passes(self):
        config = json.loads((ROOT / 'catalog/public-edition.json').read_text())
        for name in config['skills']:
            edition.source_dir(name)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'provenance.json').write_text('{"skills": [], "files": {}}')
            for name in config['skills']:
                (target / 'skills' / name).mkdir(parents=True)
                (target / 'skills' / name / 'LICENSE').write_text('MIT License\n')
            edition.export(target, check_only=True)

    def test_forbidden_text_refuses_the_export(self):
        config = json.loads((ROOT / 'catalog/public-edition.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / 'provenance.json').write_text('{"skills": [], "files": {}}')
            for name in config['skills']:
                (target / 'skills' / name).mkdir(parents=True)
                (target / 'skills' / name / 'LICENSE').write_text('MIT License\n')
            leak = edition.source_dir(config['skills'][0]) / 'leak-probe.md'
            try:
                leak.write_text('ssh onnwee@10.0.0.50\n')
                with self.assertRaises(SystemExit):
                    edition.export(target, check_only=True)
            finally:
                leak.unlink()
            self.assertFalse((target / '.skills-export').exists())


if __name__ == '__main__':
    unittest.main()
