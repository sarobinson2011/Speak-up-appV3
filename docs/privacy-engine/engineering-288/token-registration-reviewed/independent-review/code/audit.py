from pathlib import Path
import sys,json,ast,collections
sys.path.insert(0,str(Path(__file__).resolve().parent))
from archive_inspect import inspect,ident
w=Path(__file__).resolve().parents[2];out=w/'tr-review/results'
current,ci=inspect((w/'upload/I164-token-registration-correspondence-1(1).zip').read_bytes());assert ci['identity']=={'bytes':69308990,'sha256':'84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb'} and ci['entries']==2178
priorraw=(w/'upload/I164-IS01-correction(1).zip').read_bytes();prior,pi=inspect(priorraw);assert pi['identity']=={'bytes':68317556,'sha256':'5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9'}
review,ri=inspect((w/'Formal-Lab6-I164-IS01-independent-closure-review.zip').read_bytes());assert ri['identity']=={'bytes':67410780,'sha256':'6af86c83868178d81323b20705ae7c3c160da48bca29ee2d774d92be45d4e4fd'}
assert {n[16:] for n in current if n.startswith('retained/status/')}==set(prior) and all(current['retained/status/'+n]==v for n,v in prior.items())
omit='input/I164-IS01-correction.zip';assert review[omit]==priorraw
prefix='retained/closure-review/';assert {n[len(prefix):] for n in current if n.startswith(prefix)}==set(review)-{omit};assert all(current[prefix+n]==v for n,v in review.items() if n!=omit)
nested={}
def nest(es,label):
 for n,b in es.items():
  if n.endswith('.zip'):
   ee,rr=inspect(b);nested[label+n]=rr;nest(ee,label+n+'!/')
nest(current,'')
def funcs(b):
 s=b.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,ag=funcs(prior['code/managed_coverage.py']);b,bg=funcs(current['code/managed_coverage.py']);assert len(a)==78 and ag==bg and all(b[k]==v for k,v in a.items())
added=sorted(set(b)-set(a));assert added==['compile_token_registration','token_reference_premises','token_registration_projection','token_registration_source','validate_token_registration','validate_token_registration_projection']
old=prior['code/managed_coverage.py'];new=current['code/managed_coverage.py'];assert new.split(b'def token_registration_source')[0]==old.split(b'def main():')[0]
changes=json.loads(current['CHANGED-IDENTITIES.json'])
for n,pin in changes['current_components'].items():assert pin['predecessor']==ident(prior['code/'+n]) and pin['new']==ident(current['code/'+n])
assert changes['inherited_producer_functions_unchanged']==78 and changes['new_producer_functions']==added and changes['runtime_source_changes']==[]
pr=json.loads(prior['results/fresh/corrected-receipt.json']);fr=json.loads(current['results/primary/token-registration-correspondence.json'])
assert all(fr[k]==v for k,v in pr.items() if k not in ('format','contexts','extension_components'))
assert fr['prior_internal_status_components']==pr['extension_components'] and fr['prior_internal_status_receipt']==ident(prior['results/fresh/corrected-receipt.json'])
for p,f in zip(pr['contexts'],fr['contexts']):assert set(f)==set(p)|{'token_registration_correspondence'} and all(f[k]==v for k,v in p.items())
assert [r['context'] for r in fr['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'];assert fr['unchanged_obligations']==pr['unchanged_obligations'] and fr['inventory_unknown_totals']==4 and fr['lifetime_unknown_totals']==14
pins=json.loads(current['MANIFEST.json']);op=[n for n,v in pins.items() if v==fr['unchanged_obligations']];assert len(op)==1;ob=json.loads(current[op[0]]);assert [x['id'] for x in ob['obligations']]==[f'O{i:02d}' for i in range(1,12)]
supplied={}
for name,count in [('primary',285),('fresh',14),('recovered',50),('recovered-cli',1)]:
 p='results/'+name+'/';r=json.loads(current[p+'RESULT.json']);assert r['result']=='PASS' and r['checks']==count and r['error'] is None
 lines=[json.loads(x) for x in current[p+'progress.jsonl'].decode().splitlines()];assert len(lines)==count and r['rows']==lines
 supplied[name]={'checks':count,'outcomes':dict(collections.Counter(x['result'] for x in lines)),'identity':ident(current[p+'RESULT.json']),'inspected_not_rerun':True,'labels':[x['check'] for x in lines]}
recm=json.loads(current['provenance/recovery-input-MANIFEST.json']);assert all(ident(current[n])==v for n,v in recm.items())
rr=json.loads(current['provenance/recovery-input-identity.json'])
r={'result':'PASS','input':ci,'nested_archives':nested,'prior_archive':pi['identity'],'prior_review':ri['identity'],'preserved_predecessor_members':2053,'preserved_review_noninput_members':80,'inherited_producer_functions_unchanged':78,'new_producer_functions':added,'historical_validators_and_runtime_sources_unchanged':True,'current_components':changes['current_components'],'current_receipt':ident(current['results/primary/token-registration-correspondence.json']),'all_prior_context_fields_relationships_ordinals_findings_unchanged':True,'obligations':11,'supplied':supplied,'supplied_recovery_input_selection_members':len(recm),'supplied_intermediate_outer_identity':rr,'supplied_intermediate_outer_newly_verified':False,'historical_compact_recovery_and_failed_attempt_qualifications':'Preserved unchanged. Forensic snapshot manifests and compact omissions are not new runtime dependencies.'}
(out/'composition.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('input','nested_archives','supplied','current_components')},indent=2))
