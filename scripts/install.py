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
 destinations={};groups={}
 for p in (root/'skills').iterdir():
  if (p/'SKILL.md').exists():
   d=str(Path(config['personalRoot'])/p.name);destinations[d]=str(p)
   groups[d]=1 if p.name=='frontend-design' else (3 if p.name in {'hatch-pet','dependency-upgrade','opentui','technical-writing'} else 2)
 for p in (root/'shared').iterdir():destinations[str(Path(config['sharedRoot'])/p.name)]=str(p);groups[str(Path(config['sharedRoot'])/p.name)]=1
 target=str(Path(config['blacktowerRoot'])/'.agents/skills/blacktower-development')
 destinations[target]=str(root/'repository-skills/blacktower-development');groups[target]=3
 catalog=read(root/'catalog/proposed-catalog.json');keep={r['name'] for r in catalog if r['scope']=='personal'}
 personal=Path(config['personalRoot'])
 for p in baseline.keys() | installed['paths'].keys():
  q=Path(p)
  if q.parent==personal and q.name not in keep and q.name!='.system':destinations[p]=None;groups[p]=3 if q.name.startswith('principle-') or q.name=='writing-for-agents' else (1 if q.name in {'requirements-interview','session-handoff','review-agent'} else 2)
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
 protected={p:s for p,s in baseline.items() if p not in destinations and (p.endswith('/.system') or '/usr/share/' in p or Path(p).name in {'omarchy','diagnose-crash'})}
 for p,s in protected.items():
  if snapshot(p)!=s:raise RuntimeError(f'Externally owned skill changed: {p}')
 revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
 return {'sourceRoot':str(root),'sourceRevision':revision,'operations':operations,'protected':protected,'previousInstalled':installed}

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
    stage=dest.parent/('.'+dest.name+'.stage-'+run.name)
    if stage.exists() or stage.is_symlink():remove(stage)
    if op['payload'] is not None:stage.write_text(op['payload']);stage.chmod(op['desired']['mode'])
    else:copy(op['source'],stage)
    if snapshot(stage)!=op['desired']:raise RuntimeError(f'Staging failed: {dest}')
    os.replace(stage,dest)
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

def rollback(run,state):
 run=Path(run);journal=read(run/'journal.json');plan=journal['plan']
 if journal['status']=='rolled-back':return
 # All-path preflight: never partly roll back before discovering later user edits.
 for i,op in enumerate(plan['operations']):
  phase=journal['progress'].get(str(i),'pending')
  if phase=='pending':continue
  actual=snapshot(op['destination'])
  allowed=[op['desired'],op.get('original')]
  if phase in {'removing','installing'} or journal.get('rollbackProgress',{}).get(str(i))=='restoring':allowed.append(None)
  if actual not in allowed:raise RuntimeError(f'Rollback preserves intervening edits at {op["destination"]}')
  if snapshot(run/'backups'/str(i))!=op.get('original'):raise RuntimeError('Rollback backup hash mismatch')
 journal['status']='rolling-back';save(run/'journal.json',journal)
 for i in reversed(range(len(plan['operations']))):
  if journal['progress'].get(str(i),'pending')=='pending':continue
  op=plan['operations'][i];dest=Path(op['destination']);backup=run/'backups'/str(i)
  if snapshot(dest)==op.get('original'):continue
  stage=dest.parent/('.'+dest.name+'.rollback-stage-'+run.name)
  if op.get('original') is not None:
   if stage.exists() or stage.is_symlink():
    if snapshot(stage)!=op['original']:remove(stage)
   if not stage.exists() and not stage.is_symlink():copy(backup,stage)
   if snapshot(stage)!=op['original']:raise RuntimeError('Rollback staging verification failed')
  journal.setdefault('rollbackProgress',{})[str(i)]='restoring';save(run/'journal.json',journal)
  remove(dest)
  if op.get('original') is not None:os.replace(stage,dest)
  if snapshot(dest)!=op.get('original'):raise RuntimeError('Rollback verification failed')
  journal['rollbackProgress'][str(i)]='restored';save(run/'journal.json',journal)
 save(statefile(state),plan['previousInstalled']);journal['status']='rolled-back';save(run/'journal.json',journal)

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
   rollback(args.run,args.state);print('Rolled back',args.run)
  else:
   if not args.resume:
    unfinished=[p for p in args.state.glob('run-*/journal.json') if read(p)['status'] in {'applying','partial','rolling-back'}]
    if unfinished:raise RuntimeError('Resume or roll back the unfinished transaction: '+str(unfinished[0].parent))
   result=apply(None if args.resume else prepare(state=args.state,only_skills=args.only_skill,only_shared=args.only_shared),args.state,resume=args.resume,through=args.through);print(result)

if __name__=='__main__':main()
