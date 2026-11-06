#!/usr/bin/env python3
"""Guarded per-host Tadooer installation; native clients own MCP/plugin config."""
import argparse
import base64
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time
import tomllib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def digest(data): return hashlib.sha256(data).hexdigest()

def state(path):
    if path.is_symlink(): return {'link':os.readlink(path)}
    if not path.exists(): return None
    if not path.is_file(): raise RuntimeError('Expected regular file: '+str(path))
    return {'sha256':digest(path.read_bytes()),'mode':stat.S_IMODE(path.stat().st_mode)}

def run(args,check=True):
    p=subprocess.run(args,capture_output=True,text=True,timeout=90)
    if check and p.returncode:
        raise RuntimeError('Client command failed: '+shlex.join(args)+'\n'+p.stderr[-1200:])
    return p

def write(path,data,mode=0o600):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.tadooer-new')
    with open(temp,'xb') as handle:
        handle.write(data); handle.flush(); os.fsync(handle.fileno())
    temp.chmod(mode); os.replace(temp,path)

def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}

def client_json(output):
    for index,line in enumerate(output.splitlines()):
        if line.lstrip().startswith(('[','{')):
            return json.loads('\n'.join(output.splitlines()[index:]))
    raise RuntimeError('Client did not return JSON.')

def existing_mcp(home,launcher):
    claude=read_json(home/'.claude.json').get('mcpServers',{}).get('tadooer')
    if claude and (claude.get('command')!=str(launcher) or claude.get('args',[])!=[]):
        raise RuntimeError('Existing Claude Tadooer entry differs; preserve and reconcile it.')
    p=run(['codex','mcp','get','tadooer','--json'],check=False)
    codex=json.loads(p.stdout) if p.returncode==0 else None
    if codex:
        transport=codex.get('transport',codex)
        if transport.get('command')!=str(launcher) or transport.get('args',[])!=[]:
            raise RuntimeError('Existing Codex Tadooer entry differs; preserve and reconcile it.')
    return bool(codex),bool(claude)

