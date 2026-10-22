"""Bounded source correspondence pairs over authenticated saved exports.
No full-model expansion, qualified dependency/equality/actor classification or admission.
"""
import ast,copy,json,sys,argparse
from pathlib import Path
import compiler as m
ROOT=None

def setup(root):
 global ROOT
 ROOT=Path(root).resolve();c=m.setup(ROOT)
 m.need(m.sha((ROOT/'compiler/compiler.py').read_bytes())=='b8f5b7e8bbc87c7290bdfdb34e4ee5a179d536501228c70b27e7a776b37639c4','DR01-COMPILER-PIN')
 return c

def specs():
 # Read source each time: mutable imported expectations cannot change validation.
 tree=ast.parse((Path(__file__).parent/'rule_basis.py').read_bytes())
 return ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RULES' for t in n.targets)))

def compile_rules(c=None):
 c=setup(ROOT) if c is None else c
 from source_coverage import inspect
 coverage=inspect(ROOT,c.c['associations.json']['prospective'],c.groups)
 fs={r['template_id']:r['id'] for r in c.c['fields.json']['prospective']};assocs=c.c['associations.json']['prospective'];rules=[]
 for i,(name,assoc,left,right,op,guard) in enumerate(specs()):
  a=next(a for a in assocs if a['id']==assoc)
  m.need(left in fs and right in fs,'SEMANTIC-ENDPOINT')
  rules.append({'id':name,'ordinal':359218+i,'parent_association':assoc,'parent_ordinal':359206+next(j for j,x in enumerate(assocs) if x['id']==assoc),'kind':'SOURCE-CORRESPONDENCE-PAIR','qualified_dependency':'UNKNOWN','potential_equality':False,'actor_relationship':False,'contexts':sorted(c.contexts),'from':{'template':left,'class':fs[left]},'to':{'template':right,'class':fs[right]},'direction':'referencing/result occurrence -> exact governing/related source occurrence; no qualified causal direction','guard':guard,'join':{'operator':op,'keys':['candidate identity','context','authenticated saved export','exact record origin (history head/U, immutable blob reference or authenticated packet/challenge)'],'multiplicity':'one exact target per selected source; intent-owner has one per source-required owned coordinate; retained copies are distinct scoped occurrences','ordering':'rule ordinal, source record index, source pointer, target record index, target pointer'},'source':a['source'],'anchors':a['anchors']})
 m.need(len({r['id'] for r in rules})==len(rules),'DUPLICATE-RULE')
 for a in assocs:
  used={r[end]['template'] for r in rules if r['parent_association']==a['id'] for end in ['from','to']}
  m.need({e['template'] for e in a['endpoints']}<=used,'UNLOWERED-ENDPOINT:'+a['id'])
 identities=[m.ident('compiler/'+n) for n in ['compiler.py','semantic.py','rule_basis.py','source_coverage.py','runtime_inventory.py']]
 return copy.deepcopy({'format':'I164-SEMANTIC-PAIRS-1','candidate_binding':c.binding,'compiler_sources':identities,'inherited_ordinals':[1,349871],'prior_compiler_ordinals':[349872,359217],'rules':rules,'coverage':coverage,'procedure_inputs':{'operator':'VALIDATED-EXPLICIT-SOURCE-CORRESPONDENCE-PAIRS','key_namespace':['candidate','context','export','record_index','pointer','class'],'complete_model_ranges':'UNRESOLVED','historical_procedures':'NOT-DROP-IN; no expansion/binding/finalization invoked'},'ledger_duties':[{'ordinal':r['ordinal'],'parent_obligation':r['parent_ordinal'],'rule':r['id'],'required':['exact source guards','validated endpoints and origin keys','complete cardinalities separately','qualified classification separately'],'status':'UNQUALIFIED-CORRESPONDENCE-ONLY','cardinality':None} for r in rules],'full_expansion_ready':False,'final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED','unresolved':['complete source-established root/nested/lifetime directories','external evidence serialization bounds','full runtime source completeness','qualified classifications and actor/equality closure','complete immutable model and ledger binding']})

