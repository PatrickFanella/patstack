#!/usr/bin/env python3
"""Validate the curated collection, without loading every reference into an agent."""
import argparse, ast, hashlib, json, pathlib, re, sys
import yaml
ROOT=pathlib.Path(__file__).resolve().parents[1]
# Local discovery-context review limit; not a client or connected-app requirement.
PERSONAL_DESCRIPTION_BUDGET=12_000
def external_description_metrics(source_only=False):
    if source_only:
        return {'personalDescriptions': 0, 'personalBodies': 0,
                'unverifiedExternalOwners': ['omarchy', 'diagnose-crash']}
    result={'personalDescriptions': 0, 'personalBodies': 0, 'unverifiedExternalOwners': [], 'absentExternalOwners': []}
    for name in ['omarchy','diagnose-crash']:
        folder=pathlib.Path.home()/'.codex/skills'/name
        # OS owners are per host (Omarchy now runs only on Sputnik). No link means not installed;
        # a dangling link still fails below.
        if not folder.exists() and not folder.is_symlink():
            result['absentExternalOwners'].append(name);continue
        p=folder/'SKILL.md';_,front,body=p.read_text().split('---',2)
        result['personalDescriptions']+=len(yaml.safe_load(front)['description'])
        result['personalBodies']+=len(body)
    return result

def capability_path_errors(caps, source_only=False):
    errors=[];unverified=[]
    for capability in caps:
        if source_only and capability.get('kind') in {'external','system'}:
            unverified.append(capability['owner'])
        elif capability.get('kind') in {'external','system'} and not (ROOT/capability['path']).exists() and not (ROOT/capability['path']).is_symlink():
            continue  # OS owner not installed on this host
        elif not (ROOT/capability['path']).exists():
            errors.append(f'unreachable capability {capability}')
    return errors,sorted(set(unverified))

# Same names as retired local skills, but owned by external plugins or clients.
EXTERNAL_SKILL_NAMES={'frontend-design','imagegen','deslop','control-ui','control-cli','no-comments'}
LINK=re.compile(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)')
SKILL_REFERENCE=re.compile(r'(`|\*\*)([a-z0-9][a-z0-9-]*)\1\s+skill\b')

def prose(path):
    # Examples and code are illustrative, not resource links or skill references.
    text=re.sub(r'(?ms)^(```|~~~).*?^\1[^\n]*','',path.read_text())
    return re.sub(r'`[^`\n]*`(?!`)',lambda m:m.group(0) if re.fullmatch(r'`[a-z0-9-]+`',m.group(0)) else '',text)

def link_errors():
    errors=[]
    vault_rows=json.loads((ROOT/'catalog/vault-agents.json').read_text())['files']
    deployed={row['source']:pathlib.PurePosixPath(row['destination']) for row in vault_rows}
    destinations={row['destination'] for row in vault_rows}
    files=[ROOT/'README.md',ROOT/'AGENTS.md']+[p for folder in ['skills','shared','repository-skills','library/skills','project-agents','vault-agents','docs','profiles','instructions','authoring','runtime-bundles','brand'] for p in (ROOT/folder).rglob('*.md')]
    for p in files:
        relative=str(p.relative_to(ROOT))
        for link in LINK.findall(prose(p)):
            if re.match(r'^(?:[a-z][a-z0-9+.-]*:|#|<)',link):continue
            target=link.split('#')[0]
            if not target or (p.parent/target).exists():continue
            if relative in deployed and str(deployed[relative].parent/target).replace('/./','/') in destinations:continue
            errors.append(f'broken link {relative} -> {target}')
    return errors

def selectable_names():
    return {word for p in (ROOT/'profiles').glob('*.txt') for line in p.read_text().splitlines()
            if not line.lstrip().startswith('#') for word in line.split()}

def retired_reference_errors(retired):
    errors=[];selected=selectable_names()
    files=[p for folder in ['skills','shared','project-agents','vault-agents','instructions'] for p in (ROOT/folder).rglob('*.md')]
    files+=[p for name in sorted(selected) for p in (ROOT/'library/skills'/name).rglob('*.md')]
    for p in files:
        if p.name=='codemap.md':continue  # capability maps record the original names on purpose
        for number,line in enumerate(p.read_text().splitlines(),1):
            for _,name in SKILL_REFERENCE.findall(line):
                if name in retired and name not in EXTERNAL_SKILL_NAMES:
                    errors.append(f'retired skill name {p.relative_to(ROOT)}:{number}: {name} -> {retired[name].get("owner")}')
    return errors

