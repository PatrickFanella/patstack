import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/manage-roadmaps-and-issues'
spec = importlib.util.spec_from_file_location('roadmap', SKILL / 'scripts/roadmap.py')
roadmap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(roadmap)


class FakeGitHub:
    """Just enough of the GitHub REST and GraphQL API for roadmap.py, kept in memory."""

    def __init__(self):
        self.issues, self.labels, self.milestones = {}, {'bug'}, {}
        self.subs, self.blocked_by, self.pinned, self.calls = {}, {}, [], []
        self.project = None  # set to {} to give the repository a linked Project
        self.items = {}  # issue number -> {'id': item id, 'size': option name}

    def issue_json(self, n):
        i = self.issues[n]
        return dict(i, labels=[{'name': l} for l in i['labels']])

    def __call__(self, cmd, input=None, **_):
        assert cmd[:2] == ['gh', 'api'], cmd
        method, path = cmd[cmd.index('-X') + 1], cmd[-1] if '--input' not in cmd else cmd[cmd.index('--input') - 1]
        body = json.loads(input) if input else None
        self.calls.append((method, path))
        out = self.route(method, urlsplit(path).path, body)
        return subprocess.CompletedProcess(cmd, 0, json.dumps(out), '')

    def route(self, method, path, body):
        base = '/repos/subculture-collective/demo'
        if path == base:
            return {'has_issues': True}
        if path == '/orgs/subculture-collective/issue-types':
            return [{'name': 'Task'}, {'name': 'Bug'}, {'name': 'Feature'}]
        if path == f'{base}/labels':
            if method == 'POST':
                self.labels.add(body['name'])
                return {'name': body['name']}
            return [{'name': n} for n in sorted(self.labels)]
        if path == f'{base}/milestones':
            if method == 'POST':
                n = len(self.milestones) + 1
                self.milestones[body['title']] = n
                return {'number': n, 'title': body['title']}
            return [{'number': n, 'title': t} for t, n in self.milestones.items()]
        if path == f'{base}/issues':
            if method == 'POST':
                n = len(self.issues) + 1
                assert set(body['labels']) <= self.labels, body['labels']
                self.issues[n] = dict(body, number=n, id=1000 + n, node_id=f'I_{n}', state='open')
                return self.issue_json(n)
            return [self.issue_json(n) for n in sorted(self.issues)]
        m = re.fullmatch(base + r'/issues/(\d+)(/.*)?', path)
        if m:
            n, rest = int(m.group(1)), m.group(2) or ''
            by_id = {i['id']: k for k, i in self.issues.items()}
            if rest == '' and method == 'PATCH':
                self.issues[n].update(body)
            if rest == '':
                return self.issue_json(n)
            if rest == '/sub_issues':
                if method == 'POST':
                    child = by_id[body['sub_issue_id']]
                    if body.get('replace_parent'):
                        for c in self.subs.values():
                            if child in c:
                                c.remove(child)
                    assert all(child not in c for c in self.subs.values()), 'an issue has one parent'
                    self.subs.setdefault(n, []).append(child)
                return [self.issue_json(c) for c in self.subs.get(n, [])]
            if rest == '/dependencies/blocked_by':
                if method == 'POST':
                    self.blocked_by.setdefault(n, []).append(by_id[body['issue_id']])
                return [self.issue_json(b) for b in self.blocked_by.get(n, [])]
        if path == 'graphql':
            if 'pinIssue' in body['query']:
                self.pinned.append(body['variables']['i'])
                return {'data': {}}
            if 'projectsV2' in body['query']:
                nodes = [] if self.project is None else [{'id': 'P_1', 'title': 'demo', 'url': 'u', 'fields': {'nodes': [
                    {'id': 'F_size', 'name': 'Size', 'options': [{'id': 'O_' + n, 'name': n} for n in ('XS', 'S', 'M', 'L', 'XL')]}]}}]
                return {'data': {'repository': {'projectsV2': {'nodes': nodes}}}}
            if 'items(first' in body['query']:
                return {'data': {'node': {'items': {'pageInfo': {'hasNextPage': False, 'endCursor': None}, 'nodes': [
                    {'id': i['id'], 'content': {'number': n, 'repository': {'name': 'demo'}},
                     'size': {'name': i['size']} if i['size'] else None} for n, i in self.items.items()]}}}}
            if 'addProjectV2ItemById' in body['query']:
                n = int(body['variables']['c'][2:])
                assert n not in self.items, 'Content already exists in this project'
                self.items[n] = {'id': f'PI_{n}', 'size': None}
                return {'data': {'addProjectV2ItemById': {'item': {'id': f'PI_{n}'}}}}
            if 'updateProjectV2ItemFieldValue' in body['query']:
                v = body['variables']
                n = next(k for k, i in self.items.items() if i['id'] == v['i'])
                self.items[n]['size'] = v['o'][2:]
                return {'data': {}}
        raise AssertionError(f'unexpected {method} {path}')


