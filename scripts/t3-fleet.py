#!/usr/bin/env python3
"""Preview, back up, deploy and verify the personal T3 fleet scope."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def snapshot(path):
    path = Path(path)
    if path.is_symlink():
        return {'link': os.readlink(path)}
    if path.is_file():
        return {'hash': hashlib.sha256(path.read_bytes()).hexdigest(),
                'mode': path.stat().st_mode & 0o777}
    if path.is_dir():
        return {p.name: snapshot(p) for p in sorted(path.iterdir())}
    return None


def remote(command, payload):
    home = Path.home()
    state = home / '.local/state/t3-fleet'
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    planfile = state / 'plan.json'
    if command == 'plan':
        payload['before'] = {p: snapshot(home / p) for p in payload['skills']}
        payload['configBefore'] = {p: snapshot(home / p) for p in ['.codex/config.toml', '.claude.json']}
        codex = tomllib.loads((home / '.codex/config.toml').read_text()) if (home / '.codex/config.toml').exists() else {}
        claude = json.loads((home / '.claude.json').read_text()) if (home / '.claude.json').exists() else {}
        additions = {}
        removals = []
        for client, current in [('codex', codex.get('mcp_servers', {})), ('claude', claude.get('mcpServers', {}))]:
            additions[client] = []
            for name, spec in payload['mcpServers'].items():
                wanted = spec if client == 'codex' else ({'type': 'http', 'url': spec['url']} if 'url' in spec else {'type': 'stdio', **spec})
                if client == 'claude' and name in payload.get('claudeAccountManaged', []):
                    if name in current:
                        backups = list(state.glob('*/before/.claude.json'))
                        introduced = any(name not in json.loads(p.read_text()).get('mcpServers', {}) for p in backups)
                        if current[name] != wanted or not introduced:
                            raise RuntimeError('Preserve preexisting account MCP entry: ' + name)
                        removals.append(name)
                    continue
                if name in current:
                    if any(current[name].get(k) != v for k, v in wanted.items()):
                        raise RuntimeError(f'Preserve conflicting {client} MCP entry: {name}')
                else:
                    additions[client].append(name)
        payload['additions'] = additions
        payload['removeClaudeDuplicates'] = removals
        planfile.write_text(json.dumps(payload))
        planfile.chmod(0o600)
        print(json.dumps({'skillsChanged': [p for p, before in payload['before'].items() if before != desired_snapshot(payload['skills'][p])], 'mcpAdditions': additions, 'removeClaudeDuplicates': removals}))
        return
    plan = json.loads(planfile.read_text())
    if plan['revision'] != payload['revision'] or plan['skills'] != payload['skills'] or plan['mcpServers'] != payload['mcpServers']:
        raise RuntimeError('Source changed since plan; preview again')
    if command == 'apply':
        for p, expected in {**plan['before'], **plan['configBefore']}.items():
            if snapshot(home / p) != expected:
                raise RuntimeError('Destination changed since preview: ' + p)
        run = state / str(time.time_ns())
        run.mkdir(mode=0o700)
        (run / 'plan.json').write_text(json.dumps(plan))
        (run / 'plan.json').chmod(0o600)
        for relative, files in payload['skills'].items():
            path = home / relative
            if snapshot(path) == desired_snapshot(files):
                continue
            backup = run / 'before' / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() or path.is_symlink():
                if path.is_dir() and not path.is_symlink():
                    shutil.copytree(path, backup, symlinks=True)
                elif path.is_symlink():
                    backup.symlink_to(os.readlink(path))
                else:
                    shutil.copy2(path, backup)
            temp = path.with_name(path.name + '.t3-fleet-new')
            if temp.exists():
                raise RuntimeError('Preserve pending destination: ' + str(temp))
            temp.parent.mkdir(parents=True, exist_ok=True)
            if 'link' in files:
                temp.symlink_to(files['link'])
            else:
                temp.mkdir()
                for name, entry in files.items():
                    dest = temp / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(base64.b64decode(entry['content']))
                    dest.chmod(entry['mode'])
            if path.is_symlink() or path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            os.replace(temp, path)
        for relative, client in [('.codex/config.toml', 'codex'), ('.claude.json', 'claude')]:
            names = plan['additions'][client]
            removals = plan['removeClaudeDuplicates'] if client == 'claude' else []
            if not names and not removals:
                continue
            path = home / relative
            old = path.read_bytes() if path.exists() else b''
            backup = run / 'before' / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(old); backup.chmod(0o600)
            if client == 'codex':
                content = old.decode() + '\n'
                for name in names:
                    content += '\n[mcp_servers.' + json.dumps(name) + ']\n'
                    for key, value in payload['mcpServers'][name].items():
                        encoded = '{' + ', '.join(json.dumps(k) + ' = ' + json.dumps(v) for k, v in value.items()) + '}' if isinstance(value, dict) else json.dumps(value)
                        content += key + ' = ' + encoded + '\n'
                tomllib.loads(content)
            else:
                config = json.loads(old) if old else {}
                for name in removals:
                    del config['mcpServers'][name]
                for name in names:
                    spec = payload['mcpServers'][name]
                    config.setdefault('mcpServers', {})[name] = {'type': 'http', **spec} if 'url' in spec else {'type': 'stdio', **spec}
                content = json.dumps(config, indent=2) + '\n'
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_name(path.name + '.t3-fleet-new')
            temp.write_text(content);temp.chmod(0o600);os.replace(temp, path)
        (run / 'after.json').write_text(json.dumps({p: snapshot(home / p) for p in {**plan['before'], **plan['configBefore']}}))
        print('Backup and deployment receipt: ' + str(run))
    failures = [p for p, files in payload['skills'].items() if snapshot(home / p) != desired_snapshot(files)]
    for relative, client in [('.codex/config.toml', 'codex'), ('.claude.json', 'claude')]:
        text = (home / relative).read_text()
        current = tomllib.loads(text).get('mcp_servers', {}) if client == 'codex' else json.loads(text).get('mcpServers', {})
        for name, spec in payload['mcpServers'].items():
            if client == 'claude' and name in payload.get('claudeAccountManaged', []):
                if name in current:
                    failures.append('duplicate account MCP: ' + name)
                continue
            wanted = spec if client == 'codex' else ({'type': 'http', **spec} if 'url' in spec else {'type': 'stdio', **spec})
            if any(current.get(name, {}).get(k) != v for k, v in wanted.items()):
                failures.append(client + ':' + name)
    if failures:
        raise RuntimeError('Verification failed: ' + ', '.join(failures))
    print(json.dumps({'verifiedSkillDirectories': len(payload['skills']), 'sharedMcpServers': list(payload['mcpServers']), 'revision': payload['revision']}))


def desired_snapshot(files):
    if 'link' in files:
        return files
    result = {}
    for name, entry in files.items():
        node = result
        parts = name.split('/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = {'hash': hashlib.sha256(base64.b64decode(entry['content'])).hexdigest(), 'mode': entry['mode']}
    return result


def main():
    manifest = json.loads((ROOT / 'catalog/t3-fleet.json').read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify'])
    parser.add_argument('--host', required=True, choices=manifest['hosts'])
    args = parser.parse_args()
    host_home = manifest.get('hostHomes', {}).get(args.host, '/home/onnwee')
    host_python = manifest.get('hostPython', {}).get(args.host, 'python3')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    skills = {}
    for folder in manifest['skillSources']:
        for source in sorted((ROOT / folder).iterdir()):
            if not (source / 'SKILL.md').exists():
                continue
            files = {}
            for path in sorted(source.rglob('*')):
                if not path.is_file():
                    continue
                relative = str(path.relative_to(ROOT))
                committed = subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=ROOT)
                if path.read_bytes() != committed:
                    raise RuntimeError('Commit selected skill source before deployment: ' + relative)
                files[str(path.relative_to(source))] = {'content': base64.b64encode(committed).decode(), 'mode': path.stat().st_mode & 0o777}
            root = '.codex/skills' if folder == 'skills' else '.agents/skills'
            skills[root + '/' + source.name] = files
            skills['.claude/skills/' + source.name] = {'link': host_home + '/' + root + '/' + source.name}
    mcp_servers = {name: {**spec, **manifest.get('hostMcpOverrides', {}).get(args.host, {}).get(name, {})} for name, spec in manifest['mcpServers'].items()}
    payload = {'revision': revision, 'skills': skills, 'mcpServers': mcp_servers, 'claudeAccountManaged': manifest.get('claudeAccountManaged', [])}
    code = "__file__ = '/tmp/t3-fleet-deployer.py'\n" + Path(__file__).read_text().replace("if __name__ == '__main__':\n    main()", "remote(sys.argv[1], json.load(sys.stdin))")
    command = [host_python, '-c', code, args.command] if args.host == 'kvant' else ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', args.host, shlex.join([host_python, '-c', code, args.command])]
    subprocess.run(command, input=json.dumps(payload), text=True, check=True)


if __name__ == '__main__':
    main()
