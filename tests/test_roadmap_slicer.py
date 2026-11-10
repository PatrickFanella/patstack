import copy
import importlib.util
import json
import re
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/manage-roadmaps-and-issues"
spec = importlib.util.spec_from_file_location("roadmap", SKILL / "scripts/roadmap.py")
roadmap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(roadmap)
EXAMPLE = json.loads((SKILL / "assets/plan.example.json").read_text())


class FakeGitea:
    """Enough of the Gitea API, reached through a fake `tea api`, to exercise publishing."""

    def __init__(self, dependencies=True):
        self.issues, self.labels, self.milestones, self.deps, self.pins = {}, {}, {}, {}, []
        self.dependencies = dependencies
        self.writes, self.timeline = [], {}

    def __call__(self, cmd, input=None, capture_output=True, text=True):
        method, path = cmd[cmd.index("-X") + 1], cmd[-1]
        body = json.loads(input) if input else None
        if method != "GET":
            self.writes.append((method, path))
        try:
            status, data = self.route(method, path.split("?")[0], body, path)
        except KeyError:
            status, data = 404, {"message": "not found"}
        return types.SimpleNamespace(returncode=0, stdout=json.dumps(data) if data is not None else "",
                                     stderr=f"HTTP/2.0 {status} X\n")

    def route(self, method, path, body, full):
        page = int(re.search(r"page=(\d+)", full).group(1)) if "page=" in full else 1
        m = re.match(r"^/repos/o/r(/.*)?$", path)
        if not m:
            raise KeyError(path)
        rest = m.group(1) or ""
        if rest == "":
            return 200, {"has_issues": True, "internal_tracker": {"enable_issue_dependencies": self.dependencies}}
        if rest == "/issues" and method == "GET":
            items = [self.issues[n] for n in sorted(self.issues)]
            return 200, items[(page - 1) * 50: page * 50]
        if rest == "/issues" and method == "POST":
            n = len(self.issues) + 1
            names = {v["id"]: k for k, v in self.labels.items()}
            self.issues[n] = {"number": n, "title": body["title"], "body": body["body"], "state": "open",
                              "labels": [{"name": names[i]} for i in body["labels"]]}
            return 201, self.issues[n]
        if rest == "/labels":
            if method == "POST":
                self.labels[body["name"]] = {"id": len(self.labels) + 1, "name": body["name"]}
                return 201, self.labels[body["name"]]
            return 200, list(self.labels.values()) if page == 1 else []
        if rest == "/milestones":
            if method == "POST":
                self.milestones[body["title"]] = {"id": len(self.milestones) + 1, "title": body["title"]}
                return 201, self.milestones[body["title"]]
            return 200, list(self.milestones.values()) if page == 1 else []
        if rest == "/new_pin_allowed":
            return 200, {"issues": True, "pull_requests": True}
        m = re.match(r"^/issues/(\d+)(/.*)?$", rest)
        n, tail = int(m.group(1)), m.group(2) or ""
        issue = self.issues[n]
        if tail == "" and method == "GET":
            return 200, issue
        if tail == "" and method == "PATCH":
            issue.update(body)
            return 201, issue
        if tail == "/dependencies" and method == "GET":
            return 200, [self.issues[b] for b in sorted(self.deps.get(n, set()))]
        if tail == "/dependencies" and method == "POST":
            self.deps.setdefault(n, set()).add(body["index"])
            return 201, issue
        if tail == "/timeline":
            return 200, self.timeline.get(n, []) if page == 1 else []
        if tail == "/labels":
            return 200, issue["labels"]
        if tail == "/pin":
            self.pins.append(n)
            return 204, None
        raise KeyError(rest)


