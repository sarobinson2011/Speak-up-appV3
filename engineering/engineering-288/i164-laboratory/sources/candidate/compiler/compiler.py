"""Draft I164 directory/relation compiler. Does not instantiate a complete model."""
import argparse,ast,copy,json,sys,time,resource,re
from pathlib import Path
ROOT=None

def setup(root):
 global ROOT,Candidate,enc,sha,need,same,Invalid
 ROOT=Path(root).resolve();sys.path.insert(0,str(ROOT/'integration'))
 from candidate_pipeline import Candidate,enc,sha,need,same,Invalid
 need(sha((ROOT/'integration/candidate_pipeline.py').read_bytes())=='f9fba68bbc2a6c9341b676d22d3b6b233531af650e20fd11e2c38700d7c91d1d','CORRECTED-ADAPTER-PIN')
 return Candidate()
def load(p):return json.loads((ROOT/p).read_bytes())
def ident(p):
 b=(ROOT/p).read_bytes();return {'path':p,'bytes':len(b),'sha256':sha(b)}

def independent_coverage(c):
 """Independent traversal of the pinned schema DSL; never calls build/templates.
 Not an independent proof of arbitrary Python runtime/control-flow completeness.
 """
 from static_declarations import schemas
 groups,owners,optional=schemas();actual={r['template_id']:r['native_template'] for r in c.c['fields.json']['prospective']};expected={}
 frame={'presence':'BOOLEAN','availability':'STRING','encoding_length':'INTEGER','member_count':{'union':['NULL','INTEGER']},'exact_bytes':'STRING','type_tag':'STRING','key_encoding':{'union':['NULL','STRING']},'separator_encoding':'STRING','opening_delimiter':'STRING','closing_delimiter':'STRING'}
 def add(n,p,t,parent,guard='present',presence='required'):
  tid=n+':'+p;need(tid not in expected,'DUPLICATE-SELECTOR');expected[tid]=(t,parent,guard,presence)
  for f,ft in frame.items():expected[tid+'#'+f]=(ft,tid,'derived framing of '+tid,'required')
  if type(t) is str:need(t in ['STRING','INTEGER','BOOLEAN','NULL','NUMBER'],'UNKNOWN-SCALAR');return
  need(type(t) is dict,'UNKNOWN-TYPE')
  if 'wire_type' in t:need(set(t)=={'wire_type','abi_type'} and t['abi_type'] in ['uint256','bytes32','bytes'],'UNKNOWN-WIRE-TYPE');return
  if 'ref' in t:need(set(t)=={'ref'} and t['ref'] in groups,'BAD-REFERENCE');return
  if 'object' in t:
   need(set(t)=={'object'},'UNSUPPORTED-OBJECT-CONSTRUCT')
   for k,v in t['object'].items():
    q=p+('/*' if k=='@additional' else '/'+k);g='additional key not among mandatory fields' if k=='@additional' else optional.get(n,{}).get(k,'present')
    add(n,q,v,tid,g,'guarded; absent is inapplicable only under inverse guard' if g!='present' else 'required');add(n,q+'#key','STRING',tid,g)
  elif 'array' in t or 'directory' in t:
   kind='array' if 'array' in t else 'directory';need(set(t)==({'array'} if kind=='array' else {'directory','key_type'}),'UNSUPPORTED-CONTAINER')
   add(n,p+'/*',t[kind],tid,'each admitted array position' if kind=='array' else 'each retained member; lifetime multiplicity unresolved');add(n,p+'/*#key','INTEGER' if kind=='array' else 'STRING',tid,'member exists')
  elif 'tuple' in t:
   need(set(t)=={'tuple'},'UNSUPPORTED-TUPLE')
   for i,v in enumerate(t['tuple']):add(n,p+'/'+str(i),v,tid,'fixed index '+str(i))
  elif 'union' in t:
   need(set(t)<= {'union','guard'},'UNSUPPORTED-UNION')
   for i,v in enumerate(t['union']):add(n,p+'/@union/'+str(i),v,tid,'exact type alternative '+str(i))
  elif 'variants' in t:
   need(set(t)=={'variants','choice_by'},'UNSUPPORTED-VARIANT')
   for k,v in t['variants'].items():add(n,p+'/@variant/'+k,v,tid,t['choice_by']+' == '+k)
  elif 'request_method_choice' in t:
   need(set(t)=={'request_method_choice'},'UNSUPPORTED-METHOD')
   for k,v in t['request_method_choice'].items():add(n,p+'/@method/'+k,v,tid,'authenticated request.method == '+k)
  else:raise Invalid('UNSUPPORTED-SOURCE-CONSTRUCT')
 for n,g in groups.items():add(n,'',g['@value'] if n=='JSON-VALUE' else {'object':g},None)
 same(setlist(actual),setlist(expected),'SOURCE-SELECTOR-COVERAGE')
 for k,(t,parent,g,pres) in expected.items():
  a=actual[k];same([a['type'],a['parent'],a['guard'],a['presence']],[t,parent,g,pres],'SOURCE-TYPE-GUARD-PARENT:'+k)
 same(c.c['schemas.json']['prospective'],groups,'SOURCE-FORMS');same([x['record'] for x in c.c['source-forms.json']['prospective']],sorted(groups),'OMITTED-SOURCE-FORM')
 # Derive framing member coverage independently from the defining function AST.
 tree=ast.parse((ROOT/'support/code/framing_templates.py').read_bytes());returns=[n.value for n in ast.walk(tree) if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict)]
 for d in returns:same(sorted(k.value for k in d.keys),sorted(frame),'FRAMING-SOURCE-MEMBERS')
 # Independent ABI recursion from actual contract inputs, not fixture values or generated templates.
 abi=load('support/reference/contract/ABI.json')
 def abi_shape(x):
  t=x['type'];m=re.fullmatch(r'(.*)\[(\d+)\]',t)
  if m:return {'tuple':[abi_shape(dict(x,type=m[1])) for _ in range(int(m[2]))]}
  if t=='tuple':return {'object':{k['name']:abi_shape(k) for k in x['components']}}
  need(t in ['uint256','bytes32','bytes'],'UNSUPPORTED-ABI');return {'wire_type':'INTEGER' if t=='uint256' else 'STRING','abi_type':t}
 for method in ['signPetition','signPetitionWithZKProof']:
  fs=[f for f in abi if f.get('type')=='function' and f.get('name')==method];need(len(fs)==1,'ABI-FUNCTION');same(groups['ABI-'+method],{x['name']:abi_shape(x) for x in fs[0]['inputs']},'ABI-SOURCE-COVERAGE')
 # Exact authenticated action-body fields derived directly from runtime AST.
 tree=ast.parse((ROOT/'support/reference/runtime/authority.py').read_bytes());apply=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='apply');methods={}
 for node in ast.walk(apply):
  q=node.test if isinstance(node,ast.If) else None
  if isinstance(q,ast.Compare) and isinstance(q.left,ast.Name) and q.left.id=='m' and len(q.ops)==1 and isinstance(q.ops[0],ast.Eq) and isinstance(q.comparators[0],ast.Constant):
   method=q.comparators[0].value;calls=[n for n in ast.walk(ast.Module(body=node.body,type_ignores=[])) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='exact' and len(n.args)==2 and isinstance(n.args[0],ast.Name) and n.args[0].id=='b']
   need(len(calls)==1,'UNSUPPORTED-METHOD-BODY-CONSTRUCTOR');methods[method]=sorted(ast.literal_eval(calls[0].args[1]))
 sign=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='sign');calls=[n for n in ast.walk(sign) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='exact'];need(len(calls)==1,'SIGN-BODY-SOURCE');methods['sign']=sorted(ast.literal_eval(calls[0].args[1]))
 same(sorted(methods),sorted(n[5:] for n in groups if n.startswith('BODY-')),'RUNTIME-METHOD-COVERAGE')
 for m,keys in methods.items():same(sorted(groups['BODY-'+m]),keys,'RUNTIME-BODY-FIELDS:'+m)
 return {'supported_domain':'pinned schemas() DSL output, direct runtime exact-body keys for all authenticated methods, source ABI recursive arguments for two methods, framing function literal members; independent selector/guard/parent traversal; not independent arbitrary runtime Python completeness','runtime_body_fields':methods,'checked_families':len(groups),'checked_declarations':len(expected),'sources':[ident('support/code/static_declarations.py'),ident('support/code/framing_templates.py'),ident('support/reference/contract/ABI.json'),ident('support/reference/runtime/authority.py')],'complete_for_supported_traversal':True,'full_runtime_source_completeness':False,'unsupported_constructs':'REJECT','SD01_scope_expanded':False}
