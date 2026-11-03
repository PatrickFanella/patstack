#!/usr/bin/env python3
"""One-time import from the immutable pre-consolidation snapshot. Never reads installed copies."""
import json
import re
import shutil
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=Path(json.loads((ROOT/'catalog/installation.json').read_text())['archive'])
CATALOG=json.loads((ROOT/'catalog/proposed-catalog.json').read_text())
RECS=json.loads((ROOT/'catalog/recommendations.json').read_text())
TARGETS={r['name']:r['target'] for r in RECS}
PRINCIPLES={
 'boundary-drafter':'boundary-discipline exhaust-the-design-space experience-first foundational-thinking model-the-domain redesign-from-first-principles separate-before-serializing-shared-state',
 'safe-refactor-pass':'laziness-protocol migrate-callers-then-delete-legacy-apis minimize-reader-load subtract-before-you-add',
 'sweep-rewriter':'build-the-lever encode-lessons-in-structure',
 'build-sequencer':'guard-the-context-window never-block-on-the-human outcome-oriented-execution sequence-verifiable-units',
 'bug-tracer':'fix-root-causes', 'behavior-proof':'prove-it-works make-operations-idempotent',
 'ts-type-design':'type-system-discipline',
}
CONTRACTS={
 'ts-type-design':'Respect the existing module system and compiler configuration. Model external values at boundaries; justify assertions rather than treating every cast as a defect. Module-boundary enforcement and shoehorn migrations run only when explicitly requested.',
 'python-uv-workbench':'Identify whether the task concerns application code, a utility, packaging, configuration, environment management, or tests. Preserve the project package manager and import layout; use its declared Python version.',
 'boundary-drafter':'Choose a structure from the actual callers and invariants. Domain vocabulary, module design, and CQRS are separate modes: load only the mode needed. Produce design artifacts when design is requested; implement only within the requested scope.',
 'api-contract-smith':'Start with the public contract and the existing framework. Keep transport validation, authentication, business rules, and persistence responsibilities explicit. Load WebSocket guidance only for long-lived connections.',
 'cli-contract-smith':'Design flags, stdout/stderr, exit codes, and noninteractive input as a contract. Preserve human interaction when requested; make it an optional fallback for automatable operations.',
 'bash-script-craft':'Preserve argument boundaries, exit statuses, and cleanup ownership. Choose implementation, linting, or tests; an ordinary script edit does not require all three reference sets.',
 'git-surgery':'Resolve the repository, requested comparison, and configured remote first. Preserve unrelated work. Read-only Git inspection, requested history edits, PR preparation, and publishing have separate authorization boundaries.',
 'ci-medic':'Locate the failed job or requested pipeline change. Distinguish local command results from hosted checks. Reuse the existing CI provider and hooks rather than adding a second system; publishing changes requires authorization.',
 'kube-artifact-smith':'Select raw manifests, chart templates, or workload policy. Validate the rendered artifact and intended namespace before any authorized cluster operation. Generating configuration does not authorize applying it.',
 'telemetry-signal-forge':'Start with the operational question and signal. Choose metrics, tracing, dashboards, or SLO design; keep signal names, labels, units, and time windows consistent across the selected artifacts.',
 'pg-plan-reader':'Use the real schema and query plan to establish the problem. Separate read-only diagnostics from index, schema, data, replication, and production changes. Data-quality conclusions need explicit keys and population boundaries.',
 'retrieval-pipeline':'Treat ingestion, retrieval, ranking, and grounded answers as separately measurable stages. Preserve source provenance and access boundaries; evaluate retrieval results before attributing answer defects to the model.',
 'safe-refactor-pass':'Preserve observable behavior and existing repository conventions. Select cleanup or a refactor plan; planning does not authorize implementation or filing an issue. Use codemod-surgeon for repeated structural transformations.',
 'bug-tracer':'Establish a failing observation before selecting a cause. Change one causal variable at a time; verify the same reproducer after repair. Use recurring-failure analysis only for repeated incidents, not every trivial failure.',
 'diff-inspector':'Default to read-only, defect-first review of the requested change. Pin the comparison and trace findings through actual callers. Maintainability and strict thermo-nuclear modes require a specific request. Multiple reviewers are optional when scope warrants them; never assume named agent types.',
 'tech-doc-writer':'Select writing, localization, or consistency review. Preserve the requested audience, source meaning, identifiers, and stopping point. Documentation review does not authorize rewriting code or publishing comments.',
 'binary-dissector':'Identify the artifact and authorized analysis scope. Select binary inspection or protocol observation; report inferred structure separately from demonstrated behavior.',
 'blacktower-development':'Apply only inside Blacktower. Select control UI, plugin composition, release artifacts, or session lifecycle. OpenCode references here describe the software under development, not tools that Codex must have.',
}

