"""Bounded source-to-occurrence guard/emission correspondence over saved evidence."""
import ast,copy,json,argparse
from pathlib import Path
import semantic as s
import emission_sources as src
m=s.m

def families(expr,operation,bodies):
 node=ast.parse(expr,mode='eval').body
 values=node.elts if operation in ['initialize','extend'] and isinstance(node,ast.List) else [node] if operation=='append' else None
 m.need(values is not None,'UNSUPPORTED-EMISSION-DIRECTORY');out=set()
 def kind(n):
  if isinstance(n,ast.Constant) and type(n.value) is str:return {n.value}
  if isinstance(n,ast.IfExp):return kind(n.body)|kind(n.orelse)
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add) and isinstance(n.left,ast.Constant):
   if n.left.value=='BODY-':return {'BODY-'+x for x in bodies}|{'UNVALIDATED-BODY'}
   if n.left.value=='ABI-ARGUMENTS-':return {'ABI-'+x for x in ['signPetition','signPetitionWithZKProof']}
  raise m.Invalid('UNSUPPORTED-EMISSION-FAMILY:'+ast.unparse(n))
 for value in values:
  m.need(isinstance(value,ast.Tuple) and len(value.elts)==2,'UNSUPPORTED-EMISSION-TUPLE');out|=kind(value.elts[0])
 if 'RELEASE-RESULT' in out:out.add('RETRY-RELEASE-RESULT')
 return sorted(out)

def compile_map(directory,rules):
 c=s.setup(s.ROOT);m.validate(directory,c);m.same(rules,s.compile_rules(c),'EMISSION-RULE-IDENTITY')
 from correspondence import BODIES
 sources=src.source_map(s.ROOT);family={}
 for site in sources['projection']['sites']:
  site['families']=families(site['value_expression'],site['operation'],BODIES)
  for name in site['families']:m.need(name in c.groups,'UNSUPPORTED-DECLARATION:'+name)
 for name in sorted(c.groups):
  fs=[x for x in c.c['fields.json']['prospective'] if x['native_template']['record']==name];ids={x['id'] for x in fs}
  family[name]={'declarations':[{'class':x['id'],'template':x['template_id'],'type':x['native_template']['type'],'guard':x['native_template']['guard'],'parent':x['parent'],'source':x['native_template']['source'],'source_sha256':x['native_template']['source_sha256']} for x in fs],'directories':[x['id'] for x in directory['directories'] if x['class'] in ids],'relations':[x['ordinal'] for x in directory['relations'] if ids.intersection(x['endpoints'])],'semantic_rules':[x['ordinal'] for x in rules['rules'] if x['from']['class'] in ids or x['to']['class'] in ids],'multiplicity':{'exact':None,'basis':'original guarded directory cardinality expressions/dependencies; no lifetime bound from saved examples'}}
 for site in sources['runtime']['sites']:
  for name in site['families']:m.need(name in family,'UNDECLARED-RUNTIME-EMISSION')
  site['projection_sites']=[x['site'] for x in sources['projection']['sites'] if set(site['families']).intersection(x['families'])]
 return {'format':'I164-GUARD-EMISSION-1','binding':c.binding,'directory_sha256':m.sha(m.enc(directory)),'rules_sha256':m.sha(m.enc(rules)),'sources':sources,'families':family,'contexts':directory['context_definitions'],'code':[m.ident('compiler/'+n) for n in ['guard_emission.py','emission_sources.py']],'procedure_binding':{'code':m.ident('compiler/prospective_procedure.py'),'retained_count_only_input':m.ident('prospective_outputs/procedure.json'),'mode':'validated count_only/consume when procedure=True; no implicit consumption claim'},'complete_runtime_coverage':False,'backup':'KERNEL-ONLY; mapping is not authenticated backup execution','full_expansion_ready':False,'final_binding':'BLOCKED','stream_identities':'UNCOMPUTED','actual_admission':False,'remaining':['unselected runtime/helper/transitive internals','full alias/data-flow and exceptional control-flow proof','authenticated backup evidence','source-owned lifetime/history/recovery cardinalities','external serialization and storage bounds','qualified classifications and complete model binding']}

def validate_map(value,directory,rules):
 m.same(value,compile_map(directory,rules),'GUARD-EMISSION-MAP-SUBSTITUTION');return True

def trace_export(export):
 # Only the pinned read-only saved-export validator executes. No Authority,
 # signer, ingress transport, database acquisition or lifecycle is invoked.
 import ingest
 raw=(s.ROOT/src.INGEST).read_bytes();tree=ast.parse(raw);fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_export'))
 controls=[];emissions=[]
 def emit_one(objects,site,value):
  emissions.append({'site':site,'record_index':len(objects),'kind':value[0],'control_position':len(controls)});objects.append(value)
 def emit_many(objects,site,values):
  for value in values:emit_one(objects,site,value)
  return objects
 def guard(site,value):controls.append({'site':site,'kind':'IF','taken':bool(value)});return value
 def loop(site,values):
  for i,v in enumerate(values):controls.append({'site':site,'kind':'FOR','iteration':i});yield v
 class Transform(ast.NodeTransformer):
  def visit_Assign(self,n):
   site=src.key(n);n=self.generic_visit(n)
   if any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets):n.value=ast.Call(func=ast.Name(id='_emit_many',ctx=ast.Load()),args=[ast.List(elts=[],ctx=ast.Load()),ast.Constant(site),n.value],keywords=[])
   return n
  def visit_Call(self,n):
   site=src.key(n);n=self.generic_visit(n)
   if isinstance(n.func,ast.Attribute) and ast.unparse(n.func.value)=='objects':
    m.need(n.func.attr in ['append','extend'] and len(n.args)==1 and not n.keywords,'UNSUPPORTED-TRACE-EMISSION')
    return ast.copy_location(ast.Call(func=ast.Name(id='_emit_one' if n.func.attr=='append' else '_emit_many',ctx=ast.Load()),args=[ast.Name(id='objects',ctx=ast.Load()),ast.Constant(site),n.args[0]],keywords=[]),n)
   return n
  def visit_If(self,n):
   site=src.key(n);n=self.generic_visit(n);n.test=ast.Call(func=ast.Name(id='_guard',ctx=ast.Load()),args=[ast.Constant(site),n.test],keywords=[]);return n
  def visit_For(self,n):
   site=src.key(n);n=self.generic_visit(n);n.iter=ast.Call(func=ast.Name(id='_loop',ctx=ast.Load()),args=[ast.Constant(site),n.iter],keywords=[]);return n
 env=dict(ingest.__dict__);env.update(_emit_one=emit_one,_emit_many=emit_many,_guard=guard,_loop=loop)
 program=ast.fix_missing_locations(ast.Module(body=[Transform().visit(fn)],type_ignores=[]));exec(compile(program,'<pinned-read-only-ingest-trace>','exec'),env)
 got=env['validate_export'](export);original=ingest.validate_export(export);m.same(got,original,'INSTRUMENTATION-CHANGED-VALIDATION')
 m.need(len(emissions)==len(got['objects']),'TRACE-OBJECT-COVERAGE');return got,emissions,controls

