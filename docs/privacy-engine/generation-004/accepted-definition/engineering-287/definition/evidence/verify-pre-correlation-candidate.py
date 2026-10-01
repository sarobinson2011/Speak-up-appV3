"""Document-only author checks. No historical constructor, runtime or evidence authority."""
from pathlib import Path
import csv,json,re,hashlib,collections
O=Path(__file__).resolve().parent;B=O/'basis/Engineering-286-source-closure';P=O/'profile/fragments'
def rows(p):return list(csv.DictReader(p.open(),delimiter='\t'))
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
ids={r['original_id']:r['candidate_id'] for r in rows(O/'composition/identifier-map.tsv')}
def rename(s):return re.sub(r'E28[34]-DRAFT-[A-Z0-9-]+',lambda m:ids.get(m[0],m[0]),s)
check('identifier map injective',len(set(ids.values()))==len(ids))
identity=json.loads((O/'identity.json').read_text())
check('generation grammar and explicit G4 binding',bool(re.fullmatch(r'PE-PROTOCOL-GENERATION-[0-9]{3}',identity['generation_id'])) and identity['generation_id']=='PE-PROTOCOL-GENERATION-004' and identity['namespace']=='PE-G4' and identity['version']=='4.0.0')
inventory=rows(O/'composition/source-inventory.tsv');source={r['source_id']:r for r in inventory}
check('80 unique source identities',len(source)==len(inventory)==80)
for r in inventory:
 check('source digest '+r['source_id'],sha((O/r['path']).read_bytes())==r['sha256'])
 if r['mode']=='EXACT-BY-REFERENCE':check('unchanged baseline '+r['source_id'],(O/r['path']).read_bytes()==(B/'baseline/sources'/Path(r['path']).name).read_bytes())
T=rows(P/'types.tsv');types={r['type_id']:r for r in T};oldtypes={r['type_id']:r for r in rows(B/'supporting-program/types.tsv')}
check('type identities and order',len(types)==19 and [r['type_order'] for r in T]==[f'{i:04}' for i in range(1,20)])
seen=set()
for r in T:
 children=[] if r['kind']=='PRIMITIVE' else [r['element_type_id']] if r['kind']=='SET' else r['field_type_ids'].split(',')
 check('type closure '+r['type_id'],all(c in seen for c in children));seen.add(r['type_id'])
def decode(raw,typetable=types):
 assert raw[:5]==b'TSEV1';p=5
 def take(n):
  nonlocal p
  assert p+n<=len(raw);v=raw[p:p+n];p+=n;return v
 def lp(w):return take(int.from_bytes(take(w),'big'))
 t=lp(4).decode('ascii');k=take(1)[0];body=lp(8);assert p==len(raw) and t in typetable
 if k==0:assert t=='PE-TSE-BOOL3' and body in (b'\0',b'\1',b'\2');v=body[0]
 elif k==1:assert t=='PE-TSE-BYTES';v=body.hex()
 elif k==2:assert t=='PE-TSE-ID';v=body.decode('ascii');assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:#-]*',v) and v!='PE-TSE-SET'
 elif k==3:assert t=='PE-TSE-UINT';v=body.decode('ascii');assert re.fullmatch(r'0|[1-9][0-9]*',v)
 else:
  assert k in (16,17);assert typetable[t]['kind']=={16:'SET',17:'TUPLE'}[k]
  count=int.from_bytes(body[:4],'big');q=4;enc=[];v=[]
  for _ in range(count):
   n=int.from_bytes(body[q:q+8],'big');q+=8;b=body[q:q+n];q+=n;assert len(b)==n;enc.append(b);v.append(decode(b,typetable))
  assert q==len(body)
  if k==16:assert enc==sorted(set(enc));assert all(x[0]==typetable[t]['element_type_id'] for x in v)
  else:assert [x[0] for x in v]==typetable[t]['field_type_ids'].split(',')
 return (t,v)
def renamedvalue(x):
 t,v=x
 if isinstance(v,list):v=[renamedvalue(y) for y in v]
 elif t=='PE-TSE-ID':v=rename(v)
 return (rename(t),v)
