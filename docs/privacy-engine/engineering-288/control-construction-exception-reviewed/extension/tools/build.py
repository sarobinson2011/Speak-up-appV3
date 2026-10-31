from pathlib import Path
import ast,hashlib,json,difflib,shutil
TASK=Path('/workspace/i164-control-construction-offline');root=TASK/'input';prior=root/'retained/control'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
old=(prior/'code/managed_coverage.py').read_bytes();addition=(TASK/'tools/producer-addition.py').read_bytes();new=old+b'\n\n'+addition
ast.parse(new);(root/'code/managed_coverage.py').write_bytes(new)
s=(prior/'code/correspondence.py').read_text()
s=s.replace('control-callback exception','control-construction exception').replace('control_exception','control_construction').replace('derive_control','derive_construction').replace('CONTROL-','CONSTRUCTION-').replace('CONSTRUCTED-CONTROL-EXCEPTION','CONSTRUCTED-CONTROL-CONSTRUCTION-EXCEPTION')
s=s.replace("base=root/'retained/bare'","base=root/'retained/control'").replace("'_bare_predecessor'","'_control_predecessor'").replace("'_control_coverage'","'_construction_coverage'")
s=s.replace("'results/primary/callback-bare-rethrow.json'","'results/primary/control-exception.json'")
s=s.replace("'bare_basis':bb,'bare_module':p,'stored_basis':bb['stored_basis']","'control_basis':bb,'control_module':p,'stored_basis':bb['stored_basis']")
s=s.replace("bare=row['callback_bare_rethrow_correspondence']","control=row['control_exception_revocation_correspondence']").replace("bare['instance_anchor']","control['instance_anchor']").replace("bare['declaration']","control['declaration']").replace("bare['separate_observer']","control['separate_observer']")
s=s.replace("'prior_callback_bare_components'","'prior_control_components'").replace("'prior_callback_bare_receipt'","'prior_control_receipt'")
s=s.replace("'I164-CONSTRUCTION-EXCEPTION-CORRESPONDENCE-1'","'I164-CONTROL-CONSTRUCTION-CORRESPONDENCE-1'")
s=s.replace('control_error','construction_error').replace("'control-callback'","'control-create'")
s=s.replace("'CONTROL-CALLBACK-ERROR'","'CONSTRUCTION-EXPRESSION-ERROR'")
s=s.replace('CONSTRUCTED-CONSTRUCTION-EXCEPTION','CONSTRUCTED-CONTROL-CONSTRUCTION-EXCEPTION').replace('CONSTRUCTION-CALLBACK-ERROR','CONSTRUCTION-EXPRESSION-ERROR')
s=s.replace("'control_construction_revocation_correspondence','callback_bare_rethrow_correspondence'","'control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence'")
s=s.replace("Selected control callback raises after control construction, under conditional selected-owner continuity.","Selected _Control(token) expression raises before either callback, under conditional selected-owner continuity.")
s=s.replace("'gap':'No runtime control callback/error/finally/pop chain or existing cause/context observations. Control constructor failures and full outer cleanup remain unexpanded.'","'gap':'No runtime construction expression/error/finally/pop chain, allocation/initializer progress or existing cause/context observations. Full outer cleanup remains unexpanded.'")
s=s.replace("'client_handler_applicable':False,","'client_handler_applicable':False,'construction_completed':False,'completed_control_object_reference':None,'control_callback_execution':False,'client_callback_execution':False,'constructor_substep_history':None,")
s=s.replace("'control_exception_producer_history'","'construction_exception_producer_history'").replace("'runtime_control_construction_revocation_chain'","'runtime_construction_exception_revocation_chain'")
s=s.replace("'new_control_exception_limits'","'new_control_construction_limits'")
s=s.replace("'subsequent_client_handler_applicable':False,","'subsequent_client_handler_applicable':False,'construction_completion_established':False,'control_callback_execution_established':False,'client_callback_execution_established':False,")
t=ast.parse(s);lines=s.splitlines(True);changes=[]
pins={'PRODUCER_PIN':ident(new),'PREDECESSOR_MANIFEST':ident((prior/'MANIFEST.json').read_bytes()),'PREDECESSOR_RECEIPT':ident((prior/'results/primary/control-exception.json').read_bytes())}
for n in t.body:
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in pins:changes.append((n.lineno-1,n.end_lineno,n.targets[0].id+'='+repr(pins[n.targets[0].id])+'\n'))
 if isinstance(n,ast.FunctionDef) and n.name=='constructed_prior':
  changes.append((n.lineno-1,n.end_lineno,"def constructed_prior(data,submitted_catalogue,branch,case):\n exact(case,'CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');require(type(branch) is str and branch in ('control','bare','stored-client','stored-normal','normal-token'),'CONSTRUCTION-PRIOR-BRANCH');_,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)\n"))
 if isinstance(n,ast.FunctionDef) and n.name=='_construct_prior':
  changes.append((n.lineno-1,n.end_lineno,"def _construct_prior(basis,branch,case):\n exact(case,'CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');p=basis['control_module'];b=basis['control_basis']\n if branch=='control':return p._construct_checked(b,case)\n return p._construct_prior(b,branch,case)\n"))
for a,b,x in reversed(changes):lines[a:b]=[x]
s=''.join(lines);ast.parse(s);(root/'code/correspondence.py').write_text(s)
before=ast.parse(old);after=ast.parse(new);assert len(after.body)==len(before.body)+6
assert all(ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False) for a,b in zip(before.body,after.body))
p=root/'provenance';p.mkdir(exist_ok=True);(p/'intake.json').write_bytes((TASK/'intake.json').read_bytes())
(p/'changed-files.json').write_bytes(enc({'intentional_changes':{n:{'before':ident((prior/n).read_bytes()),'after':ident((root/n).read_bytes())} for n in ('code/managed_coverage.py','code/correspondence.py')},'inherited_producer_definitions_unchanged':sum(isinstance(n,ast.FunctionDef) for n in before.body),'new_producer_definitions':6,'runtime_source_changes':0,'prior_reviewed_root_changes':0}))
(p/'implementation.diff').write_text(''.join(''.join(difflib.unified_diff((prior/n).read_text().splitlines(True),(root/n).read_text().splitlines(True),fromfile='retained/control/'+n,tofile=n)) for n in ('code/managed_coverage.py','code/correspondence.py')))
print('Built additive producer and mandatory adapter; no candidate execution')
