from pathlib import Path
import sys,ast,json,difflib,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from archive_inspect import inspect,ident
w=Path(__file__).resolve().parents[2];root=w/'is01-input';out=w/'is01-review/results'
current,ci=inspect((w/'upload/I164-IS01-correction(1).zip').read_bytes());assert ci['identity']=={'bytes':68317556,'sha256':'5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9'}
prior,pi=inspect((w/'upload/I164-internal-status-return-correspondence-1(1).zip').read_bytes());assert pi['identity']=={'bytes':62835317,'sha256':'06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864'}
review,ri=inspect((w/'Formal-Lab6-I164-internal-status-return-correspondence-independent-review.zip').read_bytes());assert ri['identity']=={'bytes':66394354,'sha256':'b8135042b4638af1acebfd90ac07ba4aea844853148f8ce0c99804cac8643334'}
assert {n[9:] for n in current if n.startswith('original/')}==set(prior)
assert all(current['original/'+n]==v for n,v in prior.items())
omit='input/I164-internal-status-return-correspondence-1.zip';assert review[omit]==(w/'upload/I164-internal-status-return-correspondence-1(1).zip').read_bytes()
assert {n[7:] for n in current if n.startswith('review/')}==set(review)-{omit}
assert all(current['review/'+n]==v for n,v in review.items() if n!=omit)
nested={}
def nest(es,label):
 for n,b in es.items():
  if n.endswith('.zip'):
   ee,rr=inspect(b);nested[label+n]=rr;nest(ee,label+n+'!/')
nest(current,'')
def functions(raw):
 s=raw.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,ag=functions(current['original/code/managed_coverage.py']);b,bg=functions(current['code/managed_coverage.py']);changed=sorted(k for k in a if a[k]!=b[k]);added=sorted(set(b)-set(a));assert added==['status_exact_tree','status_typed_same']
assert changed==['status_forward_projection','status_forward_source','status_snapshot_value','validate_status_forward','validate_status_forward_projection'];assert ag==bg
historical,hg=functions(current['original/retained/state/code/managed_coverage.py']);assert len(historical)==70 and all(b[k]==v for k,v in historical.items()) and bg==hg
assert current['code/managed_coverage.py'].split(b'def status_exact_tree')[0]==current['original/code/managed_coverage.py'].split(b'def status_forward_source')[0]
cid=json.loads(current['CHANGED-IDENTITIES.json'])
for n,v in cid['intentional_implementation_changes'].items():
 assert ident(current['original/code/'+n])==v['before'] and ident(current['code/'+n])==v['after']
 diff=''.join(difflib.unified_diff(current['original/code/'+n].decode().splitlines(True),current['code/'+n].decode().splitlines(True),fromfile='original/code/'+n,tofile='code/'+n))
 assert diff.encode()==current['provenance/'+n+'.diff']
assert ident(current['provenance/primary-correspondence.py'])==cid['primary_adapter_before_root_guard']
primary=current['provenance/primary-correspondence.py'].decode();final=current['code/correspondence.py'].decode();assert final.replace(" require(stat.S_ISDIR(Path(root).lstat().st_mode),'CORRECTION-ROOT-TYPE')\n",'')==primary
oldr=json.loads(current['original/results/status-forward-correspondence.json']);fresh=json.loads(current['results/fresh/corrected-receipt.json']);assert oldr.keys()==fresh.keys() and all(oldr[k]==fresh[k] for k in oldr if k!='extension_components')
assert fresh['extension_components']=={n:ident(current['code/'+n]) for n in ('managed_coverage.py','correspondence.py')}
assert len(fresh['contexts'])==2 and len(fresh['unchanged_obligations'])==11 and fresh['inventory_unknown_totals']==4 and fresh['lifetime_unknown_totals']==14
supplied={}
for name,count in [('original-witnesses',14),('primary',268),('fresh',21),('recovered-focused',269),('recovered-public',2)]:
 p='results/'+name+'/';v=json.loads(current[p+'RESULT.json']);lines=[json.loads(s) for s in current[p+'progress.jsonl'].decode().splitlines()];assert v['checks']==count and v['rows']==lines and len(lines)==count and v['error'] is None and v['result']=='PASS'
 supplied[name]={'checks':count,'identity':ident(current[p+'RESULT.json']),'outcomes':{k:sum(r['result']==k for r in lines) for k in set(r['result'] for r in lines)},'inspected_not_rerun':True,'labels':[r['check'] for r in lines]}
recm=json.loads(current['provenance/recovery-input-manifest.json']);assert all(ident(current[n])==v for n,v in recm.items())
recraw=(json.dumps(recm,indent=2,sort_keys=True)+'\n').encode();lineage=json.loads(current['RECOVERY-LINEAGE.json']);assert ident(recraw)==lineage['decoded_manifest_identity']
result={'result':'PASS','input':ci,'present_nested_archives':nested,'prior_archive':pi['identity'],'review_archive':ri['identity'],'original_members_unchanged':len(prior),'review_noninput_members_unchanged':len(review)-1,'inherited_functions_unchanged':70,'changed_producer_functions':changed,'added_producer_functions':added,'current_components':cid,'runtime_sources_unchanged':True,'unrelated_historical_validators_unchanged':True,'receipt_only_current_component_identities_changed':True,'receipt':ident(current['results/fresh/corrected-receipt.json']),'obligations':11,'supplied_results':supplied,'supplied_recovery_manifest_selection_verified':len(recm),'supplied_intermediate_outer_archive_newly_verified':False,'historical_qualifications':'Preserved unchanged; compact omitted outer archives/forensic manifests are not new executable requirements. Exact original/review outer bytes verified locally; not reconstructed.','prior_failures_preserved':True}
(out/'composition.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('input','present_nested_archives','supplied_results','current_components')},indent=2))