class RoadmapGitHubTests(unittest.TestCase):
    def setUp(self):
        self.plan = roadmap.load_plan(SKILL / 'assets/plan.example.json')
        self.gh = FakeGitHub()
        self.api = roadmap.tracker('subculture-collective/demo', runner=self.gh)
        self.log = []

    def test_organization_repositories_default_to_github(self):
        self.assertIsInstance(self.api, roadmap.GitHub)
        self.assertIsInstance(roadmap.tracker('PatrickFanella/demo'), roadmap.Gitea)
        self.assertIsInstance(roadmap.tracker('subculture-collective/demo', host='gitea'), roadmap.Gitea)

    def test_publish_builds_sub_issues_blockers_and_types(self):
        numbers = roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        self.assertEqual(roadmap.verify(self.plan, self.api, out=self.log.append), 0, self.log)
        book = roadmap.Book(self.plan, roadmap.schedule(self.plan), numbers)
        for ident, children in roadmap.expected_edges(self.plan, book).items():
            n = numbers[ident]
            if roadmap.is_tracking(ident):
                self.assertEqual(sorted(self.gh.subs.get(n, [])), sorted(numbers[c] for c in children))
                self.assertNotIn(n, self.gh.blocked_by, 'tracking issues use sub-issues, not blockers')
            else:
                self.assertEqual(sorted(self.gh.blocked_by.get(n, [])), sorted(numbers[c] for c in children))
        self.assertEqual(self.gh.issues[numbers['roadmap']]['type'], 'Feature')
        self.assertTrue(all(self.gh.issues[numbers[i]]['type'] == 'Task' for i in numbers if i.startswith('issue:')))
        self.assertEqual(self.gh.pinned, [f"I_{numbers['roadmap']}"])
        self.assertIn('note: the repository has no linked Project; issues were not added to one', self.log)

    def test_rerun_creates_nothing(self):
        roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        before = len(self.gh.issues), sum(map(len, self.gh.subs.values())), sum(map(len, self.gh.blocked_by.values()))
        roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        after = len(self.gh.issues), sum(map(len, self.gh.subs.values())), sum(map(len, self.gh.blocked_by.values()))
        self.assertEqual(before, after)

    def test_moving_an_issue_to_another_epic_reparents_it(self):
        numbers = roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        moved = next(i for i in self.plan['issues'] if i.get('epic'))
        other = next(e['key'] for e in self.plan['epics'] if e['key'] != moved['epic'])
        moved['epic'] = other
        roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        n = numbers['issue:' + moved['key']]
        self.assertIn(n, self.gh.subs[numbers['epic:' + other]])
        self.assertEqual(sum(n in c for c in self.gh.subs.values()), 1)
        self.assertEqual(roadmap.verify(self.plan, self.api, out=self.log.append), 0, self.log)

    def test_project_items_get_their_size_and_reruns_repair_it(self):
        self.gh.project = {}
        numbers = roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        self.assertEqual(set(self.gh.items), set(numbers.values()))
        sized = {i['key']: i.get('size', 'M') for i in self.plan['issues']}
        for key, size in sized.items():
            self.assertEqual(self.gh.items[numbers['issue:' + key]]['size'], size)
        key = next(iter(sized))
        self.gh.items[numbers['issue:' + key]]['size'] = None  # an earlier run failed before setting it
        roadmap.publish(self.plan, self.api, apply=True, out=self.log.append)
        self.assertEqual(self.gh.items[numbers['issue:' + key]]['size'], sized[key])

    def test_dry_run_writes_nothing(self):
        roadmap.publish(self.plan, self.api, apply=False, out=self.log.append)
        self.assertFalse([c for c in self.gh.calls if c[0] != 'GET' and 'pinIssue' not in c[1]
                          and c[1] != 'graphql'])
        self.assertEqual(self.gh.issues, {})


if __name__ == '__main__':
    unittest.main()
