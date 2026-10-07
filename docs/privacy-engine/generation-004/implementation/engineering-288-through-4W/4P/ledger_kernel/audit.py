"""Verify delivered inventory files and exact domain partitions, without pairs.

For independent reconstruction against source bytes additionally use inventory
verify, which recomputes each saved segment summary and compares exact content.
"""
import argparse,json
from pathlib import Path
from v4_ingest.records import require,canonical
from .retained import ROOT,sha,atomic,CP2

FILES=('node-duties.jsonl','structural-duties.jsonl','potential-domain.json','governing-slots.json','required-security-duties.json','inventory-result.json')

def seal(output):
    output=Path(output)
    files={p:{'sha256':sha(output/p),'bytes':(output/p).stat().st_size} for p in FILES}
    atomic(output/'FILE-HASHES.json',canonical({'format':'CP4D-INVENTORY-FILES-V1','files':files,'qualification':False}))

def partition(groups,low,high):
    previous=low
    for a,b in sorted(r for g in groups for r in g):
        require(type(a) is int and type(b) is int and a==previous and a<b<=high,'duty partition gap/duplicate/out-of-domain reference')
        previous=b
    require(previous==high,'incomplete duty partition')

def audit(output):
    output=Path(output);pins=json.loads((output/'FILE-HASHES.json').read_bytes())
    require(set(pins['files'])==set(FILES),'complete inventory file directory')
    for name,pin in pins['files'].items():require(sha(output/name)==pin['sha256'] and (output/name).stat().st_size==pin['bytes'],'changed populated ledger '+name)
    cp=CP2();saved=cp.data('results/expansion/expansion-results.json')
    result=json.loads((output/'inventory-result.json').read_bytes())
    require(result['binding']['model_sha256']==saved['model_identity']['sha256'],'exact full model ledger binding')
    ns=[json.loads(x) for x in (output/'node-duties.jsonl').read_bytes().splitlines()]
    es=[json.loads(x) for x in (output/'structural-duties.jsonl').read_bytes().splitlines()]
    require([r['surface_order'] for r in ns]==list(range(1,saved['surface_classes']+1)),'complete ordered field-class directory')
    require([r['relation_order'] for r in es]==list(range(1,saved['relation_templates']+1)),'complete ordered structural directory')
    partition([r['token_index_ranges'] for r in ns],0,saved['tokens'])
    partition([r['structural_ordinal_ranges'] for r in es],1,saved['structural_edges']+1)
    for r in ns:
        require(r['token_count']==sum(b-a for a,b in r['token_index_ranges'])==sum(r['exposures'].values())==sum(r['contexts'].values()),'node duty count/context/exposure joins')
        require(r['disposition']=='NOT-ESTABLISHED' and r['source_qualification']=='NOT-ESTABLISHED','inventory cannot assert qualification')
    for r in es:
        require(r['structural_occurrences']==sum(b-a for a,b in r['structural_ordinal_ranges']),'structural occurrence count join')
        require(r['privacy_classification'] is None and r['disposition']=='NOT-ESTABLISHED','unqualified privacy classification invented')
    p=json.loads((output/'potential-domain.json').read_bytes());require(p['required_pairs']==saved['equality_plan']['rows'] and p['serialized_stream_sha256'] is None,'uncomputed full stream identity remains null')
    require(result['profile_admitted'] is False and not result['immutable_V4_obligations_instantiated'],'inventory is not final immutable ledger')
    return {'result':'PASS-POPULATED-INVENTORY-DOMAINS-AND-HASHES','nodes':saved['tokens'],'structural_occurrences':saved['structural_edges'],
            'potential_pairs':p['required_pairs'],'full_pair_or_link_stream_executed':False,'profile_admitted':False,
            'meaning':'exact interval partition plus pinned retained source/member identities; classification/evidence still unestablished'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'ledger_data');a=ap.parse_args();print(json.dumps(audit(a.output),indent=2))

if __name__=='__main__':main()
