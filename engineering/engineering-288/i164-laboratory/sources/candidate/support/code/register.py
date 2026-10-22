"""Append-only supporting field/register ingestion; never canonical registration."""
import csv,json
from common import *

BLOCKERS=[
 'LATEST-CANONICAL-REGISTER-DELTA-HEAD-NOT-AUTHORITATIVELY-PINNED',
 'SOURCE-QUALIFIED-SEVEN-ROLE-VISIBILITY-CUSTODY-UNAVAILABLE',
 'ACTUAL-PHASE-PRODUCER-APPOINTMENT-AND-QUALIFICATION-UNAVAILABLE',
 'PROTECTED-LIFETIME-COUNTERS-AND-COMPLETE-SHARED-LEDGER-COVERAGE-UNESTABLISHED',
 'FINITE-LIFETIME-RECOVERY-ACQUISITION-DIAGNOSTIC-DIRECTORY-UNESTABLISHED',
 'EXTERNAL-EVIDENCE-SIZE-TRUTH-AND-FINALITY-UNESTABLISHED',
 'COMPLETE-MODEL-LEDGER-REBINDING-AND-CHANGED-STREAM-IDENTITIES-UNCOMPUTED']

# These hooks describe checked record families, not qualified source classifications.
HOOKS={
 'CONFIG':'config_binding','BINDING':'config_binding','HEAD':'Fold.advance + validate_export final history',
 'COUNTS':'Fold.reserve/query/observe exact after-state','PARTITIONS':'Fold.reserve/query/backup exact after-state',
 'RESOURCES':'Fold.reserve/query/observe exact after-state','U-ENTRY':'Fold retire/open + intent',
 'STAGE':'Fold open and complete guarded fold','TRANSPORT-ENTRY':'Fold.add_attempt/query/observe',
 'RETRY-ID-ENTRY':'Fold retry-release','PENDING':'Fold all pending guards','LAST':'Fold observe',
 'BACKUP-ENTRY':'Fold backup','ATTEMPT':'Fold.add_attempt','ACTION':'Fold decide/template',
 'TEMPLATE':'Fold.template + signed_eth.validate','QUERY':'Fold query/observe','OBSERVATION':'Fold observe',
 'EVENT':'Fold.advance exact canonical event','JOURNAL':'validate_export journal','REQUEST':'validate_export request + Fold method bodies',
 'RESPONSE':'validate_export response','OWNERSHIP-META':'config_binding','OWNERSHIP-ROW':'validate_export ownership + Fold.claim',
 'UNSIGNED-INTENT':'intent + retained ABI','COMPACT-INTENT':'intent compact + retained ABI','STAGE-META':'Fold open',
 'BLOB-STORE':'Fold.get and full owned blob-set equality','SIGNED-RESULT':'validate_export sign response',
 'RELEASE-RESULT':'validate_export release response','PACKET':'validate_export packet'}