class RoadmapSlicerTest(unittest.TestCase):
    def setUp(self):
        self.plan = copy.deepcopy(EXAMPLE)

    def test_example_validates_and_orders_blockers_first(self):
        errors, _ = roadmap.validate(self.plan)
        self.assertEqual(errors, [])
        sched = roadmap.schedule(self.plan)
        position = {k: n for n, k in enumerate(sched["order"])}
        for issue in self.plan["issues"]:
            for b in issue.get("blocked_by", []):
                self.assertLess(position[b], position[issue["key"]])
        self.assertEqual(sched["order"][0], "mail-provider-spike")  # risk first
        self.assertEqual(sched["critical"][-1], "rollout")

    def test_cycles_and_unknown_blockers_are_errors(self):
        self.plan["issues"][1]["blocked_by"] = ["rollout"]
        errors, _ = roadmap.validate(self.plan)
        self.assertTrue(any("cycle" in e for e in errors), errors)
        self.plan["issues"][1]["blocked_by"] = ["nope"]
        errors, _ = roadmap.validate(self.plan)
        self.assertTrue(any("unknown blocker" in e for e in errors), errors)

    def test_oversized_issue_is_rejected(self):
        self.plan["issues"][1]["size"] = "XL"
        errors, _ = roadmap.validate(self.plan)
        self.assertTrue(any("split" in e for e in errors), errors)

    def test_dry_run_writes_nothing(self):
        fake = FakeGitea()
        roadmap.publish(self.plan, roadmap.Gitea("o/r", runner=fake), apply=False, out=lambda *_: None)
        self.assertEqual(fake.writes, [])

    def test_publish_is_idempotent_and_wires_dependencies(self):
        fake = FakeGitea()
        api = roadmap.Gitea("o/r", runner=fake)
        numbers = roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        self.assertEqual(len(fake.issues), 1 + 2 + 7)
        self.assertEqual(numbers["roadmap"], 1)
        self.assertEqual(fake.pins, [1])
        send, model, spike = numbers["issue:send-link"], numbers["issue:token-model"], numbers["issue:mail-provider-spike"]
        self.assertEqual(fake.deps[send], {model, spike})
        self.assertEqual(fake.deps[numbers["epic:tokens"]], {numbers[f"issue:{k}"] for k in
                                                            ("mail-provider-spike", "token-model", "redeem-link", "send-link")})
        self.assertEqual(fake.deps[1], {numbers["epic:tokens"], numbers["epic:client"]})
        self.assertIn(f"#{model} [A2]", fake.issues[1]["body"])
        self.assertNotIn("Being populated", fake.issues[1]["body"])
        self.assertEqual(roadmap.verify(self.plan, api, out=lambda *_: None), 0)
        before = len(fake.writes)
        roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        self.assertEqual(len(fake.writes), before)  # nothing new to do

    def test_rerun_adds_new_issue_and_rewrites_tracking_bodies(self):
        fake = FakeGitea()
        api = roadmap.Gitea("o/r", runner=fake)
        roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        self.plan["issues"].append({"key": "audit-log", "epic": "client", "title": "Log sign-in link use",
                                    "summary": "Record each issued and redeemed link.", "blocked_by": ["redeem-link"],
                                    "acceptance": ["Each redemption writes one audit row."], "verify": ["make test-auth"]})
        numbers = roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        self.assertEqual(len(fake.issues), 11)
        self.assertIn(f"#{numbers['issue:audit-log']}", fake.issues[1]["body"])

    def test_refresh_ticks_closed_issues_and_reports_frontier(self):
        fake = FakeGitea()
        api = roadmap.Gitea("o/r", runner=fake)
        numbers = roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        for key in ("mail-provider-spike", "token-model"):
            fake.issues[numbers[f"issue:{key}"]]["state"] = "closed"
        frontier = roadmap.refresh(api, 1, apply=True, out=lambda *_: None)
        self.assertEqual(set(frontier), {numbers["issue:redeem-link"], numbers["issue:send-link"]})
        self.assertIn(f"- [x] #{numbers['issue:token-model']}", fake.issues[1]["body"])
        self.assertIn(f"- [x] #{numbers['issue:token-model']}", fake.issues[numbers["epic:tokens"]]["body"])

    def test_refresh_closes_issue_whose_pr_merged_while_blocked(self):
        fake = FakeGitea()
        api = roadmap.Gitea("o/r", runner=fake)
        numbers = roadmap.publish(self.plan, api, apply=True, out=lambda *_: None)
        redeem, model = numbers["issue:redeem-link"], numbers["issue:token-model"]
        fake.timeline[redeem] = [{"type": "pull_ref", "ref_action": "closes",
                                  "ref_issue": {"number": 99, "pull_request": {"merged": True}}}]
        lines = []
        roadmap.refresh(api, 1, apply=True, out=lines.append)
        self.assertEqual(fake.issues[redeem]["state"], "open")  # its blocker is still open
        self.assertTrue(any("stays open" in l for l in lines), lines)
        fake.issues[model]["state"] = "closed"
        roadmap.refresh(api, 1, apply=True, out=lines.append)
        self.assertEqual(fake.issues[redeem]["state"], "closed")
        self.assertIn(f"- [x] #{redeem}", fake.issues[1]["body"])

    def test_disabled_dependencies_stop_before_writing(self):
        fake = FakeGitea(dependencies=False)
        with self.assertRaises(roadmap.PlanError):
            roadmap.publish(self.plan, roadmap.Gitea("o/r", runner=fake), apply=True, out=lambda *_: None)
        self.assertEqual(fake.writes, [])


if __name__ == "__main__":
    unittest.main()
