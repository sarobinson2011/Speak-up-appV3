from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, zipfile, argparse

EXPECTED = (38786604, 552, '36e4dfd8199df3a9168e47416d1e2508a8868876170c3586734c5a714adadac9')
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def inspect(b, expected=None):
    z=zipfile.ZipFile(io.BytesIO(b)); infos=z.infolist(); names=[i.filename for i in infos]
    if expected: assert (len(b),len(names),hashlib.sha256(b).hexdigest())==expected
    assert len(names)==len(set(names)) and z.testzip() is None
    for i in infos:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
        assert str(p)==i.filename and not i.is_dir()
        assert stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
    entries={n:z.read(n) for n in names}
    manifests=[]
    for name,raw in entries.items():
        if name.endswith('MANIFEST.json'):
            m=json.loads(raw); prefix=name[:-len('MANIFEST.json')]
            if isinstance(m,dict) and 'members' in m: m=m['members']
            if isinstance(m,dict) and all(isinstance(v,dict) and 'sha256' in v and 'bytes' in v for v in m.values()):
                missing=[n for n in m if prefix+n not in entries]
                checked=[]
                for n,v in m.items():
                    if prefix+n in entries:
                        assert ident(entries[prefix+n])==v,(name,n)
                        checked.append(n)
                manifests.append({'path':name,'declared':len(m),'verified_present':len(checked),'absent':missing})
    if 'MANIFEST.json' in entries:
        m=json.loads(entries['MANIFEST.json'])
        if isinstance(m,dict) and 'members' in m:
            m=m['members']
        assert isinstance(m,dict),type(m)
        assert set(m)==set(entries)-{'MANIFEST.json'},(list(m)[:5],len(m),len(entries))
        assert all(ident(entries[n])==v for n,v in m.items())
    return entries, {'identity':ident(b),'entries':len(entries),'CRC':'PASS','safe_exact_membership':'PASS','manifests':manifests}
def extract(entries, root):
    root=Path(root); assert not root.exists(),root
    for n,b in entries.items():
        p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
def main():
    a=argparse.ArgumentParser(); a.add_argument('archive'); a.add_argument('output'); a.add_argument('--extract',action='append',default=[]); q=a.parse_args()
    entries,r=inspect(Path(q.archive).read_bytes(),EXPECTED)
    r['nested_archives']={}
    def nested(es,label):
        for n,b in es.items():
            if n.endswith('.zip'):
                ne,nr=inspect(b)
                r['nested_archives'][label+n]=nr
                nested(ne,label+n+'!/')
    nested(entries,'')
    for target in q.extract: extract(entries,target)
    p=Path(q.output); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'target':r['identity'],'entries':r['entries'],'nested_archives':len(r['nested_archives']),'result':'PASS'}))
if __name__=='__main__': main()
