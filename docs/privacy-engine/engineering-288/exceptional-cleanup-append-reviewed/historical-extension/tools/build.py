from pathlib import Path
import ast,hashlib,json,difflib
T=Path(__file__).resolve().parents[1];r=T/'input';p=r/'retained/details'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,s):q=r/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(s.encode() if type(s) is str else s)
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
old=(p/'code/managed_coverage.py').read_bytes();addition=(T/'tools/producer-addition.py').read_bytes();write('code/managed_coverage.py',old+b'\n'+addition)
s=(p/'code/correspondence.py').read_text();s=s.replace('launcher-handler/initial-details','exceptional cleanup/normal append').replace('DETAILS-','CLEANUP-').replace('retained/client-construction','retained/details').replace('results/primary/client-construction-none.json','ld01/receipts/corrected-launcher-details.json').replace('_client_construction_predecessor','_launcher_details_predecessor').replace('_launcher_details_coverage','_cleanup_append_coverage')
s=s.replace("RELATION='launcher_initial_details_correspondence'","RELATION='exceptional_cleanup_append_correspondence'").replace("REQUIRED={RELATION,","REQUIRED={RELATION,'launcher_initial_details_correspondence',")
lines=s.splitlines(True);tree=ast.parse(s);edits=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('PRODUCER_PIN','PREDECESSOR_MANIFEST','PREDECESSOR_RECEIPT'):
  k=n.targets[0].id;f={'PRODUCER_PIN':r/'code/managed_coverage.py','PREDECESSOR_MANIFEST':p/'MANIFEST.json','PREDECESSOR_RECEIPT':p/'ld01/receipts/corrected-launcher-details.json'}[k];edits.append((n.lineno,n.end_lineno,k+'='+repr(ident(f.read_bytes()))+'\n'))
