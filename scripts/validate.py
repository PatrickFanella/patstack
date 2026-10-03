#!/usr/bin/env python3
"""Validate the curated collection, without loading every reference into an agent."""
import ast, hashlib, json, pathlib, re, sys
import yaml
ROOT=pathlib.Path(__file__).resolve().parents[1]
# Local discovery-context review limit; not a client or connected-app requirement.
PERSONAL_DESCRIPTION_BUDGET=12_000
def main():
    errors=[]; metrics={'authoredPersonal':0,'personalDescriptions':0,'personalBodies':0}; scripts=[]
    catalog=json.loads((ROOT/'catalog/proposed-catalog.json').read_text())
    actual={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}|{'omarchy','diagnose-crash'}
    expected={x['name'] for x in catalog if x['scope']=='personal'}
    if actual!=expected:errors.append(f'catalog mismatch {actual^expected}')
    optional={x['name'] for x in catalog if x['scope']=='optional'}
    metrics['optionalCuratedEntrypoints']=len(optional)
    for folder in ['skills','shared','repository-skills','library/skills']:
        source_root=ROOT/folder
        roots=[source_root/name for name in sorted(optional)] if folder=='library/skills' else [source_root]
        entrypoints=[p for base in roots for p in base.rglob('SKILL.md')]
        if folder=='library/skills':
            for name in optional:
                if not (source_root/name/'SKILL.md').is_file():errors.append(f'missing optional source: {name}')
        for p in entrypoints:
            try:
                _,front,body=p.read_text().split('---',2); meta=yaml.safe_load(front)
                if meta['name']!=p.parent.name:errors.append(f'name: {p}')
                if not isinstance(meta['description'],str) or not meta['description'].strip():errors.append(f'description: {p}')
                if len(p.relative_to(ROOT/folder).parts)!=2:errors.append(f'nested discovery: {p}')
                if len(body)>(8000 if p.parent.name=='hatch-pet' else 4000):errors.append(f'oversized: {p}')
                if set(meta)-{'name','description','metadata','license','compatibility','allowed-tools'}:errors.append(f'unsupported frontmatter: {p}: {set(meta)}')
                if folder=='skills':
                    metrics['authoredPersonal']+=1;metrics['personalDescriptions']+=len(meta['description']);metrics['personalBodies']+=len(body)
            except Exception as e:errors.append(f'{p}: {e}')
        for p in [p for base in roots for p in base.rglob('agents/openai.yaml')]:
            try:
                meta=yaml.safe_load(p.read_text())
                if not isinstance(meta,dict) or set(meta)-{'interface','dependencies','policy'}:errors.append(f'unsupported UI metadata: {p}')
                if 'interface' in meta and not isinstance(meta['interface'],dict):errors.append(f'UI interface: {p}')
                policy=meta.get('policy',{})
                if 'allow_implicit_invocation' in policy and not isinstance(policy['allow_implicit_invocation'],bool):errors.append(f'invocation policy: {p}')
            except Exception as e:errors.append(f'UI metadata {p}: {e}')
        for p in [p for base in roots for p in base.rglob('*.md')]:
            # Examples and code fences are illustrative, not resource links.
            text=re.sub(r'(?ms)^(```|~~~).*?^\1[^\n]*','',p.read_text())
            for link in re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)',text):
                if re.match(r'^(?:https?:|mailto:|#|data:)',link):continue
                target=link.split('#')[0]
                if target and not (p.parent/target).exists():errors.append(f'broken link {p.relative_to(ROOT)} -> {target}')
        for p in [p for base in roots for p in base.rglob('*.py')]:
            try:tree=ast.parse(p.read_text());scripts.append({'path':str(p.relative_to(ROOT)),'mode':oct(p.stat().st_mode&0o777),'imports':sorted({n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)}|{n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module})})
            except SyntaxError as e:errors.append(f'python syntax {p}: {e}')
    for name in ['omarchy','diagnose-crash']:
        p=pathlib.Path.home()/'.codex/skills'/name/'SKILL.md';_,front,body=p.read_text().split('---',2)
        metrics['personalDescriptions']+=len(yaml.safe_load(front)['description']);metrics['personalBodies']+=len(body)
    metrics['personalEntrypoints']=len(actual)
    if len(actual)!=61:errors.append(f'personal entrypoint count {len(actual)} != 61')
    metrics['personalDescriptionBudget']=PERSONAL_DESCRIPTION_BUDGET
    metrics['personalDescriptionHeadroom']=PERSONAL_DESCRIPTION_BUDGET-metrics['personalDescriptions']
    if metrics['personalDescriptionHeadroom']<0:errors.append(f'description budget {metrics}')
    caps=json.loads((ROOT/'catalog/capabilities.json').read_text())
    if len(caps)!=148 or len({x['original'] for x in caps})!=148:errors.append('incomplete capability mapping')
    for c in caps:
        if not (ROOT/c['path']).exists():errors.append(f'unreachable capability {c}')
    retired=json.loads((ROOT/'catalog/retired-names.json').read_text())
    if actual&retired.keys():errors.append('retirement map includes active names')
    metrics['retiredNames']=len(retired);metrics['mappedOriginals']=len(caps)
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/structure.json').write_text(json.dumps({'metrics':metrics,'errors':errors,'scriptDependencies':scripts},indent=2)+'\n')
    print(json.dumps({'metrics':metrics,'errors':errors},indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
