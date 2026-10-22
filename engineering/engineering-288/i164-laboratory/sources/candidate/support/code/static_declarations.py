"""Source-pinned supporting templates. No canonical class allocation or model expansion."""
import ast,re
from common import *
S='STRING';I='INTEGER';B='BOOLEAN';N='NULL'
def ref(n):return {'ref':n}
def nullable(t):return {'union':[N,t]}
def array(t):return {'array':t}
def directory(t):return {'directory':t,'key_type':S}
def obj(**kw):return {'object':kw}
def inventory():
 out=[]
 for path in ['runtime/authority.py','runtime/accounting.py','runtime/ownership.py','retained/stage_carrier.py','retained/signed_eth.py','executor/abi.py']:
  raw=(ROOT/'reference'/path).read_bytes();tree=ast.parse(raw)
  for n in ast.walk(tree):
   if isinstance(n,(ast.If,ast.Dict,ast.DictComp,ast.Compare)) or isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['exact','need']:
    out.append({'source':'reference/'+path,'sha256':sha(raw),'line':n.lineno,'end_line':n.end_lineno,'kind':type(n).__name__,'expression':ast.get_source_segment(raw.decode(),n)})
 return sorted(out,key=lambda x:(x['source'],x['line'],x['kind'],x['expression']))
def schemas():
 groups={};owners={};guards={};optional={}
 def add(record_name,fields,owner='runtime/authority.py',**over):
  groups[record_name]={k:S for k in fields.split()};groups[record_name].update(over);owners[record_name]=owner
 add('ACTION-OUTCOME-TABLE','begin append finalize proceed abandon cleanup')
 add('CONFIG','version pilot session start_nonce manager model profile config',start_nonce=I)
 add('BINDING','ownership ownership_code accounting_code code',config=ref('CONFIG'),principals=ref('PRINCIPALS'),retained=ref('RETAINED-HASHES'))
 add('PRINCIPALS','executor observer server');add('RETAINED-HASHES','anchor.py stages.py signed_eth.py lab_evm.py')
 add('HEAD','binding head',seq=I,counts=ref('COUNTS'),partitions=ref('PARTITIONS'),u=directory(ref('U-ENTRY')),active=nullable(S),resources=ref('RESOURCES'))
 add('COUNTS','',owner='runtime/accounting.py',**{k:I for k in ['attempt','query','snapshot','verifier']})
 add('PARTITIONS','',owner='runtime/accounting.py',**{k:I for k in ['query','snapshot','verifier']})
 add('RESOURCES','',owner='runtime/accounting.py',**{k:I for k in ['slots','holds','query_holds','extra_queries']})
 add('U-ENTRY','intent reservation petition',retired=B,stage=ref('STAGE'));optional['U-ENTRY']={'stage':'OPEN has committed for this retired U'}
 add('STAGE','sid message meta manager branch',n=I,index=I,nonce=I,pending=nullable(ref('PENDING')),last=nullable(ref('LAST')),attempts=I,retries=I,backups=directory(S),transport=directory(ref('TRANSPORT-ENTRY')),retry_ids=directory(S))
 add('RETRY-ID-ENTRY','key value',owner='runtime/accounting.py')
 add('BACKUP-ENTRY','key value')
 add('TRANSPORT-ENTRY','slot',owner='runtime/accounting.py',queried=B,released=B)
 add('PENDING','action phase first latest',tx=nullable(S),released=B,query=nullable(ref('QUERY')),reconciliation=nullable(S),result=S);optional['PENDING']={'result':'phase == FAILED-FROZEN'}
 add('LAST','action tx result')
 add('ATTEMPT','binding pilot session u intent sid action request',owner='runtime/accounting.py',parent=nullable(S),transaction=nullable(S),ordinal=I,retry_id=nullable(S))
 add('ACTION','version binding pilot session sid u intent reservation branch kind decision_request',index=I,attempt_ordinal=I,template=ref('TEMPLATE'))
 add('TEMPLATE','signer chain nonce target calldata value gas_limit gas_price',owner='retained/signed_eth.py')
 add('QUERY','request attempt classification',owner='runtime/accounting.py',ordinal=I)
 add('OBSERVATION','action transaction outcome manager source qualification',query=ref('QUERY'),nonce_consumed=B)
 add('EVENT','previous request kind',proof=nullable(S),after=ref('HEAD-AFTER'))
 groups['HEAD-AFTER']={k:v for k,v in groups['HEAD'].items() if k!='head'};owners['HEAD-AFTER']='runtime/authority.py'
 add('JOURNAL','challenge request_hex',response_hex=nullable(S))
 add('REQUEST','version binding pilot session principal challenge expected method u',body={'choice_by':'method','variants':{}})
 add('PACKET','signature',request=ref('REQUEST'))
 add('RESPONSE','signature',response={'choice_by':'ok','variants':{'true':ref('SUCCESS-RESPONSE'),'false':ref('ERROR-RESPONSE')}})
 add('SUCCESS-RESPONSE','request challenge',ok=B,data={'request_method_choice':{'head':ref('HEAD'),'retire':ref('HEAD'),'open':ref('HEAD'),'decide':ref('HEAD'),'query':ref('HEAD'),'observe':ref('HEAD'),'backup':ref('HEAD'),'sign':ref('SIGNED-RESULT'),'release':ref('RELEASE-RESULT'),'retry_release':ref('RETRY-RELEASE-RESULT')}})
 add('ERROR-RESPONSE','request challenge error',ok=B)
 add('SIGNED-RESULT','action tx',recovered=B,release=B)
 add('RELEASE-RESULT','head action tx bytes',lab_only=B)
 add('RETRY-RELEASE-RESULT','head action attempt tx bytes',lab_only=B)
 add('OWNERSHIP-META','format incarnation',owner='runtime/ownership.py')
 add('OWNERSHIP-ROW','owner',owner='runtime/ownership.py',coordinate={'tuple':[S,S,S]})
 add('OWNERSHIP-ROW-SQL','coord raw_hex hash',owner='runtime/ownership.py')
 add('BLOB-STORE','ref raw_hex')
 from correspondence import BODIES
 for method,fields in BODIES.items():
  add('BODY-'+method,' '.join(fields));groups['REQUEST']['body']['variants'][method]=ref('BODY-'+method)
 groups['BODY-observe']=groups['OBSERVATION'].copy()
 groups['UNVALIDATED-BODY']={'@additional':ref('JSON-VALUE')};owners['UNVALIDATED-BODY']='runtime/authority.py'
 groups['REQUEST']['body']={'union':[groups['REQUEST']['body'],ref('UNVALIDATED-BODY')],'guard':'typed successful action body OR exact refused/unanswered body; latter grants no action'}
 intent_fields='chain registry executor nonce calldata_hex value gas_limit config decision source model contract profile scope key_epoch method carrier gas_price conditional_comparison_hex'
 add('UNSIGNED-INTENT',intent_fields,arguments={'choice_by':'method','variants':{m:ref('ABI-'+m) for m in ['signPetition','signPetitionWithZKProof']}})
 add('COMPACT-INTENT','format calldata_base64',identity=ref('COMPACT-IDENTITY'))
 groups['COMPACT-IDENTITY']={k:v for k,v in groups['UNSIGNED-INTENT'].items() if k not in ['calldata_hex','arguments']};owners['COMPACT-IDENTITY']='runtime/authority.py'
 add('STAGE-META','key signature message_sha256 invocation',total=I,bindings=ref('STAGED-BINDINGS'))
 # Literal parser sets are source-owned, not fixture-derived.
 tree=ast.parse((ROOT/'reference/retained/stage_carrier.py').read_text());assign={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
 keys_=sorted(ast.literal_eval(assign['KEYS']));add('STAGED-BINDINGS',' '.join(keys_),owner='retained/stage_carrier.py')
 add('AUTHORIZED-MESSAGE','format',owner='retained/stage_carrier.py',bindings=ref('STAGED-BINDINGS'),authorized_values=array(S))
 add('CONDITIONAL-CAPSULE','format',permit_for_conditional_test=B);groups['CONDITIONAL-CAPSULE']['@additional']=ref('JSON-VALUE')
 # Source only requires two capsule keys, admitting additional canonical JSON content.
 groups['JSON-VALUE']={'@value':{'union':[N,B,I,'NUMBER',S,array(ref('JSON-VALUE')),directory(ref('JSON-VALUE'))]}};owners['JSON-VALUE']='runtime/authority.py'
 add('SIGNED-TRANSACTION','raw_hex',owner='retained/signed_eth.py',decoded=ref('DECODED-TRANSACTION'),rlp_fields={'tuple':[S]*9})
 add('DECODED-TRANSACTION','signer chain nonce target calldata value gas_limit gas_price transaction_hash',owner='retained/signed_eth.py')
 def abi_type(f):
  t=f['type'];match=re.fullmatch(r'(.*)\[(\d+)\]',t)
  if match:return {'tuple':[abi_type(dict(f,type=match[1])) for _ in range(int(match[2]))]}
  if t=='tuple':return {'object':{c['name']:abi_type(c) for c in f['components']}}
  need(t in ['uint256','bytes32','bytes'],'ABI-TYPE');return {'wire_type':I if t=='uint256' else S,'abi_type':t}
 abi=json.loads((ROOT/'reference/contract/ABI.json').read_text())
 for method in ['signPetition','signPetitionWithZKProof']:
  f=next(x for x in abi if x.get('name')==method and x['type']=='function');groups['ABI-'+method]={x['name']:abi_type(x) for x in f['inputs']};owners['ABI-'+method]='contract/ABI.json'
 return groups,owners,optional

def constructor_coverage(groups):
 result=[];field_sets={n:set(fields) for n,fields in groups.items()}
 for path in ['runtime/authority.py','runtime/accounting.py','runtime/ownership.py']:
  raw=(ROOT/'reference'/path).read_text();tree=ast.parse(raw)
  for node in ast.walk(tree):
   fields=set()
   if isinstance(node,ast.Dict):fields={k.value for k in node.keys if isinstance(k,ast.Constant) and type(k.value) is str}
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
    if node.func.id=='dict':fields={k.arg for k in node.keywords if k.arg is not None}
    if node.func.id=='exact' and len(node.args)>1:
     try:fields=set(ast.literal_eval(node.args[1]))
     except (ValueError,TypeError):pass
   if fields:
    candidates=[name for name,f in field_sets.items() if fields<=f];need(candidates,'UNDECLARED-SOURCE-CONSTRUCTOR:'+path+':'+str(node.lineno)+':'+str(sorted(fields)))
    result.append({'source':'reference/'+path,'source_sha256':sha(raw.encode()),'line':node.lineno,'fields':sorted(fields),'compatible_record_templates':sorted(candidates),'expression':ast.get_source_segment(raw,node)})
 return result

def build():
 pinned_sources();groups,owners,optional=schemas();inv=inventory();rows=[]
 from response_obligations import check_catalogue,check_rows
 response_obligations=check_catalogue(groups,optional)
 def walk(record,path,t,parent,source,guard='present',presence='required'):
  rid=record+':'+path;raw=(ROOT/source).read_bytes()
  row={'id':rid,'record':record,'selector':path,'type':t,'guard':guard,'presence':presence,'parent':parent,'source':source,'source_sha256':sha(raw),'source_rule':'source constructor/parser and full guarded inventory; ABI uses named function inputs','visibility':'UNKNOWN','dependency_classification':'UNKNOWN','custody':['UNKNOWN']*7,'canonical':False}
  rows.append(row)
  for key,typ in [('presence',B),('availability',S),('encoding_length',I),('member_count',nullable(I)),('exact_bytes',S),('type_tag',S),('key_encoding',nullable(S)),('separator_encoding',S),('opening_delimiter',S),('closing_delimiter',S)]:
   rows.append(dict(row,id=rid+'#'+key,selector=path+'#'+key,type=typ,parent=rid,guard='derived framing of '+rid,presence='required',source_rule='framing_templates.framing over canonical common.enc; source-field presence guard required',source='code/framing_templates.py',source_sha256=sha((ROOT/'code/framing_templates.py').read_bytes())))
  if isinstance(t,dict):
   if 'object' in t:
    for k,v in t['object'].items():
     p=path+('/*' if k=='@additional' else '/'+k);g='additional key not among mandatory fields' if k=='@additional' else optional.get(record,{}).get(k,'present');walk(record,p,v,rid,source,g,'guarded; absent is inapplicable only under inverse guard' if g!='present' else 'required')
     walk(record,p+'#key',S,rid,source,g)
   for kind in ['array','directory']:
    if kind in t:
     walk(record,path+'/*',t[kind],rid,source,'each retained member; lifetime multiplicity unresolved' if kind=='directory' else 'each admitted array position')
     walk(record,path+'/*#key',S if kind=='directory' else I,rid,source,'member exists')
   if 'tuple' in t:
    for i,v in enumerate(t['tuple']):walk(record,path+'/'+str(i),v,rid,source,'fixed index '+str(i))
   if 'union' in t:
    for i,v in enumerate(t['union']):walk(record,path+'/@union/'+str(i),v,rid,source,'exact type alternative '+str(i))
   if 'variants' in t:
    for name,v in t['variants'].items():walk(record,path+'/@variant/'+name,v,rid,source,t['choice_by']+' == '+name)
   if 'request_method_choice' in t:
    for name,v in t['request_method_choice'].items():walk(record,path+'/@method/'+name,v,rid,source,'authenticated request.method == '+name)
 for n,fields in groups.items():walk(n,'',fields['@value'] if n=='JSON-VALUE' else {'object':fields},None,'reference/'+owners[n])
 ids={x['id'] for x in rows};need(len(ids)==len(rows),'DUPLICATE-TEMPLATE');need(all(x['parent'] is None or x['parent'] in ids for x in rows),'PARENT')
 # Ref links prepare both contexts without constructing either complete model.
 def refs(x):
  if not isinstance(x,dict):return
  if set(x)=={'ref'}:yield x['ref'];return
  for key in ['object','variants','request_method_choice']:
   for v in x.get(key,{}).values():yield from refs(v)
  for key in ['union','tuple']:
   for v in x.get(key,[]):yield from refs(v)
  for key in ['array','directory']:
   if key in x:yield from refs(x[key])
 for row in rows:
  for n in refs(row['type']):need(n in groups,'MISSING-TYPE-REF:'+n)
 coverage=constructor_coverage(groups)
 response_coverage=check_rows(rows,response_obligations)
 return {'source_response_obligations':response_obligations,'source_response_coverage':response_coverage,'source_constructor_coverage':coverage,'format':'I164-STATIC-TEMPLATES-1','templates':rows,'constructor_guard_inventory':inv,'context_slots':[{'slot':i,'identity':n,'status':'HISTORICAL-IDENTITY-ONLY; CURRENT-BINDING-UNAVAILABLE','source':'reference/inherited-catalog.py','source_sha256':sha((ROOT/'reference/inherited-catalog.py').read_bytes())} for i,n in enumerate(['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])],'lifetime_multiplicity':'UNRESOLVED','canonical_registration':False,'actual_admission':False}
def validate(bundle):same(bundle,build(),'SOURCE-SELECTOR-COVERAGE');return bundle
if __name__=='__main__':
 b=build();(ROOT/'declarations/static.json').write_bytes(enc(b));print(len(b['templates']),len(b['constructor_guard_inventory']))

def variant_key(t,value,parent):
 # Variant names are schema strings (including the established boolean labels).
 # An unsuitable/missing discriminator rejects this alternative, so an ordered
 # union can try its declared fallback. Never coerce arbitrary JSON values.
 source=value if type(value) is dict and t['choice_by'] in value else parent
 need(type(source) is dict and t['choice_by'] in source,'VARIANT-CONTEXT')
 key=source[t['choice_by']]
 key=str(key).lower() if type(key) is bool else key
 need(type(key) is str and key in t['variants'],'VARIANT')
 return key

def validate_value(record,value,method=None,_schemas=None):
 groups,owners,optional=schemas() if _schemas is None else _schemas
 def value_at(t,v,parent,record,depth=0):
  need(depth<1000,'DECLARATION-DEPTH-LOCAL-CEILING')
  if isinstance(t,str):
   types={'STRING':str,'INTEGER':int,'BOOLEAN':bool,'NULL':type(None),'NUMBER':float};need(type(v) is types[t],'EXACT-TYPE:'+record);return
  if 'wire_type' in t:value_at(t['wire_type'],v,parent,record,depth+1);return
  if set(t)=={'ref'}:
   n=t['ref']
   if n=='JSON-VALUE':value_at(groups[n]['@value'],v,parent,n,depth+1)
   else:value_at({'object':groups[n]},v,v,n,depth+1)
   return
  if 'union' in t:
   for alt in t['union']:
    try:value_at(alt,v,parent,record,depth+1);return
    except Invalid:pass
   raise Invalid('UNION:'+record)
  if 'variants' in t:
   key=variant_key(t,v,parent);value_at(t['variants'][key],v,parent,record,depth+1);return
  if 'request_method_choice' in t:
   need(type(method) is str and method in t['request_method_choice'],'REQUEST-METHOD-CONTEXT');value_at(t['request_method_choice'][method],v,parent,record,depth+1);return
  if 'object' in t:
   need(type(v) is dict,'OBJECT:'+record);fields=t['object'];opts=optional.get(record,{})
   need(set(fields)-set(opts)-{'@additional'}<=set(v),'MISSING-FIELD:'+record);need('@additional' in fields or set(v)<=set(fields),'EXTRA-FIELD:'+record)
   if record=='PENDING':need(('result' in v)==(v['phase']=='FAILED-FROZEN'),'PENDING-VARIANT')
   for k,x in v.items():value_at(fields[k] if k in fields else fields['@additional'],x,v,record,depth+1)
   return
  if 'directory' in t:
   need(type(v) is dict and all(type(k) is str for k in v),'DIRECTORY')
   for x in v.values():value_at(t['directory'],x,v,record,depth+1)
   return
  if 'array' in t:
   need(type(v) is list,'ARRAY')
   for x in v:value_at(t['array'],x,parent,record,depth+1)
   return
  if 'tuple' in t:
   need(type(v) is list and len(v)==len(t['tuple']),'TUPLE')
   for tt,x in zip(t['tuple'],v):value_at(tt,x,parent,record,depth+1)
   return
  raise Invalid('UNKNOWN-TYPE-DECLARATION')
 value_at(ref(record),value,value,record)

def validate_export_templates(export,bundle):
 validate(bundle)
 from ingest import validate_export
 v=validate_export(export);packets={sha(enc(o)):o for k,o in v['objects'] if k=='PACKET'};checked=[]
 compiled=schemas();groups=compiled[0];refused=set()
 for _,packet,response in export['journal']:
  req=parse(hexbytes(packet))['request']
  if response is None or parse(hexbytes(response))['response']['ok'] is False:refused.add((req['method'],sha(enc(req['body']))))
 for k,o in v['objects']:
  name=k;value=o;method=None
  if k in ['U-ENTRY','TRANSPORT-ENTRY']:value=o['value']
  if k.startswith('ABI-ARGUMENTS-'):name='ABI-'+k[len('ABI-ARGUMENTS-'):]
  if k=='RESPONSE':method=packets[o['response']['request']]['request']['method']
  if k=='RELEASE-RESULT' and 'attempt' in o:name='RETRY-RELEASE-RESULT'
  if k.startswith('BODY-') and (k[5:],sha(enc(o))) in refused:name='UNVALIDATED-BODY'
  if name in groups:validate_value(name,value,method,compiled);checked.append(name)
 return {'typed_records_checked':len(checked),'families':sorted(set(checked)),'supporting_only':True,'canonical_registration':False,'actual_admission':False}
