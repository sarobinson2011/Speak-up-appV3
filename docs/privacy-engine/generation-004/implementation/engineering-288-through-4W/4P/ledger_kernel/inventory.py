"""Populated full-model duty/provenance inventory, not a qualified V4 ledger.

Consumes only saved CP2 node/structural segments. Never generates pair/link rows.
Atomic per-segment receipts allow bounded restart; --verify recomputes summaries.
"""
import argparse
from array import array
from collections import Counter
import hashlib,json,mmap,time
from pathlib import Path
from v4_ingest.records import canonical,digest,require
from admission_kernel.failures import Failures
from .retained import CP2,ROOT,sha,atomic,PINS
from .validate import EXACT_DUTIES

BASE='results/expansion/'

def append_range(rows,index):
    if rows and rows[-1][1]==index:rows[-1][1]+=1
    else:rows.append([index,index+1])

def metadata(path):
    # Exact saved CP2 model identity was checked before this bounded metadata read.
    with path.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
        def field(name,next_name):
            a=m.find(('"'+name+'":').encode())+len(name)+3
            b=m.find((',"'+next_name+'":').encode(),a)
            require(a>len(name)+2 and b>a,'retained model metadata layout')
            return json.loads(m[a:b])
        return field('surfaces','tokens'),field('relations','structural_edges')

def source_pins(cp,path,prov):
    return {p:cp.entries[BASE+p]['sha256'] for p in (path,prov)}

