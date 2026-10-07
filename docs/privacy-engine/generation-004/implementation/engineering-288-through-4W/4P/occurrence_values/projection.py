"""S90 containing-object projections. Byte checks never appoint a source.

New carrier grammar is conditional acquisition metadata, not an amendment of
S90 primitives/records. Complete external object bytes are checked first.
"""
import csv,json,re
from pathlib import Path
from v4_ingest.records import (SPEC,SCHEMAS,IDENTITY,exact,primitive,require,
                              parse,canonical,digest,validate_record)
from semantic_stream.storage import Blob,unhex,encode
from metadata_catalog.core import temporary
from scope_auth.material import payload
from .codec import compare
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'accepted/definition-completion/security-framing-fields.tsv').open() as f:
 FRAMES={r['surface_id']:r for r in csv.DictReader(f,delimiter='\t')}
FORMAT='CP4O-S90-PROJECTION-1'

def law(surface):
 if surface.startswith('CP2-REF-PARSER:'):
  parts=surface[15:].split('.')
  if len(parts)==3:
   schema,field,part=parts
   if SPEC.get(schema,{}).get(field) in ('SOURCE-REF','LIST-SOURCE-REF') and part in ('owner_source_id','source_sha256','source_anchor','material_sha256'):
    return schema,field+'.'+part,'DIGEST' if part.endswith('sha256') else 'ID'
 if surface in FRAMES:
  r=FRAMES[surface];return r['schema'],r['field'],r['type']
 if surface.startswith('SECURITY:'):
  schema,sep,field=surface[9:].partition('.')
  if sep and schema in SPEC and (field=='$record' or field in SPEC[schema]):
   return schema,field,'RECORD:'+schema if field=='$record' else SPEC[schema][field]
 require(False,'unsupported source-owned projection class '+surface,category='INCOMPLETE-EVIDENCE-UNIVERSE')

def as_blob(store,value):
 b=canonical(value);return b if isinstance(b,Blob) else store.write([b])

