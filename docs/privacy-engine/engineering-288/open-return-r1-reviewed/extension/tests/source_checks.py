"""ONE new focused source pass. No public derivation or runtime application calls."""
import ast,copy,hashlib,importlib.util,json,os,platform,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=copy.deepcopy
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def utc():
 from datetime import datetime,timezone
 return datetime.now(timezone.utc).isoformat()
def write(path,v):
 with path.open('w') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def run(out):
 out.mkdir(exist_ok=False);rows=[];started=utc();start=time.monotonic();error=None
 def check(name,fn,reject=False,layer='source/constructed projection; unauthenticated fixture'):
  detail=None
  try:
   value=fn()
   if reject:raise AssertionError('Expected rejection; accepted')
   assert value is not False
   status='PASS'
  except ValueError as exc:
   if not reject:raise
   status='REJECTED';detail=str(exc)
  row={'row':len(rows)+1,'utc':utc(),'name':name,'status':status,'layer':layer,'detail':detail};rows.append(row)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
  write(out/('row-%04d.json'%row['row']),row);print('CHECK '+json.dumps(row,sort_keys=True),flush=True)
 try:
  print('PHASE source identities and module loading',flush=True)
  manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
  def membership():
   actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
   assert actual==set(manifest)|{'MANIFEST.json'}
   for n,pin in manifest.items():
    b=(ROOT/n).read_bytes();assert pin=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
  check('exact source checkpoint membership and hashes',membership,layer='source byte identity')
  c=load(ROOT/'code/managed_coverage.py','recon_coverage');a=load(ROOT/'code/correspondence.py','recon_adapter');f=load(ROOT/'tests/fixtures.py','recon_fixtures')
  raw=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();parentcat=json.loads((ROOT/'fixtures/retained-helper-catalogue.json').read_bytes());anchors=json.loads((ROOT/'fixtures/retained-context-anchors.json').read_bytes())
  cat=c.compile_open_return(raw,parentcat)
  def oracle():
   t=ast.parse(raw);fn=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='write_new');w=fn.body[0];call=w.items[0].context_expr
   assert fn.lineno==23 and w.lineno==24 and call.func.id=='open' and call.args[0].id=='p' and type(call.args[1].value) is str and call.args[1].value=='xb'
   assert isinstance(w.items[0].optional_vars,ast.Name) and w.items[0].optional_vars.id=='f'
   assert cat['source']['open_call']['site']==[call.lineno,call.col_offset,call.end_lineno,call.end_col_offset,'Call']
   assert cat['source']['with_statement']['site']==[w.lineno,w.col_offset,w.end_lineno,w.end_col_offset,'With']
   assert cat['source']['operand_ast_field']=='With.items[0].context_expr'
   assert cat['source']['order']==['open-return:continuation','open-return:outcome']
   assert cat['guard_branches']['outcomes']==['normal-return','raise','catchable-interruption','process-termination','unobserved']
   assert cat['guard_branches']['prefixes']==['control absent','control construction and callback completed normally']
   assert cat['guard_branches']['origins']==['protected-close','protected-append']
  check('independent defining AST and outcome contract',oracle,layer='source oracle')
  check('pristine catalogue',lambda:c.validate_open_return(raw,parentcat,cat),layer='source catalogue')
  for key in ('order','open_call','operand_ast_field'):
   bad=D(cat);bad['source'][key]=[] if key=='order' else 'wrong'
   check('altered catalogue '+key,lambda bad=bad:c.validate_open_return(raw,parentcat,bad),True,'source catalogue comparison')
  bad=D(cat);bad['guard_branches']['outcomes'].remove('catchable-interruption');check('omitted guard branch',lambda:c.validate_open_return(raw,parentcat,bad),True,'source catalogue comparison')
  def integration_ast():
   t=ast.parse((ROOT/'code/correspondence.py').read_bytes());defs={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
   basis=ast.unparse(defs['_basis']);constructed=ast.unparse(defs['_construct_checked'])
   assert 'p._checked' in basis and 'p._receipt_checked' in basis and 'compile_open_return' in basis
   assert "basis['parent_module']._construct_checked" in constructed and 'validate_open_return_projection' in constructed
   assert '_basis' in ast.unparse(defs['derive']) and '_receipt_shape' in ast.unparse(defs['validate'])
  check('mandatory integration source wiring (not execution)',integration_ast,layer='adapter AST only')
  class S(str):pass
  class L(list):pass
  class M(dict):pass
  for row in anchors:
   for prefix in ('control-absent','control-normal'):
    for origin in ('protected-close','protected-append'):
     tag='/'.join([row['context'],prefix,origin]);print('PHASE '+tag,flush=True)
     p=f.parent(c,parentcat,row,prefix,origin);v=f.projection_case(c,cat,p);expect=D(v);out0=c.open_return_projection(cat,v,expect)
     def normal():
      o=c.open_return_projection(cat,v,expect)
      assert o['open_return_established_in_model'] is True and o['context_operand_established_in_model'] is True
      assert o['returned_object_role']==o['context_operand']['role'] and o['returned_object_role'] is not o['context_operand']['role']
      assert o['terminal_python_exception_in_model'] is True and o['last_pending_error_in_model']==p['original_error_pending_in_outer_handler']
      assert o['replacement_error_in_model'] is None and o['context_protocol_lookup_established'] is False
      for k in f.EXCLUDED:
       if k!='open_return_established':assert o[k] is False
      for k in ('cleanup_list_state','retained_cleanup_error_evidence','failure_origin_region','close_normal_return_completed_in_model','earlier_control_completed_in_model','original_error_pending_in_outer_handler'):assert o[k]==p[k]
      assert o['returned_object_role']['runtime_identity'] is None and o['returned_object_role']['concrete_type'] is None
      return c.validate_open_return_projection(cat,v,expect,o)
     check(tag+'/normal and independent invariants',normal)
     for stage in ('open-return:continuation','open-return:outcome'):
      for frontier in ('raise','catchable-interruption','process-termination','unobserved'):
       fv=f.projection_case(c,cat,p,(stage,frontier));fo=c.open_return_projection(cat,fv,D(fv))
       def nonnormal(fv=fv,fo=fo,frontier=frontier,stage=stage):
        assert fo['open_return_established_in_model'] is False and fo['context_operand'] is None and fo['returned_object_role'] is None
        assert fo['terminal_python_exception_in_model'] is (None if frontier in ('process-termination','unobserved') else True)
        assert len(fo['events'])==(1 if stage=='open-return:continuation' else 2)
        assert fo['cleanup_list_state']==p['cleanup_list_state'] and fo['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler']
        if frontier in ('raise','catchable-interruption'):
         assert fo['replacement_error_in_model']['frontier_stage']==stage and fo['last_pending_error_in_model']==fo['replacement_error_in_model']
        else:assert fo['replacement_error_in_model'] is None and fo['last_pending_error_in_model']==p['last_pending_error_in_model']
        return c.validate_open_return_projection(cat,fv,D(fv),fo)
       check(tag+'/'+stage+'/'+frontier,nonnormal)
       bad=D(fo);bad['terminal_python_exception_in_model']=False if fo['terminal_python_exception_in_model'] is True else True
       check(tag+'/'+stage+'/'+frontier+'/false exception claim',lambda fv=fv,bad=bad:c.validate_open_return_projection(cat,fv,D(fv),bad),True,'source projection output comparison; NOT authenticated-basis core')
     u=f.projection_case(c,cat,p,('open-return:continuation','unobserved'),'UNESTABLISHED');check(tag+'/unknown continuity retained',lambda:c.open_return_projection(cat,u,D(u)))
     for name,mut in [
      ('normal pending-error flag',lambda b:b.update(terminal_python_exception_in_model=False)),
      ('invented file creation',lambda b:b.update(file_creation_established=True)),
      ('invented protocol lookup',lambda b:b.update(context_protocol_lookup_established=True)),
      ('wrong returned occurrence',lambda b:b['returned_object_role'].update(attempt='other')),
      ('coordinated returned roles',lambda b:(b['returned_object_role'].update(symbol='other'),b['context_operand']['role'].update(symbol='other'))),
      ('subclass literal key',lambda b:b.update({S('completion'):b.pop('completion')})),
      ('subclass nested string',lambda b:b['returned_object_role'].update(symbol=S(b['returned_object_role']['symbol']))),
      ('subclass nested container',lambda b:b.update(events=L(b['events']))),
      ('bool/int substitution',lambda b:b.update(open_return_established_in_model=1))]:
      bad=D(out0);mut(bad);check(tag+'/'+name,lambda bad=bad:c.validate_open_return_projection(cat,v,expect,bad),True,'source projection output/type comparison; NOT authenticated-basis core')
     for name,mut in [('omitted continuation',lambda b:b['outcomes'].pop(0)),('reordered stages',lambda b:b['outcomes'].reverse()),('wrong owner',lambda b:b['binding']['references']['owner'].update(symbol='wrong')),('wrong token',lambda b:b['binding']['references']['token'].update(symbol='wrong')),('wrong invocation',lambda b:b['scope'].update(invocation='wrong')),('wrong context',lambda b:b['scope'].update(context='other')),('wrong source',lambda b:b['binding']['attempt']['source'].update(expression='other')),('stale instance',lambda b:b['anchor']['instance'].update(binding='stale')),('subclass input mapping',lambda b:b.update(binding=M(b['binding'])))]:
      bad=D(v);mut(bad);check(tag+'/'+name,lambda bad=bad:c.open_return_projection(cat,bad,expect),True,'source projection input comparison against constructed expectation')
     # Coordinated input edits still cannot bypass source-derived stage order.
     bad=D(v);bad['outcomes'].reverse();check(tag+'/coordinated order',lambda:c.open_return_projection(cat,bad,D(bad)),True,'source projection stage-order gate')
     bad=D(p);bad['events'][-1]['id']='wrong';check(tag+'/wrong selected attempt',lambda:c.open_return_binding(cat,bad,row['anchor'],'explicit conditional premise'),True,'source binding gate')
     bad=D(p);bad['replacement_error_in_model']={'unexpected':'replacement'};check(tag+'/replacement parent frontier',lambda:c.open_return_binding(cat,bad,row['anchor'],'explicit conditional premise'),True,'source binding gate')
     def isolation():
      original=D(expect);o=c.open_return_projection(cat,v,expect);o['binding']['references'].clear();o['context_operand']['role']['scope'].clear();o['cleanup_list_state'].clear()
      assert expect==original and c.open_return_projection(cat,v,expect)==out0
      return c.validate_open_return_projection(cat,v,expect,D(out0))
     check(tag+'/nested mutable-result isolation',isolation)
     normalized=json.loads(json.dumps(out0));check(tag+'/public JSON value shape (not public validation)',lambda:c.validate_open_return_projection(cat,v,expect,normalized))
  for ctx in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   minimal={'format':'I164-OPEN-RETURN-RECONSTRUCTION-1','contexts':[{'context':x,'helper_open_attempt_correspondence':{},a.RELATION:{}} for x in a.CONTEXTS]}
   next(x for x in minimal['contexts'] if x['context']==ctx).pop(a.RELATION)
   check('missing mandatory relation '+ctx,lambda minimal=minimal:a._receipt_shape(a.enc(minimal)),True,'public pre-derivation shape gate only')
  check('adapter exact nested key type',lambda:a.exact({'x':{S('y'):None}},'TEST'),True,'adapter exact-type helper only')
  check('adapter exact nested container',lambda:a.exact({'x':M()},'TEST'),True,'adapter exact-type helper only')
 except BaseException:
  error=traceback.format_exc();(out/'failure.txt').write_text(error);print(error,file=sys.stderr,flush=True)
 finally:
  result={'attempt':'I164-OPEN-RETURN-RECONSTRUCTION-1-SOURCE-PASS-1','status':'PASS' if error is None else 'FAILED','started_utc':started,'finished_utc':utc(),'seconds':time.monotonic()-start,'rows':rows,'counts':{s:sum(r['status']==s for r in rows) for s in ('PASS','REJECTED')},'error':error,'full_public_validations':0,'authenticated_basis_captures':0,'runtime_application_calls':0,'historical_331_replayed':False,'python':sys.version,'platform':platform.platform(),'scope':'Focused new source/constructed controls only; full public and independent acceptance pending'}
  write(out/'RESULT.json',result);print('RESULT '+json.dumps({k:v for k,v in result.items() if k not in ('rows','error')},sort_keys=True),flush=True)
 return 0 if error is None else 1
if __name__=='__main__':sys.exit(run(Path(sys.argv[1]).resolve()))