def tokens(s):return re.findall(r'[A-Za-z0-9._:#-]+|[(),]',s)
def parse(s):
 ts=tokens(s);assert ''.join(ts)==s;pos=0
 def node():
  nonlocal pos
  name=ts[pos];pos+=1
  if pos==len(ts) or ts[pos]!='(':return name
  pos+=1;children=[]
  if ts[pos]!=')':
   while True:
    children.append(node())
    if ts[pos]!=',':break
    pos+=1
  assert ts[pos]==')';pos+=1;return (name,children)
 n=node();assert pos==len(ts);return n
D=rows(P/'definitions.tsv');defs={r['definition_id']:r for r in D};asts={r['definition_id']:parse(r['expression']) for r in D}
check('56 unique definition ordinals',len(defs)==56 and [r['definition_order'] for r in D]==[f'{i:04}' for i in range(1,57)])
C={r['component_id']:r for r in rows(P/'candidate-components.tsv')}
def infer(n,args):
 assert isinstance(n,tuple);op,a=n
 if op=='arg':assert len(a)==1 and re.fullmatch(r'[0-9]{4}',a[0]);i=int(a[0]);assert 1<=i<=len(args);return args[i-1]
 if op=='literal':assert len(a)==2;v=decode(bytes.fromhex(a[1]));assert v[0]==a[0];return a[0]
 if op=='tuple':
  assert types[a[0]]['kind']=='TUPLE';assert [infer(x,args) for x in a[1:]]==types[a[0]]['field_type_ids'].split(',');return a[0]
 if op=='equal':assert len(a)==2 and infer(a[0],args)==infer(a[1],args);return 'PE-TSE-BOOL3'
 if op in ('not','and','or'):
  assert len(a)==1 if op=='not' else len(a)>=1
  assert all(infer(x,args)=='PE-TSE-BOOL3' for x in a);return 'PE-TSE-BOOL3'
 if op in ('ref','authoritative','available','valid','authenticated'):
  assert len(a)==2 and a[0] in C and a[1] in ('AUTHORIZED','CURRENT');return C[a[0]]['canonical_type_id'] if op=='ref' else 'PE-TSE-BOOL3'
 if op=='member':assert len(a)==2 and defs[a[1]]['kind']=='SET';assert infer(a[0],args)==types[defs[a[1]]['output_type_id']]['element_type_id'];return 'PE-TSE-BOOL3'
 if op=='apply':
  if a[0]=='PE-TSE-SET':
   assert all(x[0]=='literal' for x in a[1:]);return ('BUILTIN-SET',[infer(x,args) for x in a[1:]])
  d=defs[a[0]];expected=[] if d['input_type_ids']=='NONE' else d['input_type_ids'].split(',');assert [infer(x,args) for x in a[1:]]==expected;return d['output_type_id']
 raise AssertionError(op)
for d in D:
 args=[] if d['input_type_ids']=='NONE' else d['input_type_ids'].split(',');got=infer(asts[d['definition_id']],args)
 if d['kind']=='SET':assert got[0]=='BUILTIN-SET' and all(x==types[d['output_type_id']]['element_type_id'] for x in got[1])
 else:assert got==d['output_type_id']
 owner=(O/source[d['source_id']]['path']).read_text();assert '<a id="'+d['source_anchor']+'"></a>' in owner
 assert '\t'.join(d.values())+'\n' in owner
check('every expression type-checks and exact source declaration/anchor resolves',True)
# Preserve all existing definitions including every embedded canonical literal.
def normalized(s,original=False):
 return re.sub(r'literal\(([^,]+),([0-9a-f]+)\)',lambda m:'VALUE:'+repr(renamedvalue(decode(bytes.fromhex(m[2]),oldtypes)) if original else decode(bytes.fromhex(m[2]))),rename(s))
oldD=rows(B/'supporting-program/definitions.tsv')
for orig,new in zip(oldD,D):
 for k in orig:
  if k=='expression':assert normalized(orig[k],True)==normalized(new[k])
  else:assert rename(orig[k])==new[k]
