"""Focused fresh-process/recovered-root entry checks; saved source/evidence only."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);saved=(root/'results/primary/normal-session-exit-correspondence.json').read_bytes();data=m.inputs(root);cat=m.catalogue(data)
 if mode=='semantic':
  rows=m.semantic(data,cat);rec.check('fresh public semantic both contexts',lambda:len(rows)==2 and all(r['runtime_exit_chain'] is None for r in rows))
  rows[0]['declaration'].clear();rows.clear()
  bad=copy.deepcopy(cat);bad['source']['marker_component']='REPLACED.json';claims=json.loads(saved)['contexts'];claims=[x['normal_session_exit_correspondence'] for x in claims]
  for r in claims:r['declaration']=copy.deepcopy(bad);r['marker_path']['component']='REPLACED.json'
  rec.reject('fresh semantic coordinated catalogue claims substitution',lambda:m.semantic(data,bad,claims))
 elif mode=='derive':
  result=m.derive_exit(data,cat);rec.check('fresh derivation exact saved receipt',lambda:m.enc(result)==saved)
  result['contexts'][0]['normal_session_exit_correspondence']['saved_close_evidence']['value'].clear();result['contexts'].clear()
  e=dict(m.inner(data)['ctx']['e']);key='evidence/confirmed-close.json';v=json.loads(e[key]);v['normal_close_event']['state']['_phase']='READY';e[key]=m.enc(v)
  claims=[x['normal_session_exit_correspondence'] for x in json.loads(saved)['contexts']]
  for r in claims:r['saved_close_evidence']['value']=copy.deepcopy(v);r['saved_close_evidence']['identity']=m.identity(e[key])
  rec.reject('fresh derivation coordinated changed evidence and reports',lambda:m.derive_exit(data,cat,claims,e))
 elif mode=='validate':
  rec.check('fresh public receipt pristine',lambda:m.validate(root,saved)['result']=='PASS')
  v=json.loads(saved);v['contexts'][0]['normal_session_exit_correspondence']['marker_path']['component']='REPLACED.json'
  rec.reject('public receipt altered session marker binding',lambda:m.validate(root,m.enc(v)))
  v=json.loads(saved);del v['contexts'][1]['normal_session_exit_correspondence'];rec.reject('public mandatory second relation cannot be omitted',lambda:m.validate(root,m.enc(v)))
 elif mode=='constructed':
  fixtures=json.loads((root/'results/primary/fixtures.json').read_bytes())['cases'];case=fixtures[0];got=m.constructed_projection(data,cat,case);rec.check('fresh constructed public entry',lambda:got['projection']==case['output'])
  got['projection']['events'].clear();case=copy.deepcopy(fixtures[1]);case['close_case']['scope']['instance']='foreign';rec.reject('fresh public constructed wrong manager scope',lambda:m.constructed_projection(data,cat,case))
 elif mode=='recovered':
  rows,basis=m._checked(data,cat);c=data['coverage'];rec.check('recovered exact new receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   fx=normal(m,basis,idx);rec.check('recovered normal '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
   q=normal(m,basis,idx,continuity=False,terminal=('unlink-complete','missing-file'),marker='absent');rec.check('recovered missing file no implicit renewal '+str(idx),lambda:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is None and not q['output']['marker_removal_completed_in_model'])
   q['output']['marker_removal_completed_in_model']=True;rec.reject('recovered false unlink completion '+str(idx),lambda:m._construct_checked(basis,q))
   q=normal(m,basis,idx,terminal=('close-complete','process-termination'));q['output']['terminal_python_exception_in_model']=True;rec.reject('recovered termination not Python exception '+str(idx),lambda:m._construct_checked(basis,q))
   for path,val in [(('projection','references','manager','symbol'),'foreign'),(('projection','marker_path','component'),'WRONG'),(('close_case','scope','invocation'),'old'),(('token_case','invocation'),'other')]:
    bad=change(fx,path,val);rec.reject('recovered binding '+str(idx)+str(path),lambda bad=bad:m._construct_checked(basis,bad))
   got=m._construct_checked(basis,fx);got['projection']['managed_close_relation'].clear();got['anchor'].clear();rec.check('recovered mutable results isolated '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
   bad=copy.deepcopy(rows);bad[idx]['conditional_links'].pop();rec.reject('recovered missing correspondence '+str(idx),lambda:m._check_rows(basis,bad))
   for stage in cat['source']['order']:
    bad=copy.deepcopy(fx);bad['outcomes']=[r for r in bad['outcomes'] if r['stage']!=stage];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('recovered missing step '+stage+' '+str(idx),lambda bad=bad:m._construct_checked(basis,bad))
 else:raise ValueError('UNKNOWN-MODE')
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New Engineering normal-session-exit controls only')
