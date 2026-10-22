"""Source-template coverage before existing reviewed supporting ingestion."""
import argparse
from common import *
from static_declarations import validate_export_templates
from pipeline import integrate

def ingest(export,templates):
 coverage=validate_export_templates(export,templates);out=integrate(export);out['static_template_coverage']=coverage;out['static_template_identity']=sha(enc(templates));out['model_input']['static_templates']=templates;return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('export');p.add_argument('templates');p.add_argument('output');a=p.parse_args();target=Path(a.output);need(not target.exists(),'OUTPUT-EXISTS');target.write_bytes(enc(ingest(parse(Path(a.export).read_bytes(),200000000),parse(Path(a.templates).read_bytes(),100000000))))
