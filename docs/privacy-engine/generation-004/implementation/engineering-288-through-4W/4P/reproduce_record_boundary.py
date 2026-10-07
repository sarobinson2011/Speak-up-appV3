"""Exact retained-model / accepted ID-grammar compatibility obstacle only."""
import json,runpy
from pathlib import Path
from ledger_kernel.retained import ROOT,sha
from ledger_kernel.query import resolve
from v4_ingest.records import validate_record

def main():
    nodes=[json.loads(x) for x in (ROOT/'ledger_data/node-duties.jsonl').read_bytes().splitlines()]
    record=next(n for n in nodes if n['surface']['node_id']=='SECURITY:ALGORITHM.$record')
    token=resolve(ROOT/'ledger_data','node',record['token_index_ranges'][0][0])['node']
    contract=json.loads((ROOT/'inputs/selected-contract.json').read_bytes())
    assert record['surface']['node_id'] in contract['field_label_surfaces']
    template={'obligation_id':'REPRO-OBLIGATION','kind':'EXACT','target_ids':['REPRO-TARGET'],'coalition_id':'REPRO-COALITION',
              'node_ids':[token['id']],'edge_ids':[],'experiment_id':None}
    grammar_path=ROOT/'accepted/definition-completion/v4_record_grammar.py';g=runpy.run_path(str(grammar_path))
    cases=[]
    for label,fn in [('accepted OBLIGATION template',lambda:g['record_shape']('OBLIGATION',template,True)),
                     ('implementation OBLIGATION template',lambda:validate_record('OBLIGATION',template,True)),
                     ('accepted FIELD-LABEL.surface_id',lambda:g['primitive'](g['SPEC']['FIELD-LABEL']['surface_id'],record['surface']['node_id']))]:
        try:fn();cases.append({'case':label,'result':'UNEXPECTED-ACCEPT'})
        except ValueError as e:cases.append({'case':label,'result':'REJECTED','detail':str(e)})
    assert all(x['result']=='REJECTED' for x in cases)
    report={'result':'REPRODUCED-RETAINED-MODEL-RECORD-GRAMMAR-INCOMPATIBILITY','model_sha256':'08d6e7fb1e0cf37cc7effa76b50eaff0459abc158d9c6f0da52c6c58372b14f1',
            'selected_contract_sha256':sha(ROOT/'inputs/selected-contract.json'),'accepted_grammar_sha256':sha(grammar_path),
            'model_token':token,'field_label_surface_required_by_selected_contract':record['surface']['node_id'],
            'attempted_template':template,'cases':cases,'changed_accepted_source':False,'renamed_model_identifiers':False,'profile_admitted':False,
            'boundary':'Exact compatibility obstacle for the retained local model and its selected field-label directory; no broad definition review or source correction performed.'}
    (ROOT/'results/record-grammar-boundary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
