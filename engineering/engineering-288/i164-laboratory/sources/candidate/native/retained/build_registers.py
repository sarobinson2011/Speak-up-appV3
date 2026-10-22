"""Bounded additive model construction. Never enumerate pairs or serialize links.
Schema coverage is of the explicitly recorded producer forms, not source qualification.
"""
import json,hashlib,sys,resource,time,copy
from pathlib import Path
R=Path(__file__).resolve().parent
W=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
H=lambda b:hashlib.sha256(b).hexdigest()

def streamed_hash(value):
 h=hashlib.sha256()
 for chunk in json.JSONEncoder(sort_keys=True,separators=(',',':')).iterencode(value):h.update(chunk.encode())
 h.update(b'\n');return h.hexdigest()

def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(W(x))
def fields(x,path=''):
 yield path or '/','OBJECT' if type(x)==dict else 'ARRAY' if type(x)==list else 'NULLABLE-JSON' if x is None else 'BOOL' if type(x)==bool else 'UINT' if type(x)==int else 'STRING'
 if type(x)==dict:
  for k,v in sorted(x.items()):yield from fields(v,path+'/'+k.replace('~','~0').replace('/','~1'))
 elif type(x)==list:
  for i,v in enumerate(x):yield from fields(v,path+'/'+str(i))