for a,b,t in sorted(edits,reverse=True):lines[a-1:b]=[t]
s=''.join(lines)
s=s.replace("for name in ('lab_bootstrap.py','prospective_entry.py'):","for name in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):")
s=s.replace("require(b==(base/'source-evidence'/name).read_bytes(),'CLEANUP-SOURCE-IDENTITY');raws.append(b)","\n  if name=='live_connection.py':require(identity(b)=={k:json.loads(saved)['contexts'][0]['reference_declarations']['source']['source'][k] for k in ('bytes','sha256')},'CLEANUP-MANAGER-IDENTITY')\n  else:require(b==(base/'source-evidence'/name).read_bytes(),'CLEANUP-SOURCE-IDENTITY')\n  raws.append(b)")
s=s.replace("return data['coverage'].compile_launcher_details(*sources(data),data['prior']['contexts'][0]['client_construction_none_correspondence']['declaration'])","return data['coverage'].compile_cleanup_append(*sources(data),data['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration'],data['prior']['contexts'][0]['reference_declarations'])")
# New outer observer has its own slot; predecessor LD01 helper stays exact in retained root.
a=s.index('def _public_predecessor(');b=s.index('def _basis(',a);helper=s[a:b].replace('(2,','(3,').replace('get_tool(2)','get_tool(3)').replace('free_tool_id(2)','free_tool_id(3)').replace('launcher-details-authenticated-predecessor:','cleanup-append-authenticated-predecessor:');s=s[:a]+helper+s[b:]
a=s.index('def _basis(');b=s.index('def _check_rows(',a)
s=s[:a]+'''def _inner(pb):return pb['prior_module'].inner(pb['prior_basis']['fresh'])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module'];inner=_inner(pb)
 require(sources(fresh)==(*p.sources(pb['fresh'])[:2],inner['manager']),'CLEANUP-AUTHENTICATED-SOURCES')
 reference=pb['prior']['contexts'][0]['reference_declarations']
 for row in pb['prior']['contexts']:same(row['reference_declarations'],reference,'CLEANUP-AUTHENTICATED-REFERENCE-CONTEXTS')
 cat=fresh['coverage'].compile_cleanup_append(*sources(fresh),pb['catalogue'],reference)
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence']),'inner':inner}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'CLEANUP-CONTEXT-DOMAIN');out=[]
 for old in basis['prior']['contexts']:
  parent=old['launcher_initial_details_correspondence'];cat=basis['catalogue']
  out.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),
   'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Completed details assignment with selected original constructor error pending and no replacement',
   'local_reference_continuity':'Explicit conditional premise; selected raw None and handoff manager, not an arbitrary object or observed identity',
   'close_return_vs_append':'Separate operations in one try; later append failure preserves established normal close return',
   'runtime_cleanup_append_chain':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'error_report_append_expanded':False,'later_iterations_complete':False,'outer_cleanup_complete':False,'gap':'No runtime selected-object close/append chain or physical cleanup/retention proof; line172 and later remain unexpanded.'})
 return out
''' +s[b:]
s=s.replace('I164-LAUNCHER-INITIAL-CLEANUP-CORRESPONDENCE-1','I164-EXCEPTIONAL-CLEANUP-APPEND-CORRESPONDENCE-1').replace('I164-LAUNCHER-INITIAL-DETAILS-CORRESPONDENCE-1','I164-EXCEPTIONAL-CLEANUP-APPEND-CORRESPONDENCE-1')
s=s.replace('prior_client_construction_components','prior_launcher_details_components').replace('prior_client_construction_receipt','prior_launcher_details_receipt').replace('new_launcher_details_limits','new_cleanup_append_limits').replace('derive_launcher_details','derive_cleanup_append')
s=s.replace("'cleanup_loop_entered':False,","'error_report_append_expanded':False,'later_iterations_complete':False,")
a=s.index('def _premises(');b=s.index('def constructed_projection(',a)
s=s[:a]+'''def close_scope(anchor,invocation):return {'acquisition':anchor['record']['acquisition'],'instance':'validated-instance:'+hashlib.sha256(enc(anchor['instance'])).hexdigest(),'invocation':invocation+'/exceptional-managed-close'}
def _premises(basis,case):
 exact(case,'CLEANUP-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','close_case','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','CLEANUP-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'CLEANUP-CONSTRUCTED-CONTEXT');anchor=rows[0]['launcher_initial_details_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CLEANUP-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'CLEANUP-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CLEANUP-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'CLEANUP-VALIDATED-PARENT-OUTPUT')
 binding=case['binding'];require(type(binding) is dict and 'continuity' in binding,'CLEANUP-BINDING-INPUT')
 expected=basis['fresh']['coverage'].cleanup_append_binding(basis['catalogue'],parent,anchor,binding['continuity']);same(binding,expected,'CLEANUP-EXPECTED-BINDING')
 cc=case['close_case'];cr=None
 if cc is not None:
  exact(cc,'CLEANUP-CLOSE-CASE');require(type(cc) is dict,'CLEANUP-CLOSE-CASE');same(cc.get('scope'),close_scope(anchor,case['invocation']),'CLEANUP-CLOSE-SCOPE');require(cc.get('context')==case['context'] and cc.get('method')=='close','CLEANUP-CLOSE-RECEIVER-METHOD')
  d=basis['inner'];g=d['guards'];cr=basis['fresh']['coverage'].constructed_reference_path(d['manager'],g['guard_relationships'],g['guard_oracle'],cc)
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':expected,'close_result':cr,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.cleanup_append_projection(cat,case['projection'],v);c.validate_cleanup_append_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
''' +s[b:]
a=s.index('def _construct_prior(');b=s.index('def constructed_prior(',a)
s=s[:a]+'''def _construct_prior(basis,branch,case):
 exact(case,'CLEANUP-PRIOR-INPUT');require(type(branch) is str and branch in ('details','client-construction','control-construction','control','bare','stored-client','stored-normal','normal-token'),'CLEANUP-PRIOR-BRANCH')
 if branch=='details':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
''' +s[b:]
s=s.replace("'runtime_handler_details_chain':'UNAVAILABLE'","'runtime_cleanup_append_chain':'UNAVAILABLE'")
ast.parse(s);write('code/correspondence.py',s)
for n in ['code/managed_coverage.py','code/correspondence.py']:compile((r/n).read_bytes(),str(r/n),'exec')
changes={n:{'before':ident((p/n).read_bytes()),'after':ident((r/n).read_bytes())} for n in ['code/managed_coverage.py','code/correspondence.py']}
write('provenance/changed-files.json',enc({'intentional_changes':changes,'retained_predecessor_and_LD01_helper':'UNCHANGED','runtime_sources':'UNCHANGED','producer_prefix_unchanged_bytes':len(old),'new_producer_functions':len([n for n in ast.parse(addition).body if isinstance(n,ast.FunctionDef)]),'outer_monitoring_slot':3,'predecessor_LD01_slot':2,'contract':'Retained CPython3.12.14 cooperative ownership/release; new outer passive observer uses same protected lifetime pattern on distinct slot.'}))
write('provenance/implementation.diff',''.join(''.join(difflib.unified_diff((p/n).read_text().splitlines(True),(r/n).read_text().splitlines(True),fromfile='prior/'+n,tofile='current/'+n)) for n in changes))
print(json.dumps(changes,indent=2))
