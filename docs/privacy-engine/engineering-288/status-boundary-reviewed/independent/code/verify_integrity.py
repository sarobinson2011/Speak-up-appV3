"""Independent byte/membership checks. Does not execute supplied application code."""
import argparse, hashlib, io, json, stat, zipfile
from pathlib import Path, PurePosixPath

EXPECTED = {'bytes': 4269431, 'sha256': '983e8aa849be387c4f92a54953fd24e2271bb090a01a0fb589230f0edad53185'}

def ident(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def archive(raw, expected=None):
    if expected is not None: assert ident(raw) == expected
    z = zipfile.ZipFile(io.BytesIO(raw)); names = z.namelist()
    assert len(names) == len(set(names)) and z.testzip() is None
    for info in z.infolist():
        p = PurePosixPath(info.filename)
        assert not p.is_absolute() and '..' not in p.parts and str(p) == info.filename and '\\' not in info.filename
        assert not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG)
    m = json.loads(z.read('MANIFEST.json'))['members']
    assert set(names) == set(m) | {'MANIFEST.json'}
    for name, pin in m.items(): assert ident(z.read(name)) == pin, name
    return z, {'identity': ident(raw), 'entries': len(names), 'crc': 'PASS', 'safe_exact_membership': 'PASS', 'member_hashes': len(m)}

def main():
    p = argparse.ArgumentParser(); p.add_argument('archive'); p.add_argument('root'); p.add_argument('dependency_directory'); p.add_argument('parent_archive'); p.add_argument('output'); a = p.parse_args()
    root = Path(a.root); dep = Path(a.dependency_directory)
    z, result = archive(Path(a.archive).read_bytes(), EXPECTED); assert len(z.infolist()) == 463
    for n in z.namelist(): assert (root/n).read_bytes() == z.read(n), n
    assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} == set(z.namelist())
    dependencies = json.loads(z.read('provenance/dependencies.json')); result['dependency_archives'] = {}
    for key, fn in [('adoption','I164-status-contract-adoption-1.zip'), ('launcher5002','I164-launcher-5002-review(1).zip')]:
        d, meta = archive((dep/fn).read_bytes(), dependencies[key]); result['dependency_archives'][key] = meta
        members = ['CONTRACT-draft-1.txt','DECISION.json'] if key == 'adoption' else d.namelist()
        prefix = 'contract/' if key == 'adoption' else 'retained/launcher/'
        for n in members: assert z.read(prefix+n) == d.read(n)
        meta['original_members_matched'] = len(members)
    pins = json.loads(z.read('provenance/dependency-pins.json')); basis = json.loads(z.read('provenance/basis-pins.json'))
    allpins = {**pins, **{'basis/'+n: v for n,v in basis['members'].items()}}
    for n,v in allpins.items(): assert ident(z.read(n)) == v
    changes = json.loads(z.read('CHANGED-IDENTITIES.json'))
    assert changes['existing_original_files_modified'] == [] and changes['unchanged_reference_files'] == allpins
    for n,v in changes['new_files'].items(): assert ident(z.read(n)) == {k:v[k] for k in ('bytes','sha256')}
    assert set(changes['new_files']) | set(allpins) | {'MANIFEST.json','CHANGED-IDENTITIES.json'} == set(z.namelist())
    result['unchanged_reference_members'] = len(allpins)
    # Reuse predecessor byte authority; inspect archive only, never run a prior review.
    raw = Path(a.parent_archive).read_bytes()
    assert ident(raw) == {'bytes':77270588,'sha256':'1e0bbb0498e46da537aad3a2e0af2781607d9cbee10043e2a685c4efff310204'}
    parent = zipfile.ZipFile(io.BytesIO(raw)); assert parent.testzip() is None
    cr = parent.read('inputs/candidate.zip'); assert ident(cr) == basis['candidate_archive']
    candidate = zipfile.ZipFile(io.BytesIO(cr)); assert candidate.testzip() is None
    matched=[]
    for n in z.namelist():
        if n.startswith('retained/candidate/'):
            src=n.removeprefix('retained/candidate/'); assert z.read(n)==candidate.read(src); matched.append(n)
        if n.startswith('basis/'):
            src=n.removeprefix('basis/'); assert z.read(n)==candidate.read(src); matched.append(n)
    result['candidate_member_matches'] = matched
    result['parent_identity_reused'] = ident(raw)
    result['candidate_identity'] = ident(cr)
    result['predecessor_manifest_checks'] = {}
    for which in ('candidate','draft'):
        raw_tree=parent.read('inputs/'+which+'.zip'); tree=zipfile.ZipFile(io.BytesIO(raw_tree))
        assert tree.testzip() is None and len(tree.namelist())==len(set(tree.namelist()))
        table=json.loads(z.read('retained/launcher/provenance/'+which+'-members.json'))
        assert set(tree.namelist())==set(table)|{'RECOVERY-MANIFEST.json'}
        for n,pin in table.items(): assert ident(tree.read(n))==pin,n
        result['predecessor_manifest_checks'][which]={'archive':ident(raw_tree),'members':len(table),'all_exact':True}
        if which=='draft':assert tree.read('source-only/scope/remaining-obligations.json')==z.read('retained/remaining-obligations.json')
    runtime=json.loads(z.read('retained/launcher/provenance/runtime-layout.json'))
    table=json.loads(z.read('retained/launcher/provenance/candidate-members.json'))
    for destination,source in runtime.items(): assert ident(candidate.read(source))==table[source]
    result['runtime_source_map']={'members':len(runtime),'source_bytes_verified':True,'recovered_runtime_execution':False}
    # The O01-O11 table has already been reviewed. Authenticate bytes and IDs only.
    obligations=json.loads(z.read('retained/remaining-obligations.json'))
    ids=[]
    def walk(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k == 'id' and isinstance(x,str) and x.startswith('O') and len(x)==3: ids.append(x)
                walk(x)
        elif isinstance(v,list):
            for x in v: walk(x)
    walk(obligations)
    result['obligation_ids']=sorted(set(ids))
    assert result['obligation_ids']==['O%02d'%i for i in range(1,12)]
    result['historical_evidence_scope']='Exact retained bytes; no historical execution or missing frames recreated'
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':'PASS','entries':result['entries'],'reference_members':len(allpins),'candidate_matches':len(matched)}))

if __name__ == '__main__': main()
