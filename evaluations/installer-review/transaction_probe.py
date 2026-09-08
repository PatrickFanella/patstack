#!/usr/bin/env python3
"""Disposable public-function transaction probes for scripts/install.py.

All paths are created under this evaluation directory.  The probe exits zero
when expected recovery behavior passes, including an interrupted rollback.
"""
import importlib.util
import json
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent / ".runtime" / "work"
IMPLEMENTATION = Path(__file__).resolve().parents[2] / "scripts" / "install.py"
spec = importlib.util.spec_from_file_location("skill_installer", IMPLEMENTATION)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def clean(name):
    path = BASE / name
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def plan(root, expected, desired, source, previous=None):
    return {
        "sourceRoot": str(root),
        "sourceRevision": "toy",
        "operations": [{
            "destination": str(root / "target"),
            "source": str(source) if source else None,
            "expected": expected,
            "desired": desired,
            "group": 1,
            "payload": None,
            "action": "install" if desired else "retire",
        }],
        "protected": {},
        "previousInstalled": {"paths": previous or {}},
    }


def crash_at(phase):
    def fault(actual, _index):
        if actual == phase:
            raise RuntimeError("intentional interruption at " + phase)
    return fault


def check_apply_boundaries():
    results = {}
    for phase in ("after_backup", "after_remove", "after_install"):
        root = clean("apply-" + phase)
        state = root / "state"
        target = root / "target"
        source = root / "source"
        target.write_text("old")
        source.write_text("new")
        p = plan(root, installer.snapshot(target), installer.snapshot(source), source)
        try:
            installer.apply(p, state, fault=crash_at(phase))
        except RuntimeError as error:
            assert "intentional interruption" in str(error)
        else:
            raise AssertionError("fault hook did not interrupt " + phase)
        run = next(state.glob("run-*"))
        installer.apply(None, state, resume=run)
        assert target.read_text() == "new"
        assert installer.read(run / "journal.json")["status"] == "complete"
        results[phase] = "resumed"
    return results


def check_idempotency_and_edits():
    root = clean("idempotency-and-edits")
    state = root / "state"
    source = root / "source"
    target = root / "target"
    source.write_text("new")
    first = plan(root, None, installer.snapshot(source), source)
    installer.apply(first, state)
    installed = installer.read(installer.statefile(state))["paths"]
    second = plan(root, installed[str(target)], installer.snapshot(source), source, installed)
    installer.apply(second, state)
    assert target.read_text() == "new"

    edit_root = clean("intervening-edit")
    edit_state = edit_root / "state"
    edit_target = edit_root / "target"
    edit_source = edit_root / "source"
    edit_target.write_text("old")
    edit_source.write_text("new")
    interrupted = plan(edit_root, installer.snapshot(edit_target), installer.snapshot(edit_source), edit_source)
    try:
        installer.apply(interrupted, edit_state, fault=crash_at("after_backup"))
    except RuntimeError:
        pass
    run = next(edit_state.glob("run-*"))
    edit_target.write_text("human change")
    for action in (lambda: installer.apply(None, edit_state, resume=run), lambda: installer.rollback(run, edit_state)):
        try:
            action()
        except RuntimeError as error:
            assert "Drift" in str(error) or "intervening edits" in str(error)
        else:
            raise AssertionError("intervening edit was not preserved")
    assert edit_target.read_text() == "human change"
    return {"idempotent_reapply": "passed", "intervening_edit": "preserved"}


def check_rollback_and_interruption():
    root = clean("rollback")
    state = root / "state"
    target = root / "target"
    source = root / "source"
    target.write_text("old")
    source.write_text("new")
    p = plan(root, installer.snapshot(target), installer.snapshot(source), source)
    run = installer.apply(p, state)
    installer.rollback(run, state)
    assert target.read_text() == "old"

    broken = clean("interrupted-rollback")
    broken_state = broken / "state"
    broken_target = broken / "target"
    broken_source = broken / "source"
    broken_target.write_text("old")
    broken_source.write_text("new")
    broken_plan = plan(broken, installer.snapshot(broken_target), installer.snapshot(broken_source), broken_source)
    broken_run = installer.apply(broken_plan, broken_state)
    original_replace = installer.os.replace
    def fail_restore(src, dst):
        if Path(src).name.startswith(".target.rollback-stage-") and Path(dst) == broken_target:
            raise RuntimeError("simulated interruption after rollback removal")
        return original_replace(src, dst)
    installer.os.replace = fail_restore
    try:
        installer.rollback(broken_run, broken_state)
    except RuntimeError as error:
        assert "simulated interruption" in str(error)
    else:
        raise AssertionError("rollback injection did not fire")
    finally:
        installer.os.replace = original_replace
    assert not broken_target.exists(), "injection must leave destination removed"
    installer.rollback(broken_run, broken_state)
    assert broken_target.read_text() == "old"
    assert installer.read(broken_run / "journal.json")["status"] == "rolled-back"
    return {"ordinary_rollback": "passed", "interrupted_rollback": "resumed"}


if __name__ == "__main__":
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    report = {
        "apply_boundaries": check_apply_boundaries(),
        "idempotency_and_edits": check_idempotency_and_edits(),
        "rollback": check_rollback_and_interruption(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
