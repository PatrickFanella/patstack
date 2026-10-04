#!/usr/bin/env python3
"""Restore existing MCP registrations and owned skill roots to T3's v2 runtime."""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = Path.home() / '.local/state/t3-opencode-config'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def desired(manifest):
    source = json.loads(Path(manifest['sourceConfig']).read_text())
    servers = {}
    oauth_names = {'clientId': 'client_id', 'clientSecret': 'client_secret',
                   'callbackPort': 'callback_port', 'redirectUri': 'redirect_uri'}
    for name, original in source.get('mcp', {}).items():
        entry = dict(original)
        if 'enabled' in entry:
            entry['disabled'] = not entry.pop('enabled')
        if isinstance(entry.get('timeout'), int):
            entry['timeout'] = {'startup': entry['timeout'], 'execution': entry['timeout']}
        if isinstance(entry.get('oauth'), dict):
            entry['oauth'] = {oauth_names.get(k, k): v for k, v in entry['oauth'].items()}
        servers[name] = entry
    return {'skills': manifest['skillRoots'], 'mcp': {'servers': servers}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify'])
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'catalog/t3-opencode-runtime.json').read_text())
    target = Path(manifest['destination'])
    payload = (json.dumps(desired(manifest), indent=2) + '\n').encode()
    receipt = STATE / 'receipt.json'
    previous = json.loads(receipt.read_text()) if receipt.exists() else {}
    actual = digest(target)
    expected = previous.get('sha256')
    wanted = hashlib.sha256(payload).hexdigest()
    if actual not in [expected, wanted]:
        raise RuntimeError('Destination drift; preserve and review existing configuration')
    summary = {'destination': str(target), 'skillRoots': manifest['skillRoots'],
               'mcpServers': list(desired(manifest)['mcp']['servers']),
               'action': 'unchanged' if actual == wanted else 'write'}
    if args.command == 'apply':
        for relative in ['catalog/t3-opencode-runtime.json', 'scripts/t3-opencode-runtime.py']:
            import subprocess
            committed = subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=ROOT)
            if (ROOT / relative).read_bytes() != committed:
                raise RuntimeError('Commit reviewed runtime source before applying')
        STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
        if target.exists() and actual != wanted:
            backup = STATE / ('before-' + actual + '.json')
            if not backup.exists():
                backup.write_bytes(target.read_bytes())
                backup.chmod(0o600)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.tmp')
        temporary.write_bytes(payload)
        temporary.chmod(0o600)
        os.replace(temporary, target)
        receipt.write_text(json.dumps({'sha256': wanted, 'previousSha256': actual,
                                      'sourceSha256': digest(Path(manifest['sourceConfig']))}, indent=2) + '\n')
        receipt.chmod(0o600)
    if args.command == 'verify' and actual != wanted:
        raise RuntimeError('Runtime configuration does not match selected sources')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
