import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('source_validation', Path(__file__).resolve().parents[1]/'scripts/validate.py')
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)


class ExternalOwnerTests(unittest.TestCase):
    def test_source_only_still_rejects_missing_repository_capability(self):
        caps=[{'kind': 'external', 'owner': 'OS owner', 'path': '/unavailable/os-owner'},
              {'kind': 'system', 'owner': 'system owner', 'path': '/unavailable/system-owner'},
              {'kind': 'personal', 'owner': 'source owner', 'path': 'missing-capability-source'}]
        errors,unverified=validation.capability_path_errors(caps,source_only=True)
        self.assertEqual(unverified,['OS owner','system owner'])
        self.assertEqual(len(errors),1)
        self.assertIn('source owner',errors[0])

    def test_default_skips_os_owner_not_installed_on_host(self):
        errors,unverified=validation.capability_path_errors([
            {'kind': 'external', 'owner': 'OS owner', 'path': '/unavailable/os-owner'}])
        self.assertEqual(errors,[])
        self.assertEqual(unverified,[])

    def test_default_rejects_dangling_os_owner_link(self):
        with tempfile.TemporaryDirectory() as directory:
            link=Path(directory)/'os-owner'
            link.symlink_to(Path(directory)/'removed-package')
            errors,_=validation.capability_path_errors([
                {'kind': 'external', 'owner': 'OS owner', 'path': str(link)}])
        self.assertEqual(len(errors),1)

    def test_default_still_rejects_missing_repository_capability(self):
        errors,_=validation.capability_path_errors([
            {'kind': 'personal', 'owner': 'source owner', 'path': 'missing-capability-source'}])
        self.assertEqual(len(errors),1)

    def test_source_only_never_reads_installed_skills_and_reports_boundary(self):
        with patch.object(validation.pathlib.Path, 'home', side_effect=AssertionError('must not read installed owners')):
            result = validation.external_description_metrics(source_only=True)
        self.assertEqual(result['unverifiedExternalOwners'], ['omarchy', 'diagnose-crash'])
        self.assertEqual(result['personalDescriptions'], 0)

    def test_default_reports_external_owners_absent_from_host(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(validation.pathlib.Path, 'home', return_value=Path(directory)):
            result = validation.external_description_metrics()
        self.assertEqual(result['absentExternalOwners'], ['omarchy', 'diagnose-crash'])
        self.assertEqual(result['personalDescriptions'], 0)

    def test_default_still_rejects_dangling_external_owner_link(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(validation.pathlib.Path, 'home', return_value=Path(directory)):
            skills = Path(directory)/'.codex/skills'
            skills.mkdir(parents=True)
            (skills/'omarchy').symlink_to(Path(directory)/'removed-package/omarchy')
            with self.assertRaises(FileNotFoundError):
                validation.external_description_metrics()

    def test_default_counts_both_installed_owner_descriptions(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(validation.pathlib.Path, 'home', return_value=Path(directory)):
            for name in ['omarchy', 'diagnose-crash']:
                p = Path(directory)/'.codex/skills'/name/'SKILL.md'
                p.parent.mkdir(parents=True)
                p.write_text('---\nname: '+name+'\ndescription: owner\n---\nbody\n')
            result = validation.external_description_metrics()
        self.assertEqual(result['personalDescriptions'], 10)
        self.assertEqual(result['unverifiedExternalOwners'], [])


class SourceReferenceTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory)
        for folder in ['skills/alpha', 'profiles', 'catalog', 'vault-agents/vault', 'vault-agents/shared']:
            (root / folder).mkdir(parents=True)
        (root / 'README.md').write_text('[guide](docs/missing.md) and `[code](not-a-link.md)`\n')
        (root / 'AGENTS.md').write_text('')
        (root / 'profiles/core.txt').write_text('# comment\nalpha\n')
        (root / 'vault-agents/shared/ref.md').write_text('shared')
        (root / 'vault-agents/vault/AGENTS.md').write_text('[ref](.agents/references/ref.md)\n')
        rows = [{'source': 'vault-agents/vault/AGENTS.md', 'destination': '/v/AGENTS.md'},
                {'source': 'vault-agents/shared/ref.md', 'destination': '/other/.agents/references/ref.md'},
                {'source': 'vault-agents/shared/ref.md', 'destination': '/v/.agents/references/ref.md'}]
        (root / 'catalog/vault-agents.json').write_text(validation.json.dumps({'files': rows}))
        (root / 'skills/alpha/SKILL.md').write_text('Apply the **oldname** skill. Use `frontend-design` skill.\n')
        return root

    def test_links_resolve_in_repository_or_at_vault_destination(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(validation, 'ROOT', self.fixture(directory)):
            self.assertEqual(validation.link_errors(), ['broken link README.md -> docs/missing.md'])

    def test_retired_skill_reference_is_reported_but_external_owner_is_not(self):
        retired = {'oldname': {'owner': 'newname'}, 'frontend-design': {'owner': 'ui-craft'}}
        with tempfile.TemporaryDirectory() as directory, patch.object(validation, 'ROOT', self.fixture(directory)):
            errors = validation.retired_reference_errors(retired)
        self.assertEqual(errors, ['retired skill name skills/alpha/SKILL.md:1: oldname -> newname'])
