"""Additional direct-helper and original-false-flag negative controls."""
from pathlib import Path
import argparse,copy,json,runpy,traceback
C=runpy.run_path(str(Path(__file__).with_name('common.py')));globals().update({n:C[n] for n in ('enc','module','guards','monitor','Record')})
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('case_records',type=Path);a=p.parse_args();root=a.root.resolve();r=Record(a.output.resolve());guards(root);stop=lambda:None;error=None
try:
 m=module(root/'code/correspondence.py');_,stop=monitor(m);d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);_,au,an,ob=d['prior_module'].sources(d['prior_data']);v=c.handle_authentication(au,an,ob);cases=json.loads(a.case_records.read_bytes())
 for ctx in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for stage in ('retain-error','fixed-failure'):
   row=next(x for x in cases if x['case']['scope']['context']==ctx and x['source_oracle']['terminal']==stage and x['source_oracle']['kind']=='unexpected-raise');case=row['case'];out=c.client_handle_projection(cat,v,case,copy.deepcopy(case));assert out['outside_catch_failure'] is True
   bad=copy.deepcopy(out);bad['outside_catch_failure']=False;bad['outcome_classification']['unexpected_raise_outside_dispatch_catch']=False
   r.reject('original false flag coordinated duplicate rejects '+ctx+':'+stage,lambda case=case,bad=bad:c.validate_client_handle_projection(cat,v,case,case,bad),'CLIENT-PROJECTION-CORRESPONDENCE')
  row=next(x for x in cases if x['case']['scope']['context']==ctx and x['source_oracle']['terminal']=='fixed-failure' and x['source_oracle']['kind']=='intentional-fixed-raise' and x['result']['original_exception'] is not None);case=row['case'];out=c.client_handle_projection(cat,v,case,copy.deepcopy(case));bad=copy.deepcopy(out);bad['outside_catch_failure']=True;bad['completion']='unqualified-escape';bad['events'][-1]['outcome']='raise';bad['outcome_classification'].update(modeled_kind='unexpected-raise',stage_outcome='raise',unexpected_raise_outside_dispatch_catch=True)
  r.reject('caught raise cannot relabel intentional fixed failure '+ctx,lambda case=case,bad=bad:c.validate_client_handle_projection(cat,v,case,case,bad),'CLIENT-PROJECTION-CORRESPONDENCE')
  row=next(x for x in cases if x['case']['scope']['context']==ctx and x['source_oracle']['terminal']=='packet-check' and x['source_oracle']['kind']=='process-termination');case=row['case'];out=c.client_handle_projection(cat,v,case,copy.deepcopy(case));pristine=enc(out);cat_before=enc(cat);assert out['outcome_classification']['source']['guards'];out['outcome_classification']['source']['guards'][0]['kind']='forged';assert enc(out)!=pristine
  r.check('nonempty nested source mutation does not change expected catalogue '+ctx,lambda case=case,pristine=pristine,cat_before=cat_before:enc(cat)==cat_before and enc(c.client_handle_projection(cat,v,case,copy.deepcopy(case)))==pristine)
  good=c.client_handle_projection(cat,v,case,copy.deepcopy(case));events=good['events'];completion=good['completion'];r.check('direct classifier legitimate source-bound terminal '+ctx,lambda:enc(c._client_outcome_classification(cat,events,completion))==enc(good['outcome_classification']))
  r.reject('direct classifier mismatched completion and outcome '+ctx,lambda:c._client_outcome_classification(cat,events,'unqualified-escape'),'CLIENT-CLASSIFICATION-OUTCOME')
  altered=copy.deepcopy(events);altered[-1]['source']['expression']='invented source';r.reject('direct classifier stale defining anchor '+ctx,lambda:c._client_outcome_classification(cat,altered,completion),'CLIENT-CLASSIFICATION-SOURCE')
 r.reject('direct classifier missing events',lambda:c._client_outcome_classification(cat,[],'process-termination'),'CLIENT-CLASSIFICATION-EVENTS')
 # Both preserved author failures are harness issues, checked without rerunning.
 focused=json.loads((root/'original/results/focused-correction/cases.json').read_bytes());assert all('retain-error' not in x['input']['outcomes'] for x in focused)
 historical=json.loads((root/'original/results/recovered/constructed-cases.json').read_bytes())[:4];facts=[]
 for x in historical:
  expected=x['input']['manager_case']['wrapper_return']['value'];actual=x['output']['hops'][0]['value'];assert actual!=expected and actual.get('bytes_hex')=='00';facts.append({'context':x['input']['scope']['context'],'input_bytes_hex_length':len(expected['bytes_hex']),'deliberately_mutated_historical_first_hop':actual})
 (r.path/'development-failure-assessment.json').write_text(json.dumps({'selector_failure':'No retain-error fixture exists in the selected old focused cases; StopIteration is consistent with the preserved selection code.','normal_comparison_failure':'Historical returned objects have a deliberately mutated first hop; source-backed expectation is the saved input, not this output.','historical_output_facts':facts,'implementation_correction_changed_by_harness_fixes':False,'failed_campaigns_rerun':False},indent=2)+'\n')
 r.check('failed author fixture assumptions independently corroborated',lambda:bool(facts))
except BaseException as e:error={'type':type(e).__name__,'message':str(e)};(r.path/'failure.txt').write_text(traceback.format_exc());raise
finally:stop();r.finish(error,root=root.name)
print('PASS',len(r.rows),'additional focused controls')
