"""Read-only archive verification and optional fresh extraction; no application runs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

def need(ok, why):
    if not ok:
        raise ValueError(why)

def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def read(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'NONREGULAR:' + str(path))
    return path.read_bytes()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    a = ap.parse_args()
    need(not os.path.lexists(a.output), 'EXTRACTION-OUTPUT-EXISTS')
    need(not a.output.absolute().is_relative_to('/tmp'), 'NO-TMP-OUTPUT')
    raw = read(a.archive)
    with zipfile.ZipFile(a.archive) as z:
        names = z.namelist()
        need(len(names) == len(set(names)), 'DUPLICATE-MEMBER')
        for row in z.infolist():
            p = Path(row.filename)
            need(not p.is_absolute() and '..' not in p.parts and not row.is_dir(), 'UNSAFE-MEMBER')
            need(stat.S_IFMT(row.external_attr >> 16) in (0, stat.S_IFREG), 'SPECIAL-MEMBER')
        need(z.testzip() is None, 'CRC')
        manifest = json.loads(z.read('MANIFEST.json'))
        need(set(names) == set(manifest) | {'MANIFEST.json'}, 'EXACT-MEMBERSHIP')
        for name, expected in manifest.items():
            need(identity(z.read(name)) == expected, 'MEMBER-HASH:' + name)
        a.output.mkdir(parents=True)
        for name in names:
            p = a.output / name
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('xb') as f:
                f.write(z.read(name))
    actual = {str(p.relative_to(a.output)) for p in a.output.rglob('*') if p.is_file()}
    need(actual == set(names), 'EXTRACTED-MEMBERSHIP')
    for name, expected in manifest.items():
        need(identity(read(a.output / name)) == expected, 'EXTRACTED-HASH:' + name)
    basis = json.loads(read(a.output / 'provenance/BASIS.json'))
    for label, ref in basis['archives'].items():
        p = a.output / ref['path']
        need(identity(read(p)) == {k: ref[k] for k in ('bytes', 'sha256')}, 'RECOVERY-DEPENDENCY:' + label)
        with zipfile.ZipFile(p) as z:
            need(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())), 'DEPENDENCY-CRC')
            m = json.loads(z.read('PACKAGE-MANIFEST.json'))
            need(set(z.namelist()) == set(m) | {'PACKAGE-MANIFEST.json'}, 'DEPENDENCY-MEMBERSHIP')
            for name, expected in m.items():
                need(identity(z.read(name)) == expected, 'DEPENDENCY-MEMBER-HASH')
    print(json.dumps({'status': 'PASS archive CRC, fresh extraction, exact membership, manifests and included recovery dependencies',
                      **identity(raw), 'entries': len(names), 'output': str(a.output.absolute()),
                      'application_execution': False, 'database_connections': 0}, sort_keys=True))

if __name__ == '__main__':
    main()
