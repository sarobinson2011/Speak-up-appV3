"""Resolve concrete node/structural/potential identities to populated duties."""
import argparse,json,re
from pathlib import Path
from v4_ingest.records import require
from .retained import CP2,ROOT
from .coverage import contains

def row(cp,state,section,index):
    require(type(index) is int and index>=0,'negative/noninteger index')
    start=0
    for entry in state['sections'][section]:
        if start<=index<start+entry['rows']:
            with cp.get('results/expansion/'+entry['path']).open('rb') as f:
                for j,line in enumerate(f):
                    if j==index-start:return json.loads(line)
        start+=entry['rows']
    raise ValueError('reference outside complete model')

def resolve(output,kind,first,second=None):
    cp=CP2();state=cp.data('results/expansion/RECOVERY.json');out=Path(output)
    if kind=='node':
        t=row(cp,state,'tokens',first)
        with (out/'node-duties.jsonl').open() as f:
            for line in f:
                d=json.loads(line)
                if d['surface']['node_id']==t['surface']:
                    require(contains(d['token_index_ranges'],first),'node omitted from duty correspondence')
                    return {'node':t,'duty':d,'profile_admitted':False}
    elif kind=='structural':
        require(first>0,'structural ordinal is one based');e=row(cp,state,'edges',first-1)
        with (out/'structural-duties.jsonl').open() as f:
            for line in f:
                d=json.loads(line)
                if d['relation_order']==e[2]:
                    require(contains(d['structural_ordinal_ranges'],first),'structural occurrence omitted from duty correspondence')
                    return {'edge_id':'G4-STRUCTURAL-EDGE-'+str(first),'edge':e,'duty':d,'profile_admitted':False}
    elif kind=='potential':
        require(second is not None and first<second,'numeric i<j orientation required')
        a,b=row(cp,state,'tokens',first),row(cp,state,'tokens',second)
        require(a['arbitrary'] or b['arbitrary'] or a['symbolic_digest']==b['symbolic_digest'],'illegal potential pair')
        return {'edge_id':f'G4-EQUALITY-PAIR-{first}-{second}','endpoints':[a['id'],b['id']],
                'membership':'MECHANICALLY-ESTABLISHED','privacy_classification':None,'disposition':'NOT-ESTABLISHED',
                'full_actor_graph_inclusion_required':True,'source':'potential-domain.json bound to saved complete model',
                'profile_admitted':False}
    raise ValueError('missing duty or unknown query kind')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('kind',choices=['node','structural','potential']);ap.add_argument('first',type=int);ap.add_argument('second',nargs='?',type=int);ap.add_argument('--output',type=Path,default=ROOT/'ledger_data');a=ap.parse_args()
    print(json.dumps(resolve(a.output,a.kind,a.first,a.second),indent=2))

if __name__=='__main__':main()
