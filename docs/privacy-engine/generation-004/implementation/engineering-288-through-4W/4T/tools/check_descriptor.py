#!/usr/bin/env python3
"""Metadata correspondence and analytical exact text byte counts; no pair stream."""
import argparse,collections,hashlib,json,resource,struct,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
H=b'link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def wire(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def ordinal_bytes(a,b):
 # Inclusive integer ordinal range; minimum six decimal digits.
 total=0
 while a<=b:
  width=max(6,len(str(a)));end=min(b,10**width-1);total+=(end-a+1)*width;a=end+1
 return total

def analytical(names,fixed,edges):
 n=len(names)
 # Hash-safe exact tuples, not a hash-only uniqueness decision.
 unique=set(map(tuple,edges));assert len(unique)<=len(edges)
 lex=sorted(range(n),key=names.__getitem__);rank=[0]*n
 for j,i in enumerate(lex):rank[i]=j
 lengths=list(map(len,names));suffix=sum(lengths);counts=[0]*n;base=[0]*n;potcounts=[0]*n
 for i in range(n):
  suffix-=lengths[i];cnt=n-i-1;pos=rank[i];counts[pos]=potcounts[pos]=cnt;base[pos]=cnt*(lengths[i]+17)+suffix
 for i,g in fixed:
  for j,k in fixed:
   if i<j and g!=k:
    pos=rank[i];counts[pos]-=1;potcounts[pos]-=1;base[pos]-=lengths[i]+lengths[j]+17
 for a,b,order,kind in unique:
  pos=rank[a];counts[pos]+=1;base[pos]+=lengths[a]+lengths[b]+6+len(kind)+5
 rows=0;byte_count=len(H);prefix=bytearray(struct.pack('>QQ',0,byte_count));boundaries=[]
 for j in range(n):
  count=counts[j];body=base[j]+ordinal_bytes(rows+1,rows+count);rows+=count;byte_count+=body;prefix.extend(struct.pack('>QQ',rows,byte_count))
  if j%64==63 or j==n-1:boundaries.append([j+1,rows,byte_count])
 return prefix,rows,byte_count,len(unique),sum(potcounts)

def run(model_path,output=R):
 begin=time.monotonic();pin=json.loads((R/'bindings/ACTIVE-IDENTITIES.json').read_bytes())['model_sha256'];assert sha(model_path)==pin
 m=json.loads(model_path.read_bytes());tokens=m['tokens'];edges=m['structural_edges'];names=[t['id'] for t in tokens];n=len(names)
 assert n==426984 and len(set(names))==n and all(t['index']==i for i,t in enumerate(tokens))
 assert all(s and all(33<=ord(c)<=126 for c in s) for s in names)
 fixed=[];groups={}
 for i,t in enumerate(tokens):
  assert type(t['arbitrary']) is bool
  if not t['arbitrary']:fixed.append((i,groups.setdefault(t['symbolic_digest'],len(groups))))
 with (R/'inputs/links.txt').open('rb') as f:
  assert f.readline()==f'LINKS {n} {len(edges)} {len(fixed)}\n'.encode()
  for name in names:assert f.readline()==(name+'\n').encode()
  for i,g in fixed:assert f.readline()==f'{i} {g}\n'.encode()
  for a,b,r,k in edges:
   assert 0<=a<n and 0<=b<n and 1<=r<=999999
   assert f.readline()==f'{a} {b} {r} {k}\n'.encode()
  assert f.read()==b''
 prefix,rows,byte_count,unique_count,potential_count=analytical(names,fixed,edges)
 assert potential_count==m['equality_stream']['rows']==91157453467
 assert rows==unique_count+91157453467
 output.mkdir(parents=True,exist_ok=True);(output/'inputs').mkdir(exist_ok=True);(output/'results').mkdir(exist_ok=True)
 (output/'inputs/prefix.bin').write_bytes(prefix)
 totals={'format':'CP4T-EXACT-TEXT-METADATA-1','candidate_model_sha256':pin,'selected_contract_sha256':json.loads((R/'bindings/ACTIVE-IDENTITIES.json').read_bytes())['selected_contract_sha256'],'descriptor_sha256':sha(R/'inputs/links.txt'),'tokens':n,'raw_structural_rows':len(edges),'unique_structural_rows':unique_count,'structural_duplicates_removed':len(edges)-unique_count,'potential_rows':potential_count,'total_rows':rows,'serialized_bytes_analytical':byte_count,'header_hex':H.hex(),'prefix_table':{'format':'one U64BE cumulative rows, U64BE cumulative bytes per lexical from-token boundary; boundary 0 includes header','entries':n+1,'bytes':len(prefix),'sha256':hashlib.sha256(prefix).hexdigest()},'full_stream_sha256':None,'basis':'Exact descriptor-to-candidate correspondence for every token/fixed-group/structural row; sum token lengths for all later original indices, remove only unequal fixed/fixed terms, add unique structural tuples, then exact ordinal-digit ranges. No potential-pair enumeration.','potential_pairs_enumerated':False,'qualification_established':False,'seconds':time.monotonic()-begin,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (output/'results/DESCRIPTOR-CORRESPONDENCE.json').write_bytes(wire(totals))
 print(json.dumps(totals))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--model',type=Path,required=True);a.add_argument('--output',type=Path,default=R);x=a.parse_args();run(x.model,x.output)
