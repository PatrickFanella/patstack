#!/usr/bin/env python3
"""Transactional personal-skill installer: plan, apply, verify, rollback."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import uuid

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_STATE=Path('/home/onnwee/.codex/skill-installations/codex-skills')

def snapshot(p):
 p=Path(p)
 if p.is_symlink():return {'type':'symlink','target':os.readlink(p),'mode':stat.S_IMODE(p.lstat().st_mode)}
 if p.is_file():return {'type':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
 if p.is_dir():return {'type':'directory','mode':stat.S_IMODE(p.stat().st_mode),'entries':{f.name:snapshot(f) for f in sorted(p.iterdir())}}
 return None

def read(p,default=None):return json.loads(Path(p).read_text()) if Path(p).exists() else default
def save(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',dir=p.parent,delete=False) as f:
  json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno());tmp=f.name
 os.replace(tmp,p)
 fd=os.open(p.parent,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)

def copy(src,dst):
 src=Path(src);dst=Path(dst)
 if src.is_symlink():dst.symlink_to(os.readlink(src))
 elif src.is_dir():shutil.copytree(src,dst,symlinks=True)
 else:shutil.copy2(src,dst)

def remove(p):
 p=Path(p)
 if p.is_symlink() or p.is_file():p.unlink()
 elif p.is_dir():shutil.rmtree(p)

def statefile(state):return Path(state)/'installed.json'

def prepare(root=ROOT,state=DEFAULT_STATE,only_skills=None,only_shared=None):
 root=Path(root);config=read(root/'catalog/installation.json');baseline=read(root/'catalog/baseline.json');installed=read(statefile(state),{'paths':{}})
 marker=Path.home()/'.local/state/subsets-fleet/profiles/ownership.json'
 if marker.exists() and config['personalRoot'] in read(marker).get('roots',{}).values():raise RuntimeError('Subsets owns user skill selection; use subsets apply instead of the legacy personal installer')
 destinations={};groups={}
 for p in (root/'skills').iterdir():
  if (p/'SKILL.md').exists():
   d=str(Path(config['personalRoot'])/p.name);destinations[d]=str(p)
   groups[d]=1 if p.name=='style-web-ui' else (3 if p.name in {'pet-hatchery','upgrade-major-versions','build-opentui-apps','tech-doc-writer'} else 2)
 for p in (root/'shared').iterdir():destinations[str(Path(config['sharedRoot'])/p.name)]=str(p);groups[str(Path(config['sharedRoot'])/p.name)]=1
 target=str(Path(config['blacktowerRoot'])/'.agents/skills/blacktower-development')
 destinations[target]=str(root/'repository-skills/blacktower-development');groups[target]=3
 catalog=read(root/'catalog/proposed-catalog.json');keep={r['name'] for r in catalog if r['scope']=='personal'}
 personal=Path(config['personalRoot'])
 retired_names=set(read(root/'catalog/retired-names.json',{}))
 shared_root=Path(config['sharedRoot']);shared_names={p.name for p in (root/'shared').iterdir()}
 for p in installed['paths'].keys():
  q=Path(p)
  # A shared skill this installer placed and later renamed or retired.
  if q.parent==shared_root and q.name in retired_names and q.name not in shared_names and p not in destinations:
   destinations[p]=None;groups[p]=1
 for p in baseline.keys() | installed['paths'].keys():
  q=Path(p)
  if q.parent==personal and q.name not in keep and q.name!='.system':destinations[p]=None;groups[p]=3 if q.name.startswith('principle-') or q.name=='writing-for-agents' else (1 if q.name in {'define-requirements','handoff-and-recall-work','diff-auditor'} else 2)
 # Exclude only this private repo-local installation; preserve all pre-existing text.
 exclude=config['excludePath'];original=Path(exclude).read_text() if Path(exclude).exists() else ''
 marker='/.agents/skills/blacktower-development/'
 payload=original if marker in original.splitlines() else original+('' if not original or original.endswith('\n') else '\n')+marker+'\n'
 desired_exclude={'type':'file','sha256':hashlib.sha256(payload.encode()).hexdigest(),'mode':snapshot(exclude)['mode'] if snapshot(exclude) else 0o644}
 destinations[exclude]=None;groups[exclude]=3
 if only_skills or only_shared:
  selected=set()
  for names,folder,label in [(only_skills,'skills','personal'),(only_shared,'shared','shared')]:
   available={Path(dest).name:dest for dest,src in destinations.items() if (label=='personal' and Path(dest).parent==personal and Path(dest).name!='.system') or (label=='shared' and src and Path(src).parent==root/folder)}
   unknown=set(names or [])-available.keys()
   if unknown:raise RuntimeError(f'Unknown {label} skills: '+', '.join(sorted(unknown)))
   selected.update(available[name] for name in names or [])
  destinations={dest:src for dest,src in destinations.items() if dest in selected}
 operations=[]
 for dest,src in sorted(destinations.items(),key=lambda x:(groups[x[0]],x[0])):
  old=installed['paths'].get(dest,baseline.get(dest))
  desired=desired_exclude if dest==exclude else snapshot(src) if src else None
  actual=snapshot(dest)
  if actual!=old and actual!=desired:raise RuntimeError(f'Drift at {dest}; preserve local edits and refresh the reviewed baseline')
  operations.append({'destination':dest,'source':src,'expected':old,'desired':desired,'group':groups[dest],
   'ownership':'repository-local' if dest==target or dest==exclude else 'shared-personal' if Path(dest).parent==Path(config['sharedRoot']) else 'personal',
   'retiredName':Path(dest).name if desired is None else None,
   'payload':payload if dest==exclude else None,'action':'unchanged' if actual==desired else 'retire' if desired is None else 'install'})
 protected,changed=external_owners(baseline,destinations)
 revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
 return {'sourceRoot':str(root),'sourceRevision':revision,'operations':operations,'protected':protected,
  'externalOwnersChangedSinceBaseline':changed,'previousInstalled':installed}

def external_owners(baseline,destinations):
 """Snapshot OS-, system- and Omarchy-owned skills as they are now.

 Their owners update them (Codex upgrades .system; Omarchy exists only on some
 hosts), so a stale baseline is reported, not enforced. apply and verify still
 refuse any change to these paths while the installer runs."""
 protected={};changed=[]
 for p,s in baseline.items():
  if p in destinations or not (p.endswith('/.system') or '/usr/share/' in p or Path(p).name in {'omarchy','diagnose-crash'}):continue
  protected[p]=snapshot(p)
  if protected[p]!=s:changed.append(p)
 return protected,sorted(changed)

def validate_current(op,phase):
 actual=snapshot(op['destination'])
 permitted=[op['expected'],op['desired']]
 if phase in {'removing','installing','installed'}:permitted.append(None)
 if actual not in permitted:raise RuntimeError(f'Drift at {op["destination"]}; {phase} aborted')
 return actual

def apply(plan,state,fault=None,resume=None,through=3):
 state=Path(state);state.mkdir(parents=True,exist_ok=True)
 if resume:
  run=Path(resume);journal=read(run/'journal.json')
  if journal['status']=='rolled-back':raise RuntimeError('Cannot resume a rolled-back installation')
  plan=journal['plan']
 else:
  # Check every destination before starting any batch.
  for op in plan['operations']:validate_current(op,'preflight')
  run=state/('run-'+uuid.uuid4().hex);run.mkdir();(run/'backups').mkdir()
  journal={'status':'applying','plan':plan,'progress':{},'run':str(run)};save(run/'journal.json',journal)
 for p,s in plan.get('protected',{}).items():
  if snapshot(p)!=s:raise RuntimeError(f'Protected path drift: {p}')
 for i,op in enumerate(plan['operations']):
  if op['group']>through:continue
  key=str(i);phase=journal['progress'].get(key,'pending');backup=run/'backups'/key
  actual=validate_current(op,phase)
  if phase=='complete':
   if actual!=op['desired']:raise RuntimeError(f'Completed path drift: {op["destination"]}')
   continue
  # Validate staged source bytes on every resume.
  if op['source'] and snapshot(op['source'])!=op['desired']:raise RuntimeError(f'Source changed: {op["source"]}')
  if phase=='pending':
   if actual!=op['expected'] and actual!=op['desired']:raise RuntimeError('Unexpected pre-install state')
   # A no-op still gets a verified original for correct rollback semantics.
   op['original']=actual;op['backupLocation']=str(backup)
   if actual is not None:
    if backup.exists() or backup.is_symlink():
     if snapshot(backup)!=actual:raise RuntimeError(f'Incomplete backup {backup}')
    else:copy(op['destination'],backup)
    if snapshot(backup)!=actual:raise RuntimeError('Backup verification failed')
   journal['progress'][key]='backed-up';save(run/'journal.json',journal);phase='backed-up'
   if fault:fault('after_backup',i)
  if snapshot(backup)!=op.get('original'):raise RuntimeError(f'Backup changed: {backup}')
  if actual!=op['desired']:
   dest=Path(op['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
   journal['progress'][key]='removing';save(run/'journal.json',journal)
   # Recheck immediately before the bounded replacement/removal.
   validate_current(op,'removing');remove(dest)
   if fault:fault('after_remove',i)
   journal['progress'][key]='installing';save(run/'journal.json',journal)
   if op['desired'] is not None:
    stage=stage_path(dest,run)
    if stage.exists() or stage.is_symlink():remove(stage)
    try:
     if op['payload'] is not None:stage.write_text(op['payload']);stage.chmod(op['desired']['mode'])
     else:copy(op['source'],stage)
     if snapshot(stage)!=op['desired']:raise RuntimeError(f'Staging failed: {dest}')
     os.replace(stage,dest)
    finally:
     # Never leave a partial stage beside other owners' entries.
     if stage.exists() or stage.is_symlink():remove(stage)
   if fault:fault('after_install',i)
  if snapshot(op['destination'])!=op['desired']:raise RuntimeError(f'Post-install verification failed: {op["destination"]}')
  journal['progress'][key]='complete';save(run/'journal.json',journal)
 current=dict(plan['previousInstalled']['paths'])
 for i,op in enumerate(plan['operations']):
  if journal['progress'].get(str(i))=='complete':current[op['destination']]=op['desired']
 save(statefile(state),{'sourceRevision':plan['sourceRevision'],'run':str(run),'paths':current})
 journal['status']='complete' if all(journal['progress'].get(str(i))=='complete' for i in range(len(plan['operations']))) else 'partial'
 save(run/'journal.json',journal)
 return run

def stage_path(dest,run):return Path(dest).parent/('.'+Path(dest).name+'.stage-'+Path(run).name)

def released_merge(op,backup):
 """Payload restoring only the path records a takeover released from a manifest.

 Later writers (link-workstation applies) may re-save that manifest; their other
 records are kept. Returns None when a released record was claimed or changed."""
 dest=Path(op['destination'])
 if op.get('action')!='release-owner' or op.get('original') is None or dest.is_symlink() or not dest.is_file():return None
 original=json.loads(Path(backup).read_text());replacement=json.loads(op['payload'])
 released=set(original['paths'])-set(replacement['paths'])
 try:current=json.loads(dest.read_text())
 except ValueError:return None
 if not isinstance(current,dict) or not isinstance(current.get('paths'),dict):return None
 if any(k in current['paths'] and current['paths'][k]!=original['paths'][k] for k in released):return None
 merged={k:v for k,v in current.items() if not (k=='releasedTo' and v==replacement.get('releasedTo'))}
 merged['paths']={**current['paths'],**{k:original['paths'][k] for k in released}}
 return json.dumps(merged,indent=2)+'\n'

def rollback_allowed(journal,i,op):
 allowed=[op['desired'],op.get('original')]
 if journal['progress'].get(str(i)) in {'removing','installing'} or journal.get('rollbackProgress',{}).get(str(i))=='restoring':allowed.append(None)
 return allowed

def rollback(run,state):
 run=Path(run);journal=read(run/'journal.json');plan=journal['plan']
 if journal['status']=='rolled-back':return
 # All-path preflight: never partly roll back before discovering later user edits.
 for i,op in enumerate(plan['operations']):
  phase=journal['progress'].get(str(i),'pending')
  if phase=='pending':continue
  if snapshot(run/'backups'/str(i))!=op.get('original'):raise RuntimeError('Rollback backup hash mismatch')
  if snapshot(op['destination']) not in rollback_allowed(journal,i,op) and released_merge(op,run/'backups'/str(i)) is None:
   raise RuntimeError(f'Rollback preserves intervening edits at {op["destination"]}')
 journal['status']='rolling-back';save(run/'journal.json',journal)
 for i in reversed(range(len(plan['operations']))):
  op=plan['operations'][i];dest=Path(op['destination']);backup=run/'backups'/str(i)
  # A crash between staging and replacement leaves a stage named for this run.
  stale=stage_path(dest,run)
  if stale.exists() or stale.is_symlink():remove(stale)
  if journal['progress'].get(str(i),'pending')=='pending':continue
  if snapshot(dest)==op.get('original'):continue
  stage=dest.parent/('.'+dest.name+'.rollback-stage-'+run.name)
  if snapshot(dest) not in rollback_allowed(journal,i,op):
   # A later writer re-saved a released manifest: restore just the released records.
   merged=released_merge(op,backup)
   if merged is None:raise RuntimeError(f'Rollback preserves intervening edits at {dest}')
   wanted={'type':'file','mode':snapshot(dest)['mode'],'sha256':hashlib.sha256(merged.encode()).hexdigest()}
   if snapshot(dest)!=wanted:
    if stage.exists() or stage.is_symlink():remove(stage)
    stage.write_text(merged);stage.chmod(wanted['mode'])
    if snapshot(stage)!=wanted:raise RuntimeError('Rollback staging verification failed')
    # Recheck the live manifest immediately before replacing it.
    if released_merge(op,backup)!=merged:
     remove(stage);raise RuntimeError(f'Rollback preserves intervening edits at {dest}')
    os.replace(stage,dest)
   journal.setdefault('rollbackProgress',{})[str(i)]='merged-records';save(run/'journal.json',journal)
   continue
  if op.get('original') is not None:
   if stage.exists() or stage.is_symlink():
    if snapshot(stage)!=op['original']:remove(stage)
   if not stage.exists() and not stage.is_symlink():copy(backup,stage)
   if snapshot(stage)!=op['original']:raise RuntimeError('Rollback staging verification failed')
  journal.setdefault('rollbackProgress',{})[str(i)]='restoring';save(run/'journal.json',journal)
  # Recheck immediately before removal; the preflight may be stale by now.
  if snapshot(dest) not in rollback_allowed(journal,i,op):raise RuntimeError(f'Rollback preserves intervening edits at {dest}')
  remove(dest)
  if op.get('original') is not None:os.replace(stage,dest)
  if snapshot(dest)!=op.get('original'):raise RuntimeError('Rollback verification failed')
  journal['rollbackProgress'][str(i)]='restored';save(run/'journal.json',journal)
 save(statefile(state),plan['previousInstalled']);journal['status']='rolled-back';save(run/'journal.json',journal)

def refuse_released(run):
 """Predecessor rollbacks must not write paths released to Subsets back into their manifests."""
 marker=Path.home()/'.local/state/subsets-fleet/profiles/ownership.json'
 journal=read(Path(run)/'journal.json')
 if not marker.exists() or journal['status']=='rolled-back':return
 released=set(read(marker).get('transferredPaths',[]));plan=journal['plan']
 claims=[p for p in plan['previousInstalled']['paths'] if p in released]
 claims+=[op['destination'] for i,op in enumerate(plan['operations']) if journal['progress'].get(str(i),'pending')!='pending' and op['destination'] in released]
 if claims:raise RuntimeError('Subsets owns released skill paths; this rollback would reclaim '+sorted(claims)[0])

def verify(plan,state):
 failures=[]
 for op in plan['operations']:
  if snapshot(op['destination'])!=op['desired']:failures.append(op['destination'])
 for p,s in plan.get('protected',{}).items():
  if snapshot(p)!=s:failures.append(p)
 if failures:raise RuntimeError('Verification mismatch: '+', '.join(failures))
 return {'verified':len(plan['operations']),'protected':len(plan.get('protected',{}))}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['plan','apply','verify','rollback']);parser.add_argument('--state',type=Path,default=DEFAULT_STATE);parser.add_argument('--resume',type=Path);parser.add_argument('--run',type=Path);parser.add_argument('--through',type=int,choices=[1,2,3],default=3)
 parser.add_argument('--only-skill',action='append',help='Limit plan/apply/verify to a named personal skill; preserves drift checks for selected paths')
 parser.add_argument('--only-shared',action='append',help='Limit plan/apply/verify to a named shared owner; may be combined with --only-skill')
 args=parser.parse_args()
 if (args.only_skill or args.only_shared) and (args.command=='rollback' or args.resume):parser.error('Selectors cannot change the scope of a saved transaction')
 # plan/verify do not create or modify installation state.
 if args.command=='plan':print(json.dumps(prepare(state=args.state,only_skills=args.only_skill,only_shared=args.only_shared),indent=2));return
 if args.command=='verify':print(json.dumps(verify(prepare(state=args.state,only_skills=args.only_skill,only_shared=args.only_shared),args.state)));return
 args.state.mkdir(parents=True,exist_ok=True)
 with (args.state/'installer.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if args.command=='rollback':
   if not args.run:parser.error('--run is required for rollback')
   refuse_released(args.run);rollback(args.run,args.state);print('Rolled back',args.run)
  else:
   if not args.resume:
    unfinished=[p for p in args.state.glob('run-*/journal.json') if read(p)['status'] in {'applying','partial','rolling-back'}]
    if unfinished:raise RuntimeError('Resume or roll back the unfinished transaction: '+str(unfinished[0].parent))
   result=apply(None if args.resume else prepare(state=args.state,only_skills=args.only_skill,only_shared=args.only_shared),args.state,resume=args.resume,through=args.through);print(result)

if __name__=='__main__':main()
