import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('project_selection', ROOT / 'scripts/project-skills.py')
project = importlib.util.module_from_spec(spec); spec.loader.exec_module(project)


class ProjectSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.source = self.root / 'source'
        self.target = self.root / 'project'; self.state = self.root / 'state'
        for p in [self.source / 'catalog', self.source / 'library/skills/specialist', self.target]: p.mkdir(parents=True)
        (self.source / 'library/skills/specialist/SKILL.md').write_text('---\nname: specialist\ndescription: task\n---\nprocedure\n')
        (self.source / 'instructions.md').write_text('Read the local specialist for this task.\n')
        (self.target / 'AGENTS.md').write_text('Keep existing project facts.\n')
        for repo in [self.source, self.target]:
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@invalid', 'commit', '-qm', 'fixture'], check=True)
        self.config = {'canonicalRoot': str(self.target), 'sources': ['library/skills/specialist'],
                       'clients': ['codex', 'claude', 'opencode'], 'instructions': 'instructions.md',
                       'baseline': {'AGENTS.md': project.install.snapshot(self.target / 'AGENTS.md')}}
        self.save_config()
        self.qual = {'skills': {'specialist': {'status': 'structure-reviewed', 'supportedClients': self.config['clients']}}}
        self.save_qual()

    def save_config(self):
        (self.source / 'catalog/project-selections.json').write_text(json.dumps({'projects': {'fixture': self.config}}))

    def save_qual(self):
        (self.source / 'catalog/qualification.json').write_text(json.dumps(self.qual))

    def plan(self, target=None):
        return project.plan('fixture', target or self.target, self.source, self.state)

    def deploy(self, proposal):
        project.stage_links(proposal, self.state)
        return project.install.apply(proposal, self.state)

    def test_exact_selection_links_readback_and_rollback(self):
        proposal = self.plan(); self.assertFalse(self.state.exists())
        run = self.deploy(proposal)
        project.install.verify(self.plan(), self.state)
        for client in ['.agents', '.claude', '.opencode']:
            self.assertEqual((self.target / client / 'skills/specialist/SKILL.md').read_bytes(),
                             (self.source / 'library/skills/specialist/SKILL.md').read_bytes())
        self.assertIn('Keep existing project facts.', (self.target / 'AGENTS.md').read_text())
        (self.target / 'AGENTS.md').write_text('later user edit')
        with self.assertRaisesRegex(RuntimeError, 'intervening edits'): project.install.rollback(run, self.state)
        self.assertEqual((self.target / 'AGENTS.md').read_text(), 'later user edit')

    def test_other_repository_and_symlink_destinations_are_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'registered repository'): self.plan(self.source)
        external = self.root / 'external'; external.mkdir()
        (self.target / '.agents').symlink_to(external)
        with self.assertRaisesRegex(RuntimeError, 'symlink'): self.plan()
        self.assertFalse((external / 'skills').exists())

    def test_unrelated_skills_preserved_and_removed_selection_retired(self):
        unrelated = self.target / '.agents/skills/unrelated'; unrelated.mkdir(parents=True)
        (unrelated / 'SKILL.md').write_text('user-owned')
        self.deploy(self.plan())
        self.config['sources'] = []; self.save_config()
        self.deploy(self.plan())
        self.assertFalse((self.target / '.agents/skills/specialist').exists())
        self.assertFalse((self.target / '.claude/skills/specialist').is_symlink())
        self.assertEqual((unrelated / 'SKILL.md').read_text(), 'user-owned')

    def test_blocked_and_unsupported_clients_stop_before_writes(self):
        self.qual['skills']['specialist']['status'] = 'blocked'; self.save_qual()
        with self.assertRaisesRegex(RuntimeError, 'Blocked'): self.plan()
        self.qual['skills']['specialist'].update(status='structure-reviewed', supportedClients=['codex']); self.save_qual()
        with self.assertRaisesRegex(RuntimeError, 'Client contract'): self.plan()
        self.assertFalse(self.state.exists())

    def test_real_worktree_selection_uses_the_same_git_owner(self):
        worktree = self.root / 'isolated'
        subprocess.run(['git', '-C', str(self.target), 'worktree', 'add', '--detach', '-q', str(worktree), 'HEAD'], check=True)
        proposal = self.plan(worktree); self.deploy(proposal)
        self.assertTrue((worktree / '.agents/skills/specialist/SKILL.md').is_file())
        self.assertFalse((self.target / '.agents/skills/specialist').exists())
