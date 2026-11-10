"""Supplement only: mutate actual returned objects; do not replay primary controls."""
from pathlib import Path
import sys,types,json,copy,hashlib,os,traceback,collections
B=Path(__file__).resolve().parent;R=B/'candidate';O=B/'direct-alias';O.mkdir(exist_ok=False)
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def save(p,v):
 with p.open('xb') as f:f.write(enc(v));f.flush();os.fsync(f.fileno())
def load(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
rows=[];failed=[]
def emit(n,s,d=None):
 v={'sequence':len(rows)+1,'name':n,'status':s,'detail':d,'layer':'direct actual-return alias isolation / pure model comparison; no authentication'};rows.append(v);save(O/('%04d.json'%len(rows)),v)
 with (O/'progress.jsonl').open('ab') as f:f.write(enc(v));f.flush();os.fsync(f.fileno())
 print(enc(v).decode(),end='',flush=True)
try:
 c=load(R/'code/managed_coverage.py','review_alias_producer');cat=read(B/'independent/independent-catalogue.json');fixtures=read(R/'fixtures/retained-return-cases.json')
 for j in (0,12):
  f=fixtures[j];p=copy.deepcopy(f['output']);pbytes=enc(p);label=f['name']
  b=c.enter_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise');b['references']['owner']['symbol']='actual-binding-mutated';b['res_assignment']['target']='wrong'
  assert enc(p)==pbytes;emit(label+'/actual binding mutation does not reach parent','PASS')
  b=c.enter_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise');q={'scope':p['scope'],'anchor':p['instance_anchor'],'parent_result':p,'binding':b,'outcomes':[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'attempted'}]};qbefore=enc(q);cbefore=enc(cat)
  returned=c.enter_decref_projection(cat,q,q);expected=enc(returned)
  returned['binding']['references']['owner']['symbol']='actual-output-mutated';returned['scope']['instance']['binding']='actual-scope-mutated';returned['res_value_role']['C_NULL']=True;returned['events'][1]['operand_role']['method']='__exit__';returned['predecessor_projection']['res_assignment']['target']='different'
  assert enc(q)==qbefore and enc(cat)==cbefore;emit(label+'/actual returned nested mutations leave every selected premise unchanged','PASS')
  try:c.validate_enter_decref_projection(cat,q,q,returned)
  except ValueError as e:assert 'ENTER-DECREF-OUTPUT-CORRESPONDENCE' in str(e);emit(label+'/altered actual return rejected','REJECTED',str(e))
  else:emit(label+'/altered actual return accepted','DEFECT-OBSERVED');failed.append(label)
  again=c.enter_decref_projection(cat,q,q);assert enc(again)==expected and enc(q)==qbefore;emit(label+'/subsequent pristine result stable after direct mutation','PASS')
except BaseException as e:emit('supplement harness failure','FAIL',{'exception':repr(e),'traceback':traceback.format_exc()});failed.append('harness')
result={'result':'PASS' if not failed else 'FAILED','rows':len(rows),'counts':dict(collections.Counter(x['status'] for x in rows)),'failures':failed,'public_runs':0,'authenticated_constructed_runs':0};save(O/'RESULT.json',result);print(enc({'event':'RESULT','result':result}).decode(),end='',flush=True)
if failed:raise SystemExit(1)