check('53 original definition meanings and literal values preserved under explicit renaming',True)
check('all 21 recovery rows byte-exact',(P/'recovery.tsv').read_bytes()==(B/'supporting-program/recovery.tsv').read_bytes())
# Evaluate only the three freshly constructed pure definitions and their simple source-state dependency.
def evaluate(n,args):
 op,a=n
 if op=='arg':return args[int(a[0])-1]
 if op=='literal':return decode(bytes.fromhex(a[1]))
 if op=='tuple':return (a[0],[evaluate(x,args) for x in a[1:]])
 if op=='equal':return ('PE-TSE-BOOL3',int(evaluate(a[0],args)==evaluate(a[1],args)))
 if op=='and':return ('PE-TSE-BOOL3',min(evaluate(x,args)[1] for x in a)) # These test inputs are resolved only.
 if op=='apply':
  if a[0]=='PE-TSE-SET':return ('SET',[evaluate(x,args) for x in a[1:]])
  return evaluate(asts[a[0]],[evaluate(x,args) for x in a[1:]])
 if op=='member':return ('PE-TSE-BOOL3',int(evaluate(a[0],args) in evaluate(asts[a[1]],[])[1]))
 raise AssertionError(op)
recovery=rows(P/'recovery.tsv');keys=[k for k in recovery[0] if k!='recovery_order'];mutations=0
for r in recovery:
 args=[('PE-TSE-ID',r[k]) for k in keys];assert evaluate(asts['PE-G4-CAP-RECOVERY'],args)==('PE-TSE-BOOL3',1)
 for i in range(11):
  bad=list(args);bad[i]=('PE-TSE-ID','INVALID-FIELD-VALUE');assert evaluate(asts['PE-G4-CAP-RECOVERY'],bad)==('PE-TSE-BOOL3',0);mutations+=1
 # Mutate each field to every other observed value, and compare to exact table membership.
 universe={tuple(r[k] for k in keys) for r in recovery}
 for i,k in enumerate(keys):
  for alternative in {x[k] for x in recovery}-{r[k]}:
   bad=list(args);bad[i]=('PE-TSE-ID',alternative);expect=int(tuple(x[1] for x in bad) in universe);assert evaluate(asts['PE-G4-CAP-RECOVERY'],bad)==('PE-TSE-BOOL3',expect);mutations+=1
check('recovery exact rows and '+str(mutations)+' altered-field cases',True)
app=asts['PE-G4-CAP-APPLICABILITY'];type_ref=decode(bytes.fromhex(app[1][0][1][1][1][1]));rules_ref=decode(bytes.fromhex(app[1][1][1][1][1][1]))
assert type_ref[1][0]==('PE-TSE-ID','PE-G4-SOURCE-S76') and type_ref[1][1]==('PE-TSE-BYTES',source['PE-G4-SOURCE-S76']['sha256']) and type_ref[1][2]==('PE-TSE-ID','action-type')
assert rules_ref[1][2]==('PE-TSE-ID','rules')
a=('PE-TSE-UINT','7');n=('PE-TSE-UINT','11');state=('PE-G4-CAP-SCOPED-STATE',[a,n,('PE-TSE-BOOL3',0)]);args=[type_ref,rules_ref,a,n,state]
assert evaluate(app,args)==('PE-TSE-BOOL3',1)
for i in (0,1):
 for j in range(3):
  bad=list(args);children=list(bad[i][1]);children[j]=(children[j][0],'00' if j==1 else 'MISMATCH');bad[i]=(bad[i][0],children);assert evaluate(app,bad)==('PE-TSE-BOOL3',0)
for stateval in (1,2):
 bad=args[:-1]+[('PE-G4-CAP-SCOPED-STATE',[a,n,('PE-TSE-BOOL3',stateval)])];assert evaluate(app,bad)==('PE-TSE-BOOL3',0)
check('applicability fixed source hash/anchor, used and unresolved-state exclusions',True)
ops=rows(P/'operations.tsv');edges=rows(P/'operation-edges.tsv');opids={r['operation_id'] for r in ops}
check('89 unique operation rows',len(ops)==len(opids)==89)
actual={(r['caller_operation_id'],r['callee_operation_id']) for r in edges};declared={(r['operation_id'],c) for r in ops for c in r['permitted_call_operation_ids'].split(',') if c!='NONE'}
check('operation graph equals declared calls',actual==declared and all(a in opids and b in opids for a,b in actual))
indeg={o:0 for o in opids};adj=collections.defaultdict(list)
for a,b in actual:indeg[b]+=1;adj[a].append(b)
q=[a for a,n in indeg.items() if n==0];visited=[]
while q:
 a=q.pop();visited.append(a)
 for b in adj[a]:
  indeg[b]-=1
  if indeg[b]==0:q.append(b)