def count_only(directory,rules):
 directory,rules=json.loads(m.enc([directory,rules]));c=setup(ROOT);m.validate(directory,c);m.same(rules,compile_rules(c),'SEMANTIC-RULE-SUBSTITUTION')
 prior=m.count_only(directory,c)
 structural={'exact_metadata':prior['exact_metadata'],'tokens':prior['tokens'],'edges':{'exact':None,'expression':'historical edges plus prior mechanical guarded joins; retained n-ary parent obligations do not themselves emit pairs'}}
 return {'structural':structural,'parent_obligation_lowering':{a:[r['ordinal'] for r in rules['rules'] if r['parent_association']==a] for a in rules['coverage']['source_associations']},'composite_edge_count':{'exact':None,'expression':'structural edges + source-correspondence pairs, preserving distinct relation kinds; no parent-obligation double counting'},'semantic_rule_count':len(rules['rules']),'per_rule':[{'ordinal':r['ordinal'],'exact':None,'expression':'cardinality of guarded '+r['join']['operator']+' over complete context-scoped source directories','guard':r['guard']} for r in rules['rules']],'context_rule_applications':len(rules['rules'])*2,'semantic_pairs':{'exact':None,'expression':'SUM over source-established context/history/blob/envelope directories of guarded unique joins; intent-owner sums source-required coordinates','dependencies':rules['unresolved']},'full_expansion_ready':False,'final_binding':'BLOCKED'}

class View:
 def __init__(self,objects,occ,export):
  self.objects=objects;self.occ=occ;self.export=export
  self.by_kind={};self.links={}
  wanted={s for r in specs() for s in [r[2],r[3]]}
  for i,(k,o) in enumerate(objects):self.by_kind.setdefault(k,[]).append(i)
  for l in occ['candidate_occurrences']:
   if l['template'] in wanted:
    key=(l['record_index'],l['template'],l['pointer']);m.need(key not in self.links,'DUPLICATE-SEMANTIC-OCCURRENCE');self.links[key]=l
  self.actions=self.unique('ACTION',lambda o:m.sha(m.enc(o)))
  self.attempts=self.unique('ATTEMPT',lambda o:m.sha(m.enc(o)))
  self.owners=self.unique('OWNERSHIP-ROW',lambda o:m.sha(m.enc(o['coordinate'])))
  self.events=self.unique('EVENT',lambda o:o['after']['seq'])
  self.heads=self.unique('HEAD',lambda o:o['seq'])
  self.responses=self.unique('RESPONSE',lambda o:o['response']['request'])
  self.packets=self.unique('PACKET',lambda o:m.sha(m.enc(o)))
  self.journals=self.unique('JOURNAL',lambda o:o['challenge'])
  # Source-owned child emission order from ingest.validate_export; equality pins provenance.
  states=[{'binding':objects[0][1].get('binding'), 'seq':0}]+[self.obj(self.heads[n]) for n in sorted(self.heads)]
  self.states={};starts=self.by_kind.get('COUNTS',[]);m.need(len(starts)==len(states),'HISTORY-CHILD-DIRECTORY')
  for state,start in zip(states,starts):
   seq=state['seq'];cursor=start;view={'seq':seq,'u':{},'counts':cursor,'resources':cursor+2}
   if seq==0:
    m.same(objects[start:start+3],[('COUNTS',{'attempt':0,'query':0,'snapshot':0,'verifier':0}),('PARTITIONS',{'query':0,'snapshot':0,'verifier':0}),('RESOURCES',{'slots':0,'holds':0,'query_holds':0,'extra_queries':0})],'GENESIS-CHILDREN')
    self.states[0]=view;continue
   def take(kind,value):
    nonlocal cursor
    m.same(list(objects[cursor]),[kind,value],'CHILD-ORIGIN:'+str(seq));n=cursor;cursor+=1;return n
   view['counts']=take('COUNTS',state['counts']);take('PARTITIONS',state['partitions']);view['resources']=take('RESOURCES',state['resources'])
   for u,v in state['u'].items():
    row={'entry':take('U-ENTRY',{'key':u,'value':v})};view['u'][u]=row
    if 'stage' not in v:continue
    st=v['stage'];row['stage']=take('STAGE',st)
    for family,field,name in [('TRANSPORT-ENTRY','transport','transport'),('RETRY-ID-ENTRY','retry_ids','retry_ids'),('BACKUP-ENTRY','backups','backups')]:row[name]={key:take(family,{'key':key,'value':value}) for key,value in st[field].items()}
    if st['last'] is not None:row['last']=take('LAST',st['last'])
    if st['pending'] is not None:
     row['pending']=take('PENDING',st['pending'])
     if st['pending']['query'] is not None:row['query']=take('QUERY',st['pending']['query'])
   self.states[seq]=view
 def obj(self,i):return self.objects[i][1]
 def unique(self,kind,key):
  d={}
  for i in self.by_kind.get(kind,[]):
   k=key(self.obj(i));m.need(k not in d,'DUPLICATE-SEMANTIC-MATCH:'+kind);d[k]=i
  return d
 def ref(self,d,key):m.need(key in d,'MISSING-SEMANTIC-MATCH');return d[key]
 def endpoint(self,i,template):
  name,path=template.split(':',1);kind,obj=self.objects[i]
  actual='RETRY-RELEASE-RESULT' if kind=='RELEASE-RESULT' and 'attempt' in obj else kind
  m.need(name==actual,'ENDPOINT-FAMILY')
  ptr=('/value' if name in ['U-ENTRY','TRANSPORT-ENTRY'] else '')+path
  key=(i,template,ptr);m.need(key in self.links,'MISSING-SEMANTIC-ENDPOINT:'+template)
  return self.links[key]

