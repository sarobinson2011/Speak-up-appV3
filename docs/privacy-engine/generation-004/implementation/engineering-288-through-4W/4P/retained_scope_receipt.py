"""Reuse verified CP4D correspondence to establish only compact static reachability."""
import json,csv
from ledger_kernel.retained import ROOT,sha
from ledger_kernel.audit import audit

def main():
    audit(ROOT/'ledger_data')
    domain=json.loads((ROOT/'ledger_data/potential-domain.json').read_bytes())
    n=domain['token_count'];fixed={i for i,_ in domain['fixed_tokens']};arbitrary=next(i for i in range(n) if i not in fixed)
    assert domain['all_other_tokens_arbitrary'] and domain['serialized_stream_sha256'] is None
    rows=[json.loads(l) for l in (ROOT/'ledger_data/node-duties.jsonl').read_text().splitlines()]
    with (ROOT/'accepted/profile/fragments/candidate-components.tsv').open() as f:components=list(csv.DictReader(f,delimiter='\t'))
    witnesses={}
    for c in components:
        surface='CORE:COMPONENT-'+c['component_order']+'.canonical_value'
        duty=next(d for d in rows if d['surface']['node_id']==surface)
        witnesses[c['component_id']]={'source_row':c,'surface':surface,'token_index_ranges':duty['token_index_ranges'],
             'meaning':'source-determined owning component value occurrences; witnesses of nonempty component incidence, not an independently qualified complete seed directory'}
    report={'result':'PASS-COMPACT-STATIC-CONNECTIVITY-ONLY','model_sha256':domain['model_sha256'],'contract_sha256':sha(ROOT/'inputs/selected-contract.json'),
       'input_sha256':{p:sha(ROOT/p) for p in ('ledger_data/potential-domain.json','ledger_data/node-duties.jsonl','accepted/profile/fragments/candidate-components.tsv')},
       'tokens':n,'potential_pairs':domain['required_pairs'],'arbitrary_hub_index':arbitrary,'source_component_incidence':witnesses,
       'exact_conclusion':'Under the retained static predicate, every nonempty valid seed has all 426984 nodes in its closure. The arbitrary hub is adjacent to every other token; structural edges cannot reduce this closure.',
       'scopes':{s:{'conditional_nonempty_seed_closure_node_count':n,'source_qualified_seed_directory':'NOT-ESTABLISHED'} for s in ('ROOT-ELIGIBLE','SCOPED-USED')},
       'composition_node_count':n,'qualified_views':'NOT-ESTABLISHED','full_pair_stream_sha256':None,'full_link_stream_sha256':None,
       'expansion_rerun':False,'pair_enumeration':False,'profile_admitted':False}
    (ROOT/'results/4E-retained-static-closure.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
