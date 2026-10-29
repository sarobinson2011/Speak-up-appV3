"""Read-only composition audit. No supplied or completed control suite execution."""
from pathlib import Path
import ast,collections,difflib,json,sys,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from archive_inspect import inspect,ident
w=Path(__file__).resolve().parents[2];out=w/'ol-review/results'
current,ci=inspect((w/'upload/I164-owner-lock-finalization-correspondence-1(1).zip').read_bytes());assert ci['identity']=={'bytes':74161617,'sha256':'09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b'} and ci['entries']==2495
priorpath=w/'upload/I164-normal-session-exit-correspondence-1(1).zip';reviewpath=w/'Formal-Lab6-I164-normal-session-exit-independent-review.zip'
priorraw=priorpath.read_bytes();reviewraw=reviewpath.read_bytes();assert ident(priorraw)=={'bytes':70593959,'sha256':'c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a'} and ident(reviewraw)=={'bytes':71870780,'sha256':'c6c1952bde68aef3e9434968cd8838cfcbd4ab606e39fcaba112e6f73dada3df'}
with zipfile.ZipFile(priorpath) as z:prior={n:z.read(n) for n in z.namelist()}
with zipfile.ZipFile(reviewpath) as z:review={n:z.read(n) for n in z.namelist()}
assert len(prior)==2331 and {n.removeprefix('retained/exit/') for n in current if n.startswith('retained/exit/')}==set(prior)
assert all(current['retained/exit/'+n]==b for n,b in prior.items())
omit='input/I164-normal-session-exit-correspondence-1.zip';assert review[omit]==priorraw and len(review)==104
assert {n.removeprefix('retained/review/') for n in current if n.startswith('retained/review/')}==set(review)-{omit}
assert all(current['retained/review/'+n]==b for n,b in review.items() if n!=omit)
assert current['provenance/prior-review.json']==review['CHECKPOINT.json']
def funcs(raw):
 s=raw.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
old,og=funcs(prior['code/managed_coverage.py']);new,ng=funcs(current['code/managed_coverage.py']);changes=json.loads(current['provenance/changed-files.json']);assert len(old)==89 and og==ng and all(new[k]==v for k,v in old.items())
added=sorted(set(new)-set(old));assert changes['added_producer_functions']==added and changes['unchanged_inherited_functions_and_classes']==89
prefix=prior['code/managed_coverage.py'].split(b'def main():')[0];newprefix=current['code/managed_coverage.py'].split(b'def owner_finalization_source')[0];assert newprefix.startswith(prefix) and all(not line.strip() or line.lstrip().startswith(b'#') for line in newprefix[len(prefix):].splitlines())
diff=''
for n in ['code/managed_coverage.py','code/correspondence.py']:
 pins=changes['intentional_implementation_changes'][n];assert pins['current']==ident(current[n]) and pins['previous']==ident(prior[n])
 diff+=''.join(difflib.unified_diff(prior[n].decode().splitlines(True),current[n].decode().splitlines(True),fromfile='reviewed-exit/'+n,tofile='owner-finalization/'+n))
assert current['provenance/intentional.diff']==diff.encode()
sources={}
for n in ['lab_bootstrap.py','live_connection.py','prospective_entry.py']:
 assert current['source-evidence/'+n]==prior['source-evidence/'+n];sources[n]=ident(current['source-evidence/'+n])
op='results/primary/normal-session-exit-correspondence.json';np='results/primary/owner-lock-finalization.json';a=json.loads(prior[op]);b=json.loads(current[np])
assert all(b[k]==v for k,v in a.items() if k not in ('format','contexts','extension_components')) and b['prior_normal_exit_components']==a['extension_components'] and b['prior_normal_exit_receipt']==ident(prior[op])
for x,y in zip(a['contexts'],b['contexts']):assert set(y)==set(x)|{'owner_lock_finalization_correspondence'} and all(y[k]==v for k,v in x.items())
assert [x['context'] for x in b['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
pins=json.loads(current['MANIFEST.json']);obpaths=[n for n,v in pins.items() if v==b['unchanged_obligations']];assert len(obpaths)==1;ob=json.loads(current[obpaths[0]]);assert [x['id'] for x in ob['obligations']]==[f'O{i:02d}' for i in range(1,12)]
supplied={}
for name,count in [('primary',218),('recovered',57),('semantic',2),('derive',2),('constructed',2),('public',3)]:
 p='results/'+name+'/';r=json.loads(current[p+'RESULT.json']);lines=[json.loads(x) for x in current[p+'progress.jsonl'].decode().splitlines()];assert r['result']=='PASS' and r['error'] is None and r['checks']==count and r['rows']==lines and len(lines)==count
 supplied[name]={'checks':count,'outcomes':dict(collections.Counter(x['result'] for x in lines)),'identity':ident(current[p+'RESULT.json']),'labels':[x['check'] for x in lines],'inspected_not_rerun':True}
failed=json.loads(current['failures/derive-attempt-1/ATTEMPT.json']);assert failed['completed_assertions']==0 and failed['exit_code']==137 and failed['cause']=='UNESTABLISHED' and failed['counted_in_completed_totals'] is False
rec=json.loads(current['provenance/recovery-cut-manifest.json']);assert len(rec)==2459 and all(ident(current[n])==pin for n,pin in rec.items())
extra='retained/review/failures/recovered-membership/forensic-extra.bin';assert ident(current[extra])=={'bytes':25690112,'sha256':'ed75ee885f67eca2938340b1aa5c423a9e60c04bceedfd3f90933cba0c44345e'}
nested={}
def descend(es,prefix=''):
 for n,b in es.items():
  if n.endswith('.zip'):
   xx,rr=inspect(b);nested[prefix+n]=rr;descend(xx,prefix+n+'!/')
descend(current)
result={'result':'PASS','current_archive':ci,'reused_verified_prior_archive':ident(priorraw),'reused_verified_prior_review_archive':ident(reviewraw),'preserved_predecessor_members':len(prior),'preserved_prior_review_noninput_members':len(review)-1,'present_nested_archives':nested,'inherited_producer_functions_unchanged':len(old),'added_functions':added,'declared_changes_and_exact_diff':'PASS','runtime_sources_changed':0,'source_identities':sources,'all_prior_context_fields_historical_identities_relationships_ordinals_findings_unchanged':True,'obligations':11,'obligations_identity':b['unchanged_obligations'],'inventory_unknown_totals':b['inventory_unknown_totals'],'lifetime_unknown_totals':b['lifetime_unknown_totals'],'new_receipt':ident(current[np]),'supplied':supplied,'supplied_failed_attempt':failed,'supplied_recovery_cut_selection_members':len(rec),'supplied_recovery_cut_all_member_bytes_unchanged':True,'supplied_recovery_cut_manifest_identity':ident(current['provenance/recovery-cut-manifest.json']),'supplied_recovery_cut_outer_identity':json.loads(current['provenance/recovery-cut-identity.json']),'supplied_recovery_cut_outer_newly_verified':False,'historical_forensic_partial_identity':ident(current[extra]),'historical_forensic_partial_outside_strict_predecessor':True,'historical_compact_omissions':'Recorded in manifest audit; unchanged prior recovery qualifications reused, not erased'}
(out/'composition.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('current_archive','present_nested_archives','supplied')},indent=2))
