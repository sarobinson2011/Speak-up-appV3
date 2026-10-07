"""CP2 generated events, projected only after complete source event validation.

Conditional acquisition grammar. It does not appoint the producing observer.
Exact selected-contract domains/selectors are read, never model-expanded.
"""
import json,re
from pathlib import Path
from v4_ingest.records import (SPEC,IDENTITY,canonical,digest,parse,primitive,exact,
                              require,ValidationError)
from semantic_stream.storage import Blob,unhex
from scope_auth.material import payload
from metadata_catalog.core import temporary
from .projection import as_blob,bounded_record
from .codec import compare
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=json.loads((ROOT/'rebinding/selected-contract.json').read_bytes())
PARSER=tuple(CONTRACT['parser']['event_fields'])
MATERIAL=tuple(CONTRACT['material_acquisition']['fields'])
FORMAT='CP4P-GENERATED-PROJECTION-1'
TYPES=dict(schema_id='ID',record_id='ID',input_record='BYTES',output_record='BYTES',
 result_kind='ENUM-CP2-PARSER-BRANCH',phase='ENUM-STAGE',attempt_ordinal='UINT',owner_reference='SOURCE-REF',
 grammar_reference='SOURCE-REF',parent_invocation='ID',exact_bytes='BYTES',
 lookup_status='ENUM-CP2-LOOKUP-STATUS',owning_reference='SOURCE-REF')

def law(surface):
 for prefix,kind,fields in [('CP2-RECORD-PARSER:','PARSER',PARSER),('CP2-REFERENCE-MATERIAL:','MATERIAL',MATERIAL)]:
  if surface.startswith(prefix) and surface[len(prefix):] in fields:
   f=surface[len(prefix):];return kind,f,TYPES[f]
 require(False,'unsupported generated-event class',category='INCOMPLETE-EVIDENCE-UNIVERSE')

def rules(binding):
 return {'format':'CP4P-GENERATED-RULES-1','binding':binding,
  'selected_contract_sha256':digest((ROOT/'rebinding/selected-contract.json').read_bytes()),
  'parser_code':'v4_ingest.records.ingest_record',
  'code_sha256':{n:digest((ROOT/n).read_bytes()) for n in ('v4_ingest/records.py','occurrence_values/generated.py')},
  'grammar_sha256':digest((ROOT/'v4_ingest/data/security-fields.tsv').read_bytes()),
  'amendment_sha256':digest((ROOT/'amendments/PE-G4-FIELD-CLASS-REF-AMENDMENT-001/v1.0.0/BINDING.json').read_bytes()),
  'unavailable':'ABSENT-IN-CAPTURED-LOOKUP','inapplicable':'SOURCE-GUARDED-NO-INVOCATION',
  'material_grammar':'CP3-LAB-MATERIAL-V1','nullable_bytes':'ONLY-DECLARED-EVENT-OUTCOMES'}

def selector(token):
 kind,field,typ=law(token['surface']);record=token['record'];context=token['context']
 require(context in CONTRACT['contexts'],'generated context domain',category='INVALID-ACTION-CONTEXT')
 if kind=='PARSER':
  m=re.fullmatch(r'([^:]+):(.+):PARSE:([0-9]{6})',str(record))
  require(m is not None,'CP2 parser occurrence selector',category='INVALID-ACTION-CONTEXT')
  schema,rid,number=m.groups();n=int(number)
  require(schema in SPEC and 1<=n<=CONTRACT['record_parser_attempts'],'exact parser schema/attempt domain',category='INVALID-ACTION-CONTEXT');primitive('ID',rid)
  parent=schema+':'+rid;detail=n
 else:
  m=re.fullmatch(r'([^:]+):(.+):REF:([^:]+):([0-9]{6})',str(record))
  require(m is not None,'CP2 material occurrence selector',category='INVALID-ACTION-CONTEXT')
  schema,rid,f,number=m.groups();n=int(number);typeref=SPEC.get(schema,{}).get(f)
  require(typeref in ('SOURCE-REF','LIST-SOURCE-REF') and 1<=n<=(CONTRACT['reference_list_elements'] if typeref=='LIST-SOURCE-REF' else 1),'exact reference field/item domain',category='INVALID-ACTION-CONTEXT');primitive('ID',rid)
  parent=record;detail=(schema,rid,f,n)
 return kind,field,typ,context+'|'+kind+'|'+parent,detail

