import datetime as dt
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

SOURCE = pathlib.Path(__file__).with_name("gitea-package-retention-audit.py")
SPEC = importlib.util.spec_from_file_location("audit", SOURCE)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class PackageRetentionAuditTests(unittest.TestCase):
    def row(self, version="candidate-old", created=1, tagged=False):
        return {"id":1, "owner":"subculture-collective", "name":"demo", "version":version,
                "created_unix":created, "is_tagged":tagged, "manifests":[], "manifest_sha256":""}

    def test_compose_pattern_finds_a_pinned_digest(self):
        text = "image: git.subcult.tv/subculture-collective/demo@sha256:" + "a" * 64
        self.assertEqual(audit.re.findall(audit.COMPOSE_REF_RE, text),
                         ["git.subcult.tv/subculture-collective/demo@sha256:" + "a" * 64])

    def test_missing_docker_fails_closed(self):
        with patch.object(audit, "remote", side_effect=RuntimeError("Docker daemon unavailable")):
            inventory, error = audit.host_references("example")
        self.assertEqual(inventory, {"containers": [], "cached_images": [], "compose_refs": []})
        self.assertIn("Docker daemon unavailable", error)

    def test_compose_failure_preserves_partial_inventory_and_blocks_host(self):
        value = {"containers": [{"name": "stopped-test"}], "cached_images": [],
                 "compose_refs": [], "compose_errors": ["/workspace/missing.yml"]}
        with patch.object(audit, "remote", return_value=audit.json.dumps(value)):
            inventory, error = audit.host_references("example")
        self.assertEqual(inventory["containers"], value["containers"])
        self.assertIn("Compose source unreadable", error)

    def test_cached_rollback_digest_is_a_preservation_reason(self):
        row = self.row()
        refs = audit.refs_for_version(row)
        reasons, matches = audit.preservation_reasons(
            row, refs, {"git.subcult.tv/subculture-collective/demo:candidate-old"},
            dt.datetime.fromtimestamp(2, tz=dt.timezone.utc), {}, True, {1})
        self.assertTrue(matches)
        self.assertIn("referenced_by_container_or_compose_or_cached_image", reasons)

    def test_no_recovery_cutoff_blocks_an_otherwise_old_untagged_version(self):
        row = self.row()
        reasons, _ = audit.preservation_reasons(row, audit.refs_for_version(row), set(),
            dt.datetime.fromtimestamp(2, tz=dt.timezone.utc), {}, False, set())
        self.assertEqual(reasons, ["recovery_gate_unverified"])

    def test_failed_host_inventory_blocks_an_otherwise_old_untagged_version(self):
        row = self.row()
        reasons, _ = audit.preservation_reasons(row, audit.refs_for_version(row), set(),
            dt.datetime.fromtimestamp(2, tz=dt.timezone.utc), {"soyuz":"Docker unavailable"}, True, {1})
        self.assertEqual(reasons, ["host_inventory_incomplete"])

    def test_recovered_id_set_must_contain_the_exact_package_version_id(self):
        row = self.row()
        reasons, _ = audit.preservation_reasons(row, audit.refs_for_version(row), set(),
            dt.datetime.fromtimestamp(2, tz=dt.timezone.utc), {}, True, {2})
        self.assertEqual(reasons, ["not_covered_by_verified_recovery_dump"])

    def test_cutoff_and_permanent_tag_are_independent_preservation_gates(self):
        row = self.row(version="v1.2.3", created=3, tagged=True)
        reasons, _ = audit.preservation_reasons(row, audit.refs_for_version(row), set(),
            dt.datetime.fromtimestamp(2, tz=dt.timezone.utc), {}, True, set())
        self.assertIn("permanent_version_tag", reasons)
        self.assertIn("not_covered_by_verified_recovery_dump", reasons)


if __name__ == "__main__":
    unittest.main()
