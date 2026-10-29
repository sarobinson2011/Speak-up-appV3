"""Integrity/composition audit; inspects supplied records without executing their suites."""
from pathlib import Path
import ast,collections,difflib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from archive_inspect import inspect,ident
w=Path(__file__).resolve().parents[2];root=w/'ns-input';out=w/'ns-review/results'
current,ci=inspect((w/'upload/I164-normal-session-exit-correspondence-1(1).zip').read_bytes())
assert ci['identity']=={'bytes':70593959,'sha256':'c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a'} and ci['entries']==2331
pm=json.loads(current['retained/token/MANIFEST.json']);assert ident(current['retained/token/MANIFEST.json'])=={'bytes':577591,'sha256':'37bed36d549e530632d0939e379f53a49815a3145f30e13d49256de08397bf6a'}
assert {n.removeprefix('retained/token/') for n in current if n.startswith('retained/token/')}==set(pm)|{'MANIFEST.json'}
for n,pin in pm.items():assert ident(current['retained/token/'+n])==pin
rm=json.loads(current['retained/review/MANIFEST.json']);omitted='input/I164-token-registration-correspondence-1.zip'
assert rm[omitted]=={'bytes':69308990,'sha256':'84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb'}
assert {n.removeprefix('retained/review/') for n in current if n.startswith('retained/review/')}==(set(rm)-{omitted})|{'MANIFEST.json'}
assert current['provenance/prior-review.json']==current['retained/review/CHECKPOINT.json']
for n,pin in rm.items():
 if n!=omitted:assert ident(current['retained/review/'+n])==pin
def funcs(raw):
 s=raw.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,ag=funcs(current['retained/token/code/managed_coverage.py']);b,bg=funcs(current['code/managed_coverage.py']);assert len(a)==84 and ag==bg and all(b[k]==v for k,v in a.items())
added=sorted(set(b)-set(a));changes=json.loads(current['provenance/changed-files.json']);assert changes['unchanged_inherited_functions_and_classes']==len(a) and changes['added_functions']==added
assert current['code/managed_coverage.py'].split(b'def session_exit_source')[0]==current['retained/token/code/managed_coverage.py'].split(b'def main():')[0]
actualdiff=''
for n,pins in changes['intentional_implementation_changes'].items():
 assert pins['previous']==ident(current['retained/token/'+n]) and pins['current']==ident(current[n])
 actualdiff+=''.join(difflib.unified_diff(current['retained/token/'+n].decode().splitlines(True),current[n].decode().splitlines(True),fromfile='reviewed-token/'+n,tofile='normal-session-exit/'+n))
assert actualdiff.encode()==current['provenance/intentional.diff']
for n,pin in json.loads(current['source-evidence/identities.json']).items():assert ident(current['source-evidence/'+n])==pin
old=json.loads(current['retained/token/results/primary/token-registration-correspondence.json']);new=json.loads(current['results/primary/normal-session-exit-correspondence.json'])
assert all(new[k]==v for k,v in old.items() if k not in ('format','contexts','extension_components'))
assert new['prior_token_components']==old['extension_components'] and new['prior_token_receipt']==ident(current['retained/token/results/primary/token-registration-correspondence.json'])
for x,y in zip(old['contexts'],new['contexts']):assert set(y)==set(x)|{'normal_session_exit_correspondence'} and all(y[k]==v for k,v in x.items())
assert [c['context'] for c in new['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
pins=json.loads(current['MANIFEST.json']);ops=[n for n,v in pins.items() if v==new['unchanged_obligations']];assert len(ops)==1
ob=json.loads(current[ops[0]]);assert [x['id'] for x in ob['obligations']]==[f'O{i:02d}' for i in range(1,12)]
supplied={}
for name,count in [('primary',235),('constructed',2),('derive',2),('semantic',2),('validate',3),('recovered',35)]:
 p='results/'+name+'/';r=json.loads(current[p+'RESULT.json']);lines=[json.loads(x) for x in current[p+'progress.jsonl'].decode().splitlines()]
 assert r['result']=='PASS' and r['checks']==count and r['error'] is None and r['rows']==lines and len(lines)==count
 supplied[name]={'checks':count,'outcomes':dict(collections.Counter(x['result'] for x in lines)),'identity':ident(current[p+'RESULT.json']),'inspected_not_rerun':True,'labels':[x['check'] for x in lines]}
failed=json.loads(current['results/attempt-1/RESULT.json']);assert failed['result']=='FAIL' and failed['checks']==0 and failed['rows']==[]
for n in current:
 if n.startswith('results/attempt-2/'):assert current[n]==current[n.replace('results/attempt-2/','results/primary/',1)]
recm=json.loads(current['provenance/recovery-cut-manifest.json']);assert len(recm)==2297
for n,pin in recm.items():assert ident(current[n])==pin
nested={}
def descend(es,prefix=''):
 for n,b in es.items():
  if n.endswith('.zip'):
   zz,rr=inspect(b);nested[prefix+n]=rr;descend(zz,prefix+n+'!/')
descend(current)
r={'result':'PASS','current_archive':ci,'preserved_token_members':len(pm)+1,'preserved_prior_review_noninput_members':len(rm),'prior_outer_archives_newly_verified':False,'prior_outer_identity_reused_from_verified_checkpoint':True,'present_nested_archives':nested,'inherited_producer_functions_unchanged':len(a),'added_functions':added,'declared_changes_and_exact_diff':'PASS','runtime_sources_changed':0,'all_prior_context_fields_historical_identities_relationships_ordinals_findings_unchanged':True,'obligations':11,'obligations_identity':new['unchanged_obligations'],'inventory_unknown_totals':new['inventory_unknown_totals'],'lifetime_unknown_totals':new['lifetime_unknown_totals'],'new_receipt':ident(current['results/primary/normal-session-exit-correspondence.json']),'source_identities':json.loads(current['source-evidence/identities.json']),'supplied':supplied,'supplied_failed_instrumentation_attempt':failed,'supplied_intermediate_selection_members_verified':len(recm),'supplied_intermediate_outer_identity':json.loads(current['provenance/recovery-cut-identity.json']),'supplied_intermediate_outer_newly_verified':False,'historical_compact_omissions':'Recorded separately in manifest audit; no missing current recovery dependency inferred from an intentionally compact forensic snapshot'}
(out/'composition.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('current_archive','present_nested_archives','supplied','supplied_failed_instrumentation_attempt')},indent=2))
