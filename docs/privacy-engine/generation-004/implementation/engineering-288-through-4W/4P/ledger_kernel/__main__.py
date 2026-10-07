"""Small ledger construction CLI using the existing source-acquisition carrier."""
import argparse,json
from pathlib import Path
from v4_ingest.wire import decode_container
from admission_kernel.model import Model
from admission_kernel.sources import FiniteLabProvider
from .construct import acquire

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('request',type=Path);p.add_argument('--lab-contract',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    q=json.loads(a.request.read_bytes());t=json.loads(a.lab_contract.read_bytes())
    profile=json.loads(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY'])
    provider=FiniteLabProvider(t,{k:bytes.fromhex(v) for k,v in q['materials'].items()},{k:bytes.fromhex(v) for k,v in q['source_objects'].items()})
    r=acquire(provider,t['ledger_source_ref'],Model(profile['model']),profile['security_contract']['policy']['record'])
    with a.output.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(json.dumps({'result':r['result'],'obligations':len(r['templates']['obligations']),'composition_rules':len(r['templates']['composition_rules']['records']),'profile_admitted':False}))

if __name__=='__main__':main()
