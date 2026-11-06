#!/usr/bin/env python3
"""Read fresh skills/list metadata from a short-lived local Codex app-server."""
import argparse,json,queue,subprocess,threading,time
from pathlib import Path

def discover(cwds, codex='codex'):
 proc=subprocess.Popen([codex,'app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
 messages=queue.Queue()
 def pump():
  for line in proc.stdout:
   try:messages.put(json.loads(line))
   except json.JSONDecodeError:pass
 threading.Thread(target=pump,daemon=True).start()
 def request(i,method,params):
  proc.stdin.write(json.dumps({'id':i,'method':method,'params':params})+'\n');proc.stdin.flush()
  deadline=time.monotonic()+40
  while time.monotonic()<deadline:
   try:msg=messages.get(timeout=max(0.1,deadline-time.monotonic()))
   except queue.Empty:break
   if msg.get('id')==i:
    if 'error' in msg:raise RuntimeError(msg['error'])
    return msg['result']
  raise TimeoutError('Codex app-server did not answer '+method+' within 40 seconds')
 try:
  server=request(1,'initialize',{'clientInfo':{'name':'personal-skill-audit','version':'1.0.0'},'capabilities':{'experimentalApi':True}})
  proc.stdin.write(json.dumps({'method':'initialized'})+'\n');proc.stdin.flush()
  result=request(2,'skills/list',{'cwds':cwds,'forceReload':True})
  return {'server':server,'skills':result}
 finally:
  proc.terminate()
  try:proc.wait(timeout=5)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cwd',action='append',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--codex',default='codex');a=p.parse_args()
 result=discover(a.cwd,a.codex);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
 data=result['skills'];print('Discovery saved:',a.output,'response keys:',list(data))