def _pairs(rules,v):
 defs={r['join']['operator']:r for r in rules['rules']};pairs=[];seen=set()
 def emit(op,left,right):
  m.need(op in defs,'UNDECLARED-PAIR-OPERATOR');r=defs[op];a=v.endpoint(left,r['from']['template']);b=v.endpoint(right,r['to']['template'])
  m.need(a['context']==b['context']==v.occ['context'],'CROSS-CONTEXT-PAIR')
  key=(r['ordinal'],a['id'],b['id']);m.need(key not in seen,'DUPLICATE-SEMANTIC-PAIR');seen.add(key)
  pairs.append({'ordinal':r['ordinal'],'from':a['id'],'to':b['id'],'from_record':left,'to_record':right,'from_pointer':a['pointer'],'to_pointer':b['pointer'],'context':v.occ['context'],'kind':'SOURCE-CORRESPONDENCE-PAIR','qualified_dependency':'UNKNOWN'})
 for ref,i in v.attempts.items():
  a=v.obj(i);action=v.ref(v.actions,a['action']);emit('attempt_action',i,action)
  if a['parent'] is None:emit('first_ordinal',i,action)
  else:
   p=v.ref(v.attempts,a['parent']);par=v.obj(p)
   m.need(par['ordinal']<a['ordinal'] and all(par[k]==a[k] for k in ['action','u','intent','session','binding']),'ATTEMPT-ANCESTRY-KEY')
   emit('attempt_parent',i,p);emit('retry_tx',i,action);emit('retry_id',i,i)
 for i in v.actions.values():
  for op in ['template_kind','template_branch','template_intent','template_u']:emit(op,i,i)
 for seq,state in v.states.items():
  for u,row in state['u'].items():
   entry=v.obj(row['entry'])['value'];emit('retired_intent',row['entry'],row['entry'])
   owner=v.ref(v.owners,entry['reservation']);emit('reservation_owner',row['entry'],owner)
   co=v.obj(owner)['coordinate'];nonces=[int(co[2])] if 'stage' not in row else range(v.export['config']['start_nonce'],int(co[2])+3)
   for n in nonces:
    j=v.ref(v.owners,m.sha(m.enc([co[0],co[1],str(n)])))
    m.need(v.obj(j)['owner']==m.sha(m.enc(['prospective',v.obj(v.heads[seq])['binding'],u,entry['intent']])),'OWNER-KEY')
    emit('intent_owner',row['entry'],j)
   for ref,i in row.get('transport',{}).items():
    slot=v.obj(i)['value']['slot']
    if slot=='HELD':emit('held_slot',i,state['resources'])
    elif slot=='CONSUMED':emit('consumed_slot',i,state['resources'])
    else:m.need(slot=='RELEASED','UNKNOWN-SLOT')
   if 'query' in row:
    q=v.obj(row['query']);emit('query_attempt',row['query'],v.ref(v.attempts,q['attempt']));m.need(q['ordinal']==v.obj(state['counts'])['query'],'QUERY-ORDINAL');emit('query_charge',row['query'],state['counts'])
   if 'pending' in row:
    p=v.obj(row['pending']);a=v.ref(v.actions,p['action']);emit('signing_authority',row['pending'],a)
    if p['tx'] is not None:emit('persisted_signature',row['pending'],a)
    if p['released']:emit('released_attempt',row['pending'],row['pending']);emit('latest_attempt',row['pending'],v.ref(v.attempts,p['latest']))
   for i in row.get('backups',{}).values():emit('backup_retention',i,i)
 for seq,ei in v.events.items():
  e=v.obj(ei);post=v.states[seq];pre=v.states[seq-1];emit('history_after',ei,v.heads[seq])
  if e['previous']!='0'*64:emit('history_previous',ei,v.heads[seq-1])
  # Request is immutable and authenticated; select by its digest, never value coincidence.
  matches=[i for i in v.by_kind['REQUEST'] if m.sha(m.enc(v.obj(i)))==e['request']];m.need(len(matches)==1,'EVENT-REQUEST-MATCH');request=v.obj(matches[0]);u=request['u'];row=post['u'].get(u,{})
  if e['kind']=='decide':
   a=v.ref(v.actions,v.obj(row['pending'])['action'])
   m.need(v.obj(a)['decision_request']==e['request'] and v.obj(a)['attempt_ordinal']==v.obj(post['counts'])['attempt'],'DECISION-CHARGE-JOIN')
   emit('decision_charge',a,post['counts']);emit('decision_hold',a,post['resources']);emit('decision_query_hold',a,post['resources'])
  elif e['kind']=='retry-release':
   a=v.ref(v.attempts,e['proof']);m.need(v.obj(a)['request']==e['request'] and v.obj(a)['ordinal']==v.obj(post['counts'])['attempt'],'RETRY-CHARGE-JOIN')
   emit('retry_charge',a,post['counts']);emit('retry_slot',a,post['resources']);emit('retry_query_hold',a,post['resources'])
  elif e['kind']=='query':emit('query_reservation',row['query'],post['resources'])
  elif e['kind']=='backup':emit('backup_charge',row['backups'][request['body']['id']],post['counts'])
  elif e['kind']=='observe':
   matches=[i for i in v.by_kind['OBSERVATION'] if m.sha(m.enc(v.obj(i)))==e['proof']];m.need(len(matches)==1,'OBSERVATION-MATCH');oi=matches[0];o=v.obj(oi);before=pre['u'][u]
   emit('observation_action',oi,v.ref(v.actions,o['action']));emit('observation_transaction',oi,before['pending']);emit('observation_query',oi,before['query']);emit('observation_disposition',oi,oi)
   if o['outcome']!='UNAVAILABLE':
    ref=v.obj(before['pending'])['first'];emit('settled_slot',row['transport'][ref],before['transport'][ref])
 for packet,ri in v.responses.items():
  r=v.obj(ri)['response'];pi=v.ref(v.packets,packet);ji=v.ref(v.journals,r['challenge'])
  emit('response_signature',ri,ri);emit('response_packet',ri,pi);emit('response_journal',ji,ri)
  req=v.obj(pi)['request']
  if r['ok'] and req['method'] in ['release','retry_release']:
   result=r['data'];matches=[i for i in v.by_kind['RELEASE-RESULT'] if m.enc(v.obj(i))==m.enc(result)];m.need(len(matches)==1,'RELEASE-RESULT-MATCH');i=matches[0]
   matches=[seq for seq,ei in v.events.items() if v.obj(ei)['request']==m.sha(m.enc(req))];m.need(len(matches)==1,'RELEASE-EVENT-MATCH');row=v.states[matches[0]]['u'][req['u']]
   emit('release_bytes' if req['method']=='release' else 'retry_release_bytes',i,row['pending'])
   if req['method']=='retry_release':emit('retry_release_ancestry',i,v.ref(v.attempts,result['attempt']))
 pairs.sort(key=lambda p:(p['ordinal'],p['from_record'],p['from_pointer'],p['to_record'],p['to_pointer']))
 return pairs

