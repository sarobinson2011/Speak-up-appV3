"""One explicit conditional owning-source language, not a universal source parser."""
from pathlib import Path
from v4_ingest.records import require,exact,digest,canonical,SPEC
from semantic_stream.storage import Blob,unhex
from scope_auth.material import payload
from .codec import validate
from .index import ExactValues,build

def acquire(adapter,provider,trusted,request,model):
 phase=request['phase'];require(phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'),'occurrence phase',category='INVALID-ACTION-CONTEXT')
 ref=trusted.get('occurrence_source_ref');require(ref is not None,'independent owning occurrence source absent',category='MISSING-EVIDENCE')
 source=payload(provider,ref)
 exact(source,('format','binding','types','assignments'))
 require(source['format']=='CP4L-OWNING-OCCURRENCES-1','unsupported owning source grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 binding={'source_id':trusted['source_id'],'source_sha256':trusted['source_sha256'],'model_sha256':model.digest,'profile_sha256':request['profile_digest'],'contract_sha256':digest(canonical(trusted['evidence_contract'])),'phase':phase,'attempt':request['attempt'],'mapping_digest':request['mapping_digest']}
 require(source['binding']==binding,'owning source/model/profile/contract/phase/attempt join',category='INVALID-ACTION-CONTEXT')
 require(isinstance(source['types'],list) and len(source['types'])<=4096,'type declaration capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 derived=[(r[0],r[1],list(r[2])) for r in source['types']]
 from v4_ingest.typed import Codec
 Codec(derived)
 rows=source['assignments'];require(isinstance(rows,list),'occurrence assignment directory')
 require(len(rows)==len(model.tokens),'complete actual occurrence count',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 bindings=request['occurrence_bindings'];expected=trusted['occurrence_bindings']
 require(len(bindings)==len(expected)==len(model.ids) and all(k in bindings and k in expected for k in model.ids),'complete exact required occurrence bindings',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 from metadata_catalog.core import temporary
 ordered=temporary(adapter.store.root,'occurrence-rows-');adapter.store.docs.append(ordered)
 for row in rows:
  exact(row,('token_id','surface_id','context','record','codec','type_id','value_ref'))
  name=row['token_id'];require(name in model.ids and name not in ordered,'unknown/duplicate/conflicting occurrence assignment',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  t=model.tokens[model.ids[name]]
  require((row['surface_id'],row['context'],row['record'])==(t['surface'],t['context'],t['record']),'exact owning token occurrence join',category='INVALID-ACTION-CONTEXT')
  require(row['value_ref']==bindings[name]==expected[name],'independently owned value reference',category='INVALID-ACTION-CONTEXT')
  if t['surface'].startswith(('SECURITY:','SECURITY-FRAME:','CP2-REF-PARSER:')):
   from .projection import law
   _,_,typ=law(t['surface'])
   require(row['codec']=='S90-JSON-LF' and row['type_id']==typ,'S90 owning projection byte/type law',category='INVALID-ACTION-CONTEXT')
  if t['surface'].startswith('SECURITY:'):
   schema,field=t['surface'][9:].split('.',1)
   if schema in SPEC:
    typ='RECORD:'+schema if field=='$record' else SPEC[schema].get(field)
    require(typ is not None and row['codec']=='S90-JSON-LF' and row['type_id']==typ,'S90 owning field byte/type law',category='INVALID-ACTION-CONTEXT')
  ordered.add(name,dict(row.items()))
 # Acquire/validate all source dependencies before a saved equality index can be
 # reused. Its MAC is executor provenance, never owning-source qualification.
 from .projection import Projections,FORMAT
 from .generated import Generated,FORMAT as GENERATED

 projections=Projections(adapter,provider,trusted,binding,model)
 generated=Generated(projections)
 generated.prepare()
 def values():
  for t in model.tokens:
   row=ordered[t['id']];obj=payload(provider,row['value_ref'])
   if obj.get('format')==GENERATED:
    yield t['id'],generated.project(obj,row,t)
    continue
   if obj.get('format')==FORMAT:
    yield t['id'],projections.project(obj,row,t)
    continue
   require(not t['surface'].startswith(('CP2-RECORD-PARSER:','CP2-REFERENCE-MATERIAL:')),'complete source-generated event carrier required',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   require(not t['surface'].startswith(('SECURITY:','SECURITY-FRAME:','CP2-REF-PARSER:')),'exact complete containing object projection required; standalone field bytes are insufficient',category='MISSING-EVIDENCE')
   exact(obj,('format','binding','token_id','codec','type_id','encoded_hex'))
   require(obj['format']=='CP4L-OWNING-VALUE-1' and obj['binding']==binding and obj['token_id']==t['id'] and obj['codec']==row['codec'] and obj['type_id']==row['type_id'],'value source/profile/model/phase/type correspondence',category='INVALID-ACTION-CONTEXT')
   from v4_ingest.records import primitive
   primitive('BYTES',obj['encoded_hex']);raw=unhex(obj['encoded_hex']);blob=raw if isinstance(raw,Blob) else adapter.store.write([raw])
   validate(blob,row['codec'],row['type_id'],derived,[s['node_id'] for s in model.value['surfaces']])
   yield t['id'],blob
 scheduler=adapter.scheduler;identity={'binding':binding,'source_ref':dict(ref),'directory_sha256':digest(canonical(source))}
 root=scheduler.root if scheduler is not None else adapter.store.root;path=root/'occurrence-equality.sqlite'
 if scheduler is not None:
  old=scheduler.read('occurrence-values')
  if old is not None:
   require(old['complete'] and old['inputs']==identity,'stale/incomplete occurrence index')
   # Exact acquisition and canonical checks are repeated; avoids treating the
   # directory/journal alone as authenticating owning source bytes.
   for _ in values():pass
   for p,h in old['artifacts'].items():scheduler.verify(p,h)
   scheduler.event('occurrence-values','REUSED-EXACT-SOURCE-AND-INDEX')
  else:
   artifacts=build(path,values(),adapter.store,identity,adapter.remaining)
   scheduler.save('occurrence-values',identity,{'database':path.name},True,artifacts=artifacts)
 else:build(path,values(),adapter.store,identity,adapter.remaining)
 result=ExactValues(path,adapter.store,identity);adapter.occurrence_report={'complete':True,'tokens':len(model.tokens),'projections':projections.count,'containing_objects':projections.object_count,'generated_projections':generated.count,'generated_events':generated.event_count,'equality_pairs':result.count(model.tokens),'source_binding':identity,'qualification':'EXPLICIT-LAB-ASSUMPTIONS-ONLY','actual_qualification_established':False}
 return result
