from pathlib import Path
import sys,ast,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from archive_inspect import *
w=Path(__file__).resolve().parents[2];base=w/'sr-review';root=w/'sr-input'
priorraw=(w/'upload/I164-client-state-return-correspondence-1(1).zip').read_bytes();assert ident(priorraw)=={'bytes':61624841,'sha256':'0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907'};prior,pi=inspect(priorraw);assert len(prior)==1688
reviewraw=(w/'Formal-Lab6-I164-client-state-return-correspondence-independent-review.zip').read_bytes();assert ident(reviewraw)=={'bytes':60792892,'sha256':'a8762d3b81d5f5cbedfb95e5afd8d2c083143ed759f88f2b550cfebfb6de4bf6'};review,ri=inspect(reviewraw);assert len(review)==91
raw=(w/'upload/I164-internal-status-return-correspondence-1(1).zip').read_bytes();assert ident(raw)=={'bytes':62835317,'sha256':'06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864'};current,ci=inspect(raw);assert len(current)==1845
assert all(current['retained/state/'+n]==b for n,b in prior.items());assert {n.removeprefix('retained/state/') for n in current if n.startswith('retained/state/')}==set(prior)
omit='input/I164-client-state-return-correspondence-1.zip';assert review[omit]==priorraw
assert all(current['retained/review/'+n]==b for n,b in review.items() if n!=omit);assert {n.removeprefix('retained/review/') for n in current if n.startswith('retained/review/')}==set(review)-{omit}
nested={}
def nest(es,label):
 for n,b in es.items():
  if n.endswith('.zip'):
   ss,r=inspect(b);nested[label+n]=r;nest(ss,label+n+'!/')
nest(current,'')
def functions(raw):
 s=raw.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,ag=functions(prior['code/managed_coverage.py']);b,bg=functions(current['code/managed_coverage.py']);assert len(a)==70 and all(b[k]==v for k,v in a.items()) and ag==bg;added=sorted(b.keys()-a.keys());assert len(added)==6
old_source=current['failures/type-acceptance-precorrection/managed_coverage.py'];oldf,_=functions(old_source);changed=[k for k,v in oldf.items() if b[k]!=v];assert sorted(changed)==['status_forward_projection','status_snapshot_value']
oldr=json.loads(current['results/pre-type-hardening-receipt.json']);newr=json.loads(current['results/status-forward-correspondence.json']);assert all(newr[k]==v for k,v in oldr.items() if k!='extension_components')
pr=json.loads(prior['results/client-state-correspondence.json']);assert newr['prior_client_state_components']==pr['extension_components'] and newr['prior_client_state_receipt']==ident(prior['results/client-state-correspondence.json'])
for k,v in pr.items():
 if k not in ('format','extension_components','contexts'):assert newr[k]==v,k
for a,b in zip(pr['contexts'],newr['contexts']):assert set(b)==set(a)|{'internal_status_return_correspondence'} and all(b[k]==v for k,v in a.items())
assert newr['unchanged_obligations']==pr['unchanged_obligations'] and newr['inventory_unknown_totals']==4 and newr['lifetime_unknown_totals']==14
supplied={}
for path,num in [('exact-types',36),('recovered-output',205),('recovered-types',34),('pre-type-hardening-primary',204)]:
 p=root/'results'/path;r=read(p/'RESULT.json');rows=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()];assert r['result']=='PASS' and r['checks']==num and r['rows']==rows and len(rows)==num and r['error'] is None
 supplied[path]={'checks':num,'identity':ident((p/'RESULT.json').read_bytes()),'inspected_not_rerun':True,'current_code':path!='pre-type-hardening-primary','labels':[x['check'] for x in rows]}
witness=read(root/'results/exact-types/original-witnesses.json');assert len(witness)==12 and all(v['original_accepted'] for v in witness)
p=root/'failures/control-attempt-1';r=read(p/'results/RESULT.json');assert r['result']=='FAIL' and r['checks']==17 and len(r['rows'])==17 and r['rows']==[json.loads(x) for x in (p/'results/progress.jsonl').read_text().splitlines()]
failed_source=(p/'controls.py').read_text();assert "update(guards=[])" in failed_source
# Inspect the preserved ineffective mutation as data, not by rerunning the old campaign.
cat=newr['contexts'][0]['internal_status_return_correspondence']['declaration'];assert cat['declarations'][1]['source_origin']['guards']==[]
fr=read(root/'results/fresh-result.json');last=json.loads((root/'results/fresh.stdout').read_text().splitlines()[-1]);assert fr['checks']==last['checks']==len(last['rows'])==5 and fr['result']==last['result']=='PASS' and (root/'results/fresh.stderr').read_bytes()==b''
cp=json.loads(review['CHECKPOINT.json']);assert cp['independent_results']['primary_checks']==273 and cp['independent_results']['recovered_checks']==196
record={'result':'PASS','target':ci,'nested_archives':nested,'prior_target':pi,'prior_review':ri,'preserved_predecessor_members':1688,'preserved_review_non_input_records':90,'inherited_producer_functions_byte_identical':70,'inherited_top_level_statements_unchanged':True,'added_functions':added,'type_correction_changed_functions':changed,'runtime_sources_changed':0,'current_components':{n:ident(current['code/'+n]) for n in ('managed_coverage.py','correspondence.py')},'old_affected_producer':ident(old_source),'old_affected_adapter':ident(current['failures/type-acceptance-precorrection/correspondence.py']),'current_receipt':ident(current['results/status-forward-correspondence.json']),'all_prior_context_fields_relationships_ordinals_and_obligations_unchanged':True,'type_hardening_receipt_only_component_identities_changed':True,'supplied_results':supplied,'supplied_type_witnesses':witness,'supplied_fresh_process':fr,'supplied_failed_attempt':{'checks':17,'not_in_completed_totals':True,'ineffective_mutation_independently_corroborated':True},'prior_independent_counts':[273,196],'prior_failure_records_preserved':True,'intermediate_recovery_outer_archive_newly_verified':False,'supplied_intermediate_recovery':read(root/'results/recovery-input.json'),'manifest_interpretation':'Historical missing outer archives and forensic copies remain qualified; forensic snapshot MANIFEST.json documents are not declarations of new executable roots.'}
(base/'results/composition.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS 1845 entries; 1688 predecessor + 90 review records exact; 70 inherited functions; supplied36/205/34/5 and204 and failed17 separate; nested',len(nested))