def build_register():
 pinned_sources();spec=json.loads((ROOT/'reference/SCHEMA-SPEC.json').read_text());rows=list(csv.DictReader((ROOT/'reference/FIELD-CORRESPONDENCE.csv').open()))
 need(len(rows)==424 and len(spec['groups'])==41,'SPEC-COVERAGE-COUNT');groups={g['record']:g for g in spec['groups']};need(len(groups)==41,'SCHEMA-DUPLICATE');fields=[]
 for g in groups:
  need(g in HOOKS or (g.startswith('BODY-') and g[5:] in spec['request_bodies']),'MISSING-VALIDATOR-HOOK')
 for r in rows:
  source='reference/runtime/'+Path(r['source_file']).name;need(sha((ROOT/source).read_bytes())==r['source_sha256'],'DECLARATION-SOURCE')
  fields.append({'node_id':'I164:PROSPECTIVE-RETRY3-'+r['record']+'.F'+sha(r['selector'].encode())[:24], 'spec_class':r['spec_class'],'record':r['record'],'selector':r['selector'],'source_file':source,'source_sha256':r['source_sha256'],'source_anchor':r['source_anchor'],'validation_hook':HOOKS.get(r['record'],'Fold exact method body + validate_export successful response'),'visibility':'UNKNOWN','custody':['UNKNOWN']*7,'qualification':'UNAVAILABLE','phase':'UNAVAILABLE','canonical':False})
 for row in fields:
  if row['record']=='RESPONSE':
   sel=row['selector'];row['projection_pointer']=('/signature' if sel=='signature' else '/response/'+sel if sel in ['request','challenge','ok','data','error'] else '')
   row['projection_guard']=('response.ok=true' if sel=='data' else 'response.ok=false' if sel=='error' else 'saved signed envelope present')
 need(len({r['node_id'] for r in fields})==len(fields),'CLASS-COLLISION')
 for name,g in groups.items():
  expected=set(g['fields'])|{'$record','@presence','@availability','@encoding_length','@member_count'}
  need({r['selector'] for r in fields if r['record']==name}==expected,'FIELD-COVERAGE:'+name)
 # Existing authoritative byte identities are preserved; no presumed semantic equivalence.
 old=json.loads((ROOT/'reference/added-fields.json').read_text());oldids={r['node_id'] for r in old};need(not oldids&{r['node_id'] for r in fields},'EXISTING-CLASS-CONFLICT')
 rel=json.loads((ROOT/'reference/relationships-43.json').read_text());need(len(rel)==43,'INHERITED-RELATIONSHIPS')
 return {'format':'I164-RETRY3-SUPPORTING-REGISTER-1','fields':fields,'relationships_43_sha256':sha((ROOT/'reference/relationships-43.json').read_bytes()),'baseline_profile_sha256':sha((ROOT/'reference/profile-binding.json').read_bytes()),'baseline_status':'PINNED-HISTORICAL-INPUT-NOT-CURRENT-CANONICAL-CLAIM','canonical_registration':False,'blockers':BLOCKERS,'actual_admission':False}

def validate_register(reg):
 # Exact rebuild from pinned approved spec prevents forged completeness/classification status.
 same(reg,build_register(),'REGISTER-SUBSTITUTION');return reg

def reconcile(reg,existing,expected_digest):
 """Optional supplied baseline ingestion with exact bytes. No canonical write/status grant."""
 validate_register(reg);digest(expected_digest);need(sha(existing)==expected_digest,'BASELINE-IDENTITY')
 rows=parse(existing,50000000);need(type(rows) is list,'BASELINE-LIST');seen={}
 for r in rows:
  need(type(r) is dict and type(r.get('node_id')) is str,'BASELINE-ROW');need(r['node_id'] not in seen,'BASELINE-DUPLICATE');seen[r['node_id']]=r
 conflicts=[]
 for r in reg['fields']:
  if r['node_id'] in seen and enc(r)!=enc(seen[r['node_id']]):conflicts.append(r['node_id'])
 need(not conflicts,'BASELINE-CONFLICT')
 return {'baseline_sha256':expected_digest,'existing_rows':len(rows),'new_supporting_rows':sum(r['node_id'] not in seen for r in reg['fields']),'canonical_registration':False,'blockers':BLOCKERS}