def setlist(x):return sorted(x)

def compile_candidate(c):
 cov=independent_coverage(c);fields=c.c['fields.json']['prospective'];by={r['template_id']:r['id'] for r in fields};contexts=sorted(c.contexts)
 old=load('native/records/relation-rules.json');base=len(old);need(base==349871,'INHERITED-ORDINAL-COUNT')
 namespaces=set(c.c['namespace.json']['historical_classes'])|{r['id'] for r in fields}
 for r in old:need(r['relation']['from_node'] in namespaces and r['relation']['to_node'] in namespaces,'HISTORICAL-ENDPOINT')
 dirs=[];rules=[]
 def rule(kind,ends,guard,source,selector,join):
  rules.append({'ordinal':base+len(rules)+1,'kind':kind,'endpoints':ends,'contexts':contexts,'guard':guard,'source':source,'selector':selector,'join':join,'dependency_classification':'UNKNOWN','qualification':'UNAVAILABLE'})
 for f in fields:
  t=f['native_template'];src=ident('support/'+t['source']);need(src['sha256']==t['source_sha256'],'SOURCE-IDENTITY')
  framing='#' in t['selector'] and t['selector'].rsplit('#',1)[1] in ['presence','availability','encoding_length','member_count','exact_bytes','type_tag','key_encoding','separator_encoding','opening_delimiter','closing_delimiter']
  for ctx in contexts:
   dirs.append({'id':ctx+'|'+f['id'],'class':f['id'],'context':ctx,'record':t['record'],'selector':t['selector'],'type':t['type'],'guard':t['guard'],'presence':t['presence'],'parent':None if f['parent'] is None else ctx+'|'+f['parent'],'source':src,'source_rule':t['source_rule'],'cardinality':{'status':'UNRESOLVED','exact':None,'expression':{'op':'GUARDED-OCCURRENCES','family':t['record'],'selector':t['selector'],'guard':t['guard'],'context':ctx},'dependencies':['source-established-root-directory:'+t['record'],'nested-multiplicity-and-guard-directory:'+f['id'],'lifetime-and-external-evidence-domain']},'visibility':'UNKNOWN','custody':['UNKNOWN']*7})
  if f['parent']:
   rule('FRAMING' if framing else 'DECLARATION-PARENT',[f['id'],f['parent']],t['guard'],src,t['selector'],{'operator':'FRAMING-OWNER' if framing else 'NEAREST-DECLARED-ANCESTOR','keys':['context','record_index','pointer-prefix'],'cardinality':'one validated target per present child; unresolved until complete guarded directories exist'})
  if type(t['type']) is dict and set(t['type'])=={'ref'}:
   target=by[t['type']['ref']+':'];rule('REFERENCE',[f['id'],target],t['guard'],src,t['selector'],{'operator':'SAME-OBSERVED-VALUE','keys':['context','record_index','occurrence'],'cardinality':'one same-value target per present source; declaration alias only, not qualified equality edge'})
 for a in c.c['associations.json']['prospective']:
  rule('SOURCE-FOLD-OBLIGATION',[e['class'] for e in a['endpoints']],a['guard'],a['source'],a['anchors'],{'operator':'AUTHENTICATED-FOLD-ENDPOINT-SET','rule_id':a['id'],'keys':['candidate','context','saved_export_sha256'],'cardinality':'one obligation for each complete authenticated fold; endpoint sets retained, not a Cartesian causal-edge assertion','pair_lowering':'UNRESOLVED-REQUIRES-SOURCE-ESTABLISHED-INSTANCE-JOINS'})
 obligations=[{'ordinal':r['ordinal'],'source':r['source'],'required':['exact source/guard/endpoint correspondence','complete guarded directories','instance join cardinality','qualified classification separately'],'status':'NOT-ESTABLISHED','dependency':'UNKNOWN'} for r in rules]
 output={'format':'I164-DRAFT-DIRECTORY-RELATION-1','candidate_binding':c.binding,'contexts':contexts,'context_definitions':c.c['contexts.json']['historical_definitions'],'inherited_namespace':ident('candidate/namespace.json'),'inherited_relations':{'source':ident('native/records/relation-rules.json'),'ordinal_range':[1,base],'unchanged':True},'relationships43':ident('support/reference/relationships-43.json'),'directories':dirs,'relations':rules,'ledger_duties':obligations,'source_coverage':cov,'procedure_inputs':{'historical_expander':ident('native/code/expand_candidate.py'),'historical_ledger':ident('native/code/bind_ledger.py'),'historical_finalize':ident('native/code/finalize_records.py'),'compatibility':'NOT-DROP-IN; prospective operators require guarded occurrence adapter; legacy names not silently reused','pair_lowering_complete':False},'full_expansion_ready':False,'blockers':['UNRESOLVED-DIRECTORIES','SOURCE-FOLD-PAIR-LOWERING','FULL-RUNTIME-SOURCE-COMPLETENESS','QUALIFIED-CLASSIFICATIONS-AND-FINAL-BINDING'],'canonical_registration':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
 return copy.deepcopy(output) # outputs cannot mutate future expected metadata

def validate(output,c):
 # Fresh derivation, no live aliases or cached success.
 expected=compile_candidate(c);same(output,expected,'COMPILER-OUTPUT-SUBSTITUTION');return True

def count_only(output,c):
 validate(output,c)
 return {'exact_metadata':{'directories':len(output['directories']),'classes':len(output['directories'])//2,'contexts':2,'new_relation_rules':len(output['relations']),'new_context_rule_applications':2*len(output['relations']),'ledger_duties':len(output['ledger_duties']),'historical_relation_ordinals':output['inherited_relations']['ordinal_range']},'tokens':{'exact':None,'expression':'historical_tokens + SUM(cardinality(directory) for every prospective class/context)','unresolved_directory_count':len(output['directories'])},'edges':{'exact':None,'expression':'historical_edges + SUM(cardinality(typed guarded join) per context); fold obligations not yet pair-lowered'},'full_expansion_ready':False,'final_binding':'BLOCKED'}
def readiness(output,c):
 validate(output,c);raise Invalid('FULL-EXPANSION-BLOCKED:'+','.join(output['blockers']))

# Count-only algebra consumes small concrete directory rows only for fixture tests.
# Generic full-model count inputs must be source-established; fixtures cannot populate production unknowns.
def fixture_join_count(op,left,right):
 need(op in ['SAME-KEY','PARENT-KEY','CARTESIAN'],'MALFORMED-JOIN')
 need(len({r['id'] for r in left})==len(left) and len({r['id'] for r in right})==len(right),'DUPLICATE-OCCURRENCE')
 if op=='CARTESIAN':return len(left)*len(right)
 from collections import Counter
 target=Counter(r['key'] for r in right);key='parent' if op=='PARENT-KEY' else 'key'
 return sum(target[r[key]] for r in left)

def main():
 a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--output',required=True);x=a.parse_args();p=Path(x.output);need0=not p.exists()
 if not need0:raise SystemExit('output exists')
 t=time.monotonic();c=setup(x.root);out=compile_candidate(c);counts=count_only(out,c);p.mkdir();(p/'compiler-output.json').write_bytes(enc(out));(p/'counts.json').write_bytes(enc(counts));(p/'measurement.json').write_bytes(enc({'seconds':time.monotonic()-t,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'output_bytes':len(enc(out)),'count_bytes':len(enc(counts)),'scope':'this compiler only; no full-expansion estimate'}));print(json.dumps(counts['exact_metadata']))


def _validated_fixture(out,occ,export):
 """Fresh pinned authority and detached current inputs; no validation certificates.
 An authenticated saved export is mandatory, never a caller-supplied success flag.
 """
 out,occ,export=json.loads(enc([out,occ,export]))
 c=setup(ROOT) # reconstruct from pinned disk, not caller-mutable Candidate expectations
 validate(out,c)
 c.validate_output(occ,export)
 return out,occ

def instance_rows(out,occ,export):
 """Validated finite rows; same mandatory boundary as the count entry point."""
 out,occ=_validated_fixture(out,occ,export)
 return _instance_rows(out,occ)

def _instance_rows(out,occ):
 """Finite saved-example adapter; never assigns production multiplicities."""
 context=occ['context'];byclass={};byid={};fields={d['class']:d for d in out['directories'] if d['context']==context};templ={(d['record'],d['selector']):d['class'] for d in fields.values()}
 def put(row):
  if row['id'] in byid:same(row,byid[row['id']],'CONFLICTING-INSTANCE');return
  byid[row['id']]=row;byclass.setdefault(row['class'],[]).append(row)
 for l in occ['candidate_occurrences']:put({k:l[k] for k in ['id','class','record_index','pointer','occurrence']})
 for f in occ['derived_framing']:
  p=byid[f['parent']];put({'id':sha(enc([p['id'],f['class']])),'class':f['class'],'record_index':p['record_index'],'pointer':p['pointer'],'occurrence':None,'owner':p['id']})
 for i in occ['derived_indices']:
  key=sha(enc([i['class'],i['record_index'],i['value_pointer'],context]));p={'id':key,'class':i['class'],'record_index':i['record_index'],'pointer':i['value_pointer'],'occurrence':None};put(p)
  d=fields[i['class']]
  for name in i['derived_framing']:
   cl=templ[(d['record'],d['selector']+'#'+name)];put({'id':sha(enc([key,cl])),'class':cl,'record_index':p['record_index'],'pointer':p['pointer'],'occurrence':None,'owner':key})
 return byclass

def count_actual_fixture(out,occ,export):
 out,occ=_validated_fixture(out,occ,export)
 rows=_instance_rows(out,occ);summary=[];tot=0
 for r in out['relations']:
  op=r['join']['operator'];need(op in ['FRAMING-OWNER','SAME-OBSERVED-VALUE','NEAREST-DECLARED-ANCESTOR','AUTHENTICATED-FOLD-ENDPOINT-SET'],'UNSUPPORTED-FIXTURE-OPERATOR');a=rows.get(r['endpoints'][0],[])
  if op=='AUTHENTICATED-FOLD-ENDPOINT-SET':
   # One n-ary obligation over this validated fold, not invented instance pairs.
   summary.append({'ordinal':r['ordinal'],'obligations':1,'pair_count':None,'endpoint_counts':[len(rows.get(k,[])) for k in r['endpoints']]});continue
  b=rows.get(r['endpoints'][1],[]);byid={x['id']:x for x in b};matched=0
  for x in a:
   if op=='FRAMING-OWNER':targets=[byid[x['owner']]] if x.get('owner') in byid else []
   elif op=='SAME-OBSERVED-VALUE':targets=[y for y in b if y['record_index']==x['record_index'] and y['occurrence'] is not None and y['occurrence']==x['occurrence']]
   elif op=='NEAREST-DECLARED-ANCESTOR':
    targets=[y for y in b if y['record_index']==x['record_index'] and (y['pointer']==x['pointer'] or x['pointer'].startswith(y['pointer']+'/'))]
    if targets:
     n=max(len(y['pointer']) for y in targets);targets=[y for y in targets if len(y['pointer'])==n]
   need(len(targets)==1,'FIXTURE-JOIN-TARGET:'+str(r['ordinal'])+':'+str(len(targets)));matched+=len(targets)
  summary.append({'ordinal':r['ordinal'],'pairs':matched});tot+=matched
 return {'scope':'finite authenticated saved example only; unobserved classes not assigned zero in production','context':occ['context'],'observed_classes':len(rows),'instances':sum(map(len,rows.values())),'structural_pairs':tot,'relation_counts':summary,'full_expansion_ready':False}

if __name__=='__main__':main()
