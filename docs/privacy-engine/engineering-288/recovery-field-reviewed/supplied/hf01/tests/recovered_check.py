"""Focused HF-01 checks in a separately recovered exact root."""
import copy,json,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False);ns=runpy.run_path(str(root/'tests/controls.py'),run_name='_audit_only');m=ns['module'](root/'code/correspondence.py');rows=[];error=None
def check(label,fn):
 v=fn();assert v is not False,label;rows.append({'check':label,'result':'PASS'})
 with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(rows[-1])+'\n')
 return v
def reject(fn,reason=None):
 try:fn()
 except (ValueError,TypeError,KeyError) as e:
  if reason is not None:assert str(e)==reason
  return True
 raise AssertionError('Unexpected acceptance')
try:
 data=m.recovery_inputs(root);cat=m.recovery_catalogue(data);e=dict(data['ctx']['e'])
 check('recovered source catalogue',lambda:m.check_recovery_catalogue(data,cat))
 obs,capture,row=check('recovered pristine semantic',lambda:m.connected_recovery(data,cat))
 bundle=check('recovered pristine derivation',lambda:m.derive_recovery(data,cat));saved=(root/'results/hf01-correspondence.json').read_bytes();check('recovered exact receipt',lambda:m.enc(bundle)==saved)
 check('recovered pristine public',lambda:m.validate(root,saved))
 for c in bundle['contexts']:
  b=c['hf01_evidence_binding'];r=c['saved_recovery_fields'][0]
  check('recovered occurrence '+c['context'],lambda b=b,r=r:b['occurrence']['id']==r['occurrence'] and b['instance']==r['instance'])
  check('recovered same predecessor evidence '+c['context'],lambda b=b,r=r,c=c:b['trace_identity']==r['trace_identity']==next(x['trace_identity'] for x in c['saved_reference_scope'] if x['occurrence']==r['occurrence']))
 check('missing observations remain missing',lambda:row['fields'][0]['head_relation']['validator_scalar_pointer'] is None and not capture['scalar_return_recorded'])
 altered=dict(e);folder=root/'retained/review/head-witness-primary/mutated'
 for p in folder.rglob('*'):
  if p.is_file():altered[p.relative_to(folder).as_posix()]=p.read_bytes()
 check('recovered semantic original witness',lambda:reject(lambda:m.connected_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE'))
 check('recovered derivation original witness',lambda:reject(lambda:m.derive_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE'))
 raw=(root/'retained/review/head-witness-primary/altered-derived-receipt.json').read_bytes();check('recovered public original mixed receipt',lambda:reject(lambda:m.validate(root,raw)))
 d=dict(data);d['ctx']=dict(data['ctx']);d['ctx']['e']=altered
 check('recovered candidate baseline cannot become expectation',lambda:reject(lambda:m.derive_recovery(d,cat),'HF01-HEAD-EXPECTED-STATE'))
 missing=dict(e);missing.pop('evidence/session-records/binding.json')
 check('recovered semantic missing binding',lambda:reject(lambda:m.connected_recovery(data,cat,missing)))
 check('recovered derivation missing binding',lambda:reject(lambda:m.derive_recovery(data,cat,missing)))
 for i in (0,1):
  bad=copy.deepcopy(bundle);bad['contexts'][i]['hf01_evidence_binding'].clear()
  check('recovered public missing binding '+str(i),lambda bad=bad:reject(lambda:m.validate(root,m.enc(bad))))
 bad=copy.deepcopy(bundle)
 for c in bad['contexts']:
  c['saved_recovery_fields'][0]['fields'][0]['value']='f'*64;c['hf01_evidence_binding']['occurrence']['observed_local_values']['managed-local:recovery-result']['head']='f'*64
 check('recovered public coordinated mixed result',lambda:reject(lambda:m.validate(root,m.enc(bad))))
 answer=m.validate(root,saved);answer['contexts'].clear();answer['receipt'].clear();obs['contexts'].clear();capture['value_functions'].clear();row['fields'].clear()
 for c in bundle['contexts']:c['hf01_evidence_binding']['head_record'].clear();c['saved_recovery_fields'][0]['instance'].clear()
 check('recovered semantic after nested mutations',lambda:m.connected_recovery(data,cat))
 check('recovered derivation after nested mutations',lambda:m.enc(m.derive_recovery(data,cat))==saved)
 check('recovered public after nested mutations',lambda:m.validate(root,saved))
 check('all boundaries remain',lambda:bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and not bundle['new_recovery_slice_limits']['actual_admission'])
except BaseException as ex:error=repr(ex);raise
finally:
 (out/'RESULT.json').write_text(json.dumps({'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'root':str(root),'python':sys.version,'new_HF01_controls_only':True,'database_connections':0,'runtime_operations':0,'completed_review_rerun':False},indent=2)+'\n')
print('PASS',len(rows),'recovered HF-01 controls')
