"""Exercise read-only routing, owner boundaries, and conditional graph integrity."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'skill_lookup', ROOT / 'shared/find-and-load-skills/scripts/lookup.py')
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class SkillRouteTests(unittest.TestCase):
    def test_graph_targets_are_resolvable_and_references_are_reachable(self):
        graph = router.read(ROOT / 'catalog/skill-routes.json')['skills']
        registry = router.read(ROOT / 'catalog/qualification.json')['skills']
        for name, edges in graph.items():
            with self.subTest(source=name):
                router.resolve(ROOT, name, 'codex')
                source = ROOT / registry[name]['canonicalSource']
                self.assertIn('references/skill-routes.md', (source / 'SKILL.md').read_text())
                reference = (source / 'references/skill-routes.md').read_text()
                self.assertEqual(len(edges), len({e['skill'] for e in edges}))
                for edge in edges:
                    router.resolve(ROOT, edge['skill'], 'codex')
                    self.assertIn(edge['kind'], ['required', 'optional'])
                    self.assertTrue(edge['when'])
                    self.assertIn('`' + edge['skill'] + '`', reference)

    def test_selectable_skills_are_linked_named_plainly_and_reference_current_names(self):
        names = {w for p in (ROOT / 'profiles').glob('*.txt') for line in p.read_text().splitlines()
                 if not line.startswith('#') for w in line.split()}
        graph = router.read(ROOT / 'catalog/skill-routes.json')['skills']
        retired = router.read(ROOT / 'catalog/retired-names.json')
        # These work alone: tool wrappers and file helpers with no real companion step.
        standalone = {'build-userscripts', 'build-vscode-extensions', 'claude-code-git-safety',
                      'docx-files', 'find-and-load-skills', 'karakeep-bookmarks', 'pdf-files',
                      'ralph-workflow', 'use-obsidian-cli'}
        linked = set(graph) | {edge['skill'] for edges in graph.values() for edge in edges}
        self.assertEqual(names - linked, standalone)
        coined = {'forge', 'smith', 'craft', 'doctor', 'medic', 'atlas', 'baton', 'surgery',
                  'sleuth', 'lens', 'lab', 'workbench', 'workshop', 'pilot', 'ledger', 'guard',
                  'gatekeeper', 'probe', 'bench', 'bible', 'dossier', 'tuner', 'dissector',
                  'wrangler', 'grill', 'slicer', 'sequencer'}
        roots = [ROOT / prefix / name for name in sorted(names)
                 for prefix in ['skills', 'shared', 'library/skills']
                 if (ROOT / prefix / name / 'SKILL.md').exists()]
        modes = {p.name for root in roots for p in root.rglob('references/modes/*')}
        ticked = re.compile(r'`([a-z0-9]+(?:-[a-z0-9]+)+)`')
        # Tool, plugin and package names that happen to match a retired skill name.
        tools = {'agent-workspace-linux', 'agent-browser', 'ralph-loop', 'lightweight-charts'}
        for root in roots:
            with self.subTest(skill=root.name):
                self.assertFalse(coined & set(root.name.split('-')))
                for path in root.rglob('*.md'):
                    if path.name == 'codemap.md':
                        continue
                    for number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
                        if 'mode' in line.lower():
                            continue
                        for token in ticked.findall(line):
                            self.assertFalse(token in retired and token not in modes | names | tools,
                                             f'{path.relative_to(ROOT)}:{number}: {token}')

    def test_non_default_to_non_default_and_explicit_only_routes(self):
        routes = router.lookup(ROOT, 'codex', origin='develop-and-draft-fiction')
        self.assertTrue(any(r['name'] == 'edit-fiction' and r['scope'] == 'optional' for r in routes))
        with self.assertRaises(ValueError):
            router.resolve(ROOT, 'spec-implementer', 'codex')
        self.assertFalse(router.resolve(ROOT, 'plan-and-implement-changes', 'codex')['explicitOnly'])
        self.assertEqual(router.resolve(ROOT, 'react-native-expo', 'codex')['groups'], ['mobile-and-interfaces'])

    def test_rejected_routes_and_listing_do_not_mutate_selection(self):
        for name in ['poteto-mode', 'ui-architect', 'ars-malefica-maintenance', 'tadooer-workflow', '../ui-craft']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                router.resolve(ROOT, name, 'codex')
        with self.assertRaises(ValueError):
            router.resolve(ROOT, 'style-web-ui', 'opencode')
        with self.assertRaises(ValueError):
            router.lookup(ROOT, 'codex', group='missing-group')
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / '.local/state/subsets-fleet/profiles/selection.json'
            marker.parent.mkdir(parents=True)
            marker.write_text('{"profiles":["core"]}\n')
            before = marker.read_bytes()
            with patch.object(Path, 'home', return_value=Path(tmp)):
                routes = router.lookup(ROOT, 'codex', group='mobile-and-interfaces')
            self.assertEqual(marker.read_bytes(), before)
            self.assertEqual(list(Path(tmp).rglob('*.json')), [marker])
            self.assertTrue(any(r.get('name') == 'react-native-expo' and 'path' in r for r in routes))

    def test_optional_symlink_cannot_escape_the_reviewed_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'catalog').mkdir()
            (root / 'profiles').mkdir()
            (root / 'library/skills').mkdir(parents=True)
            external = root / 'outside.md'
            external.write_text('---\nname: external\n---\n')
            source = root / 'source'
            # Reuse catalog metadata in an isolated root; the entrypoint itself
            # escapes that root even though the named owner is qualified.
            source.mkdir()
            for name in ['catalog', 'profiles']:
                (source / name).symlink_to(ROOT / name, target_is_directory=True)
            skill = source / 'library/skills/react-native-expo'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').symlink_to(external)
            with self.assertRaisesRegex(ValueError, 'escaping'):
                router.resolve(source, 'react-native-expo', 'codex')

    def test_missing_required_companion_is_reported_without_losing_other_routes(self):
        routes = router.lookup(ROOT, 'opencode', origin='react-native-expo')
        proof = next(r for r in routes if r['name'] == 'verify-implementation')
        self.assertEqual(proof['kind'], 'required')
        self.assertIn('unavailable', proof)
        self.assertTrue(proof['when'])


if __name__ == '__main__':
    unittest.main()
