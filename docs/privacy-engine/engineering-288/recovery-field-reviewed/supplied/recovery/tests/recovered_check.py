"""Focused new recovery-field checks on a separately recovered exact input."""
import copy,json,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]);ns=runpy.run_path(str(root/'tests/controls.py'),run_name='_audit_only');m=ns['module'](root/'code/correspondence.py');rows=[]
def check(label,f):
 result=f();assert result is not False,label;rows.append({'check':label,'result':'PASS'});return result
def rejects(f):
 try:f()
 except (ValueError,TypeError,KeyError):return True
 raise AssertionError('Unexpected acceptance')
error=None
try:
 data=m.recovery_inputs(root);cat=m.recovery_catalogue(data)
 check('recovered catalogue',lambda:m.check_recovery_catalogue(data,cat))
 observed,capture,row=check('recovered semantic evidence',lambda:m.connected_recovery(data,cat))
 receipt=(root/'results/recovery-field-correspondence.json').read_bytes();result=check('recovered public exact receipt',lambda:m.validate(root,receipt));bundle=json.loads(receipt)
 for i in (0,1):
  view=bundle['contexts'][i];check('recovered prior extensions context '+str(i),lambda view=view:view['reference_declarations'] and view['field_declarations'])
  check('recovered three declarations context '+str(i),lambda view=view:len(view['recovery_field_declarations']['declarations'])==3)
  check('recovered three observations context '+str(i),lambda view=view:len(view['saved_recovery_fields'][0]['fields'])==3)
 for i in range(3):
  for label,edit in [('omit',lambda c,i=i:c['declarations'].pop(i)),('origin',lambda c,i=i:c['declarations'][i]['origin']['origin'].update(expression='stale')),('guard',lambda c,i=i:c['declarations'][i]['origin']['origin'].update(guards=[])),('type',lambda c,i=i:c['declarations'][i].update(type='int'))]:
   c=copy.deepcopy(cat);edit(c);check('recovered '+label+' '+str(i),lambda c=c:rejects(lambda:m.check_recovery_catalogue(data,c)))
 check('no validator scalar invention',lambda:not capture['scalar_return_recorded'] and row['fields'][0]['head_relation']['validator_scalar_pointer'] is None)
 check('distinct context occurrences',lambda:bundle['contexts'][0]['saved_recovery_fields'][0]['occurrence']!=bundle['contexts'][1]['saved_recovery_fields'][0]['occurrence'])
 check('sparse observer remains separate',lambda:bundle['new_recovery_slice_limits']['observer_frame'] is None and bundle['new_recovery_slice_limits']['separate_observer_Client_state_call']==1)
 for label,edit in [('head',lambda t:r(t)['value'].update(head='a'*64)),('authorization type',lambda t:r(t)['value'].update(new_attempt_authorized=0)),('embedding',lambda t:r(t)['value']['status'].update(connection_epoch=17))]:
  def r(t):return next(e for e in t['events'] if e['function']=='ManagedAuthority.recover' and e['event']=='return')
  e=dict(data['ctx']['e']);t=json.loads(e['evidence/execution-trace.json']);edit(t);e['evidence/execution-trace.json']=m.enc(t);check('recovered semantic rejection '+label,lambda e=e:rejects(lambda:m.connected_recovery(data,cat,e)))
 result['contexts'].clear();result['receipt'].clear();row['fields'].clear();cat['source']['fields'].clear()
 check('recovered nested returned mutation isolation',lambda:m.validate(root,receipt))
 check('returned narrowed catalogue still rejects',lambda:rejects(lambda:m.check_recovery_catalogue(data,cat)))
 check('all obligations and unknowns unchanged',lambda:bundle['new_recovery_slice_limits']['all_eleven_obligations_preserved'] and bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and bundle['new_recovery_slice_limits']['actual_admission'] is False)
except BaseException as ex:error=repr(ex);raise
finally:
 output.write_text(json.dumps({'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'root':str(root),'python':sys.version,'new_recovery_controls_only':True,'no_runtime':True,'database_connections':0},indent=2)+'\n')
print('PASS',len(rows),'recovered recovery-field controls')