def bounded_record(schema,record,register):
 # Retained primitive LIST-ID validation uses a set. Bound aggregate scalar-list
 # metadata explicitly before that validator; large BYTES remain streamed.
 size=0
 for field,kind in SPEC[schema].items():
  if kind=='LIST-ID' and field in record and isinstance(record[field],list):
   for name in record[field]:
    primitive('ID',name);size+=len(name)+64
    require(size<=4194304,'projection record reference-list capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 validate_record(schema,record,field_register=register)

class Projections:
 def __init__(self,adapter,provider,trusted,binding,model):
  self.a,self.provider,self.trusted,self.binding,self.model=adapter,provider,trusted,binding,model
  self.store=adapter.store;self.objects=temporary(self.store.root,'projection-objects-');self.records=temporary(self.store.root,'projection-records-');self.store.docs.extend([self.objects,self.records])
  self.register=[s['node_id'] for s in model.value['surfaces']];self.count=0;self.object_count=0
 def object(self,ref):
  key=ref['material_sha256']
  # Reacquire the exact source ref even if its checked object locator exists.
  obj=payload(self.provider,ref)
  exact(obj,('format','binding','encoded_hex','rules_ref'))
  expected=self.trusted.get('projection_rules_ref')
  require(expected is not None and obj['rules_ref']==expected,'independent containing projection source rules',category='INVALID-EVIDENCE-AUTHORITY')
  rules=payload(self.provider,expected)
  require(rules=={'format':'CP4O-S90-SOURCE-RULES-1','binding':self.binding,'presence':'NONNULL-TYPED-VALUE','record_ids':'EXACT-S90-IDENTITY','directory_ids':'CP2-DIRECTORY-SCHEMA'},'unsupported exact source projection rules',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  self.provider.role('source-producer-correspondence')
  require(obj['format']=='CP4O-S90-CONTAINER-1','unsupported containing source grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  require(obj['binding']==self.binding,'containing object source/model/profile/contract/phase join',category='INVALID-ACTION-CONTEXT')
  if key in self.objects:
   e=self.objects[key];blob=Blob(self.store,e['path'])
   require(blob.exact_sha()==e['sha256'],'mutated containing snapshot',category='INVALID-EVIDENCE-DIGEST')
   value=parse(blob);return key,blob,value
  primitive('BYTES',obj['encoded_hex']);raw=unhex(obj['encoded_hex']);blob=raw if isinstance(raw,Blob) else self.store.write([raw])
  # This concrete adapter projects the external S90 object consumed by the
  # authenticated collector. Another well-typed object cannot be substituted.
  require(compare(blob,self.a.octets('security_records_hex'))==0,'containing object differs from authenticated security records',category='INVALID-ACTION-CONTEXT')
  value=parse(blob);exact(value,('format','profile_digest','phase','records'))
  require(value['format']=='PE-G4-SECURITY-RECORDS-V4','S90 external format')
  require(value['profile_digest']==self.binding['profile_sha256'] and value['phase']==self.binding['phase'],'containing wrapper profile/phase',category='INVALID-ACTION-CONTEXT')
  exact(value['records'],SCHEMAS)
  for schema in SCHEMAS:
   d=value['records'][schema];exact(d,('status','justification','instances'))
   require(d['status'] in ('PRESENT','UNAVAILABLE','INAPPLICABLE'),'S90 directory status')
   if d['justification'] is not None:primitive('SOURCE-REF',d['justification'])
   require(isinstance(d['instances'],list),'S90 instance array')
   require((d['status']=='PRESENT')==bool(d['instances']),'status/instance correspondence')
   require(d['status']!='INAPPLICABLE' or d['justification'] is not None,'source justification required')
   if schema in ('POLICY','ENVELOPE','LEAKAGE') and d['status']=='PRESENT':require(len(d['instances'])==1,'single owning record')
   previous=None
   for ordinal,record in enumerate(d['instances']):
    bounded_record(schema,record,self.register);ident=record[IDENTITY[schema]]
    require('::' not in ident and (previous is None or previous<ident),'unique sorted exact record identities');previous=ident
    self.records.add(key+':'+schema+':'+ident,ordinal)
  self.objects.add(key,{'path':str(blob.path),'sha256':blob.exact_sha()});self.object_count+=1
  return key,blob,value
 def event(self,record):
  # Existing independently supplied complete trace is the concrete laboratory
  # event applicability grammar. It is not inferred from an event/field name.
  self.provider.role('assessor-competence');self.provider.role('source-producer-correspondence')
  refs=self.trusted.get('trace_refs',{});aid=record['assessment_id']
  require(aid in refs,'missing qualified event trace',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  trace=payload(self.provider,refs[aid]);require(isinstance(trace,list),'complete source trace grammar')
  matches=0
  for r in trace:
   if r.get('event_id')==record['event_id']:
    require(r==record,'source event/null applicability correspondence',category='INVALID-ACTION-CONTEXT');matches+=1
  require(matches==1,'exact unique owning event occurrence',category='INCOMPLETE-EVIDENCE-UNIVERSE')
 def project(self,obj,row,token):
  exact(obj,('format','binding','token_id','surface_id','context','record','codec','type_id','container_ref','record_id'))
  require(obj['format']==FORMAT and obj['binding']==self.binding,'projection binding',category='INVALID-ACTION-CONTEXT')
  for name,key in [('token_id','id'),('surface_id','surface'),('context','context'),('record','record')]:
   require(obj[name]==token[key],'projection exact occurrence '+name,category='INVALID-ACTION-CONTEXT')
  schema,field,kind=law(token['surface'])
  require(row['codec']==obj['codec']=='S90-JSON-LF' and row['type_id']==obj['type_id']==kind,'projection source-owned type law',category='INVALID-ACTION-CONTEXT')
  key,blob,value=self.object(obj['container_ref']);record=None
  reference=token['surface'].startswith('CP2-REF-PARSER:')
  if reference or field=='$record' or field in SPEC.get(schema,{}) or field.startswith('present:'):
   ident=obj['record_id'];primitive('ID',ident)
   if reference:
    original,part=field.split('.')
    match=re.fullmatch(re.escape(ident)+r':REF:'+re.escape(original)+r':([0-9]{6})',str(token['record']))
    require(match is not None and int(match[1])>=1,'exact source-reference parent/item occurrence',category='INVALID-ACTION-CONTEXT');ordinal=int(match[1])
   else:require(ident==token['record'],'containing record occurrence identity',category='INVALID-ACTION-CONTEXT')
   d=value['records'][schema]
   require(d['status']=='PRESENT','required containing record unavailable/inapplicable',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   k=key+':'+schema+':'+ident;require(k in self.records,'absent required containing record',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   record=d['instances'][self.records[k]]
   if schema=='ASSESSOR-EVENT':self.event(record)
  else:
   require(obj['record_id'] is None and token['record']=='CP2-DIRECTORY-'+schema,'directory/root owning occurrence correspondence',category='INVALID-ACTION-CONTEXT')
  if reference:
   ref=record[original]
   if SPEC[schema][original]=='LIST-SOURCE-REF':
    require(ordinal<=len(ref),'absent reference-list occurrence',category='INCOMPLETE-EVIDENCE-UNIVERSE');ref=ref[ordinal-1]
   else:require(ordinal==1,'scalar source-reference ordinal',category='INVALID-ACTION-CONTEXT')
   require(ref is not None,'inapplicable reference has no fabricated key',category='INCOMPLETE-EVIDENCE-UNIVERSE');output=ref[part]
  elif token['surface'].startswith('SECURITY:'):
   output=record if field=='$record' else record[field]
  elif schema=='ROOT':output=SCHEMAS if field=='schema_directory' else value[field]
  elif field.startswith('present:'):
   # Register says one per field including null. Presence here is the null tag,
   # not whether a required key is omitted (omission was already rejected).
   output=record[field[8:]] is not None
  else:
   d=value['records'][schema]
   if field=='instance_count':output=len(d['instances'])
   elif field=='record_directory':
    def chunks():
     yield b'['
     for i,r in enumerate(d['instances']):
      if i:yield b','
      yield from encode(r[IDENTITY[schema]])
     yield b']\n'
    result=self.store.write(chunks());self.count+=1;return result
   else:output=d[field]
  result=as_blob(self.store,output);self.count+=1;return result