def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n')
def read_skill(p):
 t=p.read_text();a=t.split('---',2);return yaml.safe_load(a[1]),a[2].strip()
def clean(body):
 # Remove the measured boilerplate, not operational constraints unique to a workflow.
 body=re.sub(r'## Workflow\n\n1\. Confirm the request matches.*?(?=\n## |\Z)','',body,flags=re.S)
 body=re.sub(r'## Constraints\n\n- Prefer the project.s existing stack.*?(?=\n## |\Z)','',body,flags=re.S)
 body=re.sub(r'\n## Merged Skills\s*(?=\n## Merged Skills)','',body)
 body=body.replace('Stop and ask when required credentials, CLIs, project context, or user confirmation are missing.','Resolve repository facts and available tooling first. Ask only for missing information or authorization required for the requested action; continue independent authorized work.')
 return body.strip()
def copy_resources(src,dst):
 shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
 (dst/'SKILL.md').unlink()
 # Resource modes are references, not hidden nested skill entrypoints.
 for nested in dst.rglob('SKILL.md'):nested.rename(nested.with_name('guide.md'))
 if (dst/'agents').exists():shutil.rmtree(dst/'agents')
def sections(body):
 chunks=[];head='Overview';lines=[];fence=False
 for l in body.splitlines():
  if l.startswith(('```','~~~')):fence=not fence
  if l.startswith('## ') and not fence:
   if lines:chunks.append((head,'\n'.join(lines)))
   head=l[3:];lines=[l]
  else:lines.append(l)
 if lines:chunks.append((head,'\n'.join(lines)))
 return chunks
def guide(dst,body):
 body=clean(body)
 if len(body)<=4000:write(dst/'guide.md',body);return
 links=[]
 for i,(heading,part) in enumerate(sections(body)):
  name=f'part-{i+1:02}.md';write(dst/name,part);links.append(f'- [{heading}]({name}) — read when this part of the workflow is needed.')
 write(dst/'guide.md','# Focused procedures\n\nSelect the procedure relevant to the requested operation. Paths and scripts in these procedures are relative to this directory; pass the target repository explicitly.\n\n'+'\n'.join(links))
def front(name,description,body,meta=None):
 fm={'name':name,'description':description}
 if meta:
  for k in ['license','compatibility','metadata']:
   if k in meta:fm[k]=meta[k]
 return '---\n'+yaml.safe_dump(fm,sort_keys=False,allow_unicode=True,width=1000)+'---\n\n'+body.rstrip()+'\n'

capabilities=[]
for row in CATALOG:
 name=row['name']
 if name in {'omarchy','diagnose-crash'}:
  capabilities.append({'original':name,'owner':name,'kind':'external','path':str(Path('/home/onnwee/.codex/skills')/name)});continue
 destination=ROOT/('repository-skills' if name=='blacktower-development' else 'skills')/name
 sources=row['sources'];meta={}
 if name in {'build-sequencer','behavior-proof'}:
  draft=ROOT/'catalog/import-inputs'/(name+'.md')
  meta,body=read_skill(draft);destination.mkdir()
 elif len(sources)==1:
  src=ARCHIVE/'personal'/sources[0];meta,body=read_skill(src/'SKILL.md');copy_resources(src,destination)
  if len(body)>4000 and name!='pet-hatchery':
   # Keep original resources in place so all existing relative references continue to work.
   guide(destination,body)
   body=f'# {name}\n\n{row["description"]}\n\nSelect the relevant procedure from [the task guide](guide.md). Load only that procedure, not the complete reference collection.\n\nKeep the requested scope and repository conventions. Report evidence for the operation actually performed.'
  else:body=clean(body)
 else:
  destination.mkdir();body=f'# {name}\n\n'+CONTRACTS.get(name,'Select the mode matching the requested task.')+'\n\n## Select a mode\n\n'
 if len(sources)>1 or name=='behavior-proof':
  for original in sources:
   src=ARCHIVE/'personal'/original;oldmeta,oldbody=read_skill(src/'SKILL.md')
   mode=destination/'references/modes'/original;copy_resources(src,mode);guide(mode,oldbody)
   label=oldmeta['description'].split('. ')[0].rstrip('.')[:190]
   condition='Only when explicitly requested: ' if original in {'thermo-nuclear-code-quality-review','thermo-nuclear-review','setup-ts-deep-modules'} else ''
   body+=f'- {condition}{label}. Read [the procedure](references/modes/{original}/guide.md).\n'
   capabilities.append({'original':original,'owner':name,'kind':'mode','path':str((mode/'guide.md').relative_to(ROOT))})
  body+='\nResource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.\n'
 elif sources:capabilities.append({'original':sources[0],'owner':name,'kind':'retained','path':str((destination/'SKILL.md').relative_to(ROOT))})
 write(destination/'SKILL.md',front(name,row['description'],body,meta))
 # Preserve genuine existing UI metadata only for retained entrypoints.
 if len(sources)==1 and (ARCHIVE/'personal'/sources[0]/'agents/openai.yaml').exists():
  p=destination/'agents/openai.yaml';p.parent.mkdir(exist_ok=True);shutil.copy2(ARCHIVE/'personal'/sources[0]/'agents/openai.yaml',p)

