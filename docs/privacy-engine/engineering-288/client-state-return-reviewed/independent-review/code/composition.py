"""Read-only byte/provenance audit; no predecessor campaign execution."""
from pathlib import Path,PurePosixPath
import ast,hashlib,io,json,stat,zipfile
ROOT=Path('cs-input');OUT=Path('cs-review/results')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def inspect(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  inf=z.infolist();names=[i.filename for i in inf];assert len(names)==len(set(names)) and z.testzip() is None
  for i in inf:
   n=i.filename;p=PurePosixPath(n);assert str(p)==n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and '\\' not in n and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  es={n:z.read(n) for n in names};rawm=json.loads(es['MANIFEST.json']);m=rawm.get('members',rawm);assert set(m)==set(es)-{'MANIFEST.json'}
  for n,p in m.items():assert ident(es[n])==p,n
  manifests=[]
  for n,b in es.items():
   if n.endswith('MANIFEST.json'):
    r=json.loads(b);r=r.get('members',r);prefix=n[:-len('MANIFEST.json')]
    if isinstance(r,dict) and all(isinstance(v,dict) and set(v)=={'bytes','sha256'} for v in r.values()):
     missing=[p for p in r if prefix+p not in es]
     for p,v in r.items():
      if prefix+p in es:assert ident(es[prefix+p])==v,(n,p)
     manifests.append({'manifest':n,'verified_present':len(r)-len(missing),'absent':missing})
  return es,{'identity':ident(raw),'entries':len(es),'CRC':'PASS','safe_exact_membership':'PASS','manifests':manifests}
prior_path=Path('cs-prior/Formal-Lab6-I164-outside-catch-classification-correction-independent-review.zip');prior_bytes=prior_path.read_bytes();assert ident(prior_bytes)=={'bytes':60073099,'sha256':'7c64e87084d3b7a2257794486198b35d2ba40ebdaefb272424a0e8c7e04a7759'}
review,rid=inspect(prior_bytes);assert len(review)==134;omitted='input/I164-outside-catch-classification-correction-1.zip';oldraw=review[omitted];assert ident(oldraw)=={'bytes':60424906,'sha256':'08499f314151aef36bdbe711ad6f821bf1258d28a8c0d65fd693e3b0db4a3ba5'}
old,oid=inspect(oldraw);assert len(old)==1508
for n,b in old.items():assert (ROOT/'retained/client'/n).read_bytes()==b,n
assert {p.relative_to(ROOT/'retained/client').as_posix() for p in (ROOT/'retained/client').rglob('*') if p.is_file()}==set(old)
for n,b in review.items():
 if n!=omitted:assert (ROOT/'retained/review'/n).read_bytes()==b,n
assert {p.relative_to(ROOT/'retained/review').as_posix() for p in (ROOT/'retained/review').rglob('*') if p.is_file()}==set(review)-{omitted}
# All currently present archived dependency bytes are covered. Absent nested compact-manifest entries stay explicit.
current_raw=Path('upload/I164-client-state-return-correspondence-1(1).zip').read_bytes();current,cid=inspect(current_raw);nested={}
def descend(es,label):
 for n,b in es.items():
  if n.endswith('.zip'):
   child,res=inspect(b);nested[label+n]=res;descend(child,label+n+'!/')
descend(current,'')
oldsrc=old['code/managed_coverage.py'].decode();newsrc=current['code/managed_coverage.py'].decode();a=ast.parse(oldsrc);b=ast.parse(newsrc);af={n.name:n for n in a.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};bf={n.name:n for n in b.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};assert len(af)==62 and af.keys()<=bf.keys()
assert all(ast.get_source_segment(oldsrc,n)==ast.get_source_segment(newsrc,bf[k]) for k,n in af.items())
assert [ast.dump(n,include_attributes=False) for n in a.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]==[ast.dump(n,include_attributes=False) for n in b.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
added=sorted(bf.keys()-af.keys());assert added==sorted(['_data_graph_value','client_state_projection','client_state_source','compile_client_state','data_source_domain','validate_client_state','validate_client_state_projection','validate_data_detachment'])
prior=json.loads(old['results/client-handle-correspondence.json']);now=json.loads(current['results/client-state-correspondence.json']);assert now['prior_client_handle_components']==prior['extension_components'] and now['prior_client_handle_receipt']==ident(old['results/client-handle-correspondence.json'])
for k,v in prior.items():
 if k not in ('format','extension_components','contexts'):assert now[k]==v,k
for x,y in zip(now['contexts'],prior['contexts']):
 assert set(x)==set(y)|{'client_state_return_correspondence'}
 assert all(x[k]==v for k,v in y.items())
assert now['unchanged_obligations']==prior['unchanged_obligations'] and now['inventory_unknown_totals']==4 and now['lifetime_unknown_totals']==14
supplied={}
for label,num in [('primary',171),('recovered',173)]:
 p=ROOT/'results'/label;r=read(p/'RESULT.json');rows=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()];assert r['result']=='PASS' and r['checks']==num and r['error'] is None and r['rows']==rows and len(rows)==num
 assert r['source']=={n:ident(current['code/'+n]) for n in ('managed_coverage.py','correspondence.py')}
 supplied[label]={'result_identity':ident((p/'RESULT.json').read_bytes()),'checks':num,'source_identities_confirmed':True,'inspected_not_rerun':True,'labels':[r['check'] for r in rows]}
fresh=read(ROOT/'results/fresh-result.json');log=(ROOT/'results/fresh.stdout').read_text().splitlines();fl=json.loads(log[-1]);assert fresh['result']=='PASS' and fresh['checks']==len(fl['rows'])==5 and fl['public_result']==fresh['public_result'] and sum(x.startswith('PASS ') for x in log)==5 and (ROOT/'results/fresh.stderr').read_bytes()==b''
assert fresh['public_result']['receipt']==ident(current['results/client-state-correspondence.json'])
cp=json.loads(review['CHECKPOINT.json']);assert cp['independent_results']['primary_checks']==172 and cp['independent_results']['recovered_checks']==131 and cp['preservation']['prior_independent_counts']==[217,149]
# Supplied intermediate archive is not present: current final ZIP is the independent recovery input.
result={'result':'PASS','target':cid,'present_nested_archives':nested,'reused_verified_predecessor':oid,'reused_review':rid,'preserved_prior_members':1508,'preserved_prior_review_non_input_members':133,'old_manifest_byte_identity':ident(old['MANIFEST.json']),'old_review_manifest_byte_identity':ident(review['MANIFEST.json']),'unchanged_prior_producer_functions':62,'added_functions':added,'unchanged_prior_top_level_statements':True,'runtime_source_changes':0,'prior_context_fields_relationships_ordinals_and_evidence_unchanged':True,'receipt_new_context_field':'client_state_return_correspondence','prior_components_relocated_exact':True,'supplied_controls':supplied,'supplied_fresh_process':fresh,'supplied_intermediate_recovery_identity_only':read(ROOT/'results/recovery-input.json'),'intermediate_outer_archive_newly_verified':False,'prior_review_counts_preserved':[172,131,217,149],'prior_failure_records_and_progress_reconciliation_preserved':True,'supplied_new_campaign_failures':[],'current_sources':{n:ident(current['code/'+n]) for n in ('managed_coverage.py','correspondence.py')},'current_receipt':ident(current['results/client-state-correspondence.json'])}
(OUT/'composition.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS 1508 exact predecessor members; 133 exact review records;',len(nested),'nested archive occurrences; 62 prior functions unchanged; supplied171/173/5 inspected')