def remote(mode,payload):
    home=Path.home()
    os.environ['PATH']=str(home/'.local/bin')+':'+str(home/'.local/share/mise/shims')+':/opt/homebrew/bin:'+os.environ.get('PATH','')
    for name in ('codex','claude'):
        if not shutil.which(name): raise RuntimeError(name+' installation unavailable on this host.')
    node=Path(payload['node'])
    version=run([str(node),'--version']).stdout.strip()
    if int(version.lstrip('v').split('.')[0])<24: raise RuntimeError('Tadooer adapter requires a supported Node 24+ runtime.')
    data={name:base64.b64decode(value) for name,value in payload['files'].items()}
    for name,value in data.items():
        if Path(name).is_absolute() or '..' in Path(name).parts or digest(value)!=payload['hashes'][name]:
            raise RuntimeError('Invalid deployment payload.')
    version_id=digest(json.dumps(payload['hashes'],sort_keys=True).encode())[:16]
    folder=home/'.local/share/tadooer-assistant'/version_id
    receipt_dir=home/'.local/state/tadooer-assistant'
    receipt_dir.mkdir(parents=True,exist_ok=True,mode=0o700); receipt_dir.chmod(0o700)
    plan_path=receipt_dir/'plan.json'
    receipt_path=receipt_dir/'deployment.json'
    launcher=home/'.local/bin/tadooer-mcp'
    setup=home/'.local/bin/tadooer-setup-token'
    config=home/'.config/tadooer/mcp.json'
    protected=[home/'.codex/config.toml',home/'.claude.json',home/'.claude/settings.json',home/'.claude/plugins/known_marketplaces.json',home/'.codex/plugins/marketplaces.json',launcher,setup,config]
    previous=read_json(receipt_path)
    for path,expected in previous.get('ownedFiles',{}).items():
        if state(Path(path))!=expected: raise RuntimeError('Managed file drift: '+path)
    registered=existing_mcp(home,launcher)
    market=str(folder/'marketplace')
    allowed_markets=set(previous.get('marketplaceSources',[]))
    if previous.get('folder'): allowed_markets.add(str(Path(previous['folder'])/'marketplace'))
    codex_config=home/'.codex/config.toml'
    codex_settings=tomllib.loads(codex_config.read_text()) if codex_config.exists() else {}
    codex_market=codex_settings.get('marketplaces',{}).get('subcult-tadooer',{})
    codex_source=codex_market.get('source')
    claude_market=read_json(home/'.claude/plugins/known_marketplaces.json').get('subcult-tadooer')
    claude_source=claude_market.get('source',{}).get('path') if claude_market else None
    for source in (codex_source,claude_source):
        if source and source not in allowed_markets:
            raise RuntimeError('Unmanaged Tadooer marketplace source; preserve '+source)

    launcher_bytes=('#!/bin/sh\nexec '+shlex.quote(str(node))+' '+shlex.quote(str(folder/'runtime/main.mjs'))+' "$@"\n').encode()
    setup_bytes=('#!/bin/sh\nexec '+shlex.quote(sys.executable)+' '+shlex.quote(str(folder/'marketplace/setup-token.py'))+' "$@"\n').encode()
    for path,content in ((launcher,launcher_bytes),(setup,setup_bytes)):
        if path.exists() or path.is_symlink():
            if str(path) not in previous.get('ownedFiles',{}) and (path.is_symlink() or path.read_bytes()!=content):
                raise RuntimeError('Unmanaged launcher exists: '+str(path))
    if folder.exists():
        for name,value in data.items():
            p=folder/name
            if not p.is_file() or p.is_symlink() or p.read_bytes()!=value:
                raise RuntimeError('Versioned payload drift: '+str(p))
    before={str(p):state(p) for p in protected}
    summary={'home':str(home),'versionId':version_id,'node':str(node),'nodeVersion':version,'sourceRevision':payload['sourceRevision'],'plugin':'tadooer-assistant@subcult-tadooer','runtimeSha256':payload['hashes']['runtime/main.mjs'],'registeredBefore':{'codex':registered[0],'claude':registered[1]},'authentication':'pending'}
    if config.exists():
        settings=read_json(config)
        token=Path(settings.get('tokenFile','/nonexistent'))
        if token.is_file() and not token.is_symlink() and stat.S_IMODE(token.stat().st_mode)==0o600:
            summary['authentication']='credential-file-present-unverified'
    if mode=='plan':
        write(plan_path,json.dumps({'before':before,'summary':summary},indent=2).encode())
        print(json.dumps(summary,indent=2)); return
    if mode=='apply':
        plan=read_json(plan_path)
        if plan.get('before')!=before or plan.get('summary',{}).get('versionId')!=version_id:
            raise RuntimeError('State changed since plan; re-plan and review.')
        backup=receipt_dir/('before-'+version_id+'-'+str(time.time_ns()))
        backup.mkdir(mode=0o700)
        write(backup/'states.json',json.dumps(before,indent=2).encode())
        for index,p in enumerate(protected):
            if p.is_file() and not p.is_symlink():
                target=backup/(str(index)+'.private'); shutil.copy2(p,target); target.chmod(0o600)
        folder.mkdir(parents=True,exist_ok=True)
        for name,value in data.items():
            target=folder/name
            if not target.exists(): write(target,value,0o644)
        if state(launcher) != {'sha256':digest(launcher_bytes),'mode':0o755}: write(launcher,launcher_bytes,0o755)
        if state(setup) != {'sha256':digest(setup_bytes),'mode':0o755}: write(setup,setup_bytes,0o755)
        if not config.exists():
            config.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
            write(config,json.dumps({'url':payload['url'],'tokenFile':str(config.parent/'automation-token')},indent=2).encode())
        if not registered[0]: run(['codex','mcp','add','tadooer','--',str(launcher)])
        if not registered[1]: run(['claude','mcp','add','--scope','user','tadooer','--',str(launcher)])
        summary['ownedFiles']={str(p):state(p) for p in (launcher,setup)}
        summary['folder']=str(folder); summary['backup']=str(backup)
        summary['marketplaceSources']=sorted(allowed_markets|{market})
        summary['phase']='native-installation-pending'
        write(receipt_path,json.dumps(summary,indent=2).encode())
        if codex_source and codex_source!=market:
            run(['codex','plugin','marketplace','remove','subcult-tadooer','--json'])
        if codex_source!=market: run(['codex','plugin','marketplace','add',market,'--json'])
        run(['codex','plugin','add','tadooer-assistant@subcult-tadooer','--json'])
        if claude_source and claude_source!=market:
            run(['claude','plugin','marketplace','remove','subcult-tadooer','--scope','user','--json'])
        if claude_source!=market: run(['claude','plugin','marketplace','add',market,'--scope','user','--json'])
        run(['claude','plugin','install','tadooer-assistant@subcult-tadooer','--scope','user'])
        run(['claude','plugin','update','tadooer-assistant@subcult-tadooer','--scope','user'])
        summary['ownedFiles']={str(p):state(p) for p in (launcher,setup)}
        summary['payloadHashes']=payload['hashes']
        summary['phase']='installed'
        summary['folder']=str(folder); summary['backup']=str(backup)
        write(receipt_path,json.dumps(summary,indent=2).encode())
    if mode in ('apply','verify'):
        if existing_mcp(home,launcher)!=(True,True): raise RuntimeError('MCP registrations missing.')
        cp=read_json(home/'.claude/settings.json').get('enabledPlugins',{})
        if cp.get('tadooer-assistant@subcult-tadooer') is not True:
            raise RuntimeError('Claude plugin not enabled.')
        config_text=(home/'.codex/config.toml').read_text()
        if not re.search(r'\[plugins\."tadooer-assistant@subcult-tadooer"\]\s*enabled\s*=\s*true',config_text):
            raise RuntimeError('Codex plugin not enabled.')
        for name,value in data.items():
            if (folder/name).read_bytes()!=value: raise RuntimeError('Payload hash mismatch.')
        expected_version=json.loads(data['marketplace/plugin/.codex-plugin/plugin.json'])['version']
        codex_plugins=client_json(run(['codex','plugin','list','--marketplace','subcult-tadooer','--json']).stdout)['installed']
        claude_plugins=client_json(run(['claude','plugin','list','--json']).stdout)
        for client,items in (('Codex',codex_plugins),('Claude',claude_plugins)):
            matches=[i for i in items if i.get('pluginId',i.get('id'))=='tadooer-assistant@subcult-tadooer']
            if len(matches)!=1 or not matches[0].get('enabled') or matches[0].get('version')!=expected_version:
                raise RuntimeError(client+' plugin version/enabled verification failed.')
        summary['registration']='verified'; summary['pluginInstallation']='verified'
        summary['pluginVersion']=expected_version
        print(json.dumps(summary,indent=2))