class Generated:
 def __init__(self,projections):
  self.p=projections;self.store=projections.store;self.provider=projections.provider
  self.trusted=projections.trusted;self.binding=projections.binding;self.count=0;self.event_count=0
  self.need=temporary(self.store.root,'generated-required-');self.refs=temporary(self.store.root,'generated-refs-');self.checked=temporary(self.store.root,'generated-checked-')
  self.store.docs.extend([self.need,self.refs,self.checked]);self.prepared=False
 def prepare(self):
  if self.prepared:return
  for t in self.p.model.tokens:
   if not t['surface'].startswith(('CP2-RECORD-PARSER:','CP2-REFERENCE-MATERIAL:')):continue
   kind,f,_,key,detail=selector(t);mask=self.need.get(key,0)
   bit=(detail-1)*len(PARSER)+PARSER.index(f) if kind=='PARSER' else MATERIAL.index(f)
   require(not(mask & (1<<bit)),'duplicate generated required occurrence',category='INCOMPLETE-EVIDENCE-UNIVERSE');self.need[key]=mask|(1<<bit)
  if not self.need:self.prepared=True;return
  self.provider.role('source-producer-correspondence');self.provider.role('observer-completeness')
  r=self.trusted.get('generated_rules_ref');require(r is not None,'independent generated grammar/code reference absent',category='MISSING-EVIDENCE')
  require(payload(self.provider,r)==rules(self.binding),'exact generated grammar/code/amendment binding',category='INVALID-EVIDENCE-AUTHORITY')
  ref=self.trusted.get('generated_source_ref');require(ref is not None,'complete source event directory absent',category='MISSING-EVIDENCE')
  d=payload(self.provider,ref);exact(d,('format','binding','rules_ref','events'))
  require(d['format']=='CP4P-GENERATED-DIRECTORY-1' and d['binding']==self.binding and d['rules_ref']==r,'generated source directory binding',category='INVALID-ACTION-CONTEXT')
  require(isinstance(d['events'],list),'generated source directory array');previous=None
  for row in d['events']:
   exact(row,('key','event_ref'));key=row['key'];primitive('SOURCE-REF',row['event_ref'])
   require(type(key) is str and (previous is None or previous<key) and key in self.need,'extra/duplicate/unordered generated event',category='INCOMPLETE-EVIDENCE-UNIVERSE');previous=key
   expected=(1<<(len(PARSER)*CONTRACT['record_parser_attempts']))-1 if '|PARSER|' in key else (1<<len(MATERIAL))-1
   require(self.need[key]==expected,'incomplete required containing-event field/attempt directory',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   self.refs.add(key,dict(row['event_ref']))
  require(len(self.refs)==len(self.need),'missing generated containing events',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  self.prepared=True
 def record(self,obj,schema,rid,required=True):
  key,blob,value=self.p.object(obj['container_ref']);k=key+':'+schema+':'+rid
  if k not in self.p.records:
   require(not required,'missing generated parent containing record',category='INCOMPLETE-EVIDENCE-UNIVERSE');return None
  return value['records'][schema]['instances'][self.p.records[k]]
 def bytes(self,value):
  primitive('BYTES',value);b=unhex(value);return b if isinstance(b,Blob) else self.store.write([b])
 def reference(self,ref):
  # Authentication of the source and appointment joins without requiring the
  # referenced material to exist. Used only for explicit missing/invalid lookups.
  primitive('SOURCE-REF',ref);t=self.trusted
  require(ref['owner_source_id']==t['source_id'] and ref['source_sha256']==t['source_sha256'] and t['anchors'].get(ref['source_anchor'])==ref['material_sha256'],'owning lookup source/anchor binding',category='INVALID-EVIDENCE-AUTHORITY')
  source=self.provider.sources.get(ref['source_sha256']);require(source is not None and digest(source)==ref['source_sha256'],'lookup source bytes',category='INVALID-EVIDENCE-DIGEST')
 def validate(self,key,ref):
  obj=payload(self.provider,ref)
  exact(obj,('format','binding','rules_ref','container_ref','context','kind','schema_id','record_id','invocation_id','events'))
  require(obj['format']=='CP4P-GENERATED-EVENTS-1' and obj['binding']==self.binding and obj['rules_ref']==self.trusted['generated_rules_ref'],'event source/model/profile/contract/code join',category='INVALID-ACTION-CONTEXT')
  kind=obj['kind'];schema=obj['schema_id'];rid=obj['record_id'];context=obj['context'];primitive('ID',obj['invocation_id'])
  require(schema in SPEC and context in CONTRACT['contexts'],'event schema/context domain');primitive('ID',rid)
  if ref['material_sha256'] in self.checked:
   require(self.checked[ref['material_sha256']]==key,'cross-parent event replay',category='INVALID-ACTION-CONTEXT')
  rec=self.record(obj,schema,rid,required=kind!='PARSER')
  require(isinstance(obj['events'],list),'complete containing-event array')
  if kind=='PARSER':
   require(key==context+'|PARSER|'+schema+':'+rid,'parser exact parent correspondence',category='INVALID-ACTION-CONTEXT')
   require(len(obj['events'])==CONTRACT['record_parser_attempts'],'complete exact parser attempts',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   for n,event in enumerate(obj['events'],1):
    exact(event,('fields','justification_ref'));f=event['fields'];exact(f,PARSER)
    require(f['schema_id']==schema and f['record_id']==rid and f['phase']==self.binding['phase'] and type(f['attempt_ordinal']) is int and f['attempt_ordinal']==n and f['parent_invocation']==obj['invocation_id'] and f['owner_reference']==obj['container_ref'] and f['grammar_reference']==obj['rules_ref'],'parser fields exact parent/ordinal/phase/owner/grammar',category='INVALID-ACTION-CONTEXT')
    status=f['result_kind'];require(status in CONTRACT['parser']['branch_domain'],'parser branch domain')
    if status in ('VALID-LOCAL','INVALID-LOCAL'):
     require(event['justification_ref'] is None,'invoked parser has no absent guard');raw=self.bytes(f['input_record'])
     try:
      parsed=parse(raw);bounded_record(schema,parsed,self.p.register);valid=True
     except ValidationError as e:
      # Capability/interruptions never prove local rejection.
      if e.category in ('RESOURCE-LIMIT','INCOMPLETE-EVIDENCE-UNIVERSE'):raise
      valid=False
     require(valid==(status=='VALID-LOCAL'),'dishonest parser local branch',category='INVALID-ACTION-CONTEXT')
     if valid:
      require(rec is not None,'valid parser requires available exact containing record',category='INCOMPLETE-EVIDENCE-UNIVERSE')
      require(parsed[IDENTITY[schema]]==rid,'parsed record exact identity',category='INVALID-ACTION-CONTEXT')
      require(compare(raw,as_blob(self.store,rec))==0 and compare(raw,self.bytes(f['output_record']))==0,'exact accepted parser input/output/containing record bytes',category='INVALID-ACTION-CONTEXT')
     else:require(f['output_record'] is None,'rejected parser has no typed output')
    else:
     require(f['input_record'] is None and f['output_record'] is None,'unavailable/inapplicable parser has no fabricated bytes')
     j=event['justification_ref'];require(j is not None,'missing source guarded outcome',category='MISSING-EVIDENCE')
     expected={'format':'CP4P-PARSER-GUARD-1','binding':self.binding,'context':context,'schema_id':schema,'record_id':rid,'attempt_ordinal':n,'parent_invocation':obj['invocation_id'],'result_kind':status}
     require(payload(self.provider,j)==expected,'source guard exact invocation/branch join',category='INVALID-ACTION-CONTEXT')
  elif kind=='MATERIAL':
   require(len(obj['events'])==1,'one exact acquisition per selected reference item')
   event=obj['events'][0];exact(event,('field','ordinal','fields'));field=event['field'];n=event['ordinal'];f=event['fields'];exact(f,MATERIAL)
   require(type(n) is int and SPEC.get(schema,{}).get(field) in ('SOURCE-REF','LIST-SOURCE-REF'),'source reference acquisition selector')
   require(key==context+'|MATERIAL|'+schema+':'+rid+':REF:'+field+':'+f'{n:06}','material exact parent/ordinal correspondence',category='INVALID-ACTION-CONTEXT')
   owning=rec[field]
   if SPEC[schema][field]=='LIST-SOURCE-REF':
    require(len(owning)<=CONTRACT['reference_list_elements'] and 1<=n<=len(owning),'guarded list reference multiplicity',category='INCOMPLETE-EVIDENCE-UNIVERSE');owning=owning[n-1]
   else:require(n==1,'scalar reference ordinal')
   require(owning is not None,'null owning reference has no fabricated acquisition child',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   require(f['owning_reference']==owning,'exact owning reference correspondence',category='INVALID-ACTION-CONTEXT');self.reference(owning)
   status=f['lookup_status'];require(status in CONTRACT['material_acquisition']['status_domain'],'material status domain')
   raw=self.provider.materials.get(owning['material_sha256'])
   if status=='UNAVAILABLE':require(raw is None and f['exact_bytes'] is None,'lookup unavailable requires absent material and no fabricated bytes',category='INVALID-ACTION-CONTEXT')
   else:
    observed=self.bytes(f['exact_bytes'])
    require(raw is not None and compare(raw,observed)==0,'exact consumed lookup bytes',category='INVALID-EVIDENCE-DIGEST')
    valid=digest(observed)==owning['material_sha256']
    if valid:
     try:
      value=parse(observed);exact(value,('format','payload','dependencies'));require(value['format']=='CP3-LAB-MATERIAL-V1' and isinstance(value['dependencies'],list),'material envelope')
      for dep in value['dependencies']:primitive('DIGEST',dep)
     except ValidationError as e:
      if e.category in ('RESOURCE-LIMIT','INCOMPLETE-EVIDENCE-UNIVERSE'):raise
      valid=False
    require(valid==(status=='PRESENT'),'dishonest material status',category='INVALID-ACTION-CONTEXT')
    if valid:payload(self.provider,owning) # full declared dependency closure
  else:require(False,'generated event kind')
  if ref['material_sha256'] not in self.checked:
   self.checked.add(ref['material_sha256'],key);self.event_count+=len(obj['events'])
  return obj
 def project(self,carrier,row,token):
  self.prepare();exact(carrier,('format','binding','token_id','surface_id','context','record','codec','type_id','event_ref'))
  kind,f,typ,key,detail=selector(token)
  require(carrier['format']==FORMAT and carrier['binding']==self.binding,'generated projection binding',category='INVALID-ACTION-CONTEXT')
  for a,b in [('token_id','id'),('surface_id','surface'),('context','context'),('record','record')]:require(carrier[a]==token[b],'generated exact token '+a,category='INVALID-ACTION-CONTEXT')
  require(row['codec']==carrier['codec']=='S90-JSON-LF' and row['type_id']==carrier['type_id']==typ,'generated source byte/type law',category='INVALID-ACTION-CONTEXT')
  require(key in self.refs and carrier['event_ref']==self.refs[key],'source-grounded complete event directory join',category='INVALID-ACTION-CONTEXT')
  obj=self.validate(key,self.refs[key]);event=obj['events'][detail-1 if kind=='PARSER' else 0]
  self.count+=1;return as_blob(self.store,event['fields'][f])
