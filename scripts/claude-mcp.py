#!/usr/bin/env python3
"""Preview or add portable Codex MCP registrations to Claude's user config.

Existing conflicting entries are never replaced. Credentials stay in local
configuration and its private backup; neither plans nor source contain them.
"""
import argparse
import json
import os
from pathlib import Path
import tempfile
import time
import tomllib
from urllib.parse import urlsplit


def convert(servers):
    result, skipped = {}, {}
    for name, spec in servers.items():
        if name == 'node_repl':
            skipped[name] = 'Codex desktop runtime required'
        elif spec.get('enabled') is False:
            skipped[name] = 'disabled in Codex'
        elif spec.get('command'):
            result[name] = {'type': 'stdio', **{
                key: spec[key] for key in ('command', 'args', 'env') if key in spec}}
        elif spec.get('url'):
            url = urlsplit(spec['url'])
            if url.scheme not in ('https', 'http') or not url.hostname:
                skipped[name] = 'invalid HTTP URL in Codex'
                continue
            if any(key in spec for key in ('bearer_token_env_var', 'env_http_headers')):
                skipped[name] = 'requires explicit auth adaptation'
                continue
            result[name] = {'type': 'http', 'url': spec['url']}
            if spec.get('http_headers'):
                result[name]['headers'] = spec['http_headers']
        else:
            skipped[name] = 'no supported transport'
    return result, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('plan', 'apply', 'verify'))
    args = parser.parse_args()
    home = Path.home()
    path = home / '.claude.json'
    before = path.read_bytes()
    config = json.loads(before)
    desired, skipped = convert(tomllib.loads((home / '.codex/config.toml').read_text()).get('mcp_servers', {}))
    current = config.setdefault('mcpServers', {})
    conflicts = [name for name, spec in desired.items() if name in current and current[name] != spec]
    if conflicts:
        raise RuntimeError('Preserve conflicting Claude entries: ' + ', '.join(conflicts))
    missing = sorted(set(desired) - set(current))
    print(json.dumps({'add': missing, 'matching': sorted(set(desired) & set(current)), 'skipped': skipped}, indent=2))
    if args.command == 'verify':
        if missing:
            raise RuntimeError('Missing registrations')
    elif args.command == 'apply' and missing:
        state = home / '.local/state/claude-codex-parity' / str(time.time_ns())
        state.mkdir(parents=True, mode=0o700)
        backup = state / 'claude.json.before'
        backup.write_bytes(before)
        backup.chmod(0o600)
        current.update(desired)
        fd, temp = tempfile.mkstemp(prefix='.claude-parity-', dir=home)
        try:
            with os.fdopen(fd, 'w') as stream:
                json.dump(config, stream, indent=2)
                stream.write('\n')
            if path.read_bytes() != before:
                raise RuntimeError('Claude config changed during preparation; retry')
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
        print('Private backup:', backup)


if __name__ == '__main__':
    main()