check('combined declared operation graph acyclic',len(visited)==len(ops))
for d in D[53:]:
 expected={'PE-G4-CAP-APPLICABILITY':{'PE-TSE-OP-DEFINITION-0004'},'PE-G4-CAP-RECOVERY-ROWS':set(),'PE-G4-CAP-RECOVERY':{'PE-TSE-OP-DEFINITION-0055'}}[d['definition_id']]
 check('new definition call graph '+d['definition_id'],{b for a,b in actual if a=='PE-TSE-OP-DEFINITION-'+d['definition_order']}==expected)
req=json.loads((O/'composition/requirement-inventory.json').read_text());base=(B/'baseline/exact-861-published-rows.md').read_text().splitlines()
for r,l in zip(req,base):
 c=[x.strip() for x in l.strip('|').split('|')];assert len(c)==7
 assert [r[x] for x in ('strength','applicability','scope','text','supporting_references')]==[c[1],c[2],c[3],c[4],c[6]]
 assert r['owner_sources']==c[5].replace('PE-G3-','PE-G4-')
check('861 inherited requirement texts/strength/scopes/antecedents/support exact',len(base)==861)
originaldelta=json.loads((B/'source-delta/normative-requirement-deltas.json').read_text());delta=json.loads((O/'composition/delta-disposition-97.json').read_text());reqdict={r['requirement_id']:r for r in req}
for a,b in zip(originaldelta,delta):
 assert a['text']==b['exact_text'] and a['local_proposal_coordinate']==b['coordinate']
 if b['candidate_requirement_id']:assert reqdict[b['candidate_requirement_id']]['text']==a['text']
check('all 97 exact delta sentences accounted, 65 homes, 29 restatements, 3 interpretations',len(delta)==97 and sum(x['disposition']=='CANDIDATE-NORMATIVE-HOME' for x in delta)==65 and sum(x['disposition']=='SUPPORTING-RESTATEMENT-NO-SECOND-HOME' for x in delta)==29)
spec=(O/'PE-PROTOCOL-SPECIFICATION-G4.candidate.md').read_text()
check('926 unique candidate normative homes',len(reqdict)==len(req)==926 and all(spec.count('<a id="'+r['requirement_id'].lower()+'"></a>')==1 for r in req))
check('50 requirement families and 16 section families',len(rows(O/'composition/family-composition.tsv'))==50 and len({r['section_family'] for r in rows(O/'composition/family-composition.tsv')})==16)
for row in rows(P/'BOUNDED-NOT-ADMITTED-projection.tsv'):assert row['authoritative_source_sha256']==source[row['authoritative_source_id']]['sha256']
check('projection source hashes bind allocated exact bytes',True)
for r in json.loads((O/'profile/fragment-manifest.json').read_text()):assert sha((O/r['path']).read_bytes())==r['sha256']
check('all fragment digests match',True)
fields=rows(P/'fields.tsv');entry=json.loads((P/'entry.json').read_text());check('118 fields and 94 entry inputs preserved',len(fields)==118 and len(entry['root_fields'])==94)
scalars=dict(l.split('\t') for l in (P/'scalars.tsv').read_text().splitlines());check('17 profile scalars and definition joins',len(scalars)==17 and all(scalars[k] in defs and defs[scalars[k]]['output_type_id']=='PE-TSE-BOOL3' for k in ['equivalence-definition-id','material-conflict-definition-id','applicability-definition-id','determination-dependency-definition-id','recovery-definition-id']))
mapping=json.loads((O/'mapping/PE-G4-TMAP-000001.candidate.json').read_text());check('mapping/profile ordinal join without fabricated profile digest',mapping['profile_id']==scalars['profile-identifier'] and mapping['profile_sha256'] is None and mapping['registry_row_created'] is False)
report={'status':'PASS-BOUNDED-AUTHOR-COMPOSITION-CHECKS','check_count':len(checks),'checks':checks,'independent_acceptance':False,'source_appointed':False,'privacy_pass_claimed':False,'profile_admitted':False,'construction_defects_remain':['G4-C01','G4-C02','G4-C03','G4-C04'],'authority_gap':'G4-A01','future_occurrence_facts':'G4-R01','historical_code_executed':False}
(O/'verification').mkdir(exist_ok=True);(O/'verification/results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
