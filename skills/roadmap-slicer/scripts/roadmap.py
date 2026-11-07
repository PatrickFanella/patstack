#!/usr/bin/env python3
"""Order a plan breakdown and publish it to Gitea as a Roadmap with Epic and Single-PR issues.

  check   PLAN [--preview]                      validate and order; no network
  publish PLAN --repo OWNER/NAME [--apply]      dry run unless --apply; reruns skip existing issues
  verify  PLAN --repo OWNER/NAME                read back issues, labels and dependencies
  refresh --repo OWNER/NAME --roadmap N [--apply]  tick closed issues in tracking bodies; list the frontier

Network calls go through `tea api`, so tea's login handles authentication (pass --login to choose one).
The plan format is described in references/plan-format.md.
"""
import argparse
import heapq
import json
import re
import string
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
KEY = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SIZES = {"S": 1, "M": 2, "L": 3}
KINDS = ("task", "spike")
MODES = ("afk", "hitl")
ROLE_LABELS = {
    "roadmap": ("Planning/Roadmap", "5319e7", "Tracking issue for a whole plan"),
    "epic": ("Planning/Epic", "1d76db", "Tracking issue for one feature of a roadmap"),
    "task": ("Planning/Single-PR", "0e8a16", "Delivery unit: one reviewable PR"),
    "spike": ("Planning/Spike", "fbca04", "Time-boxed investigation that ends in a recorded decision"),
}
CHECK_LINE = re.compile(r"^(\s*- \[)([ xX])(\] #(\d+)\b)", re.M)
MERMAID_LIMIT = 40


class PlanError(Exception):
    pass


# ---------------------------------------------------------------- plan model

def load_plan(path):
    try:
        plan = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PlanError(f"cannot read plan {path}: {exc}")
    plan.setdefault("epics", [])
    plan.setdefault("issues", [])
    return plan


def validate(plan):
    """Return (errors, warnings). Errors block publishing."""
    errors, warnings = [], []
    slug = plan.get("slug", "")
    if not KEY.match(slug):
        errors.append("slug: required, lowercase letters, digits and hyphens")
    roadmap = plan.get("roadmap") or {}
    for field in ("title", "goal"):
        if not str(roadmap.get(field, "")).strip():
            errors.append(f"roadmap.{field}: required")
    epics = {e.get("key"): e for e in plan["epics"]}
    issues = {}
    for e in plan["epics"]:
        if not KEY.match(str(e.get("key", ""))):
            errors.append(f"epic {e.get('key')!r}: bad key")
        if not str(e.get("title", "")).strip():
            errors.append(f"epic {e.get('key')}: title required")
        if e.get("blocked_by"):
            errors.append(f"epic {e.get('key')}: put blocked_by on its issues, not the epic")
    for i in plan["issues"]:
        k = str(i.get("key", ""))
        if not KEY.match(k):
            errors.append(f"issue {k!r}: bad key")
            continue
        if k in issues:
            errors.append(f"issue {k}: duplicate key")
        issues[k] = i
        if not str(i.get("title", "")).strip():
            errors.append(f"issue {k}: title required")
        if not str(i.get("summary", "")).strip():
            errors.append(f"issue {k}: summary required (the outcome this PR delivers)")
        kind = i.get("kind", "task")
        if kind not in KINDS:
            errors.append(f"issue {k}: kind must be one of {KINDS}")
        size = i.get("size", "M")
        if size not in SIZES:
            errors.append(f"issue {k}: size {size!r} is not S, M or L; split anything larger")
        elif size == "L":
            warnings.append(f"issue {k}: size L; confirm it still fits one reviewable PR")
        if i.get("mode", "afk") not in MODES:
            errors.append(f"issue {k}: mode must be afk or hitl")
        if kind == "task" and not i.get("acceptance"):
            errors.append(f"issue {k}: at least one acceptance criterion")
        if kind == "spike" and not str(i.get("question", "")).strip():
            errors.append(f"issue {k}: a spike needs the question it answers")
        if kind == "task" and not i.get("verify"):
            warnings.append(f"issue {k}: no verification command or check")
        if i.get("epic") and i["epic"] not in epics:
            errors.append(f"issue {k}: unknown epic {i['epic']!r}")
        if plan["epics"] and not i.get("epic"):
            warnings.append(f"issue {k}: not in an epic; it will hang off the roadmap directly")
    for k, i in issues.items():
        for b in i.get("blocked_by", []):
            if b == k:
                errors.append(f"issue {k}: blocks itself")
            elif b not in issues:
                errors.append(f"issue {k}: unknown blocker {b!r}")
        if len(i.get("blocked_by", [])) > 5:
            warnings.append(f"issue {k}: {len(i['blocked_by'])} blockers; check each is a hard edge")
    for key, e in epics.items():
        children = [k for k, i in issues.items() if i.get("epic") == key]
        if not children:
            errors.append(f"epic {key}: has no issues")
        elif len(children) < 3:
            warnings.append(f"epic {key}: {len(children)} issue(s); an epic earns its place at three or more PRs")
    if not issues:
        errors.append("issues: the plan has no issues")
    if not errors:
        cycle = find_cycle(issues)
        if cycle:
            errors.append("dependency cycle: " + " -> ".join(cycle))
    if len(issues) > 60:
        warnings.append(f"{len(issues)} issues; consider one roadmap per release")
    return errors, warnings


