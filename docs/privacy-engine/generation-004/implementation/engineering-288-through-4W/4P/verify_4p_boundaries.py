"""Explicit unchanged identities and absence of retained full-stream claims."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
from occurrence_values.generated import CONTRACT,PARSER,MATERIAL
assert len(PARSER)==10 and len(MATERIAL)==3
assert CONTRACT['record_parser_attempts']==2 and CONTRACT['reference_list_elements']==2
assert CONTRACT['parser']['branch_domain']==['VALID-LOCAL','INVALID-LOCAL','UNAVAILABLE','INAPPLICABLE']
assert CONTRACT['material_acquisition']['status_domain']==['PRESENT','UNAVAILABLE','INVALID']
assert hashlib.sha256((R/'rebinding/selected-contract.json').read_bytes()).hexdigest()=='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc'
from v4_ingest.records import primitive,ValidationError
for bad in (None,'x.$record'):
 try:primitive('BYTES' if bad is None else 'ID',bad)
 except ValidationError:pass
 else:raise AssertionError('primitive rejection changed')
report={'result':'PASS','parser_fields':list(PARSER),'material_fields':list(MATERIAL),'record_attempts':2,'reference_list_elements':2,'selected_contract_unchanged':True,'primitive_null_and_dollar_rejection_unchanged':True,'source_qualification_established':False,'actual_admission_enabled':False,'full_retained_stream_processed':False}
(R/'results/4P-preserved-boundaries.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
