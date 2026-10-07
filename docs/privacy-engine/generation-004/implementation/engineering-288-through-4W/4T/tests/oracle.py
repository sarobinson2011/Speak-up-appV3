"""Independent finite serializer: direct combinations, set union, tuple sort."""
import hashlib,itertools
HEADER=b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
def parse(raw):
 lines=raw.decode('ascii').splitlines();tag,n,m,f=lines.pop(0).split();assert tag=='LINKS';n,m,f=map(int,(n,m,f));names=lines[:n];assert len(names)==len(set(names))==n;lines=lines[n:];fixed=dict(tuple(map(int,l.split())) for l in lines[:f]);edges=[tuple(l.split()) for l in lines[f:]];assert len(edges)==m;return names,fixed,[(int(a),int(b),int(r),k) for a,b,r,k in edges]
def rows(raw):
 names,fixed,edges=parse(raw);s={(names[a],names[b],str(r).zfill(6),k) for a,b,r,k in edges}
 for a,b in itertools.combinations(range(len(names)),2):
  if a not in fixed or b not in fixed or fixed[a]==fixed[b]:s.add((names[a],names[b],'000000','EQUALS'))
 return sorted(s)
def serialize(raw):return HEADER+b''.join((str(i).zfill(6)+'\t'+'\t'.join(r)+'\n').encode('ascii') for i,r in enumerate(rows(raw),1))
def descriptor(names,fixed,edges):return (f'LINKS {len(names)} {len(edges)} {len(fixed)}\n'+'\n'.join(names)+'\n'+''.join(f'{i} {g}\n' for i,g in sorted(fixed.items()))+''.join(f'{a} {b} {r} {k}\n' for a,b,r,k in edges)).encode()
