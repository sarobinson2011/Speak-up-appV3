from pathlib import Path
import ast,copy,json,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
r=Record(sys.argv[2]);root=Path(sys.argv[1]);failure=None
try:
 guard(root,r.path);c=module(root/'code/managed_coverage.py');raws=[(root/'source-evidence'/n).read_bytes() for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py')]
 old=json.loads((root/'retained/details/ld01/receipts/corrected-launcher-details.json').read_bytes());row=old['contexts'][0];details=row['launcher_initial_details_correspondence']['declaration'];reference=row['reference_declarations'];cat=c.compile_cleanup_append(*raws,details,reference)
 r.check('static catalogue accepts exact retained defining sources',lambda:c.validate_cleanup_append(*raws,details,reference,cat))
 tree=ast.parse(raws[0]);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session');handler=fn.body[-1].body[-1].handlers[0];loop=handler.body[1];guard_=loop.body[0];tr=guard_.body[0];close,append=tr.body
 r.check('independent source ordered raw then managed inputs',lambda:[[ast.literal_eval(t.elts[0]),t.elts[1].id] for t in loop.iter.elts]==[['raw','raw'],['managed','managed']])
 r.check('independent exact identity guard',lambda:isinstance(guard_.test.ops[0],ast.IsNot) and guard_.test.comparators[0].value is None)
 r.check('same protected suite contains close then append',lambda:[ast.unparse(n) for n in tr.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"])
 r.check('normal close result discarded',lambda:isinstance(close,ast.Expr) and not close.value.args and not close.value.keywords)
 expected=[]
 def add(n):expected.append(n)
 add('loop-input-evaluation')
 for pair in loop.iter.elts:
  label=pair.elts[0].value
  for part in ('name','object','pair'):add('input-'+label+'-'+part)
 expected+=['loop-inputs-complete','loop-iterator-attempt']
 for pair in loop.iter.elts:
  label=pair.elts[0].value;add(label+'-item-next')
  for t in loop.target.elts:add(label+'-bind-'+t.id)
  for p in ('object','none','result'):add(label+'-guard-'+p)
 expected+=['selected-try-entry','close-object-evaluation','close-method-evaluation','close-call-attempt','close-normal-return','append-details-evaluation','append-key-evaluation','append-list-resolution','append-method-evaluation','append-item-name','append-item-message','append-item-complete','append-call-attempt','append-complete']
 r.check('independent source-order coverage',lambda:cat['source']['order']==expected and [x['id'] for x in cat['declarations']]==expected)
 r.check('selected managed guard and discarded raw selection',lambda:cat['source']['guard_results']=={'raw':False,'managed':True} and cat['source']['selected_name']=='managed')
 for stage in expected:
  bad=copy.deepcopy(cat);bad['source']['order'].remove(stage);bad['declarations']=[x for x in bad['declarations'] if x['id']!=stage];del bad['source']['stages'][stage]
  r.reject('coordinated missing stage '+stage,lambda bad=bad:c.validate_cleanup_append(*raws,details,reference,bad))
 for old,new in [("[('raw',raw),('managed',managed)]","[('managed',managed),('raw',raw)]"),('if obj is not None:','if obj:'),("[name,'close returned']","[name,'closed']"),('try:obj.close();details','try:obj.state();details')]:
  changed=raws[0].replace(old.encode(),new.encode());assert changed!=raws[0]
  r.reject('defining source substitution '+old,lambda changed=changed:c.compile_cleanup_append(changed,raws[1],raws[2],details,reference))
 r.save('catalogue.json',cat);r.save('independent-stage-expectations.json',{'source_ast_order':expected,'close_line':close.lineno,'append_line':append.lineno,'error_handler_line':tr.handlers[0].lineno})
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='New static source controls only; no predecessor validation or runtime execution')
