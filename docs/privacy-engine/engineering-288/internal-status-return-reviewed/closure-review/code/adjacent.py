from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class B(bytes):pass
class L(list):pass
class I(int):pass
try:
 guard(root);m=module(root/'code/correspondence.py');d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);launcher,entry=m.sources(d);fields=m.manager_fields(d);boundary=m.inner(d)['ctx']['binding'];fixtures=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases']
 rec.check('correct source declaration still validates',lambda:c.validate_status_forward(launcher,entry,fields,boundary,cat))
 for source_idx in (0,1):
  args=[launcher,entry,fields,boundary];args[source_idx]=B(args[source_idx]);rec.reject('source exact bytes '+str(source_idx),lambda:c.status_forward_source(*args),'SOURCE-TYPE')
 for key in ('manager_fields','source'):
  bad=copy.deepcopy(cat);bad={S(k) if k==key else k:v for k,v in bad.items()};rec.reject('catalogue literal key '+key,lambda:c.validate_status_forward(launcher,entry,fields,boundary,bad),'KEY-TYPE')
 bad=copy.deepcopy(cat);bad['source']['epoch_initial']=I(bad['source']['epoch_initial']);rec.reject('nested source scalar exact type',lambda:c.validate_status_forward(launcher,entry,fields,boundary,bad),'VALUE-TYPE')
 bad=copy.deepcopy(fields);bad['declarations']=L(bad['declarations']);rec.reject('source field container exact type',lambda:c.compile_status_forward(launcher,entry,bad,boundary),'VALUE-TYPE')
 bad=copy.deepcopy(boundary);bad['sites']=L(bad['sites']);rec.reject('source boundary container exact type',lambda:c.compile_status_forward(launcher,entry,fields,bad),'VALUE-TYPE')
 for fx in fixtures:
  tag=fx['context'];p=copy.deepcopy(fx['projection']);v={k:copy.deepcopy(x) for k,x in p.items() if k!='returned'};snap=copy.deepcopy(p['manager_snapshot'])
  for name in ('_phase','_reason','_epoch'):
   bad={S(k) if k==name else k:x for k,x in snap.items()};rec.reject('snapshot exact key '+name+' '+tag,lambda:c.status_snapshot_value(cat,bad),'KEY-TYPE')
  bad=copy.deepcopy(p);bad['returned'].pop();rec.reject('missing hop '+tag,lambda:c.status_forward_projection(cat,bad,v),'RETURN-LINKS')
  bad=copy.deepcopy(p);bad['returned'].reverse();rec.reject('reordered hops '+tag,lambda:c.status_forward_projection(cat,bad,v),'RETURN-LINKS')
  bad=copy.deepcopy(p);bad['returned'][1]['reference']['symbol']='another-result';rec.reject('substituted return reference '+tag,lambda:c.status_forward_projection(cat,bad,v),'RETURN-LINKS')
  bad=copy.deepcopy(p);bad['references']['control.token']['symbol']='wrong-token';badval={k:copy.deepcopy(x) for k,x in bad.items() if k!='returned'};rec.reject('coordinated wrong owner token '+tag,lambda:c.status_forward_projection(cat,bad,badval),'REFERENCE-EDGE')
  bad=copy.deepcopy(p);bad['outcomes']['manager-return']='raise';rec.reject('changed completion cannot keep normal hops '+tag,lambda:c.status_forward_projection(cat,bad,v),'PREMISE')
  bad=copy.deepcopy(cat);bad['destinations']['general_client_status']=True;rec.reject('general-client destination not source permission '+tag,lambda:c.validate_status_forward(launcher,entry,fields,boundary,bad),'SOURCE-CORRESPONDENCE')
 # Non-invoking filesystem gate: literal symlink root rejected before loading candidate.
 link=rec.path/'root-link';link.symlink_to(root,target_is_directory=True)
 rec.reject('new correction root retains symlink refusal',lambda:m.inputs(link),'CORRECTION-ROOT-TYPE')
 rec.save('symlink-record.json',{'link':str(link),'target':str(root),'purpose':'read-only root gate; not a runtime invocation'})
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent adjacent source/type/shape checks; pure constructed correspondence')