def find_cycle(issues):
    state = {}

    def visit(k, stack):
        state[k] = 1
        stack.append(k)
        for b in issues[k].get("blocked_by", []):
            if state.get(b) == 1:
                return stack[stack.index(b):] + [b]
            if b not in state:
                found = visit(b, stack)
                if found:
                    return found
        state[k] = 2
        stack.pop()
        return None

    for k in issues:
        if k not in state:
            found = visit(k, [])
            if found:
                return found
    return None


def schedule(plan):
    """Topological order with risk-first, critical-path-first tie-breaks."""
    issues = {i["key"]: i for i in plan["issues"]}
    declared = {k: n for n, k in enumerate(issues)}
    dependents = {k: [] for k in issues}
    for k, i in issues.items():
        for b in i.get("blocked_by", []):
            dependents[b].append(k)
    tail = {}

    def tail_of(k):  # weighted length of the longest chain starting at k
        if k not in tail:
            tail[k] = SIZES[issues[k].get("size", "M")] + max((tail_of(d) for d in dependents[k]), default=0)
        return tail[k]

    wave = {}

    def wave_of(k):
        if k not in wave:
            wave[k] = 1 + max((wave_of(b) for b in issues[k].get("blocked_by", [])), default=0)
        return wave[k]

    def rank(k):
        i = issues[k]
        risky = i.get("kind") == "spike" or i.get("risk") == "high"
        return (0 if risky else 1, -tail_of(k), declared[k])

    waiting = {k: len(set(i.get("blocked_by", []))) for k, i in issues.items()}
    ready = [(rank(k), k) for k, n in waiting.items() if n == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        _, k = heapq.heappop(ready)
        order.append(k)
        for d in dependents[k]:
            waiting[d] -= 1
            if waiting[d] == 0:
                heapq.heappush(ready, (rank(d), d))
    for k in issues:
        wave_of(k)
    start = max((k for k in issues if not issues[k].get("blocked_by")), key=lambda k: (tail_of(k), -declared[k]))
    critical = [start]
    while dependents[critical[-1]]:
        critical.append(max(dependents[critical[-1]], key=lambda d: (tail_of(d), -declared[d])))
    return {"order": order, "wave": wave, "critical": critical, "dependents": dependents,
            "total": sum(SIZES[i.get("size", "M")] for i in issues.values()), "critical_weight": tail_of(start)}


def assign_codes(plan, sched):
    """Epic letters follow the execution order; issues are numbered inside their epic."""
    issues = {i["key"]: i for i in plan["issues"]}
    letters, counts, codes = {}, {}, {}
    for e in plan["epics"]:
        if e.get("code"):
            letters[e["key"]] = e["code"]
    for k in sched["order"]:
        epic = issues[k].get("epic")
        if epic and epic not in letters:
            n = len([x for x in letters.values() if not x.isdigit()])
            letters[epic] = column_letter(n)
        prefix = letters.get(epic, "")
        counts[prefix] = counts.get(prefix, 0) + 1
        codes[k] = issues[k].get("code") or f"{prefix}{counts[prefix]}"
    for e in plan["epics"]:
        letters.setdefault(e["key"], column_letter(len(letters)))
    return letters, codes


def column_letter(n):
    out = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        out = chr(65 + r) + out
    return out


# ---------------------------------------------------------------- rendering

class Book:
    """Titles, codes and issue numbers shared by every rendered body."""

    def __init__(self, plan, sched, numbers=None, closed=None):
        self.plan, self.sched = plan, sched
        self.issues = {i["key"]: i for i in plan["issues"]}
        self.epics = {e["key"]: e for e in plan["epics"]}
        self.letters, self.codes = assign_codes(plan, sched)
        self.use_codes = plan.get("codes", True)
        self.numbers = {} if numbers is None else numbers
        self.closed = set() if closed is None else closed

    def marker(self, ident):
        return f"<!-- roadmap-slicer:{self.plan['slug']}:{ident} -->"

    def title(self, ident):
        if ident == "roadmap":
            return f"[Roadmap] {self.plan['roadmap']['title']}"
        if ident.startswith("epic:"):
            key = ident[5:]
            head = f"[Epic {self.letters[key]}] " if self.use_codes else ""
            return head + self.epics[key]["title"]
        key = ident[6:]
        head = f"[{self.codes[key]}] " if self.use_codes else ""
        return head + self.issues[key]["title"]

    def ref(self, ident):
        number = self.numbers.get(ident)
        return f"#{number} {self.title(ident)}" if number else f"`{ident}` {self.title(ident)}"

    def check(self, ident):
        return "x" if ident in self.closed else " "


def bullets(items, box=False):
    items = [items] if isinstance(items, str) else (items or [])
    return "\n".join(("- [ ] " if box else "- ") + str(x) for x in items)


def fill(template, values):
    text = string.Template((ASSETS / template).read_text()).safe_substitute(values)
    text = re.sub(r"(?ms)^## [^\n]*\n\s*(?=^## |\Z)", "", text)  # drop empty sections
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def task_line(book, key):
    i = book.issues[key]
    ident = "issue:" + key
    tags = [i.get("size", "M")]
    if i.get("kind") == "spike":
        tags.append("spike")
    if i.get("mode") == "hitl":
        tags.append("needs a human")
    after = [book.ref("issue:" + b).split(" ", 1)[0] for b in i.get("blocked_by", [])]
    tail = f"; after {', '.join(after)}" if after else ""
    return f"- [{book.check(ident)}] {book.ref(ident)} ({', '.join(tags)}{tail})"


def render_order(book):
    waves = {}
    for k in book.sched["order"]:
        waves.setdefault(book.sched["wave"][k], []).append(k)
    out = []
    for w in sorted(waves):
        label = ": can start now" if w == 1 else ""
        out.append(f"### Wave {w}{label}\n\n" + "\n".join(task_line(book, k) for k in waves[w]))
    return "\n\n".join(out)


def render_graph(book):
    if len(book.issues) > MERMAID_LIMIT:
        return ""
    lines = ["```mermaid", "graph TD"]
    node = {k: re.sub(r"[^A-Za-z0-9]", "_", book.codes[k] if book.use_codes else k) for k in book.issues}
    for k in book.sched["order"]:
        label = book.title("issue:" + k).replace('"', "'")
        lines.append(f'  {node[k]}["{label[:60]}"]')
    for k in book.sched["order"]:
        for b in book.issues[k].get("blocked_by", []):
            lines.append(f"  {node[b]} --> {node[k]}")
    lines.append("```")
    return "\n".join(lines)


def render_roadmap(book):
    r = book.plan["roadmap"]
    epics = []
    for key, e in sorted(book.epics.items(), key=lambda kv: book.letters[kv[0]]):
        count = sum(1 for i in book.issues.values() if i.get("epic") == key)
        epics.append(f"- [{book.check('epic:' + key)}] {book.ref('epic:' + key)}: {count} PR(s). {e.get('summary', '')}".rstrip())
    crit = book.sched["critical"]
    critical = " → ".join(book.ref("issue:" + k).split(" ", 1)[0] for k in crit)
    critical += f"\n\n{len(crit)} issues, {book.sched['critical_weight']} of {book.sched['total']} size points (S=1, M=2, L=3). Start these first; splitting work on this chain shortens the roadmap."
    return fill("roadmap.md", {
        "marker": book.marker("roadmap"),
        "goal": r["goal"].strip(),
        "plan": r.get("plan", ""),
        "structure": ("This roadmap and its epics are tracking issues, not implementation PRs." if book.epics
                      else "This roadmap is a tracking issue, not an implementation PR."),
        "decisions": bullets(r.get("decisions")),
        "epics": "\n".join(epics),
        "order": render_order(book),
        "critical": critical,
        "graph": render_graph(book),
        "rules": bullets(r.get("rules")),
        "out_of_scope": bullets(r.get("out_of_scope")),
    })


def render_epic(book, key):
    e = book.epics[key]
    children = [k for k in book.sched["order"] if book.issues[k].get("epic") == key]
    return fill("epic.md", {
        "marker": book.marker("epic:" + key),
        "summary": e.get("summary", "").strip(),
        "roadmap": book.ref("roadmap"),
        "children": "\n".join(task_line(book, k) for k in children),
        "exit": bullets(e.get("exit")),
        "out_of_scope": bullets(e.get("out_of_scope")),
    })


def render_issue(book, key):
    i = book.issues[key]
    blockers = [book.ref("issue:" + b) for b in i.get("blocked_by", [])]
    mode = i.get("mode", "afk")
    who = ("An agent can finish this alone." if mode == "afk"
           else "Needs a human checkpoint: " + (i.get("hitl_reason") or "see notes."))
    return fill("spike.md" if i.get("kind") == "spike" else "single-pr.md", {
        "marker": book.marker("issue:" + key),
        "summary": i["summary"].strip(),
        "question": i.get("question", ""),
        "timebox": i.get("timebox", "one working session"),
        "epic_line": "Epic: " + book.ref("epic:" + i["epic"]) if i.get("epic") else "",
        "roadmap": book.ref("roadmap"),
        "blocked_by": bullets(blockers) or "Nothing; this can start now.",
        "acceptance": bullets(i.get("acceptance"), box=True),
        "verify": bullets(i.get("verify")),
        "paths": bullets(i.get("paths")) + "\n\nThese are starting points, not a list of files to edit." if i.get("paths") else "",
        "out_of_scope": bullets(i.get("out_of_scope")),
        "notes": i.get("notes", ""),
        "who": who,
        "size": i.get("size", "M"),
    })


def preview(plan, sched):
    book = Book(plan, sched)
    parts = [f"# {book.title('roadmap')}\n\n" + render_roadmap(book)]
    for key in sorted(book.epics, key=lambda k: book.letters[k]):
        parts.append(f"# {book.title('epic:' + key)}\n\n" + render_epic(book, key))
    for key in sched["order"]:
        parts.append(f"# {book.title('issue:' + key)}\n\n" + render_issue(book, key))
    return "\n\n---\n\n".join(parts)


def summary(plan, sched):
    book = Book(plan, sched)
    lines = ["Execution order (wave, code, key, size, blockers):"]
    for n, k in enumerate(sched["order"], 1):
        i = book.issues[k]
        blockers = ",".join(i.get("blocked_by", [])) or "-"
        flag = " spike" if i.get("kind") == "spike" else (" risk" if i.get("risk") == "high" else "")
        lines.append(f"{n:3}. w{sched['wave'][k]} {book.codes[k]:>5} {k} {i.get('size', 'M')}{flag} <- {blockers}")
    frontier = [k for k in sched["order"] if sched["wave"][k] == 1]
    lines.append(f"Frontier ({len(frontier)}): {', '.join(frontier)}")
    lines.append(f"Critical path ({sched['critical_weight']}/{sched['total']} points): {' -> '.join(sched['critical'])}")
    lines.append(f"Waves: {max(sched['wave'].values())}; issues: {len(book.issues)}; epics: {len(book.epics)}")
    return "\n".join(lines)


# ---------------------------------------------------------------- Gitea

class ApiError(Exception):
    pass


class Gitea:
    def __init__(self, repo, login=None, runner=subprocess.run):
        if not re.match(r"^[\w.-]+/[\w.-]+$", repo or ""):
            raise PlanError("--repo must be OWNER/NAME")
        self.owner, self.name = repo.split("/")
        self.base = f"/repos/{self.owner}/{self.name}"
        self.login, self.runner = login, runner

    def call(self, method, path, body=None):
        cmd = ["tea", "api", "-i", "-X", method]
        if self.login:
            cmd += ["--login", self.login]
        if body is not None:
            cmd += ["-d", "@-"]
        cmd.append(path)
        proc = self.runner(cmd, input=None if body is None else json.dumps(body), capture_output=True, text=True)
        status = re.search(r"^HTTP/\S+ (\d{3})", proc.stderr or "", re.M)
        code = int(status.group(1)) if status else 0
        if proc.returncode != 0 or not 200 <= code < 300:
            raise ApiError(f"{method} {path} -> {code or 'no status'}: {(proc.stdout or proc.stderr or '').strip()[:300]}")
        return json.loads(proc.stdout) if (proc.stdout or "").strip() else None

    def pages(self, path):
        out, page = [], 1
        sep = "&" if "?" in path else "?"
        while True:
            batch = self.call("GET", f"{path}{sep}limit=50&page={page}") or []
            out += batch
            if len(batch) < 50:
                return out
            page += 1


def find_existing(api, slug):
    found = {}
    pattern = re.compile(r"<!-- roadmap-slicer:" + re.escape(slug) + r":(\S+) -->")
    for issue in api.pages(f"{api.base}/issues?state=all&type=issues"):
        m = pattern.search(issue.get("body") or "")
        if m:
            found[m.group(1)] = issue
    return found


def label_ids(api):
    labels = {l["name"]: l["id"] for l in api.pages(f"{api.base}/labels")}
    try:
        for l in api.pages(f"/orgs/{api.owner}/labels"):
            labels.setdefault(l["name"], l["id"])
    except ApiError:
        pass  # user-owned repository
    return labels


def wanted_labels(plan):
    named = set(plan["roadmap"].get("labels", []))
    for x in plan["epics"] + plan["issues"]:
        named |= set(x.get("labels", []))
    roles = {"roadmap", "task"} | ({"epic"} if plan["epics"] else set())
    roles |= {"spike"} if any(i.get("kind") == "spike" for i in plan["issues"]) else set()
    return roles, named


def publish(plan, api, apply, update=False, pin=True, out=print):
    errors, warnings = validate(plan)
    if errors:
        raise PlanError("plan has errors:\n  " + "\n  ".join(errors))
    for w in warnings:
        out("warning: " + w)
    sched = schedule(plan)
    repo = api.call("GET", api.base)
    if not repo.get("has_issues", True):
        raise PlanError(f"{api.owner}/{api.name} has issues disabled")
    if not (repo.get("internal_tracker") or {}).get("enable_issue_dependencies"):
        raise PlanError("issue dependencies are disabled for this repository; enable them in its settings "
                        "(internal_tracker.enable_issue_dependencies) or ask the owner")
    existing = find_existing(api, plan["slug"])
    labels = label_ids(api)
    roles, named = wanted_labels(plan)
    missing_named = sorted(n for n in named if n not in labels)
    if missing_named:
        raise PlanError("labels not in the repository (pick existing names or create them first): " + ", ".join(missing_named))
    milestones = {m["title"]: m["id"] for m in api.pages(f"{api.base}/milestones?state=all")}
    wanted_ms = {x.get("milestone") for x in [plan["roadmap"]] + plan["epics"] + plan["issues"]} - {None, ""}
    act = "" if apply else "would "
    for role in sorted(roles):
        name, color, desc = ROLE_LABELS[role]
        if name not in labels:
            out(f"{act}create label {name}")
            if apply:
                labels[name] = api.call("POST", f"{api.base}/labels",
                                        {"name": name, "color": color, "description": desc, "exclusive": True})["id"]
    for title in sorted(wanted_ms - milestones.keys()):
        out(f"{act}create milestone {title}")
        if apply:
            milestones[title] = api.call("POST", f"{api.base}/milestones", {"title": title})["id"]

    numbers = {ident: issue["number"] for ident, issue in existing.items()}
    closed = {ident for ident, issue in existing.items() if issue.get("state") == "closed"}
    book = Book(plan, sched, numbers, closed)
    idents = ["roadmap"] + [f"epic:{k}" for k in sorted(book.epics, key=lambda k: book.letters[k])]
    idents += [f"issue:{k}" for k in sched["order"]]

    def item(ident):
        if ident == "roadmap":
            return plan["roadmap"], "roadmap"
        if ident.startswith("epic:"):
            return book.epics[ident[5:]], "epic"
        i = book.issues[ident[6:]]
        return i, i.get("kind", "task")

    def body(ident):
        if ident == "roadmap":
            return render_roadmap(book)
        if ident.startswith("epic:"):
            return render_epic(book, ident[5:])
        return render_issue(book, ident[6:])

    def label_list(ident):
        data, role = item(ident)
        return [labels[n] for n in [ROLE_LABELS[role][0]] + list(data.get("labels", [])) if n in labels]

    created = []
    for ident in idents:  # tracking issues first, then work in execution order
        if ident in numbers:
            continue
        data, _ = item(ident)
        payload = {"title": book.title(ident), "labels": label_list(ident),
                   "body": book.marker(ident) + "\n\nBeing populated by roadmap-slicer." if is_tracking(ident) else body(ident)}
        if data.get("milestone"):
            payload["milestone"] = milestones.get(data["milestone"], 0)
        out(f"{act}create {ident}: {payload['title']}")
        if apply:
            numbers[ident] = api.call("POST", f"{api.base}/issues", payload)["number"]
            created.append(ident)
    pending = [i for i in idents if i not in numbers]  # only non-empty in a dry run
    for ident in idents:
        rewrite = is_tracking(ident) and (created or pending or update)
        if not (rewrite or (update and ident not in created and ident not in pending)):
            continue
        out(f"{act}write body of {ident}")
        if apply:
            api.call("PATCH", f"{api.base}/issues/{numbers[ident]}", {"title": book.title(ident), "body": body(ident)})
            if update:
                api.call("POST", f"{api.base}/issues/{numbers[ident]}/labels", {"labels": label_list(ident)})
    for ident, blockers in expected_edges(plan, book).items():
        have = set()
        if ident in numbers:
            have = {d["number"] for d in api.call("GET", f"{api.base}/issues/{numbers[ident]}/dependencies") or []}
        for b in blockers:
            if numbers.get(b) in have:
                continue
            out(f"{act}make {ident} depend on {b}")
            if apply:
                api.call("POST", f"{api.base}/issues/{numbers[ident]}/dependencies",
                         {"owner": api.owner, "repo": api.name, "index": numbers[b]})
    if pin and ("roadmap" in created or "roadmap" in pending):
        allowed = api.call("GET", f"{api.base}/new_pin_allowed") or {}
        if allowed.get("issues"):
            out(f"{act}pin the roadmap")
            if apply:
                api.call("POST", f"{api.base}/issues/{numbers['roadmap']}/pin")
        else:
            out("note: no free pin slot; the roadmap will not be pinned")
    if not apply:
        out("dry run: nothing changed. Re-run with --apply to publish.")
        return None
    out(f"published: {len(created)} created, {len(idents) - len(created)} already existed")
    return numbers


def is_tracking(ident):
    return ident == "roadmap" or ident.startswith("epic:")


def expected_edges(plan, book):
    """Child-to-child blockers, epics on their children, the roadmap on its epics (or issues)."""
    edges = {}
    for k, i in book.issues.items():
        edges[f"issue:{k}"] = [f"issue:{b}" for b in i.get("blocked_by", [])]
    for key in book.epics:
        edges[f"epic:{key}"] = [f"issue:{k}" for k in book.sched["order"] if book.issues[k].get("epic") == key]
    top = [f"epic:{k}" for k in book.epics] + [f"issue:{k}" for k, i in book.issues.items() if not i.get("epic")]
    edges["roadmap"] = top
    return edges


def verify(plan, api, out=print):
    sched = schedule(plan)
    existing = find_existing(api, plan["slug"])
    numbers = {ident: issue["number"] for ident, issue in existing.items()}
    book = Book(plan, sched, numbers)
    problems = 0
    for ident, blockers in expected_edges(plan, book).items():
        if ident not in existing:
            out(f"MISSING {ident}")
            problems += 1
            continue
        issue = existing[ident]
        role = "roadmap" if ident == "roadmap" else ("epic" if ident.startswith("epic:") else book.issues[ident[6:]].get("kind", "task"))
        if ROLE_LABELS[role][0] not in {l["name"] for l in issue.get("labels", [])}:
            out(f"LABEL   #{issue['number']} lacks {ROLE_LABELS[role][0]}")
            problems += 1
        have = {d["number"] for d in api.call("GET", f"{api.base}/issues/{issue['number']}/dependencies") or []}
        want = {numbers[b] for b in blockers if b in numbers}
        if want - have:
            out(f"DEPS    #{issue['number']} missing blockers {sorted(want - have)}")
            problems += 1
    out(f"{len(existing)} issues found, {problems} problem(s)")
    if "roadmap" in numbers:
        out(f"roadmap: #{numbers['roadmap']}")
    return problems


def refresh(api, roadmap, apply, out=print):
    """Tick checklist lines whose issues closed; untick reopened ones; print the frontier."""
    cache = {}

    def issue(n):
        if n not in cache:
            cache[n] = api.call("GET", f"{api.base}/issues/{n}")
        return cache[n]

    def sync(n):
        text = issue(n).get("body") or ""
        new = CHECK_LINE.sub(lambda m: m.group(1) + ("x" if issue(int(m.group(4)))["state"] == "closed" else " ") + m.group(3), text)
        if new != text:
            out(("" if apply else "would ") + f"update checklist in #{n}")
            if apply:
                api.call("PATCH", f"{api.base}/issues/{n}", {"body": new})
        return [int(m.group(4)) for m in CHECK_LINE.finditer(text)]

    listed = sync(roadmap)
    work = set()
    for n in dict.fromkeys(listed):
        names = {l["name"] for l in issue(n).get("labels", [])}
        if ROLE_LABELS["epic"][0] in names:
            work.update(sync(n))
        else:
            work.add(n)
    frontier, closed_now = [], []
    for n in sorted(work):
        if issue(n)["state"] != "open":
            continue
        blockers = api.call("GET", f"{api.base}/issues/{n}/dependencies") or []
        ready = all(b["state"] == "closed" for b in blockers)
        merged = merged_closing_prs(api, n)
        if merged and ready:
            # Gitea skips the closing keyword while blockers are open; finish what the PR asked for.
            out(("" if apply else "would ") + f"close #{n}: PR {', '.join(merged)} merged while it was still blocked")
            if apply:
                api.call("PATCH", f"{api.base}/issues/{n}", {"state": "closed"})
                issue(n)["state"] = "closed"
                closed_now.append(n)
                continue
        elif merged:
            out(f"note: #{n} has merged PR {', '.join(merged)} but stays open until its blockers close")
        if ready:
            frontier.append(n)
    done = sum(1 for n in work if issue(n)["state"] == "closed")
    if closed_now:
        for n in [roadmap] + [m for m in dict.fromkeys(listed) if m not in work]:
            cache.pop(n, None)
            sync(n)  # tick issues closed above
    out(f"{done}/{len(work)} work issues closed")
    out("frontier (open, no open blockers): " + (", ".join(f"#{n} {issue(n)['title']}" for n in frontier) or "none"))
    return frontier


def merged_closing_prs(api, n):
    prs = []
    for event in api.pages(f"{api.base}/issues/{n}/timeline"):
        ref = event.get("ref_issue") or {}
        if event.get("type") == "pull_ref" and event.get("ref_action") == "closes" \
                and (ref.get("pull_request") or {}).get("merged"):
            prs.append(f"!{ref['number']}")
    return prs


# ---------------------------------------------------------------- CLI

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("plan")
    c.add_argument("--preview", action="store_true", help="print every issue body with placeholder numbers")
    for name in ("publish", "verify"):
        s = sub.add_parser(name)
        s.add_argument("plan")
        s.add_argument("--repo", required=True)
        s.add_argument("--login")
        if name == "publish":
            s.add_argument("--apply", action="store_true")
            s.add_argument("--update", action="store_true", help="also rewrite titles, bodies and labels of existing issues")
            s.add_argument("--no-pin", action="store_true")
    r = sub.add_parser("refresh")
    r.add_argument("--repo", required=True)
    r.add_argument("--login")
    r.add_argument("--roadmap", type=int, required=True)
    r.add_argument("--apply", action="store_true")
    a = p.parse_args(argv)
    try:
        if a.cmd == "check":
            plan = load_plan(a.plan)
            errors, warnings = validate(plan)
            for w in warnings:
                print("warning: " + w)
            if errors:
                print("error: " + "\nerror: ".join(errors))
                return 1
            sched = schedule(plan)
            print(summary(plan, sched))
            if a.preview:
                print("\n" + preview(plan, sched))
            return 0
        api = Gitea(a.repo, a.login)
        if a.cmd == "publish":
            numbers = publish(load_plan(a.plan), api, a.apply, a.update, not a.no_pin)
            if numbers:
                return 1 if verify(load_plan(a.plan), api) else 0
            return 0
        if a.cmd == "verify":
            return 1 if verify(load_plan(a.plan), api) else 0
        refresh(api, a.roadmap, a.apply)
        return 0
    except (PlanError, ApiError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
