#!/usr/bin/env python3
"""Rebind only available mechanical metadata. Never migrate signed/job evidence."""
import argparse,hashlib,shutil
from common import *
def run(root):
 h=root/'historical/4P';c=root/'candidate';comparison=load(root/'results/MODEL-COMPARISON.json');new=comparison['new']['sha256']
 assert sha(c/'model.json')==new
 # Catalog every exact old-model occurrence in retained metadata (not inside opaque archives).
 direct=[]
 for p in sorted(h.rglob('*')):
  if p.suffix not in ('.json','.jsonl') or p.name=='PACKAGE-MANIFEST.json':continue
  if OLD.encode() not in p.read_bytes():continue
  if p.suffix=='.json':paths=list(pointers(load(p),OLD))
  else:paths=[f'/line/{i}{q}' for i,b in enumerate(p.read_text().splitlines(),1) for q in pointers(json.loads(b),OLD)]
  direct.append({'historical_path':str(p.relative_to(root)),**info(p),'model_pointers':paths,'disposition':'new mechanical derivative only' if p.relative_to(h).as_posix() in ['rebinding/ledger/potential-domain.json','rebinding/ledger/BINDING.json','ledger_data/inventory-result.json'] else 'historical only; no receipt/job migration'})
 save(root/'dependencies/DIRECT-MODEL-REFERENCES.json',direct)
 contract=load(h/'rebinding/selected-contract.json');assert sha(h/'rebinding/selected-contract.json')==CONTRACT
 assert not list(pointers(contract,OLD));sources=load(h/'rebinding/source-path-binding.json');sourcechecks=[]
 for logical,digest in contract['source_inputs'].items():
  a=sources['logical_inputs'][logical];assert a['sha256']==digest and sha(h/a['path'])==digest
  sourcechecks.append({'logical_path':logical,'physical_path':'historical/4P/'+a['path'],'sha256':digest,'whole_model_dependency':False})
 active=load(root/'historical/4Q/assembly/ACTIVE-IDENTITIES.json');active.update(model_sha256=new,model_bytes=comparison['new']['bytes'],model_status='SEPARATE-CANDIDATE-BINARY-IDENTITY-BOUND-NOT-ADMITTED',historical_model_sha256=OLD,final_profile_sha256=None)
 save(c/'ACTIVE-IDENTITIES.json',active)
 reuse=[]
 for p in sorted((h/'rebinding').rglob('*')):
  if not p.is_file() or p.name in ('BINDING.json','potential-domain.json'):continue
  assert OLD.encode() not in p.read_bytes()
  rel=p.relative_to(h/'rebinding');dest=c/'reused'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
  # These are source-row/catalog/duty facts, not completed cryptographic receipts.
  reuse.append({'historical_path':str(p.relative_to(root)),'candidate_path':str(dest.relative_to(root)),**info(dest),'reason':'Exact source dependencies unchanged; model array correspondence identical; no whole-model digest field. Mechanical content only.'})
 save(root/'dependencies/UNCHANGED-ARTIFACTS.json',{'contract_fields_checked':sorted(contract),'contract_sha256':CONTRACT,'source_checks':sourcechecks,'reused':reuse})
 domain=load(h/'rebinding/ledger/potential-domain.json');assert domain['model_sha256']==OLD and domain['serialized_stream_sha256'] is None
 domain['model_sha256']=new;domain['serialized_stream_sha256']=STREAM
 save(c/'ledger/potential-domain.json',domain)
 baseline=load(h/'ledger_data/inventory-result.json');counts={k:baseline[k] for k in ['tokens','surface_classes','relation_templates','structural_occurrences','potential_pairs','selected_contract_composition_slots','selected_contract_obligation_slots','node_exposures']}
 binding={'format':'CP4S-CANDIDATE-MECHANICAL-LEDGER-BINDING-1','model_sha256':new,'selected_contract_sha256':CONTRACT,'amendment_binding_sha256':active['amendment_binding_sha256'],'parent_4I_binding':{'path':'historical/4P/rebinding/ledger/BINDING.json',**info(h/'rebinding/ledger/BINDING.json')},'model_comparison':info(root/'results/MODEL-COMPARISON.json'),'binary_correspondence':info(c/'BINARY-CORRESPONDENCE.json'),'potential_domain':info(c/'ledger/potential-domain.json'),'reused_artifact_index':info(root/'dependencies/UNCHANGED-ARTIFACTS.json'),'qualification':'NOT-ESTABLISHED','actual_admission':False,'historical_segments':'193 unchanged prior coverage receipts retain original bindings; cited only through exact unchanged arrays and this new derivation. They are not receipts for a candidate execution job.','mechanically_established':counts}
 binding['derivation_code']={n:info(root/'tools'/n) for n in ('construct_candidate.py','rebind_metadata.py','common.py')}
 save(c/'ledger/BINDING.json',binding)
 save(c/'ledger/inventory-result.json',{'format':'CP4S-MECHANICAL-DUTY-REUSE-1','binding_sha256':sha(c/'ledger/BINDING.json'),'model_sha256':new,**counts,'result':'MECHANICAL-CORRESPONDENCE-REUSED-FOR-CANDIDATE','original_inventory':info(h/'ledger_data/inventory-result.json'),'qualification_established':False,'immutable_V4_obligations_instantiated':False,'dispositions':'ALL NOT-ESTABLISHED','no_new_segment_execution':True})
 rows=[]
 for line in (root/'historical/4Q/inventory/REQUIREMENTS.jsonl').read_text().splitlines():
  x=json.loads(line);x['historical_available_binding']=x.pop('exact_available_binding');x['candidate_required_binding']=active
  x['available_artifacts_are_historical_unless_explicitly_candidate']=True
  if x['id']=='binary-stream':
   x.update(status='AVAILABLE-MECHANICAL',category='verified-conditional-mechanical-identity',missing_dependencies=[],acquisition_action='Preserve exact historical completion and 4S correspondence; no binary rerun required.',full_model_input={'path':'candidate/BINARY-CORRESPONDENCE.json',**info(c/'BINARY-CORRESPONDENCE.json')})
  if x['id']=='final-profile':
   x['missing_dependencies']=['Actual independently governing policy/assumptions and other immutable members; exact source-owned correspondence and final outer bytes. Candidate model now exists; textual supplied evidence identities remain unresolved.']
   x['acquisition_action']='Acquire governing immutable inputs; build new final outer after all actual dependencies exist, then reacquire external records, assessments and signatures. Do not reuse old profile evidence.'
  if x['id']=='ledger':x['candidate_mechanical_metadata']={'path':'candidate/ledger/BINDING.json',**info(c/'ledger/BINDING.json')}
  if x['id']=='execution-host':x['note_4S']='4R Ubuntu host and 68m32s binary run succeeded. Does not establish resources for textual/full-model workload; new workload preflight required.'
  rows.append(x)
 (root/'inventory').mkdir(exist_ok=True);(root/'inventory/REQUIREMENTS.jsonl').write_bytes(b''.join(canonical(x) for x in rows))
 save(root/'inventory/GAP-REPORT.json',{'format':'CP4S-GAP-UPDATE-1','parent_inventory':info(root/'historical/4Q/inventory/REQUIREMENTS.jsonl'),'candidate':active,'available_mechanical':[x['id'] for x in rows if x['status']=='AVAILABLE-MECHANICAL'],'blocked':[x['id'] for x in rows if x['status']=='BLOCKED'],'requirements':len(rows),'invented_authoritative_inputs':0,'text_stream_sha256':None,'final_profile_sha256':None,'actual_admission':False,'qualification_established':False})
 witness=load(root/'historical/4Q/assembly/FULL-MODEL-WITNESS.json')
 witness.update(format='CP4S-CANDIDATE-WITNESS-ASSEMBLY-1',active=active,binary_stream_sha256=STREAM,candidate_model_sha256=new,final_model_sha256=None,state='CANDIDATE-BINARY-BOUND-FULL-WITNESS-BLOCKED',rebound_provenance={'path':'candidate/ledger/BINDING.json',**info(c/'ledger/BINDING.json')})
 for x in witness['required_slots']:
  if x['requirement_id']=='binary-stream':x.update(state='AVAILABLE-MECHANICAL',artifact={'path':'candidate/BINARY-CORRESPONDENCE.json',**info(c/'BINARY-CORRESPONDENCE.json')})
 witness['historical_results_are_not_current_job_receipts']=True
 save(c/'WITNESS-ASSEMBLY.json',witness)
 print(json.dumps({'result':'PASS','direct_old_model_references':len(direct),'unchanged_artifacts':len(reuse),'requirements':len(rows),'blocked':sum(x['status']=='BLOCKED' for x in rows)}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=R);a=ap.parse_args();run(a.root)
