#!/usr/bin/env python3
"""Save a scoped token entered locally, without echo or command-line secrets."""
import getpass
import json
import os
import re
from pathlib import Path

def main():
    config=Path(os.environ.get('TADOOER_MCP_CONFIG', str(Path.home()/'.config/tadooer/mcp.json')))
    data=json.loads(config.read_text())
    token_file=Path(data['tokenFile'])
    if token_file.exists() or token_file.is_symlink():
        raise SystemExit('A token file already exists. Preserve it; create/revoke credentials explicitly in Tadooer Connections before replacement.')
    token=getpass.getpass('Paste the scoped Tadooer automation token (hidden): ').strip()
    if not re.fullmatch(r'suite_at_[0-9a-f-]{36}\.[A-Za-z0-9_-]{43}',token):
        raise SystemExit('Invalid automation-token format; nothing written.')
    token_file.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd=os.open(token_file,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as handle:
        handle.write(token+'\n'); handle.flush(); os.fsync(handle.fileno())
    print('Private token file created. Start a fresh assistant session and verify a read operation.')

if __name__=='__main__': main()