def observe(value,directory,rules,export,context,procedure=False):
 value,directory,rules,export=json.loads(m.enc([value,directory,rules,export]));validate_map(value,directory,rules);c=s.setup(s.ROOT)
 m.need(context in c.contexts,'GUARD-CONTEXT');occ=c.ingest(export,context,c.binding);verified,emissions,controls=trace_export(export)
 sites={x['site']:x for x in value['sources']['projection']['sites']};byindex={}
 for link in occ['candidate_occurrences']:byindex.setdefault(link['record_index'],[]).append(link)
 for e in emissions:
  m.need(e['site'] in sites,'UNMAPPED-EMISSION-SITE');links=byindex.get(e['record_index'],[]);m.need(links,'UNREPRESENTED-EMISSION')
  # Root normalization is already source-owned and validated by Candidate.ingest.
  # References may introduce other schema families below the root.
  allowed=sites[e['site']]['families'];root=[x for x in links if x['pointer'] in ['', '/value'] and x['template'].split(':',1)[0] in allowed]
  m.need(root,'EMISSION-DECLARATION-GUARD');e['candidate_occurrences']=[x['id'] for x in links];e['root_declarations']=sorted({x['class'] for x in root})
 origins=[];requests={m.sha(m.enc(obj)):obj for kind,obj in verified['objects'] if kind=='REQUEST'}
 for index,(kind,obj) in enumerate(verified['objects']):
  if kind=='EVENT':
   matches=[x for x in value['sources']['event_origins']['origins'] if obj['kind'] in x['event_kinds']]
   m.need(len(matches)==1,'EVENT-PRODUCER-COVERAGE')
   origins.append({'record_index':index,'event_kind':obj['kind'],'request':obj['request'],'method':requests[obj['request']]['method'],'decision_kind':requests[obj['request']]['body'].get('kind') if requests[obj['request']]['method']=='decide' else None,'source_site':matches[0]['site'],'source':matches[0]['source'],'candidate_occurrences':[x['id'] for x in byindex[index]]})
 counts={};
 for e in emissions:counts[e['kind']]=counts.get(e['kind'],0)+1
 out={'format':'I164-GUARD-EMISSION-RESULT-1','binding':c.binding,'map_sha256':m.sha(m.enc(value)),'context':context,'export_sha256':m.sha(m.enc(export)),'occurrence_sha256':m.sha(m.enc(occ)),'emissions':emissions,'controls':controls,'runtime_event_origins':origins,'per_kind':counts,'unobserved_sites':sorted(set(sites)-{e['site'] for e in emissions}),'response_associations':occ['response_associations'],'guarded_absences':occ['guarded_absences'],'derived_framing':occ['derived_framing'],'derived_indices':occ['derived_indices'],'runtime_path_status':'authenticated saved fold; source sites are mapped, not a claim that every runtime path was executed','lifetime_multiplicity':None,'backup':'KERNEL-ONLY','full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED'}
 if procedure:
  import prospective_procedure as p
  inputs=p.count_only(directory,rules);duties=p.consume(inputs,directory,rules,occ,export)
  out['procedure']={'input_sha256':m.sha(m.enc(inputs)),'result_sha256':m.sha(m.enc(duties)),'tokens':duties['finite_tokens'],'structural_pairs':duties['finite_structural_pairs'],'semantic_pairs':duties['finite_semantic_pairs'],'production_token_count':duties['production_token_count'],'production_pair_count':duties['production_pair_count'],'unresolved':duties['unresolved']}
 return out

def validate_result(result,value,directory,rules,export,context,procedure=False):
 m.same(result,observe(value,directory,rules,export,context,procedure),'GUARD-EMISSION-RESULT-SUBSTITUTION');return True

def main():
 a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--output',required=True);a.add_argument('--export');a.add_argument('--context');a.add_argument('--procedure',action='store_true');x=a.parse_args();s.setup(x.root);d=json.loads((s.ROOT/'compiler_outputs/compiler-output.json').read_bytes());r=json.loads((s.ROOT/'prospective_outputs/semantic/rules.json').read_bytes());v=compile_map(d,r)
 if x.export:v=observe(v,d,r,json.loads(Path(x.export).read_bytes()),x.context,x.procedure)
 Path(x.output).write_bytes(m.enc(v));print('PASS bounded guard/emission correspondence; readiness/final binding BLOCKED')
if __name__=='__main__':main()
