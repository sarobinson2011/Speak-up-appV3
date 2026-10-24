"""Mechanical finite ledger only; no authority, qualification or discharge."""
import argparse, ast, copy, hashlib, importlib.util, json, traceback, zipfile
from pathlib import Path
VP=Path(__file__).with_name('verify_finite.py')
if hashlib.sha256(VP.read_bytes()).hexdigest()!='19165ca20788fa282184a300e95aa3277904e886c0ee3dc6e71fa7b8c5742b31':
    raise RuntimeError('VERIFIER-SOURCE-IDENTITY')
spec=importlib.util.spec_from_file_location('finite_verified_dependency',VP)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def ident(raw): return {'bytes':len(raw),'sha256':v.sha(raw)}
def source_contract(consumer):
    # Read names only from authenticated archive bytes; never import the builder.
    files=v.archive(consumer,v.CONSUMER)
    raw=files['sources/bind_ledger.py'];tree=ast.parse(raw)
    assignments=[n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DUTIES' for t in n.targets)]
    v.need(len(assignments)==1,'DUTY-CONTRACT');names=ast.literal_eval(assignments[0])
    v.need(type(names) is tuple and len(set(names))==len(names) and all(type(x) is str for x in names),'DUTY-NAMES')
    return {'duty_names':list(names),'sources':{n:ident(files['sources/'+n]) for n in ('bind_ledger.py','prospective_procedure.py','expand_candidate.py')}}
def derive(native,model_identity,receipt,contract):
    """Internal construction from an authenticated representation and source contract."""
    scope={'finite_model':copy.deepcopy(model_identity),'acquisition':native['acquisition_id']}
    contexts=[]
    for c in native['contexts']:
        ctx=c['context'];base={**scope,'context':ctx}
        tokens=c['occurrences'];key_index={tuple(t['key']):t['index'] for t in tokens}
        v.need(len(key_index)==len(tokens),'UNIQUE-OCCURRENCES')
        nodes=[];groups={}
        for position,g in enumerate(c['groups']):
            d=g['range'];start,end=d['range'];key=d['class'];v.need(key not in groups,'DUPLICATE-CLASS');groups[key]=g
            v.same([t['key'] for t in tokens[start:end]],d['members'],'NODE-MEMBERS')
            nodes.append({'entry_key':['NODE',ctx,key], 'binding':copy.deepcopy(base),
              'directory_position':position,'field_class':key,'token_range':[start,end],
              'occurrence_keys':copy.deepcopy(d['members']),'directory':copy.deepcopy(d),
              'exact_duties':copy.deepcopy(contract['duty_names']),'classification':'UNKNOWN',
              'qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'})
        edges=c['ordered_edges'];offset=0;relations=[];seen=set()
        for duty in c['duties']['mechanical']:
            ordinal=duty['ordinal'];v.need(ordinal not in seen,'DUPLICATE-DUTY');seen.add(ordinal)
            count=duty['count'];v.need(type(count) is int and count>=0,'DUTY-COUNT')
            selected=edges[offset:offset+count]
            v.need(len(selected)==count and all(e['ordinal']==ordinal for e in selected),'DUTY-EDGE-PARTITION')
            relations.append({'entry_key':['RELATION',ctx,ordinal],'binding':copy.deepcopy(base),
              'source_duty':copy.deepcopy(duty),'edge_range':[offset,offset+count],
              'ordered_edges':copy.deepcopy(selected),'classification':'UNKNOWN',
              'qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'})
            offset+=count
        v.need(offset==len(edges),'ALL-EDGES-BOUND')
        folds=[];fold_ordinals=set()
        for duty in c['duties']['fold']:
            ordinal=duty['ordinal'];v.need(ordinal not in fold_ordinals,'DUPLICATE-FOLD');fold_ordinals.add(ordinal)
            endpoints=[]
            for endpoint in duty['endpoints']:
                g=groups[endpoint['class']];members=endpoint['members']
                v.same(members,g['range']['members'],'FOLD-GROUP-MEMBERS')
                indices=[key_index[tuple(k)] for k in members]
                endpoints.append({'class':endpoint['class'],'token_range':copy.deepcopy(g['range']['range']),
                                  'occurrence_keys':copy.deepcopy(members),'token_indices':indices})
            folds.append({'entry_key':['FOLD',ctx,ordinal],'binding':copy.deepcopy(base),
              'source_duty':copy.deepcopy(duty),'endpoints':endpoints,'edge_range':None,
              'pair_count':None,'classification':'UNKNOWN','qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'})
        contexts.append({'context':ctx,'node_duties':nodes,'relation_duties':relations,'fold_duties':folds,
                         'retained_procedure_result':copy.deepcopy(c['duties']['retained'])})
    return {'format':'I164-FINITE-MECHANICAL-LEDGER-1','binding':scope,'verified_representation_kind':'FINITE-ACQUISITION-ONLY',
      'verification_receipt':copy.deepcopy(receipt),'governing_contract':copy.deepcopy(contract),
      'source_bindings':copy.deepcopy(native['bindings']),'contexts':contexts,'obligations':copy.deepcopy(native['obligations']),
      'qualification_established':False,'disposition':'NOT-ESTABLISHED','classification':'UNKNOWN','assessment':'SOURCE-ONLY',
      'canonical_ledger_rebound':False,'canonical_registration':False,'complete_native_model':False,
      'production_cardinalities':None,'global_lifetime_bound':None,'full_expansion_ready':False,
      'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY'}
def run(component,consumer,model,submitted=None):
    # No detached receipt is trusted. Authenticate and verify current model bytes.
    receipt=v.run(component,consumer,model);raw=v.regular(model)
    v.same(ident(raw),receipt['submitted'],'MODEL-CHANGED-DURING-VERIFICATION')
    result=derive(v.parse(raw),ident(raw),receipt,source_contract(consumer))
    if submitted is not None:v.same(v.parse(v.regular(submitted)),result,'LEDGER-SUBSTITUTION')
    return result
def summary(ledger):
    return {'status':'PASS finite mechanical ledger correspondence','binding':copy.deepcopy(ledger['binding']),
      'contexts':[{'context':c['context'],'node_duties':len(c['node_duties']),'relation_duties':len(c['relation_duties']),
                   'fold_duties':len(c['fold_duties']),'token_members':sum(len(d['occurrence_keys']) for d in c['node_duties']),
                   'edge_members':sum(len(d['ordered_edges']) for d in c['relation_duties'])} for c in ledger['contexts']],
      'source_only_obligations':len(ledger['obligations']['source_only']),'qualification_established':False,
      'canonical_ledger_rebound':False,'final_binding':'BLOCKED','actual_admission':False}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--component',required=True);ap.add_argument('--consumer',required=True);ap.add_argument('--model',required=True);ap.add_argument('--submitted');ap.add_argument('--output',required=True);a=ap.parse_args()
    out=Path(a.output);v.need(not out.exists() and not str(out.resolve()).startswith('/tmp/'),'NEW-PERSISTENT-OUTPUT');out.mkdir(parents=True)
    try:
        result=run(a.component,a.consumer,a.model,a.submitted);raw=v.enc(result)+b'\n';(out/'ledger.json').write_bytes(raw)
        s=summary(result);s['ledger']=ident(raw);(out/'result.json').write_bytes(v.enc(s)+b'\n');print(json.dumps(s))
    except BaseException:
        (out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