def payload_for(runtime,node,url,revision):
    files={'runtime/main.mjs':runtime.read_bytes()}
    source=ROOT/'integrations/tadooer'
    for p in source.rglob('*'):
        if not p.is_file(): continue
        relative=str(p.relative_to(ROOT))
        committed=subprocess.run(['git','show','HEAD:'+relative],cwd=ROOT,capture_output=True)
        if committed.returncode or committed.stdout!=p.read_bytes():
            raise RuntimeError('Commit plugin source before deployment: '+relative)
        files['marketplace/'+str(p.relative_to(source))]=committed.stdout
    return {'node':node,'url':url,'sourceRevision':revision,'files':{k:base64.b64encode(v).decode() for k,v in files.items()},'hashes':{k:digest(v) for k,v in files.items()}}

def remote_source():
    body=Path(__file__).read_text().rsplit("\nif __name__ ==",1)[0]
    return "__file__='/tmp/tadooer-assistant-host.py'\n"+body+"\nremote(sys.argv[1],json.load(sys.stdin))\n"

def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=('plan','apply','verify'))
    p.add_argument('--host',default='kvant')
    p.add_argument('--runtime',type=Path,required=True)
    p.add_argument('--node',required=True)
    p.add_argument('--url',default='https://tadooer.subcult.tv')
    p.add_argument('--revision',required=True)
    p.add_argument('--python',default='python3')
    args=p.parse_args()
    reviewed=json.loads((ROOT/'catalog/tadooer-assistant.json').read_text())['runtime']
    if args.revision!=reviewed['draft-reviser'] or digest(args.runtime.read_bytes())!=reviewed['sha256']:
        raise RuntimeError('Runtime and --revision must match the reviewed entry in catalog/tadooer-assistant.json.')
    payload=payload_for(args.runtime,args.node,args.url,args.revision)
    if args.host=='kvant': remote(args.mode,payload)
    else:
        code=remote_source()
        command=' '.join(shlex.quote(x) for x in (args.python,'-c',code,args.mode))
        result=subprocess.run(['rtk','proxy','ssh','-o','BatchMode=yes','-o','ConnectTimeout=8',args.host,command],input=json.dumps(payload),text=True,capture_output=True,timeout=300)
        if result.returncode: raise RuntimeError(result.stderr[-2000:])
        print(result.stdout)

if __name__ == '__main__': main()
