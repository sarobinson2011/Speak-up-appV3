"""NEW reconstruction from retained baseline; never restores missing prior implementation."""
from pathlib import Path
import ast,json,hashlib,copy,types
W=Path(__file__).resolve().parents[1];R=W/'construction/root';P=R/'retained/loop'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,b):
 p=R/n;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def replace_functions(source,changes):
 lines=source.splitlines(True);nodes={x.name:x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef)}
 for name,body in sorted(changes.items(),key=lambda x:nodes[x[0]].lineno,reverse=True):
  n=nodes[name];lines[n.lineno-1:n.end_lineno]=[body.strip()+'\n']
 return ''.join(lines)
def main():
 old=(P/'code/managed_coverage.py').read_bytes();new=old+(W/'tools/write_call_addition.py').read_bytes();write('code/managed_coverage.py',new)
 src=(P/'code/correspondence.py').read_text().replace('LOOP-','WC-').replace("base=root/'retained/report'","base=root/'retained/loop'").replace('prepared-error-report.json','prepared-cleanup-loop.json').replace('_error_report_predecessor','_loop_predecessor').replace('_cleanup_loop_coverage','_write_call_replacement').replace('cleanup_loop_exhaustion_correspondence','write_call_correspondence').replace('derive_cleanup_loop','derive_write_call').replace('runtime_loop_chain','runtime_write_call_chain')
 src=src.replace('I164-CLEANUP-LOOP-CORRESPONDENCE-1','I164-WRITE-CALL-REPLACEMENT-1')
 tree=ast.parse(src);lines=src.splitlines(True)
 replacements={'PRODUCER_PIN':ident(new),'PREDECESSOR_MANIFEST':ident((P/'MANIFEST.json').read_bytes()),'PREDECESSOR_RECEIPT':ident((P/'receipts/prepared-cleanup-loop.json').read_bytes())}
 for n in tree.body:
  if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in replacements:lines[n.lineno-1]=n.targets[0].id+'='+repr(replacements[n.targets[0].id])+'\n'
 src=''.join(lines);src=src.replace("REQUIRED={","REQUIRED={'cleanup_loop_exhaustion_correspondence',",1)
 # Preserve the reviewed protecting-lifetime algorithm; only this wrapper's slot/name changes.
 node=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor')
 part=''.join(src.splitlines(True)[node.lineno-1:node.end_lineno]).replace('(5,','(1,').replace('(5)','(1)').replace('cleanup-loop-authenticated-predecessor:','write-call-replacement-authenticated-predecessor:')
 changes={'_public_predecessor':part,
 'catalogue':'''def catalogue(data):
 row=data['prior']['contexts'][0]
 return data['coverage'].compile_write_call(*sources(data),row['cleanup_loop_exhaustion_correspondence']['declaration'],row['cleanup_error_report_correspondence']['declaration'],row['exceptional_cleanup_append_correspondence']['declaration'])''',
 '_basis':'''def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh']),'WC-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_write_call(*sources(fresh),pb['catalogue'],pb['prior_basis']['catalogue'],pb['prior_basis']['prior_basis']['catalogue'])
 basis={'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
 basis['session_bindings']=[_session_binding(basis,row) for row in basis['prior']['contexts']]
 return basis''',
 '_rows':'''def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'WC-CONTEXTS');rows=[]
 for i,old in enumerate(basis['prior']['contexts']):
  parent=old['cleanup_loop_exhaustion_correspondence'];cat=basis['catalogue']
  rows.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(basis['session_bindings'][i]),'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source':copy.deepcopy(d['source']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Actual validated completed loop; original constructor pending, no replacement; explicit continuation and conditional owner/lookup/reference/error continuity',
   'partial_effects':'Acknowledged close/reporting facts and UNKNOWN earlier append effects retained','runtime_write_call_chain':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'pid_value':None,'directory_count_value':None,'filename_value':None,'write_call_attempt_observed':False,'write_new_body_established':False,'outer_cleanup_complete':False,'gap':'Static conditional correspondence only; no helper body, suppression, final rethrow or physical cleanup'})
 return rows''',
 '_assemble':'''def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-WRITE-CALL-REPLACEMENT-1';result['prior_cleanup_loop_components']=result.pop('extension_components');result['prior_cleanup_loop_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_write_call_limits']={'NEW_REPLACEMENT_CONSTRUCTION':True,'unavailable_attempts_not_recovered':True,'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','pid_count_filename':None,'earlier_partial_effects_preserved':True,'write_new_body_established':False,'line175_suppression_established':False,'final_rethrow_established':False,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result''',
 '_premises':'''def _premises(basis,case):
 exact(case,'WC-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','session_binding','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-WRITE-CALL-REPLACEMENT','WC-CONSTRUCTED-CASE')
 indices=[i for i,r in enumerate(basis['prior']['contexts']) if r['context']==case['context']];require(len(indices)==1,'WC-CONTEXT');i=indices[0];anchor=basis['prior']['contexts'][i]['cleanup_loop_exhaustion_correspondence']['instance_anchor'];same(case['anchor'],anchor,'WC-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'WC-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'WC-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'WC-VALIDATED-PARENT')
 sb=basis['session_bindings'][i];same(case['session_binding'],sb,'WC-VALIDATED-DESTINATION');b=case['binding'];require(type(b) is dict and 'continuity' in b,'WC-BINDING')
 expected=basis['fresh']['coverage'].write_call_binding(basis['catalogue'],parent,anchor,sb,b['continuity']);same(b,expected,'WC-EXPECTED-BINDING')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'session_binding':copy.deepcopy(sb),'binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}''',
 '_construct_checked':'''def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.write_call_projection(cat,case['projection'],v);c.validate_write_call_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}''',
 '_construct_prior':'''def _construct_prior(basis,branch,case):
 exact(case,'WC-PRIOR-INPUT');require(type(branch) is str,'WC-PRIOR-BRANCH')
 if branch=='cleanup-loop':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)'''}
 src=replace_functions(src,changes)
 extra='''
def _session_binding(basis,row):
 anchor=row['cleanup_loop_exhaustion_correspondence']['instance_anchor'];e=basis['evidence'];sp='evidence/SMOKE-ABOUT-TO-START.json';bp='evidence/session-records/binding.json';s=json.loads(e[sp]);b=json.loads(e[bp])
 require(type(s['destination']) is str and b['configuration']['config']['session']==anchor['instance']['session_label'],'WC-DESTINATION-INSTANCE');same(b['launcher'],basis['catalogue']['source']['sources']['launcher'],'WC-DESTINATION-SOURCE')
 value={'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'recorded_destination':s['destination'],'start_record':{'path':sp,'identity':identity(e[sp]),'pointer':'/destination'},'binding_record':{'path':bp,'identity':identity(e[bp]),'pointer':'/configuration/config/session'},'source_owner_lock':copy.deepcopy(basis['catalogue']['source']['owner_lock']),'physical_resolved_destination':None,'resolution':'owner_lock yields dest after parent.resolve(); recorded destination is nominal, no host resolution performed'}
 same(value,row['normal_session_exit_correspondence']['session_binding'],'WC-INHERITED-SESSION');same(value,row['owner_lock_finalization_correspondence']['session_binding'],'WC-INHERITED-OWNER');return value
'''
 src=src.replace("if __name__=='__main__':",extra+"\nif __name__=='__main__':")
 src=src.replace('Mandatory bounded post-line172 handler departure and exact cleanup-loop exhaustion.','NEW replacement mandatory line174 evaluation and call-attempt correspondence.')
 write('code/correspondence.py',src.encode())
 for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):write('source-evidence/'+n,(P/'source-evidence'/n).read_bytes())
 for p in sorted((W/'baseline-package/new/results/focused-recovered/fixtures').glob('*.json')):write('fixtures/loop/'+p.name,p.read_bytes())
 m=types.ModuleType('replacement_preparation');m.__file__=str(R/'code/correspondence.py');exec(compile(src,m.__file__,'exec'),m.__dict__)
 data=m.inputs(R);cat=m.catalogue(data)
 public={'result':'PASS','contexts':list(m.CONTEXTS),'receipt':m.PREDECESSOR_RECEIPT.copy(),'runtime_loop_chain':'UNAVAILABLE','actual_admission':False}
 basis={'fresh':data,'prior':copy.deepcopy(data['prior']),'catalogue':cat,'public_predecessor':public,'session_bindings':[copy.deepcopy(r['normal_session_exit_correspondence']['session_binding']) for r in data['prior']['contexts']]}
 raw=m.enc(m._assemble(data,m._rows(basis),basis));write('receipts/prepared-write-call-replacement.json',raw)
 (W/'provenance/preparation.json').write_text(json.dumps({'status':'PREPARED_ONLY_NOT_AUTHENTICATED','NEW_REPLACEMENT_CONSTRUCTION':True,'prior_unavailable_bytes_not_recovered':True,'prior_36_checks_do_not_verify_replacement':True,'producer':ident(new),'adapter':ident(src.encode()),'receipt':ident(raw),'source_steps':len(cat['source']['steps']),'historical_producer_prefix':ident(old)},indent=2)+'\n')
 print((W/'provenance/preparation.json').read_text())
if __name__=='__main__':main()
