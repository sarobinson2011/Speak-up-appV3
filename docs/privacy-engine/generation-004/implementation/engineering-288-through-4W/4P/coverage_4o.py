"""Finite projection coverage; reads retained registers, never expands a model."""
import csv,json,hashlib
from pathlib import Path
from collections import Counter
from occurrence_values.projection import law,FRAMES
from v4_ingest.records import SPEC,ValidationError
ROOT=Path(__file__).resolve().parent
selected=json.loads((ROOT/'rebinding/selected-contract.json').read_bytes());rows=[]
for surface in selected['field_label_surfaces']:
 if surface.startswith(('SECURITY:','SECURITY-FRAME:','CP2-REF-PARSER:')):
  schema,field,typ=law(surface)
  row={'surface':surface,'adapter':'S90-CONTAINING-OBJECT','schema':schema,'field':field,'type':typ,'status':'IMPLEMENTED','source':'S90 correction sections 1–3; security-fields/security-framing-fields; retained CP2 Catalog._build REF selectors','test':'test_exhaustive_all_s90_fields_records_and_frames_against_python_oracle' if not surface.startswith('CP2-REF') else 'test_exhaustive_source_reference_subfields_and_list_occurrences'}
 elif surface.startswith(('CP2-RECORD-PARSER:','CP2-REFERENCE-MATERIAL:')):
  try:law(surface)
  except ValidationError as e:assert e.category=='INCOMPLETE-EVIDENCE-UNIVERSE'
  else:raise AssertionError('gap witness unexpectedly supported')
  row={'surface':surface,'adapter':None,'status':'REQUIRED-CONTAINING-ADAPTER-NOT-IMPLEMENTED','source':'selected-contract.json parser.event_fields / material_acquisition.fields; CP2 Catalog._build PARSER/MATERIAL selectors; S90 correction section 3','test':'test_required_generated_parser_boundary_is_explicit'}
 else:row={'surface':surface,'adapter':'retained CP4L typed owning values','status':'DIRECT-OWNING-VALUES-RETAINED; NO-NEW-CONTAINING-GRAMMAR-CLAIM','source':'exact existing source-owned byte/type declarations; selected finite contract inherited envelope','test':'tests.test_occurrence; source-qualified concrete inputs remain necessary'}
 rows.append(row)
counts=Counter(r['status'] for r in rows)
report={'result':'FINITE-COVERAGE-MAPPED','selected_contract_sha256':hashlib.sha256((ROOT/'rebinding/selected-contract.json').read_bytes()).hexdigest(),'classes':len(rows),'status_counts':dict(counts),'projection_counts':{'semantic_fields':sum(len(v) for v in SPEC.values()),'record_classes':len(SPEC),'framing':len(FRAMES),'source_reference_subfields':sum(r['surface'].startswith('CP2-REF-PARSER:') for r in rows)},'first_kernel_code_complete':False,'required_code_gaps':[r for r in rows if r['status']=='REQUIRED-CONTAINING-ADAPTER-NOT-IMPLEMENTED'],'null_reference_children':'No child key is fabricated for a null SOURCE-REF. Required absent actual subfield occurrences reject; a source-qualified guarded occurrence directory is required.','qualification_established':False,'full_stream_processed':False}
(ROOT/'PROJECTION-COVERAGE-4O.json').write_text(json.dumps({'summary':report,'classes':rows},indent=2)+'\n')
(ROOT/'results/4O-required-code-boundary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='required_code_gaps'}))
