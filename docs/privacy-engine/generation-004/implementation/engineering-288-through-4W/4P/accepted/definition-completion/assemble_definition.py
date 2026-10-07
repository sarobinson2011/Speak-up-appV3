"""S90 definition declaration and schema graph. No dummy governing policy/profile."""
from pathlib import Path
import csv,json,hashlib,runpy
O=Path(__file__).resolve().parents[1]
D=O/'definition-completion'
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def rows(name):return list(csv.DictReader((D/name).open(),delimiter='\t'))
def declaration():
 paths=['sources/PE-G4-SOURCE-S90.md','definition-completion/ACCEPTANCE-CONTRACT.txt','definition-completion/security-fields.tsv','definition-completion/security-relations.tsv','definition-completion/security-custody.tsv','definition-completion/qualification-interface.tsv','definition-completion/budget.py','definition-completion/assemble_definition.py','definition-completion/v4_record_grammar.py','definition-completion/E287-SOURCE-DETERMINED-CORRECTION.txt','definition-completion/security-framing-fields.tsv','definition-completion/framing-custody.tsv','definition-completion/NONVACUITY-CONTRACT.txt']
 fields=rows('security-fields.tsv');rels=rows('security-relations.tsv')
 base=runpy.run_path(str(O/'privacy/expand_privacy.py'))['construct']()
 schemas=sorted({f['schema'] for f in fields})
 nodes=[{'id':f['surface_id'],'kind':'SECURITY-FIELD-TEMPLATE','owner':'PE-G4-SOURCE-S90#schemas','exposure':'UNKNOWN','reuse':'NONE'} for f in fields]
 nodes += [{'id':'SECURITY:'+s+'.$record','kind':'SECURITY-RECORD-TEMPLATE','owner':'PE-G4-SOURCE-S90#schemas','exposure':'UNKNOWN','reuse':'NONE'} for s in schemas]
 # This graph is a schema overapproximation. Repeated records must be expanded
 # using exact source-established directories; template counts are not occurrence counts.
 return {'format':'PE-G4-DEFINITION-DECLARATION-V4','status':'UNINSTANTIATED-DEFINITION-NOT-GOVERNING-PRIVACY','source':'PE-G4-SOURCE-S90','input_sha256':{p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in paths},'prior_graph':{'tokens':base[2],'structural_edges':base[3],'potential_equality_rule':'left.arbitrary OR right.arbitrary OR equal symbolic_digest'},'security_templates':nodes,'framing_templates':rows('security-framing-fields.tsv'),'framing_custody':rows('framing-custody.tsv'),'security_relations':rels,'security_fields':fields,'record_instantiation':'Exact independently source-validated directory for every schema; no empty defaults; replicate every record in both contexts and every custody/equality edge','owning_header_join':'CORE:AUTHORIZATION-HEADER.profile-sha256','governing_policy':None,'source_appointment':None,'privacy_admission':False}

def instantiate_security(directory):
 """Mechanical expansion only. Caller directories are not authenticated by this function."""
 fields=rows('security-fields.tsv');rels=rows('security-relations.tsv');schemas={f['schema'] for f in fields}
 if type(directory) is not dict or set(directory)!=schemas:raise ValueError('complete directory required')
 one={'POLICY','ENVELOPE','LEAKAGE'}
 for s,ids in directory.items():
  if type(ids) is not list or not ids or any(type(x) is not str or not x or '::' in x for x in ids) or len(set(ids))!=len(ids) or (s in one and len(ids)!=1):raise ValueError('invalid record directory')
 tokens=[];by={}
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for s in sorted(schemas):
   for record in directory[s]:
    for surface in ['SECURITY:'+s+'.$record']+[f['surface_id'] for f in fields if f['schema']==s]:
     token={'id':context+'::'+surface+'::'+record,'surface':surface,'record':record,'context':context,'exposure':'UNKNOWN','reuse':'NONE','arbitrary':True}
     tokens.append(token);by.setdefault((context,surface),[]).append(token['id'])
 edges=[]
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for r in rels:
   left=by[(context,r['from_node'])]
   right=by.get((context,r['to_node']),[context+'::'+r['to_node']])
   for a in left:
    for b in right:edges.append([a,b,r['relation'],r['origin']])
 return {'tokens':tokens,'structural_edges':edges,'equality_policy':'All inherited pairs retained; every arbitrary security token potentially equals every old/new token','directory_authenticated':False,'profile_admitted':False}

if __name__=='__main__':
 (O/'definition-completion/DEFINITION-DECLARATION-V4.json').write_bytes(canonical(declaration()))