def _procedure(pairs,rules,context):
 # Role-specific fixture work groups, not canonical classes or complete token ranges.
 ids=sorted({p[k] for p in pairs for k in ['from','to']});index={v:i for i,v in enumerate(ids)};steps=[]
 for r in rules['rules']:
  selected=[p for p in pairs if p['ordinal']==r['ordinal']]
  steps.append({'ordinal':r['ordinal'],'source_class':r['from']['class'],'target_class':r['to']['class'],'context':context,'lookup_operator':'PARENT-RECORD','source_rows':[[index[p['from']],p['from']+'/'+p['to'],p['to'],True] for p in selected],'target_rows':[[index[t],t,None,True] for t in sorted({p['to'] for p in selected})],'count':len(selected),'classification':'SOURCE-CORRESPONDENCE; not structural containment'})
 return {'fixture_occurrence_index':ids,'lookup_steps':steps,'index_scope':'LOCAL-FIXTURE-ONLY; not canonical token allocation','complete_model_ranges':None,'ledger_duties':[{'ordinal':s['ordinal'],'required_finite_count':s['count'],'disposition':'NOT-ESTABLISHED','qualification':'UNAVAILABLE'} for s in steps]}

def lower(directory,rules,occ,export):
 directory,rules,occ,export=json.loads(m.enc([directory,rules,occ,export]));c=setup(ROOT)
 m.validate(directory,c);m.same(rules,compile_rules(c),'SEMANTIC-RULE-SUBSTITUTION');c.validate_output(occ,export)
 from ingest import validate_export
 verified=validate_export(export);view=View(verified['objects'],occ,export);pairs=_pairs(rules,view)
 counts=[{'ordinal':r['ordinal'],'pairs':sum(p['ordinal']==r['ordinal'] for p in pairs)} for r in rules['rules']]
 return {'format':'I164-SEMANTIC-PAIR-RESULT-1','binding':c.binding,'rule_identity':m.sha(m.enc(rules)),'directory_identity':m.sha(m.enc(directory)),'context':occ['context'],'saved_export_sha256':m.sha(m.enc(export)),'pairs':pairs,'counts':counts,'exact_finite_pairs':len(pairs),'procedure_input':{'ordering':'rule ordinal then exact endpoint origin','instance_range_assignment':'NOT-PERFORMED; IDs are exact existing occurrence IDs','lookup_plan':_procedure(pairs,rules,occ['context']),'ledger_counts':counts,'ledger_status':'MECHANICAL-ONLY; qualification and complete directories unavailable'},'full_expansion_ready':False,'final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}

def validate_result(result,directory,rules,occ,export):
 m.same(result,lower(directory,rules,occ,export),'SEMANTIC-PAIR-RESULT-SUBSTITUTION');return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();setup(a.root);c=compile_rules();d=json.loads((ROOT/'compiler_outputs/compiler-output.json').read_bytes());p=Path(a.output);p.mkdir();(p/'rules.json').write_bytes(m.enc(c));(p/'counts.json').write_bytes(m.enc(count_only(d,c)));print(len(c['rules']),'rules; readiness BLOCKED')
if __name__=='__main__':main()