def build(output,seconds=150,verify=False,stop_after=None):
    began=time.monotonic();output=Path(output);output.mkdir(parents=True,exist_ok=True)
    cp=CP2();saved=cp.data(BASE+'RECOVERY.json');report=cp.data(BASE+'expansion-results.json');checked=cp.data(BASE+'verification-results.json')
    contract=json.loads((ROOT/'inputs/selected-contract.json').read_bytes())
    require(contract==cp.data('contract/selected-contract.json'),'exact selected finite contract content')
    require(report['tokens']==checked['tokens_verified'] and report['structural_edges']==checked['structural_rows_verified'],'retained verification joins')
    require(report['model_identity']['sha256']==saved['model_identity']['sha256'],'saved model/receipt join')
    surfaces,relations=metadata(cp.get(BASE+'model.json'))
    node_prov=cp.data(BASE+'surface-provenance.json');relation_prov=cp.data(BASE+'relation-provenance.json')
    old_duties=[json.loads(b) for b in cp.get(BASE+'model-duty-ledger.jsonl').read_bytes().splitlines()]
    require(len(surfaces)==len(node_prov)==report['surface_classes'] and len(relations)==len(relation_prov)==len(old_duties)==report['relation_templates'],'complete retained provenance catalog')
    binding={'model_sha256':report['model_identity']['sha256'],'selected_contract_sha256':sha(ROOT/'inputs/selected-contract.json'),
             'CP2_zip_sha256':PINS['2'],'code':{p:sha(ROOT/p) for p in ('ledger_kernel/inventory.py','ledger_kernel/retained.py')},
             'accepted_contract_sha256':sha(ROOT/'accepted/definition-completion/ACCEPTANCE-CONTRACT.txt')}
    state=output/'construction-state.json'
    if state.exists():require(json.loads(state.read_bytes())['binding']==binding,'construction checkpoint code/input identity changed; choose a new output')
    completed=[];receipts=[];last=0
    def progress(stage):
        nonlocal last
        elapsed=time.monotonic()-began
        r={'stage':stage,'segments_committed':len(completed),'seconds':round(elapsed,3),'pair_stream_executed':False}
        atomic(state,canonical({'binding':binding,**r,'completed':completed}))
        if elapsed-last>=5 or stage in ('complete','paused'):
            print(json.dumps(r),flush=True);last=elapsed
        if stage!='complete' and (elapsed>seconds or (stop_after is not None and len(completed)>=stop_after)):
            return True
        return False
    by_node={};by_relation={};fixed=[];token_surfaces=array('I',[0])*report['tokens'];token_context=array('B',[0])*report['tokens']
    offset=0
    for section in ('tokens','edges'):
        offset=0
        for number,e in enumerate(saved['sections'][section]):
            key=f'{section}-{number:06}';cache=output/'segments'/(key+'.json')
            pins=source_pins(cp,e['path'],e['provenance_path'])
            if cache.exists() and not verify:
                blob=json.loads(cache.read_bytes());require(blob['binding']==binding and blob['inputs']==pins and digest(canonical(blob['data']))==blob['data_sha256'],'corrupt/incompatible derived segment; rerun --verify')
                data=blob['data']
            else:
                data={'groups':{},'rows':0,'fixed':[]}
                p,pp=cp.get(BASE+e['path']),cp.get(BASE+e['provenance_path'])
                with p.open('rb') as a,pp.open('rb') as b:
                    for local,line in enumerate(a):
                        row=json.loads(line);provenance_line=b.readline();require(bool(provenance_line),'missing retained row provenance')
                        prov=json.loads(provenance_line);idx=offset+local
                        if section=='tokens':
                            order=prov['surface_order'];require(row['index']==prov['token_index']==idx,'exact node/provenance ordinal')
                            require(1<=order<=len(surfaces) and row['surface']==surfaces[order-1]['node_id'],'node/source field-class correspondence')
                            require(row['context']==prov['context'] and row['record']==prov['record'],'owning record/context provenance')
                            g=data['groups'].setdefault(str(order),{'ranges':[],'exposures':{},'contexts':{}})
                            append_range(g['ranges'],idx)
                            for label,val in [('exposures',row['exposure']),('contexts',row['context'])]:g[label][val]=g[label].get(val,0)+1
                            if not row['arbitrary']:data['fixed'].append([idx,row['symbolic_digest']])
                        else:
                            aidx,bidx,order,kind=row;require(0<=aidx<len(token_surfaces) and 0<=bidx<len(token_surfaces),'structural endpoint domain')
                            require(prov[0]==idx+1 and prov[1]==order and prov[2]==token_context[aidx]==token_context[bidx],'edge exact ordinal/template/context provenance')
                            rel=relations[order-1]
                            require(rel['from_node']==surfaces[token_surfaces[aidx]-1]['node_id'] and rel['to_node']==surfaces[token_surfaces[bidx]-1]['node_id'] and rel['relation']==kind,'structural duty source relation join')
                            g=data['groups'].setdefault(str(order),{'ranges':[],'count':0});append_range(g['ranges'],idx+1);g['count']+=1
                        data['rows']+=1
                    require(not b.readline(),'extra provenance rows')
                require(data['rows']==e['rows'],'segment exact count')
                blob={'binding':binding,'inputs':pins,'data':data,'data_sha256':digest(canonical(data))}
                if cache.exists():require(json.loads(cache.read_bytes())==blob,'derived segment differs from exact independent recomputation')
                else:atomic(cache,canonical(blob))
            require(data['rows']==e['rows'],'cached source count mismatch')
            target=by_node if section=='tokens' else by_relation
            for order,g in data['groups'].items():
                merged=target.setdefault(order,{'ranges':[],'count':0,'exposures':{},'contexts':{}})
                for a,b in g['ranges']:
                    if merged['ranges'] and merged['ranges'][-1][1]==a:merged['ranges'][-1][1]=b
                    else:merged['ranges'].append([a,b])
                    if section=='tokens':
                        for i in range(a,b):token_surfaces[i]=int(order)
                merged['count']+=sum(b-a for a,b in g['ranges'])
                for k in ('exposures','contexts'):
                    for name,count in g.get(k,{}).items():merged[k][name]=merged[k].get(name,0)+count
            if section=='tokens':
                fixed.extend(data['fixed'])
                # Context is available from saved token provenance without guessing interval layout.
                # Reuse the source-provenance rows; this is O(N), never O(pair universe).
                for line in cp.get(BASE+e['provenance_path']).open('rb'):
                    v=json.loads(line);token_context[v['token_index']]=0 if v['context']=='SYMBOLIC-U-ONE' else 1
            offset+=data['rows'];completed.append(key);receipts.append({'path':'segments/'+cache.name,'sha256':sha(cache),'inputs':pins})
            if progress(section):return {'result':'PAUSED','segments':len(completed),'profile_admitted':False}
        require(offset==report['tokens' if section=='tokens' else 'structural_edges'],'complete required domain count')
    require(set(by_node)==set(map(str,range(1,len(surfaces)+1))) and all(token_surfaces),'all model field classes and nodes covered')
    require(set(by_relation)==set(map(str,range(1,len(relations)+1))),'all structural template duties covered')
    for i,old in enumerate(old_duties,1):require(by_relation[str(i)]['count']==old['expanded_structural_occurrences'] and old['source_provenance']==relation_prov[i-1],'CP2 source-duty ledger reuse join')
    groups=Counter(v for i,v in fixed);n=report['tokens'];f=len(fixed)
    pairs=n*(n-1)//2-f*(f-1)//2+sum(c*(c-1)//2 for c in groups.values())
    require(pairs==report['equality_plan']['rows']==checked['exact_pair_count_independently_checked'],'exact compact potential obligation domain')
    nodes=[]
    for i,s in enumerate(surfaces,1):
        g=by_node[str(i)];nodes.append({'inventory_id':f'CP4D-NODE-CLASS-{i:06}','surface_order':i,'surface':s,'provenance':node_prov[i-1],
          'token_index_ranges':g['ranges'],'token_count':g['count'],'contexts':g['contexts'],'exposures':g['exposures'],
          'exact_duty_families':list(EXACT_DUTIES),'classification':'EXACT-DUTY-REVIEW-REQUIRED','disposition':'NOT-ESTABLISHED',
          'coverage_status':'MECHANICALLY-ESTABLISHED','source_qualification':'NOT-ESTABLISHED'})
    edges=[];surface_orders={s['node_id']:i for i,s in enumerate(surfaces,1)}
    for i,r in enumerate(relations,1):
        g=by_relation[str(i)];edges.append({'inventory_id':f'CP4D-RELATION-{i:06}','relation_order':i,'relation':r,'provenance':relation_prov[i-1],
          'structural_ordinal_ranges':g['ranges'],'structural_occurrences':g['count'],'node_source_orders':[surface_orders[r['from_node']],surface_orders[r['to_node']]],
          'required_exact_checks':['SOURCE-OWNERSHIP','SOURCE-ESTABLISHED-LINKAGE','DECLARATION-RECORD-JOINS'],
          'privacy_classification':None,'disposition':'NOT-ESTABLISHED','coverage_status':'MECHANICALLY-ESTABLISHED','source_qualification':'NOT-ESTABLISHED'})
    atomic(output/'node-duties.jsonl',b''.join(canonical(x) for x in nodes));atomic(output/'structural-duties.jsonl',b''.join(canonical(x) for x in edges))
    potential={'format':'CP4D-INTERNAL-EXACT-DOMAIN-V1','model_sha256':binding['model_sha256'],'token_count':n,'required_pairs':pairs,
      'predicate':report['equality_plan']['predicate'],'numeric_orientation':'i<j','fixed_tokens':fixed,
      'all_other_tokens_arbitrary':True,'coverage':'all legal index pairs; no sampling, filters or actor-edge pruning',
      'privacy_classification':None,'disposition':'NOT-ESTABLISHED','serialized_stream_sha256':None,
      'meaning':'Executable obligation-domain inventory; not a qualified classifier, serialized stream hash or admitted V4 ledger'}
    atomic(output/'potential-domain.json',canonical(potential))
    slots={s:[{'record_id':rid,'source':'selected finite contract schema_directories.'+s,'populated_V4_record':False,
              'disposition':'NOT-ESTABLISHED','missing':'independent source-owned policy/target/view/classification/evidence values'} for rid in contract['schema_directories'][s]] for s in ('OBLIGATION','COMPOSITION','EXPERIMENT','POLICY','QUALIFICATION')}
    atomic(output/'governing-slots.json',canonical(slots))
    obligations={'exact_families':list(EXACT_DUTIES),'whole_view_claim_families':['COLLISION','CROSS-ACTION-TRACKING','ACTOR-INFORMATION'],
      'NV1':{'mechanical_law':'canonical 0 <= numerator < denominator','maximum':None,'status':'SOURCE-VALUE-MISSING'},
      'NV2':{'required':'nonempty genuine alternatives, complete adversary-class and matched leakage/schedule/auxiliary scope','status':'NOT-ESTABLISHED'},
      'NV3':{'required':'exact policy/world/envelope/model/targets/views/qualification invocation and qualified assertion','status':'NOT-ESTABLISHED'},
      'NV4':{'required':'inherited ordered failure collection','implementation':'ledger_kernel.validate + admission_kernel.admission'},
      'composition':{'UNION':'min(1, sum(exact qualified bound * source-established multiplicity))','maximum':None,'terms':None,'status':'NOT-ESTABLISHED'},
      'policy_defaults_introduced':False,'actual_qualification_established':False}
    atomic(output/'required-security-duties.json',canonical(obligations))
    inputs={k:e for k,e in cp.entries.items() if k.startswith(BASE) and (k==BASE+'model.json' or any(k==BASE+p for r in receipts for p in r['inputs']) or k in [BASE+x for x in ('RECOVERY.json','expansion-results.json','verification-results.json','surface-provenance.json','relation-provenance.json','model-duty-ledger.jsonl')])}
    result={'result':'COMPLETE-MECHANICAL-DUTY-CORRESPONDENCE','binding':binding,'tokens':n,'surface_classes':len(surfaces),'structural_occurrences':report['structural_edges'],'relation_templates':len(relations),'potential_pairs':pairs,
      'node_exposures':dict(sum((Counter(x['exposures']) for x in nodes),Counter())),
      'dispositions':'ALL NOT-ESTABLISHED for privacy/source qualification','immutable_V4_obligations_instantiated':False,
      'selected_contract_obligation_slots':len(slots['OBLIGATION']),'selected_contract_composition_slots':len(slots['COMPOSITION']),
      'full_pair_or_link_stream_executed':False,'profile_admitted':False,'seconds':round(time.monotonic()-began,3),
      'source_members':inputs,'derived_segments':receipts}
    atomic(output/'inventory-result.json',canonical(result));progress('complete');return result

