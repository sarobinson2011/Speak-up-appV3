# PE-G4-SOURCE-S88 — canonical profile integration construction

Unpublished successor construction under standing authorization. This defines a representation for the already authorized G4 policies; it adds no public-linkage exception, provider, actor, source appointment or occurrence fact. The inherited three-member outer container, source-owned body, expression program and signed V2 evidence preimages remain unchanged.

<a id="serialization"></a>
## serialization

The unpublished G4 PRIVACY member MUST use the exact PE-G4-PRIVACY-PROFILE-V2 canonical declaration and procedure binding specified here; the earlier integration candidate MUST NOT be substituted as a governing member.

<a id="authority"></a>
## authority

The PRIVACY member MUST bind the exact external source-appointed evidence authority; missing or mismatched appointment inputs MUST prevent construction of production outer-profile bytes, and structural equality MUST NOT be represented as independent appointment validation.

<a id="admission"></a>
## admission

Successful serialization MUST NOT grant admission; source completeness, complete observer/coalition evidence, exact component/composition scope, existing signed V2 preimages and all S83/S84/S86/S87 protections MUST remain required.

## Exact representation and boundary

The new PRIVACY payload is canonical JSON: sorted object keys, compact separators, ASCII escapes, exactly one terminal LF. Ordered arrays preserve declaration/operation order. The exact fields and constructors below are normative candidate declarations. The format binds component identity/type/mode, the complete supplied static model (surfaces, relations, both contexts, structural edges and the exact complete equality stream descriptor), the active policy source identifiers, the exact source/implementation byte digests, evidence-contract identifiers and the exact appointment record. Candidate-only status markers and unavailable future occurrence/evidence placeholders are excluded from this immutable member.

The prior PE-TSE-PRIVACY-PROFILE-CONSTRUCTION-V1 register cannot represent the extra G4 declaration and observer/provenance surfaces without extension. PE-G4-PRIVACY-PROFILE-V2 is therefore an explicit new unpublished member grammar, not an issuer extra attached to the old validator. A final G4 admission validator must independently regenerate this format and use the same freshly rebuilt model for all checks. Merely accepting the format tag, verifying byte hashes, obtaining an arbitrary signature or passing synthetic fixtures is insufficient.

The SOURCE-OWNED-BODY remains exactly the 17 ordered scalar lines, canonical projection TSV and exact 21-row recovery TSV. EXPRESSION-PROGRAM retains the inherited dataclass field names and parsed expression-tree shape; no host calls, additional fields or altered execution semantics are introduced. These two members can be materialized before appointment. The outer container remains PE-TSE-IMMUTABLE-PROFILE-V1 plus LF, followed by L64 name and L64 bytes for SOURCE-OWNED-BODY, EXPRESSION-PROGRAM and PRIVACY in that order. No evidence bundle becomes a fourth member.

The appointment shape check is not proof of authority. Trusted appointment input must originate outside the issuer's profile/evidence from the competent source. No default appointment, key, signature or production profile is provided in this package. The source/evidence admission implementation is a distinct unfinished integration obligation; this serializer does not pretend to discharge it. Tests use only explicitly synthetic appointment shapes and retain no resulting full-profile bytes/digest.

## Exact fresh member constructor

```python
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
```

## Exact fresh PRIVACY/container constructor

