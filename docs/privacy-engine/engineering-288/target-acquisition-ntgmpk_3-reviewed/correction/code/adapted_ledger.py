import adapted_verify_finite as v
"""Bounded adaptation: selected reviewed pure functions; acceptance is in evaluate.py."""
import argparse, ast, copy, hashlib, importlib.util, json, traceback, zipfile
from pathlib import Path
def ident(raw): return {'bytes':len(raw),'sha256':v.sha(raw)}
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
def summary(ledger):
    return {'status':'PASS finite mechanical ledger correspondence','binding':copy.deepcopy(ledger['binding']),
      'contexts':[{'context':c['context'],'node_duties':len(c['node_duties']),'relation_duties':len(c['relation_duties']),
                   'fold_duties':len(c['fold_duties']),'token_members':sum(len(d['occurrence_keys']) for d in c['node_duties']),
                   'edge_members':sum(len(d['ordered_edges']) for d in c['relation_duties'])} for c in ledger['contexts']],
      'source_only_obligations':len(ledger['obligations']['source_only']),'qualification_established':False,
      'canonical_ledger_rebound':False,'final_binding':'BLOCKED','actual_admission':False}
