"""Transaction recovery coverage for the local skill installer."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_installer", ROOT / "scripts" / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


def toy_plan(root, expected, desired, source, previous=None):
    target = root / "target"
    return {
        "sourceRoot": str(root),
        "sourceRevision": "toy",
        "operations": [{
            "destination": str(target), "source": str(source) if source else None,
            "expected": expected, "desired": desired, "group": 1,
            "payload": None, "action": "install" if desired else "retire",
        }],
        "protected": {},
        "previousInstalled": {"paths": previous or {}},
    }


class InstallerTransactionTests(unittest.TestCase):
    def make_fixture(self, directory, old="old", new="new"):
        root = Path(directory)
        target, source = root / "target", root / "source"
        target.write_text(old)
        source.write_text(new)
        return root, root / "state", target, source

    def test_apply_resumes_after_each_apply_boundary(self):
        for phase in ("after_backup", "after_remove", "after_install"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as directory:
                root, state, target, source = self.make_fixture(directory)
                plan = toy_plan(root, installer.snapshot(target), installer.snapshot(source), source)
                def interrupt(actual, _index):
                    if actual == phase:
                        raise RuntimeError("expected interruption")
                with self.assertRaisesRegex(RuntimeError, "expected interruption"):
                    installer.apply(plan, state, fault=interrupt)
                run = next(state.glob("run-*"))
                installer.apply(None, state, resume=run)
                self.assertEqual(target.read_text(), "new")
                self.assertEqual(installer.read(run / "journal.json")["status"], "complete")

    def test_reapply_is_idempotent_and_intervening_edit_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root, state, target, source = self.make_fixture(directory)
            first = toy_plan(root, installer.snapshot(target), installer.snapshot(source), source)
            installer.apply(first, state)
            installed = installer.read(installer.statefile(state))["paths"]
            installer.apply(toy_plan(root, installed[str(target)], installer.snapshot(source), source, installed), state)
            self.assertEqual(target.read_text(), "new")

        with tempfile.TemporaryDirectory() as directory:
            root, state, target, source = self.make_fixture(directory)
            plan = toy_plan(root, installer.snapshot(target), installer.snapshot(source), source)
            def interrupt_after_backup(phase, _index):
                if phase == "after_backup":
                    raise RuntimeError("expected interruption")
            with self.assertRaisesRegex(RuntimeError, "expected interruption"):
                installer.apply(plan, state, fault=interrupt_after_backup)
            run = next(state.glob("run-*"))
            target.write_text("human edit")
            with self.assertRaisesRegex(RuntimeError, "Drift"):
                installer.apply(None, state, resume=run)
            with self.assertRaisesRegex(RuntimeError, "intervening edits"):
                installer.rollback(run, state)
            self.assertEqual(target.read_text(), "human edit")

    def test_rollback_resumes_after_destination_removal(self):
        with tempfile.TemporaryDirectory() as directory:
            root, state, target, source = self.make_fixture(directory)
            run = installer.apply(toy_plan(root, installer.snapshot(target), installer.snapshot(source), source), state)
            original_replace = installer.os.replace
            def interrupt_restore(src, dst):
                if Path(src).name.startswith(".target.rollback-stage-") and Path(dst) == target:
                    raise RuntimeError("expected rollback interruption")
                return original_replace(src, dst)
            installer.os.replace = interrupt_restore
            try:
                with self.assertRaisesRegex(RuntimeError, "expected rollback interruption"):
                    installer.rollback(run, state)
            finally:
                installer.os.replace = original_replace
            self.assertFalse(target.exists())
            self.assertEqual(installer.read(run / "journal.json")["rollbackProgress"]["0"], "restoring")
            installer.rollback(run, state)
            self.assertEqual(target.read_text(), "old")
            self.assertEqual(installer.read(run / "journal.json")["status"], "rolled-back")


if __name__ == "__main__":
    unittest.main()
