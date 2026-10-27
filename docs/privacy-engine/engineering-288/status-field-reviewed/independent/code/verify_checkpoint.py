"""Verify final review packaging and its exact embedded target."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, sys, zipfile

path = Path(sys.argv[1])
raw = path.read_bytes()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    infos = z.infolist()
    assert len(infos) == len(set(i.filename for i in infos)) and z.testzip() is None
    for info in infos:
        name = PurePosixPath(info.filename)
        assert not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename and str(name) == info.filename
        assert not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) == stat.S_IFREG
    members = json.loads(z.read('MANIFEST.json'))['members']
    assert set(members) == set(z.namelist()) - {'MANIFEST.json'}
    for name, pin in members.items():
        data = z.read(name)
        assert pin == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}, name
    target = z.read('input/I164-status-field-correspondence-1.zip')
    assert len(target) == 38539130 and hashlib.sha256(target).hexdigest() == 'b51b313de9d03d3bc5eb8436d18e219b05f173144be46d51f090d5119b244504'
    with zipfile.ZipFile(io.BytesIO(target)) as embedded:
        assert len(embedded.namelist()) == 489 and embedded.testzip() is None
    checkpoint = json.loads(z.read('CHECKPOINT.json'))
    assert checkpoint['target']['entries'] == 489 and checkpoint['preservation']['admission'] is False
print(json.dumps({'archive': path.name, 'bytes': len(raw), 'entries': len(infos), 'sha256': hashlib.sha256(raw).hexdigest(), 'CRC': 'PASS', 'safe_exact_membership': 'PASS', 'manifest_hashes': 'PASS', 'embedded_target': 'PASS'}, sort_keys=True))