def project(value,record,occurrence):
 """Complete nested occurrence walk; no opaque scalar hash replacement.
 Every container/key/index/null/value and exact representation gets a row.
 This is an actual supporting occurrence directory, not a STATIC model expansion.
 """
 out=[]
 def visit(v,path,parent):
  typ={dict:'OBJECT',list:'ARRAY',str:'STRING',int:'INTEGER',bool:'BOOLEAN',type(None):'NULL',float:'NUMBER'}.get(type(v));need(typ is not None,'PROJECTION-TYPE');raw=enc(v);rid=sha(enc([record,occurrence,path]));row={'id':rid,'record':record,'occurrence':occurrence,'pointer':path,'parent':parent,'type':typ,'exact_bytes_hex':raw.hex(),'encoding_length':len(raw),'presence':True,'visibility':'UNKNOWN','qualification':'UNAVAILABLE','canonical':False}
  if type(v) in [dict,list]:row['member_count']=len(v)
  out.append(row)
  if type(v) is dict:
   for k,x in sorted(v.items()):
    # Directory keys themselves are exposed, separately from the values they select.
    kp=path+'/~key/'+k.replace('~','~0').replace('/','~1');kid=visit(k,kp,rid)
    visit(x,path+'/'+k.replace('~','~0').replace('/','~1'),kid)
  elif type(v) is list:
   for i,x in enumerate(v):visit(x,path+'/'+str(i),rid)
  return rid
 visit(value,'',None);return out

def final_binding(reg,claims=None):
 validate_register(reg)
 # This bounded adapter has no authority to discharge these outside obligations.
 # Even caller-supplied true flags cannot grant final admission.
 raise Invalid('FINAL-BINDING-BLOCKED:'+','.join(BLOCKERS))


def validate_response_projection(objects,rows,links,reg):
 """Bind real emitted envelope occurrences to source selectors and authenticated journal.
 No missing response is turned into an envelope; no opaque raw hex substitutes for parsing.
 """
 from correspondence import verify_signature
 validate_register(reg)
 packets={sha(enc(obj)):obj for kind,obj in objects if kind=='PACKET'}
 journals={obj['challenge']:obj for kind,obj in objects if kind=='JOURNAL'}
 expected_indices=[i for i,(kind,obj) in enumerate(objects) if kind=='RESPONSE']
 need([x['occurrence'] for x in links]==expected_indices,'ENVELOPE-COVERAGE')
 response_rows=[x for x in rows if x['record']=='RESPONSE']
 need(len(response_rows)==sum(len(project(objects[i][1],'RESPONSE',i)) for i in expected_indices),'ENVELOPE-ROW-COVERAGE')
 coverage=[]
 for link in links:
  keys(link,'occurrence request_hash packet_hash challenge');integer(link['occurrence']);i=link['occurrence'];z=objects[i][1];keys(z,'response signature');res=z['response'];boolean(res.get('ok'));keys(res,'request challenge ok '+('data' if res['ok'] else 'error'));verify_signature('server',res,z['signature'])
  need(link['packet_hash'] in packets and link['challenge'] in journals,'ENVELOPE-JOIN')
  packet=packets[link['packet_hash']];journal=journals[link['challenge']]
  need(sha(enc(packet['request']))==link['request_hash'] and packet['request']['challenge']==link['challenge'],'ENVELOPE-REQUEST')
  need(res['request']==link['packet_hash'] and res['challenge']==link['challenge'],'ENVELOPE-RESPONSE')
  need(hexbytes(journal['request_hex'])==enc(packet) and journal['response_hex'] is not None and hexbytes(journal['response_hex'])==enc(z),'ENVELOPE-JOURNAL-BYTES')
  actual=[x for x in response_rows if x['occurrence']==i];same(actual,project(z,'RESPONSE',i),'ENVELOPE-EXACT-PROJECTION')
  pointers={x['pointer']:x for x in actual};present=['request','challenge','ok','signature','data' if res['ok'] else 'error']
  for field in present:
   definition=next(x for x in reg['fields'] if x['record']=='RESPONSE' and x['selector']==field);path=definition['projection_pointer'];need(path in pointers,'ENVELOPE-SELECTOR')
   coverage.append({'spec_class':definition['spec_class'],'node_id':definition['node_id'],'occurrence_id':pointers[path]['id'],'envelope_occurrence_id':pointers['']['id'],'pointer':path,'request_hash':link['request_hash'],'packet_hash':link['packet_hash'],'challenge':link['challenge'],'canonical':False})
 return coverage
