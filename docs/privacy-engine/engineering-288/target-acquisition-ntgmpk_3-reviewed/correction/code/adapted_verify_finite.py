"""Bounded adaptation: selected reviewed pure functions; acceptance is in evaluate.py."""
import argparse, hashlib, io, json, stat, traceback, zipfile
from pathlib import Path, PurePosixPath
CONTEXTS = ['SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO']
class Rejected(ValueError): pass
def need(ok, why):
    if not ok: raise Rejected(why)
def enc(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False, ensure_ascii=True).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def same(a,b,why): need(enc(a)==enc(b),why)
def parse(raw):
    def unique(rows):
        d={}
        for k,v in rows:
            need(k not in d,'DUPLICATE-JSON-KEY'); d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda _: (_ for _ in ()).throw(Rejected('NONFINITE')))
def regular(p):
    p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR');return p.read_bytes()
def check(value,bundle,bundle_identity,component_identity):
    """Internal pure structural check; public run authenticates expectations afresh."""
    fixed={'format':'I164-FINITE-NATIVE-REPRESENTATION-1','source_bundle_sha256':bundle_identity['sha256'],'component_sha256':component_identity['sha256'],
      'classification':'UNKNOWN','qualification':'UNAVAILABLE','assessment':'SOURCE-ONLY','finite_consumer_acceptance':True,
      'complete_native_model':False,'ledger_rebound':False,'production_cardinalities':None,'global_lifetime_bound':None,
      'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED',
      'actual_admission':False,'backup':'KERNEL-ONLY'}
    for k in ['acquisition_id','bindings','native_contract','obligations']: fixed[k]=bundle[k]
    need(set(value)==set(fixed)|{'contexts'},'TOP-SCHEMA')
    for k,v in fixed.items():same(value[k],v,'BINDING-OR-STATUS:'+k)
    need(len(bundle['obligations']['source_only'])==11,'SOURCE-OBLIGATIONS')
    same([c['context'] for c in value['contexts']],CONTEXTS,'CONTEXT-ORDER')
    same([c['context'] for c in bundle['contexts']],CONTEXTS,'SOURCE-CONTEXT-ORDER')
    summaries=[]
    for current,source in zip(value['contexts'],bundle['contexts']):
        ctx=source['context'];tokens=source['tokens'];rows=current['occurrences']
        need(set(current)=={'context','occurrences','groups','ordered_edges','duties'},'CONTEXT-SCHEMA')
        need(len(rows)==len(tokens),'TOKEN-COUNT');keys=set()
        for i,(row,t) in enumerate(zip(rows,tokens)):
            same(row,{'index':i,'key':t['key'],'class':t['class'],'payload_hex':t['exact_bytes_hex'],'metadata':t},'OCCURRENCE:'+ctx+':'+str(i))
            need(t['key'][:2]==[bundle['acquisition_id'],ctx],'ACQUISITION-CONTEXT')
            key=tuple(t['key']);need(key not in keys,'DUPLICATE-OCCURRENCE');keys.add(key)
            need(bytes.fromhex(row['payload_hex']).hex()==row['payload_hex'],'EXACT-BYTE-ENCODING')
        need(len(current['groups'])==len(source['directory_ranges']),'GROUP-COUNT')
        cursor=0
        for group,directory in zip(current['groups'],source['directory_ranges']):
            need(set(group)=={'range','rows'},'GROUP-SCHEMA');same(group['range'],directory,'GROUP-DIRECTORY')
            start,end=directory['range']
            need(type(start) is int and type(end) is int and start==cursor and start<=end<=len(tokens),'RANGE-PARTITION')
            same(directory['members'],[t['key'] for t in tokens[start:end]],'GROUP-MEMBERS')
            need(all(t['class']==directory['class'] for t in tokens[start:end]) and directory['context']==ctx,'GROUP-CLASS-CONTEXT')
            same(group['rows'],[[i,enc(tokens[i]['key']).decode(),None,True] for i in range(start,end)],'GROUP-ROWS')
            cursor=end
        need(cursor==len(tokens),'TOKEN-COVERAGE')
        pairs={};kinds={}
        for kind in ['structural_pairs','semantic_pairs']:
            for p in source[kind]:
                pairs.setdefault(p['ordinal'],[]).append(p);kinds[p['ordinal']]=kind
        offset=0;ordinals=set()
        for step in source['lookup_steps']:
            ordinal=step['ordinal'];need(ordinal not in ordinals,'DUPLICATE-ORDINAL');ordinals.add(ordinal)
            need(step['context']==ctx and step['lookup_operator']=='PARENT-RECORD','KEYED-RELATION-CONTRACT')
            expected=pairs.get(ordinal,[]);target={}
            for i,key,parent,new in step['target_rows']:
                need(type(i) is int and 0<=i<len(tokens) and new is True and key not in target,'TARGET-WORK-ROW')
                same(parse(key),tokens[i]['key'],'TARGET-KEY');target[key]=i
            joins=[];seen=set()
            for i,key,parent,new in step['source_rows']:
                need(type(i) is int and 0<=i<len(tokens) and new is True and key not in seen and parent in target,'SOURCE-WORK-ROW')
                seen.add(key);j=target[parent];same(parse(key),[ordinal,tokens[i]['key'],tokens[j]['key']],'EDGE-WORK-KEY');joins.append([i,j])
            same(joins,[[p['from_index'],p['to_index']] for p in expected],'DIRECT-KEYED-JOIN')
            same(len(expected),step['count'],'RULE-COUNT')
            for p in expected:
                a,b=p['from_index'],p['to_index']
                same(p['from'],tokens[a]['key'],'PAIR-SOURCE');same(p['to'],tokens[b]['key'],'PAIR-TARGET')
                need(offset<len(current['ordered_edges']),'MISSING-EDGE')
                same(current['ordered_edges'][offset],{'ordinal':ordinal,'source_index':a,'target_index':b,'source_key':p['from'],'target_key':p['to']},'ORDERED-EDGE:'+str(offset));offset+=1
        need(set(pairs)<=ordinals and offset==len(current['ordered_edges']),'EDGE-CONSERVATION')
        same(current['duties'],{'mechanical':source['mechanical_duties'],'fold':source['fold_obligations'],'retained':source['retained_procedure_result']},'DUTIES-AND-UNKNOWN')
        summaries.append({'context':ctx,'occurrences':len(rows),'groups':len(current['groups']),'structural_edges':len(source['structural_pairs']),'semantic_edges':len(source['semantic_pairs']),'ordered_edges':offset,'fold_duties':len(source['fold_obligations'])})
    return {'status':'PASS bounded finite-output verification','contexts':summaries,'obligations':11,'classification':'UNKNOWN','complete_native_model':False,'production_universe_established':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False}
