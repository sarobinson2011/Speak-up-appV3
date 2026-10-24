"""Focused author controls; no predecessor review or producer execution."""
import argparse,copy,json,sys,time,zipfile,collections,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import finite_inputs as f

def main():
    ap=argparse.ArgumentParser()
    for n in ['component','root','draft','built','output']:ap.add_argument('--'+n,required=True,type=Path)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    results=[];bundle=f.parse(f.read(a.built/'bundle.json'));original=f.enc(bundle)
    def ok(name,claim):
        if not claim:raise AssertionError(name)
        results.append({'name':name,'result':'PASS'});print(name,flush=True)
    # Independent construction arithmetic uses saved rows, without adapter
    # derivation or compiler row generation, and preserves every duplicate value.
    with zipfile.ZipFile(a.component/'inputs/I164-snapshot-evaluation-v3-3m90kxzp.zip') as z:
        for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
            occ=f.parse(z.read(context+'/occurrences.json'));saved=f.parse(z.read(context+'/procedure-result.json'))
            c=next(c for c in bundle['contexts'] if c['context']==context)
            originals={x['id']:x for x in occ['candidate_occurrences']}
            framing={hashlib.sha256((json.dumps([x['parent'],x['class']],sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest():x for x in occ['derived_framing']}
            ok(context+' independent source and framing membership',set(originals)|set(framing)=={t['key'][2] for t in c['tokens']})
            ok(context+' independent contiguous token index',[t['index'] for t in c['tokens']]==list(range(len(c['tokens']))))
            token={t['key'][2]:t for t in c['tokens']};pairs=c['structural_pairs'];edges={(p['from'][2],p['to'][2]) for p in pairs if p['kind']=='FRAMING'}
            ok(context+' every exact framing parent',edges=={(k,v['parent']) for k,v in framing.items()})
            ok(context+' every framing byte',all(token[k]['exact_bytes_hex']==v['exact_bytes_hex'] for k,v in framing.items()))
            ok(context+' counts agree with retained receipts',[len(c['tokens']),len(pairs),len(c['semantic_pairs'])]==[saved['finite_tokens'],saved['finite_structural_pairs'],saved['finite_semantic_pairs']])
            # Authenticated response origin rules independently selected by template.
            bytemplate=collections.defaultdict(list)
            for o in originals.values():bytemplate[o['template']].append(o)
            expected=set()
            for left,right in [('RESPONSE:/signature','RESPONSE:/response'),('RESPONSE:/response','PACKET:/signature'),('JOURNAL:/response_hex','RESPONSE:/signature')]:
                assert len(bytemplate[left])==len(bytemplate[right])==1
                expected.add((bytemplate[left][0]['id'],bytemplate[right][0]['id']))
            ok(context+' independently selected response joins',{(p['from'][2],p['to'][2]) for p in c['semantic_pairs']}==expected)
            repeated=collections.defaultdict(list)
            for t in c['tokens']:repeated[t['exact_bytes_hex']].append(t['key'])
            ok(context+' equal contents retain distinct keys',any(len(v)>1 for v in repeated.values()) and all(len(v)==len({tuple(k) for k in v}) for v in repeated.values()))
    mutations=[]
    def add(name,change):mutations.append((name,change))
    add('missing occurrence',lambda b:b['contexts'][0]['tokens'].pop())
    add('duplicate occurrence',lambda b:b['contexts'][0]['tokens'].append(copy.deepcopy(b['contexts'][0]['tokens'][0])))
    add('substituted occurrence bytes',lambda b:b['contexts'][0]['tokens'][0].update(exact_bytes_hex='00'))
    add('wrong token index type',lambda b:b['contexts'][0]['tokens'][0].update(index=False))
    add('context substitution',lambda b:b['contexts'][0].update(context='SYMBOLIC-U-TWO'))
    add('context reversal',lambda b:b['contexts'].reverse())
    add('cross acquisition token',lambda b:b['contexts'][0]['tokens'][0]['key'].__setitem__(0,'OTHER'))
    add('cross acquisition join',lambda b:b['contexts'][0]['semantic_pairs'][0]['to'].__setitem__(0,'OTHER'))
    add('stale candidate',lambda b:b['bindings']['candidate/identity.json'].update(sha256='0'*64))
    add('mixed export',lambda b:b['export_identity'].update(sha256='0'*64))
    add('missing directory',lambda b:b['contexts'][0]['directory_ranges'].pop())
    add('zero production unknown',lambda b:b['contexts'][0]['directory_ranges'][0]['production_cardinality'].update(exact=0))
    add('altered endpoint',lambda b:b['contexts'][0]['structural_pairs'][0].update(to_index=0))
    add('reversed structural order',lambda b:b['contexts'][0]['structural_pairs'].reverse())
    add('reversed semantic order',lambda b:b['contexts'][0]['semantic_pairs'].reverse())
    add('coordinated reduced count',lambda b:(b['contexts'][0]['structural_pairs'].pop(),b['contexts'][0]['counts'].update(structural_pairs=2364)))
    add('altered native parent key',lambda b:next(s for s in b['contexts'][0]['lookup_steps'] if s['count'])['source_rows'][0].__setitem__(2,'OTHER'))
    add('historical Cartesian substitution',lambda b:b['contexts'][0]['lookup_steps'][0].update(lookup_operator='CARTESIAN'))
    add('missing mechanical duty',lambda b:b['contexts'][0]['mechanical_duties'].pop())
    add('qualified duty',lambda b:b['contexts'][0]['mechanical_duties'][0].update(classification='QUALIFIED'))
    add('nary obligation discharged',lambda b:b['contexts'][0]['fold_obligations'][0].update(disposition='SATISFIED'))
    add('missing O11',lambda b:b['obligations']['source_only'].pop())
    add('readiness escalation',lambda b:b.update(full_expansion_ready=True))
    add('model completion escalation',lambda b:b.update(complete_native_model=True))
    add('ledger rebound escalation',lambda b:b.update(ledger_rebound=True))
    add('admission escalation',lambda b:b.update(actual_admission=True))
    add('native source substitution',lambda b:b['native_contract']['pure_consumer'].update(ast_sha256='0'*64))
    for name,change in mutations:
        mutant=copy.deepcopy(bundle);change(mutant);assert f.enc(mutant)!=original,'NO-OP MUTATION '+name
        try:f.run(a.component,a.root,a.draft,mutant)
        except ValueError as ex:ok('reject '+name,'FINITE-NATIVE-INPUT-SUBSTITUTION' in str(ex))
        else:raise AssertionError('ACCEPTED '+name)
    # Mutated returned/copy/alias objects must not change a subsequent fresh derivation.
    e,i,receipt,records=f._prepare(a.component,a.root,a.draft);first=f._derive(i,receipt)
    alias=first['contexts'][0]['tokens'];alias[0]['key'][0]='MUTATED';first['obligations']['source_only'].clear()
    e,i,receipt,records=f._prepare(a.component,a.root,a.draft);second=f._derive(i,receipt)
    ok('pristine derivation after nested alias mutation',f.enc(second)==original)
    ok('retained native consumer exact pair agreement',sum(r['pairs'] for r in f._consume(second))==sum(c['counts']['structural_pairs']+c['counts']['semantic_pairs'] for c in bundle['contexts']))
    # Fresh public acceptance is separately executed by validate on a recovered root.
    result={'status':'PASS','controls':results,'count':len(results),'seconds':time.monotonic()-start,'full_model':False,'actual_admission':False}
    (a.output/'checks.json').write_bytes(f.enc(result)+b'\n')
if __name__=='__main__':main()
