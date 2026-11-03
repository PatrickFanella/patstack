#!/usr/bin/env python3
"""Deploy three shared marketing procedures and dated reading copies, transactionally."""
import argparse
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('voice-ledger', 'content-recaster', 'launch-dossier')


def receive(command, payload, home=None):
    home = Path(home) if home else Path.home()
    state = home / '.local/state/marketing-fleet'
    state.mkdir(parents=True, exist_ok=True)
    namespace = {'__file__': str(state / 'installer.py'), '__name__': 'marketing_installer'}
    exec(compile(payload['installer'], 'canonical-install.py', 'exec'), namespace)
    snapshot, read, save = (namespace[name] for name in ('snapshot', 'read', 'save'))
    desired_map = payload['destinations']
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    with (state / 'lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if command == 'rollback':
            previous = read(state / 'installed.json', {})
            if not previous.get('run'):
                raise RuntimeError('No managed transaction to roll back')
            namespace['rollback'](previous['run'], state)
            return {'rolledBack': previous['run']}
        previous = read(state / 'installed.json', {'paths': {}})
        if command == 'plan':
            operations, preserved = [], {}
            stage = home / '.local/share/marketing-fleet/sources' / digest
            for relative, spec in sorted(desired_map.items()):
                parts = PurePosixPath(relative).parts
                if not parts or relative.startswith('/') or '..' in parts:
                    raise RuntimeError('Invalid relative path')
                if not (relative.startswith('.agents/skills/') or relative.startswith('.claude/skills/')
                        or relative.startswith('Work/Research/Marketing-Packets/')):
                    raise RuntimeError('Unexpected destination scope')
                dest = home / relative
                linked_parent = next((p for p in dest.parents if p.is_symlink()), None)
                if linked_parent:
                    if relative.startswith('.claude/skills/'):
                        preserved[str(dest)] = snapshot(dest)
                        continue
                    raise RuntimeError('Linked parent retains its owner: '+str(linked_parent))
                source, content = None, None
                if 'link' in spec:
                    target = str(home / spec['link'])
                    mask = os.umask(0); os.umask(mask)
                    wanted = {'type': 'symlink', 'target': target,
                              'mode': (0o777 & ~mask) if sys.platform == 'darwin' else 0o777}
                    source = stage / relative
                    source.parent.mkdir(parents=True, exist_ok=True)
                    if source.is_symlink():
                        if os.readlink(source) != target:
                            raise RuntimeError('Staged link changed')
                    elif source.exists():
                        raise RuntimeError('Staged link conflicts with a file')
                    else:
                        source.symlink_to(target)
                else:
                    source = stage / relative
                    for name, encoded in spec['files'].items():
                        if name.startswith('/') or '..' in PurePosixPath(name).parts:
                            raise RuntimeError('Invalid source filename')
                        path = source / name
                        if any(p.is_symlink() for p in path.parents) or path.is_symlink():
                            raise RuntimeError('Linked staging path')
                        data = base64.b64decode(encoded)
                        path.parent.mkdir(parents=True, exist_ok=True)
                        if path.exists() and path.read_bytes() != data:
                            raise RuntimeError('Immutable staging source changed')
                        path.write_bytes(data)
                        path.chmod(0o644)
                    wanted = snapshot(source)
                actual = snapshot(dest)
                old = previous['paths'].get(str(dest))
                if str(dest) not in previous['paths'] and actual is not None:
                    if actual == wanted:
                        preserved[str(dest)] = actual
                        continue
                    raise RuntimeError('Unmanaged destination retains its owner: '+str(dest))
                if actual != old:
                    raise RuntimeError('Destination drift: '+str(dest))
                operations.append({'destination': str(dest), 'source': str(source) if source else None,
                                   'expected': old, 'desired': wanted, 'payload': content, 'group': 1,
                                   'action': 'unchanged' if actual == wanted else 'install'})
            plan = {'sourceRoot': payload['sourceRoot'], 'sourceRevision': payload['sourceRevision'],
                    'operations': operations, 'protected': preserved, 'previousInstalled': previous,
                    'payloadDigest': digest}
            save(state / 'plan.json', plan)
            return {'operations': [{'destination': o['destination'], 'action': o['action']}
                                   for o in operations], 'preserved': list(preserved), 'payloadDigest': digest}
        plan = read(state / 'plan.json')
        if not plan or plan['payloadDigest'] != digest:
            raise RuntimeError('Preview this exact payload first')
        if command == 'apply':
            # The canonical installer rechecks destination and staged-source snapshots.
            run = namespace['apply'](plan, state)
            return {'run': str(run), **namespace['verify'](plan, state)}
        return namespace['verify'](plan, state)


def bundle(packets):
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    destinations = {}
    for name in NAMES:
        files = {}
        for path in sorted((ROOT / 'shared' / name).rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            committed = subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT)
            if path.read_bytes() != committed:
                raise RuntimeError('Commit selected source before deployment: '+relative)
            files[path.relative_to(ROOT / 'shared' / name).as_posix()] = base64.b64encode(committed).decode()
        destinations['.agents/skills/'+name] = {'files': files}
        destinations['.claude/skills/'+name] = {'link': '.agents/skills/'+name}
    files = {}
    packet_sources = {}
    source_files = []
    for spec in packets:
        name, raw_path = spec.split('=', 1)
        if not name.replace('-', '').isalnum():
            raise RuntimeError('Invalid packet name')
        source = Path(raw_path).resolve()
        packet_sources[name] = str(source)
        repo = Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=source,text=True).strip())
        source_revision = subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
        origin = subprocess.check_output(['git','remote','get-url','origin'],cwd=source,text=True).strip().removesuffix('.git')
        if not origin.startswith('https://git.subcult.tv/'):
            raise RuntimeError('Review reference-link host for '+origin)
        for path in sorted(source.rglob('*')):
            if not path.is_file():
                continue
            if path.suffix not in {'.md', '.json', '.txt'}:
                continue
            original = path.read_bytes()
            data = original
            if path.suffix == '.md':
                def relink(match):
                    raw = match.group(1)
                    target, _, fragment = raw.strip('<>').partition('#')
                    if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target):
                        return match.group(0)
                    resolved = (path.parent / unquote(target)).resolve()
                    if resolved.is_relative_to(source):
                        return match.group(0)
                    if not resolved.is_relative_to(repo):
                        raise RuntimeError('Reference outside source repository: '+str(resolved))
                    url = origin+'/src/commit/'+source_revision+'/'+quote(resolved.relative_to(repo).as_posix())
                    return ']('+url+('#'+fragment if fragment else '')+')'
                data = re.sub(r'\]\(([^)]+)\)', relink, original.decode()).encode()
            key = name+'/'+path.relative_to(source).as_posix()
            files[key] = base64.b64encode(data).decode()
            source_files.append({'destination':key,'source':str(path),'repository':str(repo),
                'sourceRevision':source_revision,'sourceSha256':hashlib.sha256(original).hexdigest(),
                'readingCopySha256':hashlib.sha256(data).hexdigest()})
    files['SOURCE-MANIFEST.json'] = base64.b64encode((json.dumps(source_files,indent=2)+'\n').encode()).decode()
    notes = '# Marketing reading bundle\n\nThese are dated reading copies. Edit the owning project or skill source, then prepare a new reviewed sync.\n\n'
    notes += '\n'.join('- '+k+': `'+v+'`' for k,v in packet_sources.items())+'\n'
    files['README.md'] = base64.b64encode(notes.encode()).decode()
    destinations['Work/Research/Marketing-Packets/2026-10-19'] = {'files': files}
    installer = (ROOT / 'scripts/install.py').read_text()
    return {'sourceRoot': str(ROOT), 'sourceRevision': revision,
            'installer': installer, 'destinations': destinations, 'packetSources': packet_sources}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['bundle','plan','apply','verify','rollback'])
    parser.add_argument('--payload', type=Path, required=True)
    parser.add_argument('--packet', action='append', default=[])
    parser.add_argument('--host', choices=['kvant','sputnik','soyuz','dozor','almaz','nuc'])
    args = parser.parse_args()
    if args.command == 'bundle':
        args.payload.parent.mkdir(parents=True, exist_ok=True)
        if args.payload.exists():
            raise RuntimeError('Preserve existing payload; choose a new filename')
        args.payload.write_text(json.dumps(bundle(args.packet), indent=2)+'\n')
        print(str(args.payload))
        return
    payload = json.loads(args.payload.read_text())
    if args.host == 'kvant':
        result = receive(args.command, payload)
    elif args.host:
        host_python = '/opt/homebrew/bin/python3' if args.host == 'soyuz' else 'python3'
        code = "__file__ = '/tmp/marketing-fleet.py'\n"+Path(__file__).read_text().replace(
            "if __name__ == '__main__':\n    main()", "print(json.dumps(receive(sys.argv[1], json.load(sys.stdin))))")
        completed = subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8',args.host,
            shlex.join([host_python,'-c',code,args.command])], input=json.dumps(payload),
            text=True, check=True, capture_output=True)
        result = json.loads(completed.stdout)
    else:
        parser.error('--host is required for deployment')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
