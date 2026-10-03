#!/usr/bin/env python3
"""Plan/apply source links using the existing guarded transaction installer."""
import argparse, json, subprocess, fcntl
from pathlib import Path
import install
ROOT=Path(__file__).resolve().parents[1]
STATE=Path.home()/'.codex/skill-installations/codex-source-links'

def plan(only_links=None):
    config=install.read(ROOT/'catalog/workstation-links.json')
    previous=install.read(install.statefile(STATE), {'paths':{}})
    operations=[]
    links=config['links']
    if only_links:
        unknown=set(only_links)-links.keys()
        if unknown:raise RuntimeError('Unknown source links: '+', '.join(sorted(unknown)))
        links={dest:source for dest,source in links.items() if dest in only_links}
    for dest,source in links.items():
        if not Path(source).exists(): raise RuntimeError('Missing source: '+source)
        desired={'type':'symlink','target':source,'mode':0o777}
        expected=previous['paths'].get(dest,config['baseline'].get(dest))
        actual=install.snapshot(dest)
        if actual not in [expected,desired]:raise RuntimeError('Drift: '+dest)
        # Payload is a staged symlink outside the authored tree.
        operations.append({'destination':dest,'source':None,'expected':expected,'desired':desired,'group':1,'payload':None,'action':'unchanged' if actual==desired else 'link'})
    return {'sourceRoot':str(ROOT),'sourceRevision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'operations':operations,'protected':{},'previousInstalled':previous}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['plan','apply','verify','rollback']);parser.add_argument('--run',type=Path);parser.add_argument('--only-link',action='append',help='Limit plan/apply/verify to an exact registered destination');args=parser.parse_args()
    if args.command=='rollback' and args.only_link:parser.error('A selector cannot change a saved rollback scope')
    if args.command=='plan':print(json.dumps(plan(args.only_link),indent=2));return
    if args.command=='verify':print(json.dumps(install.verify(plan(args.only_link),STATE)));return
    STATE.mkdir(parents=True,exist_ok=True)
    with (STATE/'installer.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if args.command=='rollback':
            if not args.run:parser.error('--run required')
            install.rollback(args.run,STATE);return
        if args.only_link:
            # A bounded link deployment must still use a committed manifest and installer.
            # Unrelated dirty sources do not authorize copying or linking their changes.
            for relative in ['catalog/workstation-links.json','scripts/link-workstation.py','scripts/install.py']:
                committed=subprocess.check_output(['git','show','HEAD:'+relative],cwd=ROOT)
                if (ROOT/relative).read_bytes()!=committed:raise RuntimeError('Commit reviewed link source: '+relative)
        elif subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise RuntimeError('Commit reviewed source before applying links')
        pending=[p.parent for p in STATE.glob('run-*/journal.json') if install.read(p)['status'] in {'applying','partial','rolling-back'}]
        if pending:raise RuntimeError('Roll back unfinished source-link transaction: '+str(pending[0]))
        proposal=plan(args.only_link);stage=STATE/'sources';stage.mkdir(exist_ok=True)
        for i,op in enumerate(proposal['operations']):
            p=stage/str(i)
            if p.is_symlink():p.unlink()
            elif p.exists():raise RuntimeError('Unexpected source stage: '+str(p))
            p.symlink_to(op['desired']['target']);op['source']=str(p)
        print(install.apply(proposal,STATE))
if __name__=='__main__':main()