# Rich shared owners: union all resources, preferring the richer Codex content.
for name in ['scope-grill','relay-baton']:
 dst=ROOT/'shared'/name;shutil.copytree(ARCHIVE/'shared'/name,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 shutil.copytree(ARCHIVE/'personal'/name,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 capabilities.append({'original':name,'owner':name,'kind':'shared','path':f'shared/{name}/SKILL.md'})
capabilities.append({'original':'diff-auditor','owner':'system review-agent','kind':'system','path':'/home/onnwee/.codex/skills/.system/review-agent/SKILL.md'})

for owner,slugs in PRINCIPLES.items():
 dst=ROOT/'skills'/owner;entry=dst/'SKILL.md';links=[]
 for slug in slugs.split():
  original='principle-'+slug;meta,body=read_skill(ARCHIVE/'personal'/original/'SKILL.md')
  p=dst/'references/principles'/f'{slug}.md';write(p,body)
  links.append(f'- [{slug.replace("-"," ")}](references/principles/{slug}.md) — consult only for this specific design or execution concern.')
  capabilities.append({'original':original,'owner':owner,'kind':'principle-reference','path':str(p.relative_to(ROOT))})
 write(entry,entry.read_text()+'\n## Conditional design notes\n\n'+'\n'.join(links))
src=ARCHIVE/'personal/writing-for-agents';copy_resources(src,ROOT/'authoring/writing-for-agents');meta,body=read_skill(src/'SKILL.md');guide(ROOT/'authoring/writing-for-agents',body)
capabilities.append({'original':'writing-for-agents','owner':'authoring reference','kind':'reference','path':'authoring/writing-for-agents/guide.md'})
write(ROOT/'authoring/writing-for-agents/SKILL-MECHANICS.md','# Codex skill mechanics\n\nNames, descriptions, and paths support discovery; bodies and resources load when needed. Use concise automatic entrypoints for distinct jobs and conditional references for related procedures. Explicit-only invocation uses `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; preserve the user’s chosen invocation behavior. A reference file can be read directly without invoking another skill. Do not use legacy `disable-model-invocation` as a Codex policy.\n')

# Rewrite retired skill mentions with the actual procedure, retaining labels as provenance.
index={r['original']:r for r in capabilities}
for f in [*ROOT.joinpath('skills').rglob('*.md'),*ROOT.joinpath('shared').rglob('*.md'),*ROOT.joinpath('repository-skills').rglob('*.md'),*ROOT.joinpath('authoring').rglob('*.md')]:
 text=f.read_text()
 for old,r in sorted(index.items(),key=lambda x:len(x[0]),reverse=True):
  if r['kind'] in {'retained','external','shared','system'}:continue
  # Convert explicit invocations into current owner/mode instructions, not dead commands.
  text=re.sub(r'(?<![\w/.-])\$'+re.escape(old)+r'\b',r['owner']+' ('+old+' procedure)',text)
 text=text.replace('~/.config/opencode/skills/','/home/onnwee/.codex/skills/')
 text=text.replace('`subagent_type=Explore`','an available exploration agent').replace('Agent tool with subagent_type=Explore','available exploration tooling')
 write(f,text)
assert len(index)==138,(len(index),set(r['name'] for r in RECS)-index.keys())
write(ROOT/'catalog/capabilities.json',json.dumps(capabilities,indent=2))
write(ROOT/'catalog/retired-names.json',json.dumps({r['original']:{'owner':r['owner'],'procedure':r['path']} for r in capabilities if r['kind'] not in {'retained','external'}},indent=2))
print('Created',len(list((ROOT/'skills').glob('*/SKILL.md'))),'authored personal skills plus 2 external skills;',len(capabilities),'original capabilities mapped.')
