"""Verify one reviewed finite output; never construct a model or execute builders."""
import argparse, hashlib, io, json, stat, traceback, zipfile
from pathlib import Path, PurePosixPath
CONTEXTS = ['SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO']
INPUT = (45747644, '94791c65c3502d85fc452c0e9c100391f5d0199f7690462e92b91c1a600caa8b', 60)
CONSUMER = (6636286, 'cb88382f2e16ee9fbd44a30f05033ef12c6e467b838784fa25fa16b88bc5e5f5', 40)
BUNDLE = 'e724e49952a6501ab45952416fdd422e9a989cf05f81b8e29254a50088b0a09b'
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
def archive(path,pin):
    raw=regular(path);need((len(raw),sha(raw))==pin[:2],'ARCHIVE-IDENTITY')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist();need(len(names)==pin[2] and len(set(names))==len(names),'ARCHIVE-MEMBERSHIP')
        need(z.testzip() is None,'CRC')
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            need(not p.is_absolute() and '..' not in p.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'UNSAFE-MEMBER')
        manifest=parse(z.read('MANIFEST.json'));need(set(names)==set(manifest)|{'MANIFEST.json'},'EXACT-MEMBERSHIP')
        for n,v in manifest.items():
            b=z.read(n);same({'bytes':len(b),'sha256':sha(b)},v,'MEMBER:'+n)
        return {n:z.read(n) for n in names}
def trusted(component,consumer):
    a=archive(component,INPUT);c=archive(consumer,CONSUMER)
    need(sha(a['outputs/bundle.json'])==BUNDLE,'BUNDLE-IDENTITY')
    pins=parse(a['provenance/candidate-members.json'])
    for n in ['expand_candidate.py','bind_ledger.py','prospective_procedure.py']:
        path=('compiler/' if n=='prospective_procedure.py' else 'native/code/')+n
        raw=c['sources/'+n];same({'bytes':len(raw),'sha256':sha(raw)},pins[path],'NATIVE-SOURCE:'+n)
    return parse(a['outputs/bundle.json'])
def check(value,bundle):
    """Internal pure structural check; public run authenticates expectations afresh."""
    fixed={'format':'I164-FINITE-NATIVE-REPRESENTATION-1','source_bundle_sha256':BUNDLE,'component_sha256':INPUT[1],
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
def run(component,consumer,submitted):
    bundle=trusted(component,consumer);raw=regular(submitted);result=check(parse(raw),bundle)
    result['submitted']={'bytes':len(raw),'sha256':sha(raw)};return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--component',required=True);ap.add_argument('--consumer',required=True);ap.add_argument('--submitted',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    out=Path(a.output);need(not out.exists() and not str(out.resolve()).startswith('/tmp/'),'NEW-PERSISTENT-OUTPUT');out.mkdir(parents=True)
    try:
        result=run(a.component,a.consumer,a.submitted);(out/'result.json').write_bytes(enc(result)+b'\n');print(json.dumps(result))
    except BaseException:
        (out/'failure.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':main()
