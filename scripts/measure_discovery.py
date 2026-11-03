#!/usr/bin/env python3
"""Measure emitted discovery metadata; never estimate model tokens from characters."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 target={r['name'] for r in json.loads((ROOT/'catalog/proposed-catalog.json').read_text()) if r['scope']=='personal'}
 retired=set(json.loads((ROOT/'catalog/retired-names.json').read_text()))
 original={r['original'] for r in json.loads((ROOT/'catalog/capabilities.json').read_text())}
 report={'measurement':'fresh local Codex app-server skills/list forceReload; literal emitted name and description characters','tokens':None,'tokenLimitation':'Neither skills/list nor independent evaluation tooling exposed model input or billing token counts. No character-to-token estimates are used.','contexts':{}}
 for phase in ['before','after']:
  data=json.loads((ROOT/f'reports/discovery-{phase}.json').read_text())
  report.setdefault('runtime',{})[phase]=data['server']
  for row in data['skills']['data']:
   assert not row['errors'],row['errors']
   skills=row['skills'];personal=[s for s in skills if s['name'] in (original if phase=='before' else target) and ('/.codex/skills/' in s['path'] and '/.system/' not in s['path'] or s['path'].startswith('/usr/share/omarchy/'))]
   names=[s['name'] for s in skills]
   if phase=='after':
    assert {s['name'] for s in personal}==target
    assert not set(names)&retired
    assert names.count('scope-grill')==names.count('relay-baton')==1
    assert ('blacktower-development' in names)==(pathlib.Path(row['cwd']).name=='blacktower')
    assert all(s['enabled'] for s in personal)
   report['contexts'].setdefault(row['cwd'],{})[phase]={'entrypoints':len(skills),'personalEntrypoints':len(personal),'descriptionCharacters':sum(len(s['description']) for s in skills),'nameAndDescriptionCharacters':sum(len(s['name'])+len(s['description']) for s in skills),'personalDescriptionCharacters':sum(len(s['description']) for s in personal),'personalNameAndDescriptionCharacters':sum(len(s['name'])+len(s['description']) for s in personal),'names':[s['name'] for s in skills]}
 (ROOT/'reports/context-measurements.json').write_text(json.dumps(report,indent=2)+'\n')
 for cwd,phase in report['contexts'].items():
  print(cwd)
  for label,values in phase.items():print(label,{k:v for k,v in values.items() if k!='names'})
if __name__=='__main__':main()
