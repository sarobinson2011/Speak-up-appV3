from pathlib import Path
import sys,json,ast,difflib,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None
receipt=json.loads((root/'results/primary/control-construction.json').read_bytes())
try:
 # Declared byte changes and all inherited function bodies are read-only comparisons.
 changes=json.loads((root/'provenance/changed-files.json').read_bytes());diff='';definitions={}
 for n in ('code/managed_coverage.py','code/correspondence.py'):
  pins=changes['intentional_changes'][n]
  before=(root/'retained/control'/n).read_bytes();after=(root/n).read_bytes();assert identity(before)==pins['before'] and identity(after)==pins['after']
  diff+=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='retained/control/'+n,tofile=n))
  if n.endswith('managed_coverage.py'):
   oldtree=ast.parse(before);newtree=ast.parse(after);oldf={x.name:x for x in oldtree.body if isinstance(x,ast.FunctionDef)};newf={x.name:x for x in newtree.body if isinstance(x,ast.FunctionDef)}
   assert len(oldf)==117 and len(newf)-len(oldf)==6
   for name,f in oldf.items():assert ast.get_source_segment(before.decode(),f)==ast.get_source_segment(after.decode(),newf[name]),name
   assert ast.dump(ast.Module(body=[x for x in oldtree.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]))==ast.dump(ast.Module(body=[x for x in newtree.body if not isinstance(x,ast.FunctionDef)],type_ignores=[]))
   definitions={'inherited_unchanged':117,'new':sorted(set(newf)-set(oldf))}
 assert diff==(root/'provenance/implementation.diff').read_text()
 for n in ('prospective_entry.py','lab_bootstrap.py'):assert (root/'source-evidence'/n).read_bytes()==(root/'retained/control/source-evidence'/n).read_bytes()
 # Reconcile actual supplied logs without re-executing them.
 supplied={}
 def parse_printed(p):
  rows=[]
  for line in p.read_text().splitlines():
   a=line.split(' ',1)
   if len(a)==2 and a[0].isdigit():
    name,status=a[1].rsplit(' ',1);rows.append((int(a[0]),name,status))
  return rows
 for label,stem,n in [('primary-interrupted','failures/interrupted-processes/primary',285),('completion-interrupted','failures/interrupted-completion',71)]:
  p=root/stem;progress=[json.loads(s) for s in (p/'results/progress.jsonl').read_text().splitlines()];stdout=parse_printed(p/'processes/stdout.log');assert len(progress)==len(stdout)==n
  assert [(i+1,x['check'],x['result']) for i,x in enumerate(progress)]==stdout
  assert not (p/'results/RESULT.json').exists() and not (p/'processes/exit-status.json').exists()
  supplied[label]={'corroborated_rows':n,'complete_group':False,'result_and_exit':'UNRECOVERED'}
 for label in ('source-completion','public-final-completion'):
  result=json.loads((root/'results'/label/'RESULT.json').read_bytes());progress=[json.loads(s) for s in (root/'results'/label/'progress.jsonl').read_text().splitlines()];stdout=parse_printed(root/'processes'/label/'stdout.log');ex=json.loads((root/'processes'/label/'exit-status.json').read_bytes())
  assert result['checks']==1 and len(progress)==len(stdout)==1 and result['rows']==progress
  assert [(1,progress[0]['check'],progress[0]['result'])]==stdout and ex['returncode']==0 and ex['timed_out'] is False
  supplied[label]={'checks':1,'rows':progress,'exit':ex,'separate_completed_group':True}
 rej=json.loads((root/'results/public-final-completion/validator-rejection.json').read_bytes());supplied['final_rejection_layer']='Public post-derivation receipt comparison only';supplied['saved_public_rejection']=rej
 assert 'CONSTRUCTION-STALE-OR-ALTERED-RECEIPT' in json.dumps(rej)
 limits=receipt['new_control_construction_limits'];assert limits['inventory_unknown_totals']==4 and limits['lifetime_unknown_totals']==14 and limits['all_eleven_obligations_preserved'] is True and limits['actual_admission'] is False
 r.save('preservation-and-supplied.json',{'definitions':definitions,'declared_diff_exact':True,'runtime_sources_unchanged':True,'all_old_context_fields_unchanged':True,'supplied':supplied,'scope_limits':limits,'intermediate_cut_original_outer_identity_freshly_verified':False,'prior_qualified_accounting':json.loads((root/'retained/review/CHECKPOINT.json').read_bytes())['prior_accounting']})
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,controls_reexecuted=0,scope='Read-only preservation and supplied-record audit after preserved diff-order harness failure')
