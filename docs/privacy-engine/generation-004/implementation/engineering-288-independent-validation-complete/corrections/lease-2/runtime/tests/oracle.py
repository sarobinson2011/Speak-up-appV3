"""Independent finite set + TSV oracle. Does not import either native implementation."""
import hashlib,itertools,json
from pathlib import Path
HEADER=b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
def digest(b):return hashlib.sha256(b).hexdigest()
def entry(p):return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}
def make(root):
 root=Path(root);root.mkdir(parents=True,exist_ok=True)
 names=['z.last','a.first','q.$record','m.middle','b.fixed','x.free']
 fixed={0:0,1:1,2:0,4:2}
 edges=[(1,0,1,'CHILD'),(0,1,2,'PARENT'),(2,2,1,'SELF'),(1,0,1,'CHILD'),(2,4,9,'USES')]
 structural={(names[a],names[b],f'{r:06d}',k) for a,b,r,k in edges}
 potential={(names[a],names[b],'000000','EQUALS') for a,b in itertools.combinations(range(len(names)),2) if a not in fixed or b not in fixed or fixed[a]==fixed[b]}
 required=sorted(structural|potential)
 text=HEADER+b''.join(('\t'.join((f'{i:06d}',*r))+'\n').encode() for i,r in enumerate(required,1))
 desc=f'LINKS {len(names)} {len(edges)} {len(fixed)}\n'+''.join(x+'\n' for x in names)+''.join(f'{i} {g}\n' for i,g in fixed.items())+''.join(f'{a} {b} {r} {k}\n' for a,b,r,k in edges)
 (root/'descriptor.txt').write_text(desc);(root/'complete.tsv').write_bytes(text)
 (root/'model.json').write_text(json.dumps({'laboratory_only':True,'names':names,'fixed':fixed,'structural':edges},sort_keys=True)+'\n')
 (root/'contract.json').write_text('{"laboratory_only":true,"contract":"small-static-links-oracle-v1"}\n')
 return {'root':root,'text':text,'structural':len(structural),'potential':len(potential),'rows':len(required),'required':required}
def manifest(f,kind='deterministic-laboratory-emitter',data=None,expected=None):
 root=f['root'];src={'kind':kind}
 if kind=='immutable-laboratory-file':
  (root/'supplied.tsv').write_bytes(f['text'] if data is None else data);src['file']=entry(root/'supplied.tsv')
 text=f['text'] if data is None else data
 return {'format':'CP4V-BYTE-SOURCE-1','model':entry(root/'model.json'),'contract':entry(root/'contract.json'),'descriptor':entry(root/'descriptor.txt'),'source':src,'expected':expected or {'bytes':len(text),'sha256':digest(text)},'serialization':'S90-FCR-S70-STATIC-LINKS-TSV','laboratory_only':True}
def rows_wire(rows):return HEADER+b''.join(('\t'.join((f'{i:06d}',*r))+'\n').encode() for i,r in enumerate(rows,1))