def main(source_only=False,write_report=False):
    errors=[]; metrics={'authoredPersonal':0,'personalDescriptions':0,'personalBodies':0}; scripts=[]
    catalog=json.loads((ROOT/'catalog/proposed-catalog.json').read_text())
    actual={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}|{'omarchy','diagnose-crash'}
    expected={x['name'] for x in catalog if x['scope']=='personal'}
    if actual!=expected:errors.append(f'catalog mismatch {actual^expected}')
    shared={p.parent.name for p in (ROOT/'shared').glob('*/SKILL.md')}
    if shared!={x['name'] for x in catalog if x['scope']=='shared'}:errors.append(f'shared catalog mismatch {shared^{x["name"] for x in catalog if x["scope"]=="shared"}}')
    optional={x['name'] for x in catalog if x['scope']=='optional'}
    metrics['optionalCuratedEntrypoints']=len(optional)
    for folder in ['skills','shared','repository-skills','library/skills','project-agents']:
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
                if folder!='project-agents' and len(p.relative_to(ROOT/folder).parts)!=2:errors.append(f'nested discovery: {p}')
                if len(body)>(8000 if p.parent.name=='pet-hatchery' else 4000):errors.append(f'oversized: {p}')
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
        for p in [p for base in roots for p in base.rglob('*.py')]:
            try:tree=ast.parse(p.read_text());scripts.append({'path':str(p.relative_to(ROOT)),'mode':oct(p.stat().st_mode&0o777),'imports':sorted({n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)}|{n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module})})
            except SyntaxError as e:errors.append(f'python syntax {p}: {e}')
    external=external_description_metrics(source_only)
    for key in ['personalDescriptions','personalBodies']:metrics[key]+=external[key]
    metrics['sourceOnly']=source_only
    metrics['unverifiedExternalOwners']=external['unverifiedExternalOwners']
    metrics['absentExternalOwners']=external.get('absentExternalOwners',[])
    metrics['personalDescriptionScope']='repository sources' if source_only else 'sources and installed OS owners'
    metrics['personalEntrypoints']=len(actual)
    if len(actual)!=54:errors.append(f'personal entrypoint count {len(actual)} != 54')
    metrics['personalDescriptionBudget']=PERSONAL_DESCRIPTION_BUDGET
    metrics['personalDescriptionHeadroom']=PERSONAL_DESCRIPTION_BUDGET-metrics['personalDescriptions']
    if metrics['personalDescriptionHeadroom']<0:errors.append(f'description budget {metrics}')
    caps=json.loads((ROOT/'catalog/capabilities.json').read_text())
    if len(caps)!=167 or len({x['original'] for x in caps})!=167:errors.append('incomplete capability mapping')
    capability_errors,unverified=capability_path_errors(caps,source_only)
    errors.extend(capability_errors)
    metrics['unverifiedCapabilityOwners']=unverified
    retired=json.loads((ROOT/'catalog/retired-names.json').read_text())
    if actual&retired.keys():errors.append('retirement map includes active names')
    errors.extend(link_errors())
    errors.extend(retired_reference_errors(retired))
    metrics['retiredNames']=len(retired);metrics['mappedOriginals']=len(caps)
    if write_report:
        (ROOT/'reports').mkdir(exist_ok=True)
        (ROOT/'reports/structure.json').write_text(json.dumps({'metrics':metrics,'errors':errors,'scriptDependencies':scripts},indent=2)+'\n')
    print(json.dumps({'metrics':metrics,'errors':errors},indent=2));return bool(errors)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-only',action='store_true',help='Validate repository sources; report installed OS owners as unverified')
    parser.add_argument('--write-report',action='store_true',help='Refresh the tracked reports/structure.json evidence file')
    args=parser.parse_args()
    sys.exit(main(args.source_only,args.write_report))
