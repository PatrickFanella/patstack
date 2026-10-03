import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("vault_expiry", Path(__file__).with_name("expire-vaultwarden-session.py"))
expiry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(expiry)


class ExpiryTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "vaultwarden-session-policy.json").write_text('{"max_age_seconds": 14400}')
        self.session = self.root / "vaultwarden-session"
        self.session.write_text("fixture-key")
        os.utime(self.session, (1000, 1000))

    def test_unexpired_session_is_preserved_without_lock(self):
        with patch.object(expiry.subprocess, "run") as lock:
            self.assertEqual(expiry.expire(self.root, now=15399), 0)
        lock.assert_not_called()
        self.assertTrue(self.session.exists())

    def test_four_hour_boundary_locks_removes_and_records_no_key(self):
        with patch.object(expiry.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)):
            self.assertEqual(expiry.expire(self.root, now=15400), 0)
        self.assertFalse(self.session.exists())
        receipt = self.root / "vaultwarden-session-expiry-receipt.json"
        self.assertEqual(json.loads(receipt.read_text())["result"], "expired")
        self.assertNotIn("fixture-key", receipt.read_text())
        self.assertEqual(receipt.stat().st_mode & 0o777, 0o600)

    def test_failed_lock_still_removes_saved_key_and_records_failure(self):
        with patch.object(expiry.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 30)):
            self.assertEqual(expiry.expire(self.root, now=15400), 1)
        self.assertFalse(self.session.exists())
        receipt = json.loads((self.root / "vaultwarden-session-expiry-receipt.json").read_text())
        self.assertEqual(receipt["result"], "expiry_incomplete")

    def test_concurrent_unlock_preserves_new_session(self):
        def fresh_session(*args, **kwargs):
            self.session.write_text("new-fixture-key")
            os.utime(self.session, (15401, 15401))
            return subprocess.CompletedProcess([], 0)
        with patch.object(expiry.subprocess, "run", side_effect=fresh_session):
            expiry.expire(self.root, now=15400)
        self.assertEqual(self.session.read_text(), "new-fixture-key")
        receipt = json.loads((self.root / "vaultwarden-session-expiry-receipt.json").read_text())
        self.assertEqual(receipt["result"], "superseded_by_fresh_session")


if __name__ == "__main__":
    unittest.main()
