"""Independent static source anchors for local caps and branch schedule; no import of runtime."""
import ast,hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);dirs=json.loads((root/'candidate/directories.json').read_bytes())
paths={x:'support/reference/runtime/'+x+'.py' for x in ['authority','accounting','ownership']}
trees={k:ast.parse((root/p).read_bytes()) for k,p in paths.items()};text={k:(root/p).read_text() for k,p in paths.items()}
def snippets(key,needles):
 found=[]
 for n in ast.walk(trees[key]):
  if isinstance(n,ast.Compare):
   s=ast.unparse(n)
   if any(needle in s for needle in needles):found.append({'line':n.lineno,'expression':s})
 assert found,(key,needles);return found
checks=[]
# Expected cap values are paired with source comparisons or named source constants,
# not taken from the generated model-adapter metadata.
expected={'U':64,'stage':1,'aggregate_attempt_guard':2070,'attempt':102,'slots_plus_holds':16,'stage_queries':2086,'shared_queries':3110,'extra_queries':16,'stage_backups':85,'shared_snapshots':130,'verifier':64,'stage_verifier':18,'events':12000,'journal':384000,'shared_owners':4096}
assert {k:v['max'] for k,v in dirs['local'].items()}==expected
constants={}
for k in ['authority','ownership']:
 for n in trees[k].body:
  if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant):
   for t in n.targets:
    if isinstance(t,ast.Name):constants[t.id]=n.value.value
assert constants['MAX_ROWS']==expected['journal'] and constants['MAX_EVENTS']==expected['events'] and constants['MAX_COORDINATES']==expected['shared_owners']
anchors={
 'retirement_and_single_stage':snippets('authority',["len(s['u']) < 64","s['active'] is None"]),
 'attempt_slot_query_caps':snippets('accounting',["2070","102","16","2086","3110"]),
 'snapshot_caps':snippets('authority',["s['counts']['snapshot'] < 130","s['partitions']['snapshot'] < 85"]),
 'verifier_caps':snippets('accounting',["s['counts']['verifier'] < 64","s['partitions']['verifier'] < 18"]),
 'history_and_journal_caps':snippets('authority',['MAX_EVENTS','MAX_ROWS']),
 'ownership_cap':snippets('ownership',['MAX_COORDINATES'])}
# Source dictionaries also establish the complete aggregate/partition counter limits.
limits=[]
for n in ast.walk(trees['accounting']):
 if isinstance(n,ast.Dict):
  try:v=ast.literal_eval(n)
  except (ValueError,TypeError):continue
  if isinstance(v,dict) and 'query' in v:limits.append(v)
assert {'attempt':2070,'query':3110,'snapshot':130,'verifier':64} in limits
assert {'query':2086,'snapshot':85,'verifier':18} in limits
stage=ast.parse((root/'support/reference/retained/stages.py').read_bytes());ceil=next(ast.literal_eval(n.value) for n in stage.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CEILINGS' for t in n.targets))
assert ceil=={'signPetition':41972,'signPetitionWithZKProof':21376};appends={k:(v+511)//512 for k,v in ceil.items()};assert appends=={'signPetition':82,'signPetitionWithZKProof':42}
# Existing structural bounds reused, with arithmetic checked. This is not a new reachability proof.
assert dirs['structural_attempt_upper_bounds']['ordinary']==82+4+15==82+5+14==101
assert dirs['structural_attempt_upper_bounds']['ZK']==42+4+15==42+5+14==61
# Common.py encoding separates bool/int; source state guards/returns are not rerun.
assert dirs['lifetime_acquisition_recovery_diagnostics']['status']=='UNRESOLVED'
assert dirs['physical_storage']['status']=='UNRESOLVED' and dirs['external_evidence']['bound'] is None
result={'status':'PASS','local_caps':expected,'source_anchors':anchors,'source_constants':{k:constants[k] for k in ['MAX_ROWS','MAX_EVENTS','MAX_COORDINATES']},'counter_limit_dictionaries':limits,'message_ceilings':ceil,'max_appends':appends,'structural_bounds':{'ordinary':101,'ZK':61,'status':'existing reviewed structural bound, arithmetic corroborated; attainability not established'},'branch_review':'begin b, appends b+1..b+n, finalize b+n+1, petition p=b+n+2; alternate abandon/cleanup reach at most p+2; source ownership range preserved. Branch guard meaning inspected, no lifecycle executed.','remaining_bounds':'lifetime acquisition/recovery/diagnostics, physical storage and external evidence unresolved'}
out.write_text(json.dumps(result,indent=2)+'\n');print('Source cap/branch audit PASS')