```python
"""S88 canonical extended PRIVACY member constructor. Not an admission validator.
The governing appointment must be provided externally; no dummy production default.
"""
from pathlib import Path
import json,hashlib,re,runpy
O=Path(__file__).resolve().parents[2]
A=runpy.run_path(str(Path(__file__).with_name('assemble_members.py')))
POLICY_FILES=['privacy/observation_correlation.py','privacy/cross_role_correlation.py','privacy/cross_role_uniqueness.py','privacy/expand_privacy.py','profile/integration/privacy_member.py','profile/integration/assemble_members.py','profile/integration/evidence_auth.py']
def appointment_shape(value):
 keys={'authority_id','algorithm','public_key','key_fingerprint_sha256','owner_source_id','owner_anchor'}
 if not isinstance(value,dict) or set(value)!=keys:raise ValueError('INVALID-EVIDENCE-AUTHORITY: exact appointment required')
 if value['algorithm']!='ED25519-RFC8032':raise ValueError('appointment algorithm')
 for k in ('authority_id','owner_source_id','owner_anchor'):
  if not isinstance(value[k],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*',value[k]) or value[k]=='PE-TSE-SET':raise ValueError('appointment identity')
 if not isinstance(value['public_key'],str) or not re.fullmatch('[0-9a-f]{64}',value['public_key']):raise ValueError('appointment key')
 if hashlib.sha256(bytes.fromhex(value['public_key'])).hexdigest()!=value['key_fingerprint_sha256']:raise ValueError('appointment fingerprint')
 return value

def declaration():
 # The model has been regenerated by verify_expansion before integration.
 raw=(O/'privacy/expanded/PRIVACY.candidate.json').read_bytes();model=json.loads(raw)
 if A['canonical'](model)!=raw:raise ValueError('noncanonical model')
 if model['format']!='PE-G4-PRIVACY-INTEGRATION-CANDIDATE-V1':raise ValueError('model format')
 for path,digest in model['input_sha256'].items():
  if hashlib.sha256((O/path).read_bytes()).hexdigest()!=digest:raise ValueError('model input mismatch')
 # Candidate status and unavailable future evidence are not actual immutable observations.
 static={k:model[k] for k in ('surfaces','relations','tokens','structural_edges','equality_stream','actor_graph_policy')}
 components=A['rows']('candidate-components.tsv')
 return {'format':'PE-G4-PRIVACY-PROFILE-V2','profile_id':'PE-G4-TSE-PROFILE-000001-V0001','format_source':'PE-G4-SOURCE-S88','format_source_sha256':hashlib.sha256((O/'sources/PE-G4-SOURCE-S88.md').read_bytes()).hexdigest(),'policy_sources':['PE-G4-SOURCE-S83','PE-G4-SOURCE-S84','PE-G4-SOURCE-S86','PE-G4-SOURCE-S87'],'components':[{'id':c['component_id'],'mode':c['binding_mode'],'canonical_type':c['canonical_type_id'],'necessity':'PREDICATE-INPUT','privacy':c['privacy_class']} for c in components],'public_output':False,'declaration_input_sha256':model['input_sha256'],'procedures_sha256':{p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in POLICY_FILES},'model':static,'evidence_contract':{'signature_domain':'PE-TSE-PRIVACY-EVIDENCE-V2\n','object_digest_domain':'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n','appointment_comparison':'EXACT-EXTERNAL-SOURCE-APPOINTMENT','bundles':['ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'],'kinds':['ADMISSION-COMPONENT','ADMISSION-COMPOSITION'],'admission_gate':'FULL-INDEPENDENT-SOURCE-EVIDENCE-AND-MODEL-VALIDATION-REQUIRED'}}

def member(appointment,trusted_appointment):
 appointment_shape(appointment);appointment_shape(trusted_appointment)
 if appointment!=trusted_appointment:raise ValueError('INVALID-EVIDENCE-AUTHORITY: external appointment mismatch')
 payload=declaration();payload['appointment']=appointment
 return A['canonical'](payload)

def construct_outer(appointment,trusted_appointment):
 privacy=member(appointment,trusted_appointment);body,program=A['member_bytes']()
 return A['encode_container']({'SOURCE-OWNED-BODY':body,'EXPRESSION-PROGRAM':program,'PRIVACY':privacy})

def validate_serialization(raw,appointment,trusted_appointment):
 """Exact regeneration only. No signature/appointment truth or admission claim."""
 decoded=A['decode_container'](raw);expected=construct_outer(appointment,trusted_appointment)
 if raw!=expected:raise ValueError('PROFILE-DIGEST-MISMATCH')
 return {'serialization':'EXACT','member_count':len(decoded),'independent_authority_established':False,'privacy_evidence_verified':False,'profile_admitted':False}
if __name__=='__main__':
 # No production outer bytes can be generated from the inputs actually available.
 try:construct_outer(None,None)
 except ValueError as e:print('BOUNDARY — '+str(e))
 else:raise AssertionError('missing appointment accepted')
```

