"""Narrow reconciliation of CP4D literal-node finding with accepted edge IDs."""
import json,runpy
from pathlib import Path
from ledger_kernel.retained import ROOT,sha
from ledger_kernel.query import resolve
from v4_ingest.records import validate_record

def main():
    old=json.loads((ROOT/'results/record-grammar-boundary.json').read_bytes())
    token=old['model_token'];idx=token['index'];surface=token['surface']
    gpath=ROOT/'accepted/definition-completion/v4_record_grammar.py';g=runpy.run_path(str(gpath))
    potential=resolve(ROOT/'ledger_data','potential',1,idx)
    relation=next(json.loads(line) for line in (ROOT/'ledger_data/structural-duties.jsonl').read_text().splitlines()
                  if surface in (json.loads(line)['relation']['from_node'],json.loads(line)['relation']['to_node']))
    ordinal=relation['structural_ordinal_ranges'][0][0]
    structural=resolve(ROOT/'ledger_data','structural',ordinal)
    assert idx in structural['edge'][:2]
    base={'obligation_id':'REPRO-OBLIGATION','kind':'EXACT','target_ids':['REPRO-TARGET'],'coalition_id':'REPRO-COALITION','node_ids':[],'edge_ids':[],'experiment_id':None}
    cases=[]
    for name,row,expected in [('literal-node',dict(base,node_ids=[token['id']]),False),
                              ('structural-edge-only',dict(base,edge_ids=[structural['edge_id']]),True),
                              ('potential-edge-only',dict(base,edge_ids=[potential['edge_id']]),True)]:
        for impl,fn in [('accepted',lambda r:g['record_shape']('OBLIGATION',r,True)),('implementation',lambda r:validate_record('OBLIGATION',r,True))]:
            try:fn(row);accepted=True
            except ValueError:accepted=False
            assert accepted==expected
            cases.append({'case':name,'validator':impl,'accepted':accepted,'template':row})
    try:g['primitive'](g['SPEC']['FIELD-LABEL']['surface_id'],surface);field_accepts=True
    except ValueError:field_accepts=False
    assert not field_accepts
    r={'result':'PASS-NARROW-IDENTIFIER-RECONCILIATION','model_sha256':old['model_sha256'],'contract_sha256':sha(ROOT/'inputs/selected-contract.json'),
       'accepted_grammar_sha256':sha(gpath),'cases':cases,'structural_edge':structural,'potential_edge':potential,
       'field_label_surface':surface,'field_label_accepts_literal':False,
       'conclusion':'Literal OBLIGATION.node_ids entry fails primitive ID. Legal accepted edge_ids permit incident-edge references without embedding that token spelling. This is not a universal OBLIGATION instantiation impossibility and does not establish complete duty coverage. FIELD-LABEL.surface_id still directly requires the literal selected surface and has no edge_ids alternative.',
       'remaining_obstacle':'Selected finite FIELD-LABEL surface directory versus accepted primitive ID grammar; authoritative narrow resolution required.',
       'sources_changed':False,'model_renamed':False,'full_stream_executed':False,'profile_admitted':False}
    (ROOT/'results/identifier-reconciliation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('cases','structural_edge','potential_edge')},indent=2))
if __name__=='__main__':main()
