"""Candidate-bound offline saved-export adapter. Never a full-model binder."""
import sys,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import baseline
from common import enc,sha,parse,need,same,Invalid
from pipeline import integrate
from ingest import validate_export
from static_declarations import validate_value
from framing_templates import framing
PIN='d2b76814433f1d3c96bccdb2eaaa6ddb1521cafcd2c616fc1b93d064995a2130'

def local(path):
 need(type(path) is str and not Path(path).is_absolute() and '..' not in Path(path).parts,'OUT-OF-DIRECTORY')
 p=ROOT/path;need(p.resolve().is_relative_to(ROOT.resolve()) and p.is_file(),'MISSING-OR-OUT-OF-DIRECTORY');return p

def identity(path):
 b=local(path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b)}

class Candidate:
 def __init__(self):
  need(sha(local('candidate/identity.json').read_bytes())==PIN,'STALE-CANDIDATE')
  baseline.validate_disk() # source-derived, exact native and prospective preservation
  self.c={p.name:parse(p.read_bytes(),100000000) for p in (ROOT/'candidate').iterdir()}
  self.fields={r['template_id']:r for r in self.c['fields.json']['prospective']}
  self.groups=self.c['schemas.json']['prospective'];self.optional=self.c['schemas.json']['optional']
  self.contexts={x['context'] for x in self.c['contexts.json']['associations']}
  self.binding={'candidate':identity('candidate/identity.json'),'profile':identity('candidate/profile-binding.json'),
    'register':{n:identity('candidate/'+n+'.json') for n in ['fields','schemas','source-forms','namespace','native-mapping','associations']},
    'contexts':identity('candidate/contexts.json'),'directories':identity('candidate/directories.json'),
    'duties':identity('candidate/ledger-duties.json'),'runtime':self.c['profile-binding.json']['runtime'],
    'reviewed_adapters':self.c['profile-binding.json']['adapters'],'downstream_adapter':identity('integration/candidate_pipeline.py')}
 def check_binding(self,b):
  # Resolve every supplied file reference before identity equality; no external paths or stale mixtures.
  def walk(x):
   if isinstance(x,dict):
    if 'path' in x and 'sha256' in x:same(identity(x['path']),x,'REFERENCE-IDENTITY')
    else:
     for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(b);same(b,self.binding,'MIXED-CANDIDATE-BINDING')
 def ingest(self,export,context,binding):
  self.check_binding(binding);need(context in self.contexts,'CONTEXT-DIRECTORY')
  # Existing authenticated fold/projection is retained, including response links and original bytes.
  old=integrate(export);v=validate_export(export);objects=v['objects']
  packets={sha(enc(o)):o for k,o in objects if k=='PACKET'};refused=set()
  for _,p,r in export['journal']:
   req=parse(bytes.fromhex(p))['request']
   if r is None or parse(bytes.fromhex(r))['response']['ok'] is False:refused.add((req['method'],sha(enc(req['body']))))
  projection={(r['occurrence'],r['pointer']):r for r in old['actual_occurrences']}
  links=[];frames=[];absent=[];indices=[]
  def esc(k):return str(k).replace('~','~0').replace('/','~1')
  def emit(tid,value,index,pointer,key=None):
   need(tid in self.fields,'CLASS-DIRECTORY:'+tid);field=self.fields[tid]
   original=projection.get((index,pointer));need(original is not None,'OCCURRENCE-DIRECTORY')
   same(original['exact_bytes_hex'],enc(value).hex(),'OCCURRENCE-VALUE')
   lid=sha(enc([PIN,context,index,pointer,tid]));links.append({'id':lid,'candidate_sha256':PIN,'context':context,'class':field['id'],'template':tid,'occurrence':original['id'],'pointer':pointer,'record_index':index})
   for name,val in framing(value,key).items():
    f=self.fields.get(tid+'#'+name);need(f is not None,'FRAMING-CLASS')
    frames.append({'parent':lid,'class':f['id'],'exact_bytes_hex':enc(val).hex()})
  def walk(t,rec,selector,value,parent,index,pointer,method,key=None,depth=0):
   need(depth<300,'LOCAL-RECURSION-CEILING');tid=rec+':'+selector;emit(tid,value,index,pointer,key)
   if isinstance(t,str) or 'wire_type' in t:return
   if 'ref' in t:
    n=t['ref'];shape=self.groups[n]['@value'] if n=='JSON-VALUE' else {'object':self.groups[n]}
    walk(shape,n,'',value,value,index,pointer,method,key,depth+1);return
   if 'union' in t:
    for i,alt in enumerate(t['union']):
     # Whole record already validated. Probe a union alternative with its true discriminator context.
     probe=alt
     while isinstance(probe,dict) and ('variants' in probe or 'request_method_choice' in probe):
      if 'request_method_choice' in probe:probe=probe['request_method_choice'][method]
      else:
       src=value if type(value) is dict and probe['choice_by'] in value else parent
       choice=src[probe['choice_by']];choice=str(choice).lower() if type(choice) is bool else choice
       probe=probe['variants'][choice]
     g=dict(self.groups);g['_ROOT']={'value':probe}
     try:validate_value('_ROOT',{'value':value},method,(g,{},self.optional))
     except Invalid:continue
     walk(alt,rec,selector+'/@union/'+str(i),value,parent,index,pointer,method,key,depth+1);return
    raise Invalid('UNION-NO-ALTERNATIVE')
   if 'variants' in t:
    src=value if type(value) is dict and t['choice_by'] in value else parent
    choice=src[t['choice_by']];choice=str(choice).lower() if type(choice) is bool else choice
    walk(t['variants'][choice],rec,selector+'/@variant/'+choice,value,parent,index,pointer,method,key,depth+1);return
   if 'request_method_choice' in t:
    walk(t['request_method_choice'][method],rec,selector+'/@method/'+method,value,parent,index,pointer,method,key,depth+1);return
   if 'object' in t:
    for k,typ in t['object'].items():
     if k!='@additional' and k not in value:
      need(k in self.optional.get(rec,{}),'ABSENT-REQUIRED');absent.append({'class':self.fields[rec+':'+selector+'/'+k]['id'],'record_index':index,'parent_pointer':pointer,'context':context,'status':'ABSENT-UNDER-VALIDATED-SOURCE-GUARD'} )
    for k,x in value.items():
     sel=selector+('/'+k if k in t['object'] else '/*');typ=t['object'].get(k,t['object'].get('@additional'))
     walk('STRING',rec,sel+'#key',k,value,index,pointer+'/~key/'+esc(k),method,depth=depth+1)
     walk(typ,rec,sel,x,value,index,pointer+'/'+esc(k),method,k,depth+1)
   elif 'directory' in t:
    for k,x in value.items():
     walk('STRING',rec,selector+'/*#key',k,value,index,pointer+'/~key/'+esc(k),method,depth=depth+1)
     walk(t['directory'],rec,selector+'/*',x,value,index,pointer+'/'+esc(k),method,k,depth+1)
   elif 'array' in t or 'tuple' in t:
    for i,x in enumerate(value):
     s=selector+('/*' if 'array' in t else '/'+str(i));typ=t.get('array') if 'array' in t else t['tuple'][i]
     walk(typ,rec,s,x,parent,index,pointer+'/'+str(i),method,depth=depth+1)
     if 'array' in t:
      f=self.fields[rec+':'+selector+'/*#key']
      indices.append({'class':f['id'],'record_index':index,'parent_pointer':pointer,'ordinal':i,'value_pointer':pointer+'/'+str(i),'context':context,'derived_framing':framing(i),'status':'DERIVED-ORDINAL; no wire key'})
  for index,(kind,obj) in enumerate(objects):
   name=kind;value=obj;pointer='';method=None
   if kind in ['U-ENTRY','TRANSPORT-ENTRY']:value=obj['value'];pointer='/value'
   if kind.startswith('ABI-ARGUMENTS-'):name='ABI-'+kind[len('ABI-ARGUMENTS-'):]
   if kind=='RESPONSE':method=packets[obj['response']['request']]['request']['method']
   if kind=='RELEASE-RESULT' and 'attempt' in obj:name='RETRY-RELEASE-RESULT'
   if kind.startswith('BODY-') and (kind[5:],sha(enc(obj))) in refused:name='UNVALIDATED-BODY'
   need(name in self.groups,'UNDECLARED-RECORD:'+name)
   validate_value(name,value,method,(self.groups,{},self.optional))
   walk(self.groups[name]['@value'] if name=='JSON-VALUE' else {'object':self.groups[name]},name,'',value,value,index,pointer,method)
  byclass={}
  for link in links:byclass.setdefault(link['class'],[]).append(link['id'])
  reverse={}
  for link in links:reverse.setdefault(link['occurrence'],[]).append(link)
  response_joins=[]
  for join in old['response_selector_coverage']:
   candidates=reverse.get(join['occurrence_id'],[]) # includes referenced RESPONSE-OK/ERROR declarations
   need(candidates,'RESPONSE-CANDIDATE-ASSOCIATION')
   response_joins.append({'authenticated_association':join,'candidate_occurrences':[l['id'] for l in candidates],'classes':[l['class'] for l in candidates],'candidate_sha256':PIN,'context':context})
  unassigned=[{'occurrence':r['id'],'record':r['record'],'pointer':r['pointer'],'reason':'supporting extraction wrapper; no candidate class equivalence asserted'} for r in old['actual_occurrences'] if r['id'] not in reverse]
  associations=[{'rule':a['id'],'source':a['source'],'endpoints':[{'class':e['class'],'occurrences':byclass.get(e['class'],[])} for e in a['endpoints']], 'status':'SOURCE-FOLD-VALIDATED; endpoint index, not qualified causal edge'} for a in self.c['associations.json']['prospective']]
  return {'format':'I164-CANDIDATE-DOWNSTREAM-1','binding':binding,'context':context,'saved_export_sha256':sha(enc(export)),
   'supporting_pipeline':old,'candidate_occurrences':links,'derived_framing':frames,'derived_indices':indices,'guarded_absences':absent,'response_associations':response_joins,'unassigned_extraction_wrappers':unassigned,'association_index':associations,
   'model_input':{'candidate_profile':binding['profile'],'register':binding['register'],'context':context,'context_definitions':binding['contexts'],'directories':binding['directories'],'ledger_duties':binding['duties'],'scope':'FINITE-SAVED-EXAMPLE; not complete immutable model'},
   'correspondence':'PASS','blockers':baseline.BLOCKERS,'final_binding':'BLOCKED','canonical_registration':False,'actual_admission':False,'stream_identities':'UNCOMPUTED'}
 def validate_output(self,out,export):
  self.check_binding(out['binding']);same(out,self.ingest(export,out['context'],out['binding']),'DOWNSTREAM-SUBSTITUTION');return True
 def final_binding(self,*args,**kwargs):return baseline.final_binding(self.c)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['binding','ingest','validate','final-bind']);ap.add_argument('--export');ap.add_argument('--context');ap.add_argument('--binding');ap.add_argument('--input');ap.add_argument('--output');a=ap.parse_args();c=Candidate()
 if a.action=='final-bind':c.final_binding()
 elif a.action=='binding':out=c.binding
 else:
  e=parse(Path(a.export).read_bytes(),200000000)
  if a.action=='validate':out={'valid':c.validate_output(parse(Path(a.input).read_bytes(),500000000),e),'final_binding':'BLOCKED'}
  else:out=c.ingest(e,a.context,parse(Path(a.binding).read_bytes(),1000000))
 if a.output:
  p=Path(a.output);need(not p.exists(),'OUTPUT-EXISTS');p.write_bytes(enc(out))
 else:print(enc(out).decode(),end='')
