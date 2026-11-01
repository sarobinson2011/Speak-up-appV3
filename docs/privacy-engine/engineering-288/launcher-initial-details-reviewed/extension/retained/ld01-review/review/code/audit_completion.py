from pathlib import Path
import sys,json,ast,difflib,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None
receipt=json.loads((root/'results/primary/launcher-details.json').read_bytes());old=json.loads((root/'retained/client-construction/results/primary/client-construction-none.json').read_bytes())
try:
 changes=json.loads((root/'provenance/changed-files.json').read_bytes());diff=''
 for n in ('code/managed_coverage.py','code/correspondence.py'):
  a=(root/'retained/client-construction'/n).read_bytes();b=(root/n).read_bytes();assert identity(a)==changes['intentional_changes'][n]['before'] and identity(b)==changes['intentional_changes'][n]['after']
  diff+=''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='reviewed/'+Path(n).name,tofile='proposed/'+Path(n).name))
  if n.endswith('managed_coverage.py'):
   assert b==a+b'\n'+(root/'tools/producer-addition.py').read_bytes();aa=ast.parse(a);bb=ast.parse(b);assert len(bb.body)==len(aa.body)+6 and sum(isinstance(x,ast.FunctionDef) for x in aa.body)==129 and all(ast.dump(x)==ast.dump(y) for x,y in zip(aa.body,bb.body))
 assert diff==(root/'provenance/implementation.diff').read_text()
 for n in ('prospective_entry.py','lab_bootstrap.py'):assert (root/'source-evidence'/n).read_bytes()==(root/'retained/client-construction/source-evidence'/n).read_bytes()
 allowed={'format','extension_components','contexts'}
 assert receipt['prior_client_construction_components']==old['extension_components']
 for k,v in old.items():
  if k not in allowed:assert receipt[k]==v,k
 supplied={}
 for label,n in [('source-corrected',66),('primary',862),('recovered',391)]:
  result=json.loads((root/'results'/label/'RESULT.json').read_bytes());progress=[json.loads(x) for x in (root/'results'/label/'progress.jsonl').read_text().splitlines()];out=[]
  for line in (root/'processes'/label/'stdout.log').read_text().splitlines():
   part=line.split(' ',1)
   if len(part)==2 and part[0].isdigit():a,b=part[1].rsplit(' ',1);out.append((int(part[0]),a,b))
  ex=json.loads((root/'processes'/label/'exit-status.json').read_bytes());assert result['result']=='PASS' and result['checks']==n and result['rows']==progress and len(progress)==len(out)==n and [(i+1,x['check'],x['result']) for i,x in enumerate(progress)]==out and ex['returncode']==0 and not ex['timed_out']
  supplied[label]={'controls':n,'result_identity':identity((root/'results'/label/'RESULT.json').read_bytes()),'exit':ex,'scope':result['scope']}
 failure=json.loads((root/'failures/source-initial/results/RESULT.json').read_bytes());assert failure['checks']==0 and json.loads((root/'failures/source-initial/processes/exit-status.json').read_bytes())['returncode']==1
 r.save('preservation-and-supplied.json',{'inherited_producer_functions':129,'new_functions':6,'producer_prefix_bytes_exact':True,'declared_diff_exact':True,'runtime_sources_unchanged':True,'all_prior_context_fields_preserved':True,'prior_envelope_preserved_except_declared_extension':True,'supplied':supplied,'supplied_failures':{n:(root/n).read_text() for n in ('failures/source-initial/RECORD.json','failures/recovery-cut-preparation/RECORD.json','failures/preparation-textencoder/RECORD.txt')},'historical_qualifications':json.loads((root/'provenance/prior-review-incorporation.json').read_bytes()),'limits':receipt['new_launcher_details_limits']})
 r.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,controls_reexecuted=0,scope='Complete only unfinished read-only preservation/supplied-record audit after retained reviewer separator assumption failure')