def blocked(output):
    p=json.loads((Path(output)/'inventory-result.json').read_bytes());f=Failures()
    f.add('INVALID-EVIDENCE-AUTHORITY','Selected retained finite contract does not establish independent model/classifier/policy/assessor/observer authority')
    f.add('MISSING-EVIDENCE','Source-owned concrete obligation/composition, policy/target/view and qualified assessment objects absent')
    if p['node_exposures'].get('UNKNOWN',0):f.add('INVALID-SURFACE-LABELS','Unresolved UNKNOWN model exposures/custody remain')
    f.add('INCOMPLETE-EVIDENCE-UNIVERSE','Complete mechanical duty domain is not a qualified semantic ledger/discharge; required full stream identities remain null')
    return f.result('ACTUAL',{'mechanical_inventory':{k:p[k] for k in ('tokens','structural_occurrences','potential_pairs','surface_classes','relation_templates')},'qualification':'NOT-ESTABLISHED'})

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('operation',choices=['build','verify','status']);ap.add_argument('--output',type=Path,default=ROOT/'ledger_data');ap.add_argument('--seconds',type=float,default=150);ap.add_argument('--stop-after',type=int);a=ap.parse_args()
    r=blocked(a.output) if a.operation=='status' else build(a.output,a.seconds,a.operation=='verify',a.stop_after)
    print(json.dumps({k:v for k,v in r.items() if k not in ('source_members','derived_segments')},indent=2));return 0 if r['result']=='COMPLETE-MECHANICAL-DUTY-CORRESPONDENCE' else 3 if r['result']=='PAUSED' else 2

if __name__=='__main__':raise SystemExit(main())
