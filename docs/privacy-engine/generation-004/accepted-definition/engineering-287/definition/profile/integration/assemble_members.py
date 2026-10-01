"""Fresh implementation of S71 member serialization; executes no historical code.
These two deterministic members supply bytes, not source ownership/admission.
"""
from pathlib import Path
import csv,json,re,hashlib,unicodedata,struct
O=Path(__file__).resolve().parents[2]
P=O/'profile/fragments'
SCALARS='profile-identifier profile-version governing-successor-generation governing-mapping-identifier profile-sha256-algorithm projection-component-count definition-count equivalence-definition-id material-conflict-definition-id applicability-definition-id determination-dependency-definition-id comparison-timing-rule execution-gate commitment-gate recovery-definition-id privacy-classification observability-classification'.split()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
def text(b):
 s=b.decode('utf-8')
 if not s.endswith('\n') or s.endswith('\n\n') or '\r' in s or s.startswith('\ufeff') or unicodedata.normalize('NFC',s)!=s or any(l.endswith((' ','\t')) for l in s.splitlines()):raise ValueError('noncanonical text')
 return s
def rows(name):return list(csv.DictReader(text((P/name).read_bytes()).splitlines(),delimiter='\t'))
def parse(s):
 tokens=re.findall(r'[A-Za-z0-9._:#-]+|[(),]',s)
 if ''.join(tokens)!=s:raise ValueError('expression tokens')
 pos=0
 def item():
  nonlocal pos
  name=tokens[pos];pos+=1
  if pos==len(tokens) or tokens[pos]!='(':return name
  pos+=1;args=[]
  if tokens[pos]!=')':
   while True:
    args.append(item())
    if tokens[pos]!=',':break
    pos+=1
  if tokens[pos]!=')':raise ValueError('expression closing')
  pos+=1;return [name,*args]
 value=item()
 if pos!=len(tokens):raise ValueError('expression trailing')
 return value

def member_bytes():
 scalars=[line.split('\t') for line in text((P/'scalars.tsv').read_bytes()).splitlines()]
 if [r[0] for r in scalars]!=SCALARS or any(len(r)!=2 for r in scalars):raise ValueError('scalar order')
 st=dict(scalars);defs=rows('definitions.tsv');types=rows('types.tsv');comps=rows('candidate-components.tsv');fields=rows('fields.tsv');entry=json.loads((P/'entry.json').read_bytes())
 if st['definition-count']!=f'{len(defs):06}' or st['projection-component-count']!=f'{len(comps):06}':raise ValueError('count')
 projection=(P/'BOUNDED-NOT-ADMITTED-projection.tsv').read_bytes();recovery=(P/'recovery.tsv').read_bytes();text(projection);text(recovery)
 body=''.join(k+': '+v+'\n' for k,v in scalars).encode()+projection+recovery
 ty=[]
 for t in types:
  children=[] if t['kind']=='PRIMITIVE' else [t['element_type_id']] if t['kind']=='SET' else t['field_type_ids'].split(',')
  ty.append([t['type_id'],[t['kind'],children]])
 ds=[{'id':d['definition_id'],'inputs':[] if d['input_type_ids']=='NONE' else d['input_type_ids'].split(','),'output':d['output_type_id'],'expression':parse(d['expression']),'kind':d['kind'],'source':d['source_id'],'anchor':d['source_anchor']} for d in defs]
 mapping={'id':'component_id','represented':'represented_type_id','canonical':'canonical_type_id','decoder':'representation_decoder_definition_id','canonicalizer':'canonicalization_definition_id','normalizer':'normalization_definition_id','available':'availability_condition_definition_id','valid':'validity_condition_definition_id','authenticated':'authentication_definition_id','source':'authority_source_id','anchor':'authority_anchor'}
 cs=[{k:c[v] for k,v in mapping.items()} for c in comps]
 fs=[{'id':f['field_id'],'type':f['type_id'],'equality':f['equality_definition_id'],'source':f['source_id'],'anchor':f['source_anchor']} for f in fields]
 if entry['groups']!=[]:raise ValueError('nonempty group schema requires governing declaration translation')
 program={'types':ty,'definitions':ds,'components':cs,'fields':fs,'root_definition':entry['root_definition'],'root_fields':entry['root_fields'],'groups':entry['groups']}
 return body,canonical(program)

def encode_container(members):
 """Transport framing only; never call this a validated profile or admitted mapping."""
 if list(members)!=['SOURCE-OWNED-BODY','EXPRESSION-PROGRAM','PRIVACY'] or any(not isinstance(b,bytes) or not b for b in members.values()):raise ValueError('exact nonempty member set required')
 def lp(b):return struct.pack('>Q',len(b))+b
 return b'PE-TSE-IMMUTABLE-PROFILE-V1\n'+b''.join(lp(n.encode('ascii'))+lp(b) for n,b in members.items())
def decode_container(raw):
 magic=b'PE-TSE-IMMUTABLE-PROFILE-V1\n'
 if not isinstance(raw,bytes) or not raw.startswith(magic):raise ValueError('container header')
 pos=len(magic)
 def lp():
  nonlocal pos
  if len(raw)-pos<8:raise ValueError('truncated length')
  size=int.from_bytes(raw[pos:pos+8],'big');pos+=8
  if size>len(raw)-pos:raise ValueError('truncated member')
  b=raw[pos:pos+size];pos+=size;return b
 out={}
 for expected in ('SOURCE-OWNED-BODY','EXPRESSION-PROGRAM','PRIVACY'):
  if lp()!=expected.encode():raise ValueError('member order/name')
  b=lp()
  if not b:raise ValueError('empty member')
  out[expected]=b
 if pos!=len(raw):raise ValueError('trailing container bytes')
 return out

def write_or_verify():
 body,program=member_bytes();root=O/'profile/integration'
 for name,b in [('SOURCE-OWNED-BODY.txt',body),('EXPRESSION-PROGRAM.json',program)]:
  p=root/name
  if p.exists():assert p.read_bytes()==b,'member regeneration mismatch: '+name
  else:p.write_bytes(b)
 report={'status':'TWO-MEMBERS-CONSTRUCTED','members':[{'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for name,b in [('SOURCE-OWNED-BODY',body),('EXPRESSION-PROGRAM',program)]],'governing_privacy_member':None,'outer_profile_sha256':None,'profile_admitted':False}
 (O/'verification/profile-integration.json').write_bytes(canonical(report));return report
if __name__=='__main__':
 write_or_verify();print('PASS — source-owned body and expression-program members regenerated exactly.')
