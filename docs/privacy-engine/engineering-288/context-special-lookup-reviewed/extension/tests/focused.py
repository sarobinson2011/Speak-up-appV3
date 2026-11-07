"""One new SOURCE-CONSTRUCTED pass. No public derivation or authenticated basis.
The C-source oracle reads the defining BEFORE_WITH code independently of the catalogue.
"""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
ROWS=[];D=copy.deepcopy;START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def write(path,value):
 with open(path,'x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 row={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(row)
 write(OUT/('%04d.json'%len(ROWS)),row)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
def check(name,fn,layer='source-constructed projector / independent oracle'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='source-constructed projector input'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 record(name,layer,'FAIL','expected ValueError');raise AssertionError(name)
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def mutate(v,path,value):
 x=D(v);t=x
 for k in path[:-1]:t=t[k]
 t[path[-1]]=value;return x
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
def main():
 manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
 check('checkpoint member bytes',lambda:all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in manifest.items()),'source artifact identity')
 c=load(ROOT/'code/managed_coverage.py','lookup_source');a=load(ROOT/'code/correspondence.py','lookup_adapter');f=load(ROOT/'reference/r1/tests/fixtures.py','retained_fixture_builder')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 old=(ROOT/'reference/r1/I164-open-return-reconstruction-1-source.zip').read_bytes()
 import io,zipfile
 with zipfile.ZipFile(io.BytesIO(old)) as z:oldproducer=z.read('code/managed_coverage.py')
 check('reviewed producer prefix unchanged',lambda:(ROOT/'code/managed_coverage.py').read_bytes().startswith(oldproducer),'source artifact identity')
 # Oracle intentionally reads the fixed source, not declarations or their step list.
 text=bc.decode();body=text[text.index('        inst(BEFORE_WITH,'):text.index('        inst(WITH_EXCEPT_START,')]
 enter=body.index('_PyObject_LookupSpecial(mgr, &_Py_ID(__enter__))');ex=body.index('_PyObject_LookupSpecial(mgr, &_Py_ID(__exit__))');call=body.index('_PyObject_CallNoArgs(enter)')
 check('C oracle: enter then exit before invocation',lambda:enter<ex<call and body.count('_PyObject_LookupSpecial(')==2,'independent defining-source oracle')
 check('C oracle: missing distinct from raised lookup',lambda:body.count('if (!_PyErr_Occurred(tstate))')==2 and body.count('PyExc_TypeError')==2,'independent defining-source oracle')
 special=tt.decode().split('_PyObject_LookupSpecial(PyObject *self, PyObject *attr)',1)[1].split('\nPyObject *',1)[0]
 check('C oracle: type lookup and descriptor binding',lambda:'_PyType_Lookup(Py_TYPE(self), attr)' in special and 'tp_descr_get' in special and 'res = f(res, self, (PyObject *)(Py_TYPE(self)));' in special,'independent defining-source oracle')
 tree=ast.parse(launcher);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='write_new')
 check('launcher oracle: exact with operand',lambda:fn.lineno==23 and fn.body[0].lineno==24 and ast.unparse(fn.body[0].items[0].context_expr)=="open(p, 'xb')",'independent defining-source oracle')
 pc=json.loads((ROOT/'fixtures/r1-catalogue.json').read_bytes());hc=json.loads((ROOT/'fixtures/helper-catalogue.json').read_bytes());anchors=json.loads((ROOT/'fixtures/anchors.json').read_bytes())
 cat=c.compile_context_lookup(launcher,bc,tt,pc)
 check('catalogue order matches independent oracle',lambda:cat['source']['method_order']==['__enter__','__exit__'] and cat['source']['order']==['lookup:continuation','lookup:__enter__','lookup:__exit__'])
 check('catalogue exact source validation',lambda:c.validate_context_lookup(launcher,bc,tt,pc,D(cat)))
 for path,value in [(('source','order'),['lookup:continuation','lookup:__exit__','lookup:__enter__']),(('source','method_order'),['__exit__','__enter__']),(('source','steps',1,'allowed'),['found']),(('declarations',1,'method'),'__exit__'),(('source','special_lookup','line'),1),(('parent_catalogue_sha256',),'0'*64)]:
  reject('catalogue mutation '+repr(path),lambda p=path,v=value:c.validate_context_lookup(launcher,bc,tt,pc,mutate(cat,p,v)),'source-derived catalogue comparison')
 reject('altered interpreter source',lambda:c.compile_context_lookup(launcher,bc.replace(b'__enter__',b'__other__',1),tt,pc),'exact defining-source input pin')
 ct=ast.parse((ROOT/'code/correspondence.py').read_bytes());defs={x.name:x for x in ct.body if isinstance(x,ast.FunctionDef)}
 def has(name,needle):return needle in ast.unparse(defs[name])
 check('mandatory R1 basis and receipt comparison wired',lambda:has('_basis','p._basis(pd)') and has('_basis',"fresh['saved'] == p.enc(p._assemble(pb))"),'static adapter call-path audit; not public execution')
 check('mandatory parent construction revalidation wired',lambda:has('_construct_checked',"basis['parent_module']._construct_checked") and has('_construct_checked','validate_context_lookup_projection'),'static adapter call-path audit; not authenticated-core execution')
 check('public derive includes both-context lookup rows',lambda:has('derive','_assemble(_basis(inputs(root)))') and has('_rows',"basis['prior']['contexts']") and has('_assemble','ctx[RELATION]'),'static adapter call-path audit')
 minimal={'format':'I164-CONTEXT-SPECIAL-LOOKUP-1','contexts':[{'context':x,'context_special_lookup_correspondence':{},'open_return_context_operand_correspondence':{}} for x in a.CONTEXTS]}
 check('JSON gate admits required relation shape',lambda:a._receipt_shape(a.enc(minimal))==minimal,'pre-derivation shape gate only; synthetic receipt')
 for i in (0,1):
  bad=D(minimal);del bad['contexts'][i][a.RELATION]
  reject('missing mandatory relation '+str(i),lambda b=bad:a._receipt_shape(a.enc(b)),'pre-derivation shape gate only')
 normal=[{'stage':'lookup:continuation','outcome':'normal'},{'stage':'lookup:__enter__','outcome':'found'},{'stage':'lookup:__exit__','outcome':'found'}]
 for row in anchors:
  for prefix in ('control-absent','control-normal'):
   for origin in ('protected-close','protected-append'):
    tag=row['context']+'/'+prefix+'/'+origin
    hp=f.parent(c,hc,row,prefix,origin)
    # New constructed premise follows the reviewed absence qualification. No old
    # fixture or receipt is changed: False in its old helper is not arrival proof.
    if prefix=='control-absent':hp['earlier_control_completed_in_model']=None
    rc=f.projection_case(c,pc,hp);p=c.open_return_projection(pc,rc,rc)
    b=c.context_lookup_binding(cat,p,p['instance_anchor'],'explicit conditional premise')
    v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':D(normal)}
    output=c.context_lookup_projection(cat,D(v),D(v))
    check(tag+'/normal result exact',lambda:c.validate_context_lookup_projection(cat,D(v),D(v),D(output)))
    check(tag+'/normal oracle pending original and stop',lambda:output['terminal_python_exception_in_model'] is True and output['last_pending_error_in_model']==p['original_error_pending_in_outer_handler'] and output['replacement_error_in_model'] is None and all(output[k] is False for k in ('enter_invocation_established','exit_invocation_established','context_manager_entry_established','f_binding_established','file_creation_established','actual_admission')))
    check(tag+'/distinct symbolic roles and unknown callability',lambda:output['method_roles']['__enter__']['symbol']!=output['method_roles']['__exit__']['symbol'] and all(r['callability']=='UNKNOWN' and r['runtime_identity'] is None and r['descriptor_effects']=='UNKNOWN' for r in output['method_roles'].values()))
    check(tag+'/prior effects and lineage retained',lambda:output['cleanup_list_state']==p['cleanup_list_state'] and output['retained_cleanup_error_evidence']==p['retained_cleanup_error_evidence'] and output['predecessor_projection']==p and output['earlier_control_completed_in_model']==(True if prefix=='control-normal' else None))
    # Allowed frontier families come from this test's source oracle, not generated guards.
    for ix in range(3):
     outcomes=('raise','catchable-interruption','process-termination','unobserved') if ix==0 else ('missing-method','raise','catchable-interruption','process-termination','unobserved')
     for outcome in outcomes:
      q=D(v);q['outcomes']=D(normal[:ix+1]);q['outcomes'][-1]['outcome']=outcome;r=c.context_lookup_projection(cat,D(q),D(q))
      def oracle(r=r,q=q,ix=ix,outcome=outcome):
       abrupt=outcome in ('process-termination','unobserved')
       return (c.validate_context_lookup_projection(cat,D(q),D(q),D(r)) and len(r['events'])==ix+1 and r['method_roles']['__exit__'] is None and (r['method_roles']['__enter__'] is not None)==(ix==2) and r['terminal_python_exception_in_model'] is (None if abrupt else True) and (r['replacement_error_in_model'] is None)==abrupt and r['enter_invocation_established'] is False and r['exit_invocation_established'] is False and r['cleanup_list_state']==p['cleanup_list_state'])
      check(tag+'/'+str(ix)+'/'+outcome,oracle)
      if outcome=='missing-method':check(tag+'/'+str(ix)+'/missing diagnostic qualified',lambda r=r:r['replacement_error_in_model']['diagnostic_requested_type']=='TypeError' and r['replacement_error_in_model']['diagnostic_completion_established'] is False and r['replacement_error_in_model']['exact_type'] is None)
    u=D(v);u['binding']['continuity']='UNESTABLISHED';u['outcomes']=[{'stage':'lookup:continuation','outcome':'unobserved'}]
    check(tag+'/unestablished continuation stays unobserved',lambda:c.context_lookup_projection(cat,D(u),D(u))['terminal_python_exception_in_model'] is None)
    bad=D(v);bad['binding']['continuity']='UNESTABLISHED'
    reject(tag+'/invented continuation',lambda:c.context_lookup_projection(cat,D(bad),D(bad)))
    for path,val in [(('outcomes',),normal[:2]),(('outcomes',),[normal[0],normal[2],normal[1]]),(('outcomes',),normal+[normal[2]]),(('outcomes',1,'outcome'),'normal'),(('outcomes',1,'outcome'),True),(('scope','invocation'),'other-invocation'),(('binding','references','token','symbol'),'wrong-token'),(('binding','references','owner','symbol'),'wrong-owner'),(('binding','operand_role','symbol'),'wrong-operand'),(('binding','operand_occurrence','source','expression'),'other()')]:
     q=mutate(v,path,val)
     reject(tag+'/input '+repr(path),lambda q=q:c.context_lookup_projection(cat,D(q),D(q)))
    q=D(v);q['outcomes'][1]['outcome']='raise'
    reject(tag+'/exit after failed enter',lambda:c.context_lookup_projection(cat,D(q),D(q)))
    for path,val in [(('completion',),'normal-overall-return'),(('terminal_python_exception_in_model',),False),(('terminal_python_exception_in_model',),1),(('method_roles','__enter__','callability'),'ESTABLISHED'),(('method_roles','__exit__','runtime_identity'),'invented'),(('method_roles','__enter__','receiver','symbol'),'other-object'),(('context_manager_entry_established',),True),(('replacement_error_in_model',),{}),(('events',1,'method'),'__exit__')]:
     reject(tag+'/output '+repr(path),lambda path=path,val=val:c.validate_context_lookup_projection(cat,D(v),D(v),mutate(output,path,val)),'source-constructed output-comparison core; not authenticated basis')
    for path,val in [(('outcomes',1,'outcome'),S('found')),(('outcomes',),L(normal)),(('binding','references',),Q(b['references']))]:
     q=mutate(v,path,val);reject(tag+'/exact type '+repr(path),lambda q=q:c.context_lookup_projection(cat,q,D(v)),'exact-type input gate before normalization')
    q=D(output);q[S('kind')]=q.pop('kind')
    reject(tag+'/subclass literal key',lambda:c.validate_context_lookup_projection(cat,D(v),D(v),q),'exact-type submitted-output gate')
    q=mutate(v,('parent_result','returned_object_role','symbol'),'stale-role')
    reject(tag+'/coordinated return-role substitution',lambda:c.context_lookup_binding(cat,q['parent_result'],q['anchor'],'explicit conditional premise'),'source binding constraints, not public validation')
    q=D(v);q['parent_result']['events'][-1]['outcome']='raise'
    reject(tag+'/false R1 normal outcome',lambda:c.context_lookup_binding(cat,q['parent_result'],q['anchor'],'explicit conditional premise'),'source binding constraints')
    before=D(v);catbefore=D(cat);changed=D(output);changed['method_roles']['__enter__']['receiver']['scope']['context']='mutated';changed['predecessor_projection']['binding']['references']['token']['symbol']='mutated';changed['events'].clear()
    check(tag+'/nested mutable result isolation',lambda:v==before and cat==catbefore and c.context_lookup_projection(cat,D(v),D(v))==output)
    reject(tag+'/mutated result rejected',lambda:c.validate_context_lookup_projection(cat,D(v),D(v),changed),'source-constructed output-comparison core; not authenticated basis')
    # No live basis is forged to test the parent core. Its execution remains pending.
 return {'source_only':True,'full_public_runs':0,'authenticated_basis_core_runs':0,'application_runs':0,'runtime_protocol_invocations':0}
try:
 details=main();result={'result':'PASS','started_seconds':START,'finished_utc':utc(),'seconds':time.monotonic()-START,'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'rows':len(ROWS),'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
