import copy,json,pathlib,sys,time,ast
import construction_inputs as c
P=pathlib.Path(__file__).resolve().parents[1];root=pathlib.Path(sys.argv[1]);rows=[]
def pass_(name,**k):
 rows.append(dict(case=name,status='PASS',**k));(P/'results/focused.json').write_text(json.dumps(rows,indent=2))
def reject(name,f):
 try:f()
 except ValueError as e:pass_(name,rejection=str(e))
 else:raise AssertionError('UNEXPECTED ACCEPT '+name)
_,base=c.static_inputs(root);c.validate_static(root,base);pass_('actual current static model ledger contract')
m='model-input.json';l='ledger-input.json'
changes=[('model omitted',lambda x:x.pop(m)),('ledger omitted',lambda x:x.pop(l)),('stale candidate',lambda x:x[m]['binding']['candidate_binding'].clear()),('mixed contexts',lambda x:x[m]['directory_program']['contexts'].reverse()),('missing directory',lambda x:x[m]['directory_program']['directories'].pop()),('wrong guard',lambda x:x[m]['directory_program']['directories'][0].update(guard='always')),('wrong type',lambda x:x[m]['directory_program']['directories'][0].update(type='ANY')),('rule omitted',lambda x:x[m]['semantic_rule_program']['rules'].pop()),('ordinal changed',lambda x:x[m]['semantic_rule_program']['rules'][0].update(ordinal=1)),('duty omitted',lambda x:x[l]['procedure_input']['relation_duties'].pop()),('node duty omitted',lambda x:x[l]['procedure_input']['directory_ranges'].pop()),('unknown cardinality zero',lambda x:x[l]['procedure_input']['directory_ranges'][0].update(cardinality=0)),('qualification escalated',lambda x:x[l]['procedure_input']['relation_duties'][0].update(classification='QUALIFIED')),('source substitution',lambda x:x[m]['binding']['consumed_current_inputs']['native/code/expand_candidate.py'].update(sha256='0'*64)),('native invoke enabled',lambda x:x[m]['invocation'].update(allowed=True)),('current model invented',lambda x:x[m]['totals'].update(tokens=5742)),('native duties removed',lambda x:x[l]['native_duty_names'].pop()),('future evidence exclusion',lambda x:x[l].update(excluded=['restoration'])),('scope substitution',lambda x:x[m]['binding'].update(assessment='OPERATIONAL')),('evidence duty removed',lambda x:x[l]['candidate_ledger_requirements']['classification_duties'].pop())]
for name,edit in changes:
 bad=copy.deepcopy(base);edit(bad);assert c.enc(bad)!=c.enc(base);reject(name,lambda:c.validate_static(root,bad))
for key,value in [('qualified',True),('complete_instantiated_model',True),('canonical_registration',True),('full_expansion_ready',True),('final_binding','COMPLETE'),('global_lifetime_bound',0),('actual_admission',True),('actual_admission',0)]:
 bad=copy.deepcopy(base);bad[m]['status'][key]=value;reject('status '+key+' '+str(value),lambda:c.validate_static(root,bad))
for i in range(11):
 bad=copy.deepcopy(base);target=base[m]['obligations'][i]['id']
 for part in (m,l):
  bad[part]['obligations']=[o for o in bad[part]['obligations'] if o['id']!=target]
  assert len(bad[part]['obligations'])==10 and not any(o['id']==target for o in bad[part]['obligations'])
 reject('coordinated obligation omission '+target,lambda:c.validate_static(root,bad))
bad=copy.deepcopy(base);bad[l]['procedure_input']['relation_duties'].clear();bad[m]['directory_program']['ledger_duties'].clear();reject('coordinated duty omission',lambda:c.validate_static(root,bad))
# Returned mutable structures never feed fresh expected data.
base[m]['binding']['contexts'].clear();base[l]['procedure_input']['relation_duties'].clear()
_,pristine=c.static_inputs(root);c.validate_static(root,pristine);pass_('fresh pristine static validation after returned nested mutation')
# Actual retained finite-plan guard, isolated pure function only: no model expansion.
source=root/'preflight/preflight.py';tree=ast.parse(source.read_bytes());n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='inspect_plan')
env={'require':c.need,'CONTEXTS':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']};exec(compile(ast.Module(body=[n],type_ignores=[]),str(source),'exec'),env)
d=pristine[m]['directory_program']['directories'][0]
fixture={'contexts':env['CONTEXTS'],'directories':{d['class']:{'count':None,'source':d['source'],'guard':d['guard']}},'relations':{},'required_relations':[],'status':'DRAFT-UNQUALIFIED','admission':False}
reject('retained finite-plan interface rejects UNKNOWN multiplicity',lambda:env['inspect_plan'](fixture,[d['class']]))
pass_('both context definitions and input ranges retained',contexts=pristine[m]['directory_program']['contexts'],directories=len(pristine[m]['directory_program']['directories']),duties=len(pristine[l]['procedure_input']['relation_duties']))
print('PASS',len(rows),'focused controls',flush=True)
