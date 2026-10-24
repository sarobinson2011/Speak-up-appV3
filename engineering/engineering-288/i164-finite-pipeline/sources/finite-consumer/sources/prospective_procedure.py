"""Validated prospective procedure/count/duty adapter. No full model allocation."""
import ast,json,argparse
from pathlib import Path
import semantic as s
m=s.m

def snap(*x):return json.loads(m.enc(x))
def binding(directory,rules):
 c=s.setup(s.ROOT);m.validate(directory,c);m.same(rules,s.compile_rules(c),'PROCEDURE-RULE-BINDING')
 return {'candidate':c.binding,'directory_sha256':m.sha(m.enc(directory)),'rules_sha256':m.sha(m.enc(rules)),'contexts':directory['context_definitions'],'procedure_source':m.ident('compiler/prospective_procedure.py'),'retained_lookup':m.ident('native/code/expand_candidate.py'),'retained_ledger':m.ident('native/code/bind_ledger.py')}
def duty_names():
 tree=ast.parse((s.ROOT/'native/code/bind_ledger.py').read_bytes())
 return list(ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DUTIES' for t in n.targets))))
def count_only(directory,rules):
 directory,rules=snap(directory,rules);b=binding(directory,rules);counts=s.count_only(directory,rules);names=duty_names()
 dirs=[{'class':d['class'],'context':d['context'],'directory_sha256':m.sha(m.enc(d)),'range':None,'cardinality':None,'expression':'cardinality of source-established guarded directory','duty_names':names,'classification':'UNKNOWN','disposition':'NOT-ESTABLISHED'} for d in directory['directories']]
 # Parent n-ary obligations remain duties, not a second set of pairs.
 relations=[{'ordinal':r['ordinal'],'kind':r['kind'],'count':None,'edge_range':None,'classification':'UNKNOWN','disposition':'NOT-ESTABLISHED'} for r in directory['relations']+rules['rules']]
 return {'format':'I164-PROSPECTIVE-PROCEDURE-INPUT-1','binding':b,'counts':counts,'directory_ranges':dirs,'relation_duties':relations,'coverage':{'runtime_site_count':len(rules['coverage']['runtime_inventory']),'full_runtime_completeness':False,'backup_authenticated':False,'parent_lowering':counts['parent_obligation_lowering']},'resolved_local_step':'twelve retained parent associations have bounded child rules; not full runtime pair completeness','blockers':['UNRESOLVED-DIRECTORIES-AND-CARDINALITIES','FULL-RUNTIME-EMISSION-AND-GUARD-COVERAGE','BACKUP-AUTHENTICATED-EVIDENCE','QUALIFIED-CLASSIFICATIONS-APPOINTMENTS','COMPLETE-IMMUTABLE-MODEL-AND-LEDGER','CANONICAL-TARGET-PROCEDURE-DESIGNATION'],'full_expansion_ready':False,'final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate_input(value,directory,rules):
 m.same(value,count_only(directory,rules),'PROCEDURE-INPUT-SUBSTITUTION');return True
class Group:
 def __init__(self,rows):self.rows=rows;self.parts=[(0,rows,True)]
 def entries(self,prefix=None):return iter(self.rows)
 def get(self,key):
  matches=[(i,new) for i,k,parent,new in self.rows if k==key];m.need(len(matches)==1,'PROCEDURE-UNIQUE-TARGET');return matches[0]
def lookup():
 tree=ast.parse((s.ROOT/'native/code/expand_candidate.py').read_bytes());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pairs');env={'need':m.need}
 exec(compile(ast.Module(body=[node],type_ignores=[]),'<pinned-retained-pure-pairs>','exec'),env);return env['pairs']
def consume(value,directory,rules,occ,export):
 value,directory,rules,occ,export=snap(value,directory,rules,occ,export)
 validate_input(value,directory,rules)
 lowered=s.lower(directory,rules,occ,export)
 rows=m.instance_rows(directory,occ,export);structural=m.count_actual_fixture(directory,occ,export)
 # Finite class/context ranges, contiguous in a local-only index; absent classes
 # may have empty fixture ranges but their production cardinality remains None.
 ranges=[];index={};position=0
 for d in directory['directories']:
  if d['context']!=occ['context']:continue
  members=sorted(rows.get(d['class'],[]),key=lambda x:x['id']);start=position
  for member in members:
   m.need(member['id'] not in index,'DUPLICATE-RANGE-MEMBER');index[member['id']]=position;position+=1
  ranges.append({'class':d['class'],'context':occ['context'],'range':[start,position],'members':[x['id'] for x in members],'qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'})
 fn=lookup();duties=[];offset=0
 for step in lowered['procedure_input']['lookup_plan']['lookup_steps']:
  ids=lowered['procedure_input']['lookup_plan']['fixture_occurrence_index']
  left=[[index[ids[i]],key,parent,new] for i,key,parent,new in step['source_rows']];right=[[index[ids[i]],key,parent,new] for i,key,parent,new in step['target_rows']]
  p={'rels':[{'from_node':step['source_class'],'to_node':step['target_class']}],'rules':['PARENT-RECORD'],'details':[None],'groups':{('SOURCE',occ['context']):Group(left),('TARGET',occ['context']):Group(right)},'old_rel_n':0}
  # Role separation required even for same-class joins.
  p['rels']=[{'from_node':'SOURCE','to_node':'TARGET'}]
  actual=list(fn(p,0,occ['context']));expected=[(index[x['from']],index[x['to']]) for x in lowered['pairs'] if x['ordinal']==step['ordinal']]
  m.same(sorted(actual),sorted(expected),'PROCEDURE-PAIR-CONSUMPTION');m.need(len(actual)==step['count'],'PROCEDURE-COUNT')
  duties.append({'ordinal':step['ordinal'],'kind':'SOURCE-CORRESPONDENCE-PAIR','count':len(actual),'local_semantic_edge_range':[offset,offset+len(actual)],'classification':'UNKNOWN','qualification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED'});offset+=len(actual)
 return {'format':'I164-PROSPECTIVE-MECHANICAL-DUTY-RESULT-1','binding':value['binding'],'procedure_input_sha256':m.sha(m.enc(value)),'context':occ['context'],'saved_export_sha256':m.sha(m.enc(export)),'occurrence_sha256':m.sha(m.enc(occ)),'pair_result_sha256':m.sha(m.enc(lowered)),'range_scope':'FINITE-SAVED-EXPORT-ONLY; not complete-model indices','node_ranges':ranges,'structural_duties':structural['relation_counts'],'semantic_duties':duties,'finite_tokens':position,'finite_structural_pairs':structural['structural_pairs'],'finite_semantic_pairs':offset,'production_token_count':None,'production_pair_count':None,'unresolved':value['blockers'],'full_expansion_ready':False,'final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}
def validate_result(result,value,directory,rules,occ,export):
 m.same(result,consume(value,directory,rules,occ,export),'PROCEDURE-DUTY-SUBSTITUTION');return True
def readiness(value,directory,rules):
 validate_input(value,directory,rules);raise m.Invalid('PROSPECTIVE-READINESS-BLOCKED:'+','.join(value['blockers']))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--rules',required=True);ap.add_argument('--export');ap.add_argument('--context');ap.add_argument('--output',required=True);a=ap.parse_args();c=s.setup(a.root)
 d=json.loads((s.ROOT/'compiler_outputs/compiler-output.json').read_bytes());r=json.loads(Path(a.rules).read_bytes());v=count_only(d,r)
 if a.export:
  m.need(a.context in c.contexts,'PROCEDURE-CONTEXT');e=json.loads(Path(a.export).read_bytes());o=c.ingest(e,a.context,c.binding);v=consume(v,d,r,o,e)
 Path(a.output).write_bytes(m.enc(v));print('PASS bounded procedure correspondence; readiness/final binding BLOCKED')
if __name__=='__main__':main()
