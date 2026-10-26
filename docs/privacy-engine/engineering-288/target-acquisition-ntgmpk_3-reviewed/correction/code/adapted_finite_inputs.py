"""Bounded adaptation: selected reviewed pure functions; acceptance is in evaluate.py."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
FORMAT = 'I164-FINITE-ACQUISITION-NATIVE-INPUT-1'
PAIRS_AST = '3f4af79df7baecd5c7bb1130ff9b16d58107f7d154f76223d02e1850c69cb64a'
class Rejected(ValueError): pass
def need(v, why):
    if not v: raise Rejected(why)
def enc(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(b): return {'bytes': len(b), 'sha256': sha(b)}
def same(a,b,why): need(enc(a)==enc(b),why)
def read(p):
    p=Path(p);need(stat.S_ISREG(p.lstat().st_mode),'NONREGULAR:'+str(p))
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:return f.read()
def parse(b):
    def pairs(rows):
        d={}
        for k,v in rows:need(k not in d,'DUPLICATE-JSON-KEY');d[k]=v
        return d
    def constant(v):raise Rejected('NONFINITE-JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant)
def native_contract(root,draft):
    targets={}
    for kind,name in [('model','model-input.json'),('ledger','ledger-input.json')]:
        target=parse(read(Path(draft)/'outputs'/name))['native_target']
        raw=read(Path(root)/target['source']['path']);same(ident(raw),{k:target['source'][k] for k in ('bytes','sha256')},'NATIVE-SOURCE')
        f=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name==target['function'])
        same([a.arg for a in f.args.args],target['parameters'],'NATIVE-SIGNATURE')
        same(sha(ast.dump(f,include_attributes=False).encode()),target['ast_sha256'],'NATIVE-AST')
        targets[kind]=target
    raw=read(Path(root)/'native/code/expand_candidate.py')
    f=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='pairs')
    need(sha(ast.dump(f,include_attributes=False).encode())==PAIRS_AST,'PURE-PAIRS-AST')
    return {'historical_targets':targets,'pure_consumer':{'file':'native/code/expand_candidate.py','source':ident(raw),'function':'pairs','parameters':['p','number','ctx'],'ast_sha256':PAIRS_AST},
      'input_mapping':{'token_index':'context-local integer i; no historical/global offset','occurrence_key':'JSON encoding of [acquisition_id, context, local_occurrence_id]',
       'work_row':'[i, unique source-edge key, exact target occurrence key, true]','target_row':'[i, target occurrence key, null, true]',
       'groups':'role-separated SOURCE/TARGET Group entries(), get(key), parts','rules':['PARENT-RECORD'],'old_rel_n':0,
       'node_ranges':'finite class/context ranges only','ledger':'mechanical duty inputs only; no saved current model binding'},
      'direct_prepare_allowed':False,'direct_ledger_build_allowed':False,'historical_arrays_appended':False}
def _qualified(acquisition,context,local):return [acquisition,context,local]
def _derive(i,receipt):
    """Provisional construction; public acceptance also runs authenticated validators."""
    import compiler as m
    import semantic as s
    import ingest
    import prospective_procedure as pp
    a=i['archives']['acquisition'];ev=i['archives']['evaluation']
    export=parse(a['export.json']);fold=ingest.validate_export(export)
    acquisition=i['basis']['acquisition_id'];directory=i['directory'];rules=i['rules']
    contexts=[]
    for context in tuple(r['context'] for r in receipt['contexts']):
        occ=parse(ev[context+'/occurrences.json']);duty=parse(ev[context+'/procedure-result.json'])
        lineage=parse(ev[context+'/lineage.json']);same(lineage['acquisition_id'],acquisition,'LINEAGE-ACQUISITION')
        same(lineage['context'],context,'LINEAGE-CONTEXT');need(lineage['cross_acquisition_joins'] is False,'LINEAGE-JOIN')
        byclass=m._instance_rows(directory,occ)
        projected={p['id']:p for p in occ['supporting_pipeline']['actual_occurrences']}
        need(len(projected)==len(occ['supporting_pipeline']['actual_occurrences']),'DUPLICATE-PROJECTION')
        source={p['id']:p for p in occ['candidate_occurrences']}
        need(len(source)==len(occ['candidate_occurrences']),'DUPLICATE-SOURCE-OCCURRENCE')
        frames={sha(m.enc([f['parent'],f['class']])):f for f in occ['derived_framing']}
        need(len(frames)==len(occ['derived_framing']),'DUPLICATE-FRAME')
        # This selected acquisition has no derived array indices. Do not invent
        # their wire bytes or silently claim support for a future acquisition.
        need(not occ['derived_indices'],'UNSUPPORTED-ACQUISITION-DERIVED-INDEX')
        tokens=[];ranges=[];index={};rowmap={}
        dirs=[d for d in directory['directories'] if d['context']==context]
        for d in dirs:
            start=len(tokens);members=sorted(byclass.get(d['class'],[]),key=lambda r:r['id'])
            for row in members:
                local=row['id'];need(local not in index,'DUPLICATE-TOKEN');idx=len(tokens);index[local]=idx;rowmap[local]=row
                if local in source:
                    link=source[local];original=projected[link['occurrence']]
                    same([original['occurrence'],original['pointer']],[row['record_index'],row['pointer']],'PROJECTED-SOURCE-LOCATION')
                    provenance={'kind':'SOURCE-OCCURRENCE','candidate_occurrence':link,'projection':original}
                    exact=original['exact_bytes_hex']
                else:
                    need(local in frames,'UNSUPPORTED-OCCURRENCE');frame=frames[local]
                    provenance={'kind':'DERIVED-FRAMING','framing':frame,'owner':_qualified(acquisition,context,frame['parent'])}
                    exact=frame['exact_bytes_hex']
                bytes.fromhex(exact)
                tokens.append({'index':idx,'key':_qualified(acquisition,context,local),'class':d['class'],
                  'directory':d['id'],'instance':row,'exact_bytes_hex':exact,'provenance':provenance,
                  'guard':d['guard'],'source':d['source'],'selector':d['selector'],
                  'classification':'UNKNOWN','qualification':'UNAVAILABLE'})
            ranges.append({'directory':d['id'],'class':d['class'],'context':context,'range':[start,len(tokens)],
              'members':[_qualified(acquisition,context,r['id']) for r in members],
              'production_cardinality':d['cardinality'],'visibility':d['visibility'],'custody':d['custody']})
        # Exact keyed structural joins. Each operation has a different source
        # selection law. Equal values never merge occurrence identities.
        structural=[];fold_obligations=[];summaries=[]
        for r in directory['relations']:
            op=r['join']['operator'];start=len(structural)
            need(op in ('FRAMING-OWNER','SAME-OBSERVED-VALUE','NEAREST-DECLARED-ANCESTOR','AUTHENTICATED-FOLD-ENDPOINT-SET'),'UNSUPPORTED-CARTESIAN-OR-JOIN')
            if op=='AUTHENTICATED-FOLD-ENDPOINT-SET':
                endpoints=[{'class':cl,'members':[_qualified(acquisition,context,x['id']) for x in sorted(byclass.get(cl,[]),key=lambda x:x['id'])]} for cl in r['endpoints']]
                fold_obligations.append({'ordinal':r['ordinal'],'context':context,'endpoints':endpoints,'pair_count':None,'obligations':1,'classification':'UNKNOWN','disposition':'NOT-ESTABLISHED'})
                summaries.append({'ordinal':r['ordinal'],'obligations':1,'pair_count':None,'endpoint_counts':[len(x['members']) for x in endpoints]});continue
            right=byclass.get(r['endpoints'][1],[])
            for x in sorted(byclass.get(r['endpoints'][0],[]),key=lambda x:x['id']):
                if op=='FRAMING-OWNER':matches=[y for y in right if y['id']==x.get('owner')]
                elif op=='SAME-OBSERVED-VALUE':matches=[y for y in right if y['record_index']==x['record_index'] and y['occurrence'] is not None and y['occurrence']==x['occurrence']]
                else:
                    matches=[y for y in right if y['record_index']==x['record_index'] and (y['pointer']==x['pointer'] or x['pointer'].startswith(y['pointer']+'/'))]
                    if matches:matches=[y for y in matches if len(y['pointer'])==max(len(t['pointer']) for t in matches)]
                need(len(matches)==1,'EXACT-STRUCTURAL-TARGET');y=matches[0]
                structural.append({'ordinal':r['ordinal'],'from':_qualified(acquisition,context,x['id']),'to':_qualified(acquisition,context,y['id']),
                  'from_index':index[x['id']],'to_index':index[y['id']],'kind':r['kind'],'operator':op})
            summaries.append({'ordinal':r['ordinal'],'pairs':len(structural)-start})
        same(summaries,duty['structural_duties'],'STRUCTURAL-RECEIPT-COUNTS')
        # Reuse reviewed prospective semantic selector/join logic, with actual
        # authenticated objects. A Cartesian fallback is never available.
        semantic=s._pairs(rules,s.View(fold['objects'],occ,export))
        semantics=[]
        for p in semantic:
            need(p['context']==context and p['from'] in index and p['to'] in index,'SEMANTIC-ENDPOINT')
            semantics.append({**p,'from':_qualified(acquisition,context,p['from']),'to':_qualified(acquisition,context,p['to']),
              'from_index':index[p['from']],'to_index':index[p['to']]})
        steps=[];mechanical=[]
        for r, pool in [(r,structural) for r in directory['relations']]+[(r,semantics) for r in rules['rules']]:
            selected=[p for p in pool if p['ordinal']==r['ordinal']]
            if r['kind']=='SOURCE-FOLD-OBLIGATION':continue
            left=[];right={}
            for p in selected:
                source_key=enc([r['ordinal'],p['from'],p['to']]).decode();target_key=enc(p['to']).decode()
                left.append([p['from_index'],source_key,target_key,True]);right[target_key]=[p['to_index'],target_key,None,True]
            steps.append({'ordinal':r['ordinal'],'kind':r['kind'],'context':context,'source_rule':copy.deepcopy(r),
              'lookup_operator':'PARENT-RECORD','source_rows':left,'target_rows':[right[k] for k in sorted(right)],'count':len(selected)})
            mechanical.append({'ordinal':r['ordinal'],'kind':r['kind'],'count':len(selected),'classification':'UNKNOWN','qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'})
        rc=next(c for c in receipt['contexts'] if c['context']==context)
        same([len(tokens),len(structural),len(semantics)],[rc['finite_tokens'],rc['finite_structural_pairs'],rc['finite_semantic_pairs']],'FINITE-RECEIPT-TOTALS')
        same({r['directory']:r['range'][1]-r['range'][0] for r in ranges},rc['counts'],'COMPLETE-DIRECTORY-VECTOR')
        same([{'class':r['class'],'context':context,'range':r['range'],'members':[k[2] for k in r['members']],'qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'} for r in ranges],duty['node_ranges'],'EXACT-PROCEDURE-RANGES')
        for d in duty['semantic_duties']:
            same(sum(p['ordinal']==d['ordinal'] for p in semantics),d['count'],'SEMANTIC-DUTY-COUNT')
        contexts.append({'context':context,'lineage':lineage,'tokens':tokens,'directory_ranges':ranges,
          'structural_pairs':structural,'semantic_pairs':semantics,'lookup_steps':steps,
          'mechanical_duties':mechanical,'fold_obligations':fold_obligations,'retained_procedure_result':duty,
          'counts':{'tokens':len(tokens),'structural_pairs':len(structural),'semantic_pairs':len(semantics)},
          'ordering':{'tokens':'source directory order, then local occurrence ID','structural_pairs':'inherited ordinal, source occurrence ID, unique target','semantic_pairs':'reviewed ordinal/source record/pointer/target record/pointer'},
          'index_scope':'THIS ACQUISITION AND CONTEXT ONLY; no historical model offset'})
    return {'format':FORMAT,'scope':'FINITE-SELECTED-ACQUISITION-INPUT-ONLY',
      'acquisition_id':acquisition,'export_identity':ident(a['export.json']),'export_exact_bytes_hex':a['export.json'].hex(),
      'evidence_count_receipt':copy.deepcopy(receipt),'bindings':copy.deepcopy(receipt['bindings']),'contexts':contexts,
      'native_contract':native_contract(i['root'],i['draft']),
      'obligations':i['obligations'],'native_duty_names':pp.duty_names(),
      'input_identities':copy.deepcopy(i['component_bindings']),
      'classification':'UNKNOWN','qualification':'UNAVAILABLE','assessment':'SOURCE-ONLY','global_lifetime_bound':None,
      'global_storage_byte_bound':None,'production_cardinalities':None,'complete_native_model':False,'ledger_rebound':False,
      'canonical_registration':False,'operational_assurance':False,'full_expansion_ready':False,'final_binding':'BLOCKED',
      'stream_identities':'UNCOMPUTED','actual_admission':False,'backup':'KERNEL-ONLY','cross_acquisition_joins':False}
def _consume(bundle):
    """Exercise exact native pure lookup on each finite work group. Not a builder."""
    import prospective_procedure as pp
    fn=pp.lookup();results=[]
    for c in bundle['contexts']:
        context=c['context'];pairs=c['structural_pairs']+c['semantic_pairs'];checked=0
        for step in c['lookup_steps']:
            need(step['lookup_operator']=='PARENT-RECORD','NO-CARTESIAN-SUBSTITUTION')
            p={'rels':[{'from_node':'SOURCE','to_node':'TARGET'}],'rules':['PARENT-RECORD'],'details':[None],
               'groups':{('SOURCE',context):pp.Group(step['source_rows']),('TARGET',context):pp.Group(step['target_rows'])},'old_rel_n':0}
            actual=list(fn(p,0,context));expected=[(q['from_index'],q['to_index']) for q in pairs if q['ordinal']==step['ordinal']]
            same(actual,expected,'NATIVE-EXACT-ORDERED-PAIR-CORRESPONDENCE');same(len(actual),step['count'],'NATIVE-COUNT');checked+=len(actual)
        same(checked,len(pairs),'NATIVE-PAIR-CONSERVATION')
        results.append({'context':context,'tokens':len(c['tokens']),'pairs':checked,'lookup_groups':len(c['lookup_steps']),'fold_obligations':len(c['fold_obligations'])})
    return results