def main(base):
 resource.setrlimit(resource.RLIMIT_AS,(6*1024**3,6*1024**3));resource.setrlimit(resource.RLIMIT_CPU,(180,180));start=time.monotonic();print('START: bounded metadata only',flush=True)
 raw=(base/'model.json').read_bytes();assert H(raw)=='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d';m=json.loads(raw);del raw
 old={k:{'sha256':H(W(v)),'count':len(v) if type(v)==list else None} for k,v in m.items()}
 contract=json.loads((base/'contract.json').read_bytes());assert H((base/'contract.json').read_bytes())=='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc'
 original43=json.loads((R/'mapping/records/relationships-43.json').read_bytes());assert len(original43)==43
 forms=json.loads((R/'registers/source-forms.json').read_bytes());rows=[];edges=[];lookup={};schemas={}
 for form in forms:
  name=form['name'];schema=[]
  for pointer,typ in fields(form['shape']):
   # Exact registered field-class identity; no aliases or occurrence-qualified IDs.
   fid='I164:'+name+'.F'+H(pointer.encode())[:24]
   row={'node_id':fid,'record':name,'selector':pointer,'representation':typ,'owner_source_id':'I164-EXACT-CUT-PROFILE-3','owner_authority':'STEVE-PROJECT-AUTHORITY','source_file':form['source'],'source_sha256':H((R/form['source']).read_bytes()),'source_anchor':form['anchor'],'phase':form['phase'],'paths':form['paths'],'slots':form['slots'],'guard':form['guard'],'declared_exposure':'UNKNOWN','custody':['UNKNOWN']*7,'reuse':'NONE','genuine_value':'UNAVAILABLE','qualification':'UNAVAILABLE'}
   rows.append(row);schema.append({'pointer':pointer,'representation':typ,'field':fid});lookup[name,pointer]=fid
  record='I164:'+name+'.$record';rows.append({**row,'node_id':record,'selector':'$record','representation':'CANONICAL-RECORD-BYTES'})
  for x in schema:edges.append({'from_node':x['field'],'to_node':record,'relation':'OWNS-RECORD-FIELD'})
  schemas[name]={'fields':schema,'record':record,'source_sha256':H((R/form['source']).read_bytes()),'slots':form['slots'],'guard':form['guard']}
 # All original relationship endpoints, including currently unavailable external facts.
 components=sorted({f['retained_flow'][side] for f in original43 for side in ['from','to']} | {c['id'] for method in ['signPetition','signPetitionWithZKProof'] for c in json.loads((R/('records/program-'+method+'.json')).read_bytes())['components']})
 for cid in components:
  fid='I164:PROJECTION.'+cid
  rows.append({'node_id':fid,'record':'PROJECTION','selector':cid,'representation':'OWNING-TYPED-PROJECTION','owner_source_id':'I164-EXACT-CUT-PROFILE-3','owner_authority':'STEVE-PROJECT-AUTHORITY','source_file':'records/coverage.json','source_sha256':H((R/'records/coverage.json').read_bytes()),'source_anchor':cid,'phase':['E','PRE-EXECUTION','PRE-COMMITMENT'],'paths':['signPetition','signPetitionWithZKProof'],'slots':64,'guard':'slot<=actual submissions; component applicability retained; unavailable is not absent','declared_exposure':'UNKNOWN','custody':['UNKNOWN']*7,'reuse':'NONE','genuine_value':'UNAVAILABLE','qualification':'UNAVAILABLE'})
 for f in original43:edges.append({'from_node':'I164:PROJECTION.'+f['retained_flow']['from'],'to_node':'I164:PROJECTION.'+f['retained_flow']['to'],'relation':'I164-RETAINED-RELATION-'+str(f['ordinal'])})
 # Full source-to-record/projection links; no field excluded as an opaque wrapper.
 for method in ['signPetition','signPetitionWithZKProof']:
  spec=json.loads((R/('records/program-'+method+'.json')).read_bytes())
  for cid in [c['id'] for c in spec['components']]:
   target='I164:PROJECTION.'+cid
   for row in rows:
    if row['record']=='CARRIER-'+method and ('/'+cid+'-' in row['selector'] or '/'+cid+'/' in row['selector']):edges.append({'from_node':row['node_id'],'to_node':target,'relation':'I164-TYPED-READ-OR-OPENING'})
   edges.append({'from_node':target,'to_node':'I164:EFFECTS.$record','relation':'I164-REQUIRED-COMPARISON-BEFORE-EFFECT'})
  edges.append({'from_node':'I164:OBSERVER-'+method+'.$record','to_node':'I164:CARRIER-'+method+'.$record','relation':'I164-SAME-CALL-PROJECTION'})
 # Framing/status/presence remain explicit fields; seven custody cells per class,
 # UNKNOWN always; these do not become claims of actual visibility.
 source_rows=list(rows)
 for row in source_rows:
  for tag in ['PRESENCE','STATUS','ENCODING-LENGTH']:
   q={**row,'node_id':row['node_id']+'-'+tag if not row['node_id'].endswith('.$record') else row['node_id'][:-8]+'.RECORD-'+tag,'selector':row['selector']+'#'+tag,'representation':tag};rows.append(q);edges.append({'from_node':q['node_id'],'to_node':row['node_id'],'relation':'I164-FRAMING-'+tag})
 ids={r['node_id'] for r in rows};assert len(ids)==len(rows)
 assert all(e['from_node'] in ids and e['to_node'] in ids for e in edges)
 print('REGISTER',len(rows),'fields',flush=True);write(R/'registers/fields.json',rows);write(R/'registers/schemas.json',schemas);write(R/'registers/dependencies.json',edges)
 # Preserve every inherited array element exactly, append extension in stable order.
 startn=len(m['tokens']);starte=len(m['structural_edges']);starts=len(m['surfaces']);startr=len(m['relations'])
 m['surfaces'] += [{'node_id':r['node_id'],'kind':'OWNING-SCHEMA','owner_source_id':r['owner_source_id'],'owner_anchor':r['source_anchor'],'declared_exposure':'UNKNOWN','reuse':'NONE','source_data':''} for r in rows]
 m['relations']+=edges
 print('BASE-PRESERVED; expanding added token directories',flush=True);idx={};arbitrary=H(b'ARBITRARY')
 for context in ['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']:
  for row in rows:
   for slot in range(1,row['slots']+1):
    i=len(m['tokens']);idx[row['node_id'],context,slot]=i;m['tokens'].append({'index':i,'id':'I164-TOKEN-'+str(i),'surface':row['node_id'],'context':context,'record':slot,'exposure':'UNKNOWN','reuse':'NONE','arbitrary':True,'symbolic_digest':arbitrary})
 slotmap={r['node_id']:r['slots'] for r in rows}
 print('TOKENS',len(m['tokens']),flush=True)
 for number,e in enumerate(edges,startr+1):
  for context in ['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']:
   a,b=e['from_node'],e['to_node'];aa,bb=slotmap[a],slotmap[b]
   for slot in range(1,max(aa,bb)+1):m['structural_edges'].append([idx[a,context,min(slot,aa)],idx[b,context,min(slot,bb)],number,e['relation']])
 print('EDGES',len(m['structural_edges']),flush=True)
 # Exact cardinality by counting appended arbitrary tokens. No pair enumeration.
 added=len(m['tokens'])-startn;n=startn;m['equality_stream']={**m['equality_stream'],'rows':m['equality_stream']['rows']+n*added+added*(added-1)//2,'sha256':None}
 m['equality_stream']['bytes']=len(b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n')+8*m['equality_stream']['rows']
 out=R/'candidate';out.mkdir(exist_ok=True)
 # JSON iterencode avoids another giant serialized allocation.
 print('SERIALIZING',flush=True)
 with (out/'model.json').open('w') as f:
  for chunk in json.JSONEncoder(sort_keys=True,separators=(',',':')).iterencode(m):f.write(chunk)
  f.write('\n')
 del idx
 def fh(p):
  h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  return h.hexdigest()
 candidate_hash=fh(out/'model.json')
 for k,n in [('surfaces',starts),('relations',startr),('tokens',startn),('structural_edges',starte)]:assert H(W(m[k][:n]))==old[k]['sha256']
 extension={'format':'I164-REGISTER-MODEL-BINDING-1','profile':'I164-EXACT-CUT-PROFILE-3','parent_profile':'I164-EXACT-CUT-PROFILE-2','model_sha256':candidate_hash,'model_bytes':(out/'model.json').stat().st_size,'parent_model_sha256':'dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d','parent_contract_sha256':H((base/'contract.json').read_bytes()),'registers':{str(f.relative_to(R)):fh(f) for f in (R/'registers').glob('*.json')},'programs':{str(f.relative_to(R)):fh(f) for f in (R/'records').glob('program-signPetition*.json')},'unknown_custody_preserved':True,'binary_stream_sha256':None,'textual_stream_sha256':None,'actual_admission':False}
 write(out/'profile-binding.json',extension)
 # The inherited finite contract is historical; this wrapper does not impersonate CP2.
 write(out/'finite-directory.json',{'format':'I164-FINITE-DIRECTORY-1','parent_contract':extension['parent_contract_sha256'],'profile_binding_sha256':H(W(extension)),'max_submissions':64,'method_guards':'exactly one selected method per slot, both modeled','schemas_sha256':H((R/'registers/schemas.json').read_bytes()),'source_qualification':'UNAVAILABLE','candidate_streams':'UNCOMPUTED','actual_admission':False})
 write(out/'delta.json',{'old_arrays':old,'new_arrays':{k:{'count':len(m[k]),'sha256':streamed_hash(m[k])} for k in ['surfaces','relations','tokens','structural_edges']},'inherited_prefixes_exact':True,'changed_fields':['surfaces','relations','tokens','structural_edges','equality_stream.rows','equality_stream.bytes','equality_stream.sha256'],'unchanged_fields':['actor_graph_policy','equality_stream.format','equality_stream.row_encoding','equality_stream.ordering','equality_stream.predicate'],'new_equality_stream':m['equality_stream'],'historical_binary_and_textual_evidence_not_rebound':True,'new_model_sha256':candidate_hash})
 write(R/'results/register-construction.json',{'result':'PASS-ADDITIVE-REGISTER-CONSTRUCTION','fields':len(rows),'added_tokens':added,'added_relations':len(edges),'model_bytes':(out/'model.json').stat().st_size,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'pairs_processed':0,'qualification_established':False,'actual_admission':False})
 print((R/'results/register-construction.json').read_text())
if __name__=='__main__':main(Path(sys.argv[1]))
