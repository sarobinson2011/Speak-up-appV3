"""SOURCE-ONLY to validated draft construction/ledger inputs. Never expands a model.
Historical prepare/build are NOT invoked with UNKNOWN directories or fake models.
"""
import argparse,ast,copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ENTRY_SHA='d37590bf1a2c1f0af0a24869acddbfea75313a6ca38a221c0a0974742ce64a92'
FILES=('model-input.json','ledger-input.json','provenance.json','source-only-result.json')
def need(v,msg):
 if not v:raise ValueError(msg)
def enc(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def ident(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def same(a,b,msg):need(enc(a)==enc(b),msg)
def entry():
 p=P/'source-only/code/scope_integration.py';need(ident(p)['sha256']==ENTRY_SHA,'SOURCE-ONLY-ENTRY-IDENTITY')
 sys.path.insert(0,str(p.parent));import scope_integration as s
 need(Path(s.__file__).resolve()==p.resolve(),'MIXED-ENTRY-MODULE');return s

def source_contract(root,path,name):
 raw=(root/path).read_bytes();tree=ast.parse(raw)
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
 need(len(nodes)==1,'NATIVE-INTERFACE');n=nodes[0]
 return {'source':{'path':path,**ident(root/path)},'function':name,'parameters':[a.arg for a in n.args.args],'line':n.lineno,'end_line':n.end_lineno,'ast_sha256':hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()}

def static_inputs(root):
 """Current exact root and actual native inputs; no caller-supplied expectations."""
 s=entry();root,b,x=s.preflight(root)
 paths={'directory':'layout_outputs/directory.json','rules':'layout_outputs/rules.json','procedure':'layout_outputs/procedure.json'}
 values={k:s.load(root/v) for k,v in paths.items()};d=values['directory'];r=values['rules'];p=values['procedure']
 same(d['candidate_binding'],b['scope']['candidate_binding'],'DRAFT-CANDIDATE')
 same(d['contexts'],['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'DRAFT-CONTEXT-ORDER')
 same(p['binding']['candidate'],d['candidate_binding'],'DRAFT-PROCEDURE-CANDIDATE')
 same(p['binding']['contexts'],d['context_definitions'],'DRAFT-PROCEDURE-CONTEXTS')
 ordered=d['relations']+r['rules']
 same([a['ordinal'] for a in ordered],[a['ordinal'] for a in p['relation_duties']],'DRAFT-DUTY-ORDINALS')
 need(len(set(a['ordinal'] for a in ordered))==len(ordered),'DUPLICATE-ORDINAL')
 same([(a['context'],a['class']) for a in d['directories']],[(a['context'],a['class']) for a in p['directory_ranges']],'DRAFT-DIRECTORY-DUTIES')
 need(all(a['cardinality'] is None and a['range'] is None and a['classification']=='UNKNOWN' and a['disposition']=='NOT-ESTABLISHED' for a in p['directory_ranges']),'DIRECTORY-UNKNOWN')
 need(all(a['count'] is None and a['edge_range'] is None and a['classification']=='UNKNOWN' and a['disposition']=='NOT-ESTABLISHED' for a in p['relation_duties']),'RELATION-UNKNOWN')
 tree=ast.parse((root/'native/code/bind_ledger.py').read_bytes())
 assignments=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DUTIES' for t in n.targets)]
 need(len(assignments)==1,'NATIVE-DUTIES');duties=list(ast.literal_eval(assignments[0].value))
 need(all(a['duty_names']==duties for a in p['directory_ranges']),'NATIVE-DUTY-COMPATIBILITY')
 current=[*paths.values(),*['candidate/'+n for n in ('identity.json','profile-binding.json','contexts.json','inheritance.json','native-mapping.json','namespace.json','ledger-duties.json')],'native/records/relation-rules.json','native/candidate/identity.json','native/candidate/ledger/binding.json','native/code/expand_candidate.py','native/code/bind_ledger.py','native/code/finalize_records.py','compiler/prospective_procedure.py','compiler/layout_consumers.py','preflight/sources/S90-FCR.md','support/reference/relationships-43.json']
 refs={n:ident(root/n) for n in current}
 common={'assessment':'SOURCE-ONLY','candidate_binding':d['candidate_binding'],'contexts':s.load(root/'candidate/contexts.json'),'consumed_current_inputs':refs,'root_manifest':ident(P/'source-only/universe/provenance/root-members.json'),'scope_manifest':ident(P/'source-only/scope/protected-scope-v2.json'),'expression_input':ident(P/'source-only/scope/expression-bindings.json'),'obligations_input':ident(P/'source-only/scope/remaining-obligations.json'),'adapter_source':ident(Path(__file__)),'source_only_entry':ident(P/'source-only/code/scope_integration.py')}
 status={'draft_metadata_validity':'REQUIRES-CURRENT-VALIDATION','complete_instantiated_model':False,'qualified':False,'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY','global_lifetime_bound':None,'global_storage_byte_bound':None}
 model={'format':'I164-SOURCE-ONLY-DRAFT-MODEL-INPUT-1','binding':common,'status':status,'directory_program':d,'semantic_rule_program':r,'procedure_input':{'path':paths['procedure'],**refs[paths['procedure']]},'inheritance':s.load(root/'candidate/inheritance.json'),'historical_model_identity':{'path':'native/candidate/identity.json',**refs['native/candidate/identity.json'],'role':'HISTORICAL-REFERENCE-ONLY; not current model bytes verified'},'native_target':source_contract(root,'native/code/expand_candidate.py','prepare'),'invocation':{'allowed':False,'reason':'Native prepare requires concrete verified parent/base models and complete finite occurrence groups; UNKNOWN guarded directories are not instantiated groups. Prospective typed joins are consumed by the existing procedure adapter, not substituted into historical prepare.'},'cardinality_inputs':b['expressions'],'totals':{'tokens':None,'pairs':None,'model_bytes':None},'obligations':b['obligations']['obligations']}
 ledger={'format':'I164-SOURCE-ONLY-DRAFT-LEDGER-INPUT-1','binding':common,'status':status,'procedure_input':p,'candidate_ledger_requirements':s.load(root/'candidate/ledger-duties.json'),'native_duty_names':duties,'inherited_relations':d['inherited_relations'],'native_target':source_contract(root,'native/code/bind_ledger.py','build'),'invocation':{'allowed':False,'reason':'Native build requires verified saved current model identity, instantiated groups, structural counts and edge/token ranges. Historical binding remains inherited evidence, not a prospective binding.'},'obligations':b['obligations']['obligations']}
 return root,copy.deepcopy({'model-input.json':model,'ledger-input.json':ledger})

def validate_static(root,submitted):
 root,expected=static_inputs(root);same(submitted,expected,'DRAFT-INPUT-SUBSTITUTION');return root

def provenance(values,receipt):
 return {'format':'I164-DRAFT-CONSTRUCTION-PROVENANCE-1','inputs':{n:{'bytes':len(enc(v)),'sha256':hashlib.sha256(enc(v)).hexdigest()} for n,v in values.items()},'source_only_result':{'bytes':len(enc(receipt)),'sha256':hashlib.sha256(enc(receipt)).hexdigest()},'validation_path':['scope_integration.validate','universe.consume','cardinality.consume','layout_consumers.derive','Candidate.ingest','prospective_procedure.consume','construction_inputs.validate_static','construction_inputs.consume_draft','prospective_procedure.validate_input'],'constructed_kind':'DRAFT-METADATA-INPUTS; not model or ledger instances','current_model_identity':None,'current_ledger_identity':None,'qualification_established':False,'actual_admission':False}

def consume_draft(root,values):
 """Feed emitted objects to the retained prospective procedure input validator."""
 sys.path.insert(0,str(root/'compiler'))
 import semantic,prospective_procedure
 semantic.setup(root)
 model=values['model-input.json'];ledger=values['ledger-input.json']
 prospective_procedure.validate_input(ledger['procedure_input'],model['directory_program'],model['semantic_rule_program'])
 return True

def build(root):
 root,values=static_inputs(root)
 consume_draft(root,values) # actual emitted objects, retained procedure validator
 receipt=entry().validate(root) # real reviewed current validators; no detached receipt shortcut
 same(receipt['candidate_binding'],values['model-input.json']['binding']['candidate_binding'],'RECEIPT-CANDIDATE')
 need(len(receipt['obligations'])==11,'RECEIPT-OBLIGATIONS')
 return copy.deepcopy({**values,'source-only-result.json':receipt,'provenance.json':provenance(values,receipt)})

def validate(root,bundle):
 need(type(bundle) is dict and set(bundle)==set(FILES),'DRAFT-MEMBERSHIP')
 values={n:bundle[n] for n in ('model-input.json','ledger-input.json')}
 root=validate_static(root,values)
 same(bundle['provenance.json'],provenance(values,bundle['source-only-result.json']),'DRAFT-PROVENANCE')
 consume_draft(root,values)
 entry().validate_result(root,bundle['source-only-result.json']) # full authoritative current regeneration
 return {'format':'I164-DRAFT-INPUTS-VALIDATED-1','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'metadata_correspondence':True,'native_prepare_invoked':False,'native_ledger_build_invoked':False,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False}

def write_bundle(dest,bundle):
 dest=Path(dest);need(not dest.exists(),'OUTPUT-EXISTS');dest.mkdir(parents=True)
 for n in FILES:(dest/n).write_bytes(enc(bundle[n]))
 (dest/'MANIFEST.json').write_bytes(enc({n:ident(dest/n) for n in FILES}))
def read_bundle(dest):
 s=entry();dest=Path(dest);need({q.name for q in dest.iterdir()}==set(FILES)|{'MANIFEST.json'},'BUNDLE-MEMBERSHIP')
 m=s.load(dest/'MANIFEST.json');need(set(m)==set(FILES),'BUNDLE-MANIFEST-MEMBERSHIP')
 for n in (*FILES,'MANIFEST.json'):need((dest/n).is_file() and not (dest/n).is_symlink(),'BUNDLE-PATH')
 for n in FILES:same(ident(dest/n),m[n],'BUNDLE-BYTES')
 return {n:s.load(dest/n) for n in FILES}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--output');ap.add_argument('--validate');a=ap.parse_args();need(bool(a.output)!=bool(a.validate),'MODE')
 if a.output:write_bundle(a.output,build(a.root));print('PASS draft model/ledger inputs constructed; full expansion/final binding BLOCKED')
 else:print(json.dumps(validate(a.root,read_bundle(a.validate)),sort_keys=True))
