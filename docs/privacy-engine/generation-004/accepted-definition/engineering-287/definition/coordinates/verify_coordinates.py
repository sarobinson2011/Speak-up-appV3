"""Synthetic, document-only coordinate and predicate checks. No source authentication."""
from pathlib import Path
import csv,json,hashlib,itertools,runpy,io,contextlib,copy
O=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): ns=runpy.run_path(str(O/'verify-candidate.py'))
T=ns['types'];D=ns['defs'];asts=ns['asts'];decode=ns['decode']
def rows(p):return list(csv.DictReader((O/p).open(),delimiter='\t'))
def enc(x):
 t,v=x
 if t=='PE-TSE-BOOL3':k=0;b=bytes([v])
 elif t=='PE-TSE-BYTES':k=1;b=bytes.fromhex(v)
 elif t=='PE-TSE-ID':k=2;b=v.encode('ascii')
 elif t=='PE-TSE-UINT':k=3;b=v.encode('ascii')
 else:
  k={'SET':16,'TUPLE':17}[T[t]['kind']];vs=[enc(z) for z in v]
  if k==16:vs=sorted(set(vs))
  b=len(vs).to_bytes(4,'big')+b''.join(len(z).to_bytes(8,'big')+z for z in vs)
 tb=t.encode('ascii');return b'TSEV1'+len(tb).to_bytes(4,'big')+tb+bytes([k])+len(b).to_bytes(8,'big')+b
B='PE-TSE-BOOL3';ID='PE-TSE-ID';BY='PE-TSE-BYTES';U='PE-TSE-UINT'
def ev(n,args=(),refs=None):
 op,a=n
 if op=='arg':return args[int(a[0])-1]
 if op=='literal':return decode(bytes.fromhex(a[1]))
 if op=='tuple':return a[0],[ev(z,args,refs) for z in a[1:]]
 if op=='equal':return B,int(ev(a[0],args,refs)==ev(a[1],args,refs))
 if op=='not':v=ev(a[0],args,refs)[1];return B,2 if v==2 else 1-v
 if op in ('and','or'):
  vs=[ev(z,args,refs)[1] for z in a];dominant=0 if op=='and' else 1
  return B,dominant if dominant in vs else 2 if 2 in vs else 1-dominant
 if op=='apply':return ev(asts[a[0]],[ev(z,args,refs) for z in a[1:]],refs)
 if op=='ref':return B,refs[a[0]]
 raise AssertionError(op)
def fixture(t,path='FIXTURE'):
 if t==ID:return t,path
 if t==BY:return t,hashlib.sha256(path.encode()).hexdigest()
 if t==U:return t,'7'
 if t==B:return t,1
 return t,[fixture(c,path+'-'+str(i)) for i,c in enumerate(T[t]['field_type_ids'].split(','),1)]
semid='PE-G4-CAP-SEMANTIC-BASIS-COORDINATE';eid='PE-G4-CAP-E-BASIS-COORDINATE';gid='PE-G4-CAP-GATE-OBSERVATION-BINDING'
sem=fixture(D[semid]['output_type_id']);e=fixture(D[eid]['output_type_id'])
# Independently owned scopes; cuts join their corresponding fixed scopes.
e[1][7][1][0]=copy.deepcopy(sem[1][8]);e[1][8][1][0]=copy.deepcopy(sem[1][9])
g=fixture(D[gid]['output_type_id']);g[1][0]=copy.deepcopy(sem);g[1][2]=(ID,'PRE-EXECUTION');g[1][4][1][0]=copy.deepcopy(sem[1][8]);g[1][5][1][0]=copy.deepcopy(sem[1][9])
for name,x in [(semid,sem),(eid,e),(gid,g)]:
 assert ev(asts[name],x[1])==x and decode(enc(x))==x
 layout=[r for r in rows('coordinates/argument-layout.tsv') if r['definition_id']==name]
 assert [r['type_id'] for r in layout]==D[name]['input_type_ids'].split(',')
 assert [r['argument_order'] for r in layout]==[f'{i:04}' for i in range(1,len(layout)+1)]
header='coordinate_order\tcoordinate_definition_id\tcanonical_value_hex\n'
def coordinates(s,ee):return (header+''.join(f'{i:04}\t{name}\t{enc(x).hex()}\n' for i,(name,x) in enumerate([(semid,s),(eid,ee)],1))).encode()
base=coordinates(sem,e)
assert (O/'coordinates/ordering-coordinate-template.tsv').read_bytes()==header.encode()
config=json.loads((O/'coordinates/coordinate-construction.json').read_text())
assert config['ordering_empty_sha256']==hashlib.sha256(header.encode()).hexdigest()
assert config['dependency_definitions']==[semid,eid] and config['ordering_definitions']==[]
assert not config['gate_evidence_in_authorization_coordinate_set'] and not config['actual_DepD_substituted']
for r in rows('profile/fragments/BOUNDED-NOT-ADMITTED-projection.tsv'):
 assert r['dependency_coordinate_definition_ids']==','.join([semid,eid])
