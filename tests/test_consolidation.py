"""Check source preservation and selection behavior of the approved consolidation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / 'catalog/consolidation-2026-11-09.json').read_text())
spec = importlib.util.spec_from_file_location('consolidated_lookup', ROOT / 'shared/skill-stack-router/scripts/lookup.py')
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class ConsolidationTests(unittest.TestCase):
    def test_removed_names_cannot_be_selected_or_resolved(self):
        profiles = {line for p in (ROOT / 'profiles').glob('*.txt') for line in p.read_text().splitlines() if line and not line.startswith('#')}
        retired = json.loads((ROOT / 'catalog/retired-names.json').read_text())
        previous = {name for row in LEDGER['owners'].values() for name in row['formerOwners'] if name not in LEDGER['owners']}
        previous.update(LEDGER['deleted'])
        for name in previous:
            with self.subTest(name=name):
                self.assertNotIn(name, profiles)
                self.assertIn(name, retired)
                for prefix in ['skills', 'shared', 'library/skills']:
                    self.assertFalse((ROOT / prefix / name / 'SKILL.md').exists())
                with self.assertRaises(ValueError):
                    router.resolve(ROOT, name, 'codex')

    def test_original_executables_and_binary_resources_survive_moves(self):
        for owner, row in LEDGER['owners'].items():
            for i, (old, former) in enumerate(row['formerOwners'].items()):
                target = ROOT / row['source'] if i == 0 else (ROOT / row['procedures'][old]).parent
                for relative, digest in former['resourceHashes'].items():
                    # Entry text and navigation intentionally change. Executable
                    # resources, data, licenses and assets must remain intact.
                    if Path(relative).suffix in {'.md', '.yaml', '.yml'} or '__pycache__' in Path(relative).parts:
                        continue
                    with self.subTest(owner=owner, former=old, resource=relative):
                        path = target / relative
                        self.assertTrue(path.is_file(), path)
                        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_deleted_originals_are_recoverable_and_not_runtime_sources(self):
        qualification = json.loads((ROOT / 'catalog/qualification.json').read_text())['skills']
        for name, row in LEDGER['deleted'].items():
            folder = ROOT / row['archive']
            self.assertTrue((folder / 'entrypoint.md').is_file())
            self.assertFalse((folder / 'SKILL.md').exists())
            self.assertEqual(qualification[name]['status'], 'archived')
            for relative, digest in row['resourceHashes'].items():
                path = folder / ('entrypoint.md' if relative == 'SKILL.md' else relative)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_every_current_profile_resolves_without_a_retired_owner(self):
        sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'runtime-bundles/subsets-fleet/scripts')]
        try:
            from stack_selection import available, selection
            names = available(ROOT)
            selected = set()
            for p in (ROOT / 'profiles').glob('*.txt'):
                selected.update(selection(ROOT, [p.stem])[0])
            self.assertEqual(selected, set(names))
            self.assertEqual(len(selected), 104)
            core = selection(ROOT, [])[0]
            self.assertEqual(len(core), 37)
            self.assertIn('prose-unslop', core)
            self.assertIn('studio-brand-system', core)
            self.assertIn('ui-craft', core)
            self.assertIn('postgres-workbench', core)
        finally:
            del sys.path[:2]

    def test_common_owner_does_not_erase_explicit_or_coaching_modes(self):
        # A general implementation request can select the owner, while the
        # former explicit /implement workflow remains conditional.
        self.assertFalse(router.resolve(ROOT, 'build-sequencer', 'codex')['explicitOnly'])
        record = LEDGER['owners']['build-sequencer']
        self.assertTrue((ROOT / record['procedures']['spec-implementer']).is_file())
        record = LEDGER['owners']['story-workbench']
        self.assertTrue((ROOT / record['procedures']['story-mentor']).is_file())
        self.assertTrue((ROOT / record['procedures']['story-cowriter']).is_file())
        # Provider-specific procedures do not make a missing provider callable.
        record = LEDGER['owners']['agent-fanout-plan']
        self.assertEqual(record['formerOwners']['opencode-deepwork']['qualification']['supportedClients'], ['opencode'])
