"""Small model/register ingestion path; all outputs explicitly supporting only."""
import argparse,json
from common import *
from ingest import ingest_file,validate_export
from register import build_register,validate_register,project,final_binding,validate_response_projection

from model_adapter import declarations,occurrence_relations

def integrate(export,reg=None,include_projection=True):
 reg=build_register() if reg is None else validate_register(reg)
 v=validate_export(export);objects=v.pop('objects');rows=[]
 if include_projection:
  for index,(kind,obj) in enumerate(objects):rows.extend(project(obj,kind,index))
 response_coverage=validate_response_projection(objects,rows,v['response_links'],reg) if include_projection else None
 ids={r['id'] for r in rows};need(len(ids)==len(rows),'OCCURRENCE-COLLISION');need(all(r['parent'] is None or r['parent'] in ids for r in rows),'DANGLING-CONTAINMENT')
 return {'format':'I164-RETRY3-CORRESPONDENCE-INGESTION-2','validation':v,'register':reg,'actual_occurrences':rows,'response_selector_coverage':response_coverage,'model_input':declarations(reg),'occurrence_relations':occurrence_relations(rows),'mechanical_duties':[{'kind':'EXACT-SOURCE-RECORD-CONTAINMENT','status':'LOCALLY-CHECKED','count':len(rows)},{'kind':'SOURCE-VISIBILITY-CUSTODY-QUALIFICATION','status':'UNAVAILABLE'},{'kind':'FULL-SYMBOLIC-MODEL-AND-LIFETIME-DIRECTORY','status':'UNESTABLISHED'}],'canonical_registration':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['ingest','register','final-bind']);ap.add_argument('--input');ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);need(not out.exists(),'OUTPUT-EXISTS')
 if a.action=='register':r=build_register()
 elif a.action=='final-bind':r=final_binding(build_register())
 else:r=integrate(parse(Path(a.input).read_bytes(),200000000))
 out.write_bytes(enc(r));print(json.dumps({'status':r.get('final_binding','SUPPORTING-ONLY'),'output':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'actual_admission':False}))
if __name__=='__main__':main()
