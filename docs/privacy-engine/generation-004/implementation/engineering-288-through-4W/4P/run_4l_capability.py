"""Bounded local projection-capability witness; no source qualification claim."""
import json
from pathlib import Path
from fixtures.construct import dataset,wire,sha
from v4_ingest.records import validate_record
from occurrence_values.codec import validate
from semantic_stream.storage import Store,ACTIVE

def main():
 q,t=dataset();directory=json.loads(bytes.fromhex(q['security_records_hex']))
 row=next(r for r in directory['records']['ASSESSOR-EVENT']['instances'] if r['event_kind']=='READ');row['input_bytes']=None
 validate_record('ASSESSOR-EVENT',row,field_register=[s['node_id'] for s in t['model']['surfaces']])
 store=Store();token=ACTIVE.set(store)
 try:
  try:validate(store.write([b'null\n']),'S90-JSON-LF','BYTES',[],[])
  except ValueError as e:rejected=str(e)
  else:raise AssertionError('standalone null silently accepted as ordinary BYTES')
 finally:ACTIVE.reset(token);store.close()
 r={'result':'DEMONSTRATED-PROJECTION-COVERAGE-BOUNDARY','schema':'ASSESSOR-EVENT','field':'input_bytes','canonical_record_sha256':sha(wire(row)),'complete_local_record_with_null_valid':True,'standalone_null_as_BYTES_rejected':True,'detail':rejected,'remaining_adapter':'source-grounded extraction from exact complete containing record with record identity, nullable-field applicability and occurrence joins; not an unconditional nullable BYTES rule','source_qualification_established':False,'full_retained_stream_processed':False,'profile_admitted':False}
 Path('results/4L-projection-boundary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
