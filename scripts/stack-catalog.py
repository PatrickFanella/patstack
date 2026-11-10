#!/usr/bin/env python3
"""Render the task-stack reference from profiles and canonical skill metadata."""
import argparse
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime-bundles/subsets-fleet/scripts'))
sys.path.insert(0, str(ROOT / 'scripts'))
from stack_selection import available, selection


def render(root=ROOT):
    config = json.loads((root / 'catalog/skill-stacks.json').read_text())
    sources = available(root)
    core = set(selection(root, [])[0])
    groups = {}
    for path in sorted((root / 'profiles').glob('*.txt')):
        names = {s.strip() for s in path.read_text().splitlines()
                 if s.strip() and not s.startswith('#')}
        groups[path.stem] = names
    order = ['core', *sorted(set(groups) - {'core'})]
    table = ['| Stack | Added beyond core | Total selected | Use it for |', '|---|---|---|---|']
    for name in order:
        names = groups[name]
        table.append(f"| [`{name}`](../profiles/CATALOG.md#{name}) | {0 if name == 'core' else len(names - core)} | {len(names | core)} | {config['stackDescriptions'][name]} |")
    guide = [
        '# Skills and task stacks', '',
        'Subsets manages the user-level skill selection across clients. Patstack owns',
        'the authored sources, profiles, qualification and relationship catalog.',
        'There is one selected stack, with generated views into one reviewed library;',
        'there is no separate always-installed personal layer.', '',
        '## Contents', '',
        '- [Everyday core](#everyday-core)', '- [Task sets](#task-sets)',
        '- [Client views and exceptions](#client-views-and-exceptions)',
        '- [Required and optional companions](#required-and-optional-companions)',
        '- [Selection and recovery](#selection-and-recovery)', '',
        '## Everyday core', '',
        f'`core` selects **{len(core)} skills** for frequent repository, web/API,',
        'documentation and operations work. It includes planning, debugging, review,',
        'Git/CI delivery, UI quality, common languages, data changes, research,',
        'verification and continuation. Related workflows load conditional procedures',
        'from their canonical owner; removed skills have no discovery entrypoints.', '',
        'Core is a working toolkit, not a request to load every skill body. Agents',
        'read the relevant procedure and its needed references. There is no need',
        'to choose a specialist set for an occasional task: the router can resolve',
        'inactive sources from the same library.', '',
        '## Task sets', '',
        f'The **{len(groups) - 1} task sets** combine disciplines around an outcome. Core is always',
        'included. Sets overlap deliberately; they are not exclusive professional',
        'categories. Several can be combined. All **' + str(len(sources)) + ' selectable owners**',
        'belong to at least one set, including core.', '', *table, '',
        'The [membership reference](../profiles/CATALOG.md) lists the core and every',
        'set\'s additions with source links and descriptions. The additions exclude',
        'core duplicates; total selected counts the union.', '',
        '## Client views and exceptions', '',
        '| Client view | Path |', '|---|---|',
    ]
    for client, row in config['clients'].items():
        guide.append(f"| {client} | `~/{row['root']}` |")
    guide += [
        '', 'Subsets creates individual links to the selected immutable bundle sources.',
        'It does not replace whole client directories. Native views follow the',
        'declared source contracts; Cursor and Copilot use Claude-compatible Agent',
        'Skills files. Shared compatibility roots may also be visible to a client.',
        'Installed files do not prove that tools, authentication or invocation',
        'semantics are identical in every application.', '',
        'Package/system/plugin skills, app-specific skills and repository/vault',
        'skills retain their owners and locations. Unknown entries are preserved.',
        'A same-name collision requires review instead of overwriting another owner.',
        'The initial takeover requires exact matches to predecessor installer',
        'receipts; changed files stop migration before skill paths change. Released',
        'ownership manifests and original files are backed up in the transaction.', '',
        'Client location references: [Cursor skills](https://cursor.com/help/customization/skills)',
        'and [Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).', '',
        '## Required and optional companions', '',
        'The [relationship catalog](../catalog/skill-routes.json) connects default',
        'and specialist skills, including specialist-to-specialist links. Each link',
        'states its condition. Required steps apply only when that condition holds;',
        'optional helpers are read only when useful. A link does not authorize',
        'edits after an audit, publication after drafting, or agent delegation.', '',
        'For example, UI implementation requires behavior proof before claiming',
        'success; Python Temporal work can require replay tests; fiction drafting',
        'can consult dialogue or world-continuity specialists. Already loaded',
        'procedures are reused rather than recursively loading the relationship graph.', '',
        '## Selection and recovery', '',
        'Preview and apply a task set:', '',
        '```sh', 'rtk proxy subsets apply --build-and-ship --dry-run',
        'rtk proxy subsets apply --build-and-ship', 'rtk proxy subsets apply --group core',
        '```', '',
        'Start a fresh agent session after changing discovery. To undo a switch,',
        'use the recorded run directory with `~/.agents/bin/skill-profile rollback --run`.',
        'Undo later runs first. Rollback refuses subsequent edits and retains the',
        'canonical sources. Receipts are under `~/.local/state/subsets-fleet/profiles`.', '',
        'Edit source skills and profiles in patstack, validate and commit, then build',
        'and deploy a new bundle. The legacy personal/profile/link installers must',
        'not reclaim these paths after migration. Project and vault deployers remain',
        'separate. See [the adapter runbook](../runtime-bundles/subsets-fleet/README.md).', '',
    ]
    catalog = ['# Task-stack membership', '',
               'Generated by `python scripts/stack-catalog.py` from the canonical profiles.',
               'See [the guide](../docs/SKILL-GROUPS.md) for selection, ownership and recovery.', '',
               '## Contents', ''] + [f'- [{name}](#{name})' for name in order]
    for name in order:
        names = groups[name] if name == 'core' else groups[name] - core
        catalog += ['', '## ' + name, '', config['stackDescriptions'][name], '',
                    f"{len(names)} {'core members' if name == 'core' else 'additions'}; {len(groups[name] | core)} selected in total.", '',
                    '| Skill | Purpose |', '|---|---|']
        for member in sorted(names):
            source = sources[member]
            meta = yaml.safe_load((source / 'SKILL.md').read_text().split('---', 2)[1])
            description = ' '.join(meta['description'].split()).replace('|', '\\|')
            relative = source.relative_to(root).as_posix()
            catalog.append(f'| [`{member}`](../{relative}/SKILL.md) | {description} |')
    routes = ['# Task stacks', '',
              'Use the current default owner first. For a specialist, choose the relevant',
              'task set below and ask the read-only lookup for its members. Read one',
              'needed procedure at a time; selecting a set is not required for lookup.', '',
              '| Stack | Task |', '|---|---|']
    routes += [f"| `{name}` | {config['stackDescriptions'][name]} |" for name in order]
    return {'docs/SKILL-GROUPS.md': '\n'.join(guide),
            'profiles/CATALOG.md': '\n'.join(catalog) + '\n',
            'shared/find-and-load-skills/references/groups.md': '\n'.join(routes) + '\n'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for relative, text in render().items():
        path = ROOT / relative
        if args.check:
            if path.read_text() != text:
                raise SystemExit('Stale task guide: ' + relative)
        else:
            path.write_text(text)
    print('Task-stack catalog checked' if args.check else 'Task-stack catalog written')
