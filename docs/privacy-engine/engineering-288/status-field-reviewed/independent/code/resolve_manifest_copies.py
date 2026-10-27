"""Resolve partial historical manifest references using exact retained bytes."""
from pathlib import Path
import hashlib, io, json, sys, zipfile

source = Path(sys.argv[1])
destination = Path(sys.argv[2])
found = {}
missing = []

def identity(raw):
    return len(raw), hashlib.sha256(raw).hexdigest()

def register(raw, label):
    found.setdefault(identity(raw), set()).add(label)

def walk(raw, label):
    register(raw, label)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = set(archive.namelist())
        for name in sorted(names):
            data = archive.read(name)
            member = label + '!/' + name
            register(data, member)
            if name.endswith('MANIFEST.json'):
                manifest = json.loads(data)
                manifest = manifest.get('members', manifest)
                prefix = name[:-len('MANIFEST.json')]
                if isinstance(manifest, dict) and all(isinstance(v, dict) and 'bytes' in v and 'sha256' in v for v in manifest.values()):
                    for relative, pin in manifest.items():
                        if prefix + relative not in names:
                            missing.append({'manifest': member, 'absent_relative_member': relative, 'identity': pin})
            if name.endswith('.zip'):
                walk(data, member)

walk(source.read_bytes(), 'I164-status-field-correspondence-1.zip')
assert len(missing) == 3
for row in missing:
    row['matching_preserved_objects'] = sorted(found.get((row['identity']['bytes'], row['identity']['sha256']), set()))
    assert row['matching_preserved_objects'], row
destination.write_text(json.dumps({'result': 'PASS', 'partial_historical_manifest_references': missing, 'partial_copies_not_complete_roots': True}, indent=2) + '\n')
print('PASS: all three partial-manifest references resolve to exact preserved bytes')