def leaves(x,path=()):
 if isinstance(x[1],list):
  for i,c in enumerate(x[1]):yield from leaves(c,path+(i,))
 else:yield path
mutations=0
for which,x in enumerate([sem,e]):
 for path in leaves(x):
  changed=copy.deepcopy(x);p=changed
  for i in path[:-1]:p=p[1][i]
  t,v=p[1][path[-1]];p[1][path[-1]]=(t,str(int(v)+1) if t==U else ('00'+v if t==BY else v+'-CHANGED'))
  assert decode(enc(changed))==changed
  assert coordinates(changed,e) !=base if which==0 else coordinates(sem,changed)!=base
  if which==0:assert ev(asts['PE-G4-CAP-SEMANTIC-BASIS-EQUAL'],[sem,changed])==(B,0)
  mutations+=1
# Bounded structural obligations only: these comparisons DO NOT establish authority/currentness.
def joins(s,ee,gg):
 return (gg[1][0]==s and ee[1][7][1][0]==s[1][8] and ee[1][8][1][0]==s[1][9]
 and gg[1][4][1][0]==s[1][8] and gg[1][5][1][0]==s[1][9]
 and gg[1][2][1] in ('PRE-EXECUTION','PRE-COMMITMENT') and len(bytes.fromhex(gg[1][1][1]))==32 and len(bytes.fromhex(gg[1][7][1]))==32)
assert joins(sem,e,g)
g2=copy.deepcopy(g);g2[1][4][1][1]=(ID,'LATER-ROOT-CUT');g2[1][5][1][1]=(ID,'LATER-STATE-CUT');g2[1][2]=(ID,'PRE-COMMITMENT')
assert joins(sem,e,g2) and enc(g)!=enc(g2) and coordinates(sem,e)==base
negative=0
for field,value in [(0,fixture(sem[0],'WRONG')),(1,(BY,'00')),(2,(ID,'UNKNOWN')),(7,(BY,'00'))]:
 bad=copy.deepcopy(g);bad[1][field]=value;assert not joins(sem,e,bad);negative+=1
for target,fields in [('E',(7,8)),('GATE',(4,5))]:
 for field in fields:
  ee=copy.deepcopy(e);gg=copy.deepcopy(g);x=ee if target=='E' else gg;x[1][field][1][0]=fixture(sem[1][8][0],'WRONG-SCOPE')
  assert not joins(sem,ee,gg);negative+=1
# Inspect candidate expressions rather than substitute a separately coded classifier.
gates=[]
for v,b in itertools.product(range(3),repeat=2):
 refs={'ROOT-ELIGIBLE':v,'SCOPED-USED':b};eq=ev(asts['PE-G4-CAP-EQ'],refs=refs)[1];mc=ev(asts['PE-G4-CAP-MC'],refs=refs)[1]
 expected='CONFLICT' if v==0 or b==1 else 'EQUIVALENT' if (v,b)==(1,0) else 'INDETERMINATE'
 actual='CONFLICT' if mc==1 else 'EQUIVALENT' if eq==1 else 'INDETERMINATE'
 assert actual==expected and not (eq==mc==1)
 if 2 not in (v,b):assert {eq,mc}=={0,1}
 gates.append({'v':v,'b':b,'EQ':eq,'MC':mc,'validated_gate_outcome':actual})
counts={0:0,1:0,2:0}
for vs in itertools.product(range(3),repeat=5):
 actual=ev(asts['PE-G4-CAP-FIVE-COMPLETE-CLASSIFIER'],[(B,x) for x in vs])[1]
 expected=2 if 2 in vs else 0 if 0 in vs else 1
 assert actual==expected;counts[actual]+=1
assert [r['condition_id'] for r in rows('coordinates/materiality-disposition.tsv')]==[f'M{i:02}' for i in range(1,14)]
report={'status':'PASS-BOUNDED-AUTHOR-CHECKS','synthetic_fixtures_only':True,'immutable_leaf_mutations':mutations,'invalid_structural_join_cases':negative,'gate_vectors':gates,'evaluation_vectors':243,'evaluation_counts':counts,'full_DepD_substituted':False,'source_adequacy_established':False,'profile_admitted':False}
(O/'verification/coordinate-materiality.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — fixed coordinate serialization and mutation sensitivity; current gate cuts remain separate.')
print('PASS — 9 materiality states and 243 complete-five evaluation combinations.')
