"""Record an unresolved label interpretation; do not assert a new flag contract."""
from pathlib import Path
import copy,json,types,sys,os,hashlib
w=Path(__file__).resolve().parents[2];root=w/'ch-input';out=w/'ch-review/results/classification-caveat.json'
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED')
 if event=='exec' and args[0].co_filename.rsplit('/',1)[-1].lower() in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PRODUCER-EXECUTION')
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith(str(root)+'/') and (args[2] or 0)&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('INPUT-WRITE')
sys.addaudithook(audit)
p=root/'code/correspondence.py';m=types.ModuleType('caveat');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);_,authority,anchor,observations=d['prior_module'].sources(d['prior_data']);v=c.handle_authentication(authority,anchor,observations)
cases=json.loads((w/'ch-review/independent-primary/core/constructed-cases.json').read_bytes());rows=[];stages=['client-call','owner-lookup','owner-guard']
for i in (0,2):
 for index,stage in enumerate(stages):
  x=copy.deepcopy(cases[i]['case']);x['manager_case']=None;x['outcomes']={s:'normal' for s in stages[:index]};x['outcomes'][stage]='process-termination'
  r=c.client_handle_projection(cat,v,x,copy.deepcopy(x));accepted=c.validate_client_handle_projection(cat,v,x,copy.deepcopy(x),copy.deepcopy(r));assert accepted is True
  assert r['completion']=='process-termination' and r['outside_catch_failure'] is True and r['original_exception'] is r['fixed_client_failure'] is None and r['destinations']==[]
  changed=copy.deepcopy(r);changed['outside_catch_failure']=False
  try:c.validate_client_handle_projection(cat,v,x,copy.deepcopy(x),changed)
  except ValueError as e:assert str(e)=='CLIENT-PROJECTION-CORRESPONDENCE';error=str(e)
  else:raise AssertionError('unexpected changed-label acceptance')
  rows.append({'case':x,'result':r,'projection_validator_accepted':accepted,'same_case_false_label_rejected':error})
out.write_text(json.dumps({'kind':'INTERPRETATION-CAVEAT','cases':rows,'source':{'bytes':len((root/'code/managed_coverage.py').read_bytes()),'sha256':hashlib.sha256((root/'code/managed_coverage.py').read_bytes()).hexdigest()},'counted_in_primary_or_recovered_assertion_totals':False,'uniform_flag_meaning_imposed_by_reviewer':False,'Python_unwind_or_actual_evidence_established':False,'requests_or_session_operations':0},indent=2)+'\n');print('Recorded six conditional prefix-termination cases; no exception or unwind claim')