## Exact V2 evidence authentication subroutine

This independently authored subroutine preserves the inherited V2 signed and object-digest preimages. Its expected evidence/tokens/links bytes must come from the governing regenerated model and independently computed result/scope records, never an issuer cache. Authentication of those bytes alone is not validation of source truth, observer completeness or graph policy. The three required bundle scopes remain distinct. Transport tests use ephemeral in-memory keys and non-production payloads; no key, signed fixture, appointment or full profile is stored.

```python
"""Fresh exact V2 four-file evidence authentication. Not source appointment/admission.
Expected bytes must come from independent governing model regeneration, never issuer caches.
"""
from pathlib import Path
import runpy,hashlib,re
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
NAMES=('evidence.tsv','tokens.tsv','links.tsv','signature.txt')
def h(b):return hashlib.sha256(b).hexdigest()
def object_digest(files):return h(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(len(files[n]).to_bytes(8,'big')+files[n] for n in NAMES))
def authenticate(appointment,trusted,files,digest,expected):
 """expected exact evidence/tokens/links bytes include scope, profile and computed results."""
 def fail(code):return {'result':'FAIL','failure':code,'source_authority_established':False,'profile_admitted':False}
 try:
  P['appointment_shape'](appointment);P['appointment_shape'](trusted)
  if appointment!=trusted:raise ValueError('appointment mismatch')
 except (ValueError,TypeError):return fail('INVALID-EVIDENCE-AUTHORITY')
 if not isinstance(files,dict) or set(files)!=set(NAMES) or not all(isinstance(x,bytes) for x in files.values()):return fail('MISSING-EVIDENCE')
 try:
  sig=files['signature.txt'].decode('ascii')
  prefix=trusted['authority_id']+' '
  if not sig.startswith(prefix) or not re.fullmatch('[0-9a-f]{128}\n',sig[len(prefix):]):raise ValueError('signature grammar')
  payload=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+files['evidence.tsv']+files['tokens.tsv']+files['links.tsv']
  Ed25519PublicKey.from_public_bytes(bytes.fromhex(trusted['public_key'])).verify(bytes.fromhex(sig[len(prefix):-1]),payload)
 except Exception:return fail('INVALID-EVIDENCE-AUTHENTICATION')
 if object_digest(files)!=digest:return fail('INVALID-EVIDENCE-DIGEST')
 if not isinstance(expected,dict) or set(expected)!=set(NAMES[:-1]) or any(not isinstance(v,bytes) for v in expected.values()):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
 if any(files[k]!=expected[k] for k in NAMES[:-1]):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
 return {'result':'EXACT-EVIDENCE-BYTES-AUTHENTICATED','failure':'NONE','source_authority_established':False,'profile_admitted':False}
def authenticate_bundle(appointment,trusted,objects,expected_by_scope):
 scopes={'ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'}
 if not isinstance(objects,dict) or set(objects)!=scopes or not isinstance(expected_by_scope,dict) or set(expected_by_scope)!=scopes:return {'result':'FAIL','failure':'MISSING-EVIDENCE','profile_admitted':False}
 result={}
 for scope in sorted(scopes):
  item=objects[scope]
  if not isinstance(item,dict) or set(item)!={'files','object_sha256'}:return {'result':'FAIL','failure':'MISSING-EVIDENCE','profile_admitted':False}
  result[scope]=authenticate(appointment,trusted,item['files'],item['object_sha256'],expected_by_scope[scope])
 return {'result':'BUNDLE-AUTHENTICATED' if all(r['failure']=='NONE' for r in result.values()) else 'FAIL','scopes':result,'profile_admitted':False}
```
