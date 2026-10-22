"""Independent byte/identity/class/declaration audit. No candidate runtime execution."""
import ast,collections,csv,gzip,hashlib,io,json,pathlib,sys,time,zipfile
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]);checks=[];started=time.monotonic()
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def read(p):return (root/p).read_bytes()
def load(p):return json.loads(read(p))
def identity(p):b=read(p);return {'bytes':len(b),'sha256':sha(b)}
def check(n,f):
 r=f();checks.append({'name':n,'status':'PASS','detail':r});out.write_text(json.dumps({'checks':checks,'seconds':time.monotonic()-started},indent=2)+'\n')
def inheritance():
 x=load('provenance/inheritance.json');hist=load('provenance/historical-archive-MANIFEST.json')['files'];assert len(x['members'])==51
 for p,v in x['members'].items():assert v==hist[p]==identity('native/'+p),p
 assert load('candidate/inheritance.json')==x
 pins=load('provenance/input-pins.json');assert sha(read('provenance/input-pins.json'))=='a1dd7d9b5fc0c4731b77be609acccd2e169490df9073adb3b393f9c30a4d2fc6'
 for p,v in pins.items():assert v=={'path':p,**identity(p)},p
 h=load('provenance/historical90.json')['files'];assert len(h)==90;old=load('support/provenance/historical-hashes.json')['files']
 for v in h:assert identity('historical90/'+v['path'])=={'bytes':v['bytes'],'sha256':v['sha256']} and old[v['path']]==v['sha256']
 rel=read('native/retained/mapping/records/relationships-43.json');assert len(json.loads(rel))==43 and rel==read('support/reference/relationships-43.json') and sha(rel)=='761772d3372c13cce1c61a551154534cc7d23ea32fc97a18db0794bbfdd27591'
 m=load('support/MANIFEST.json');paths={str(p.relative_to(root/'support')) for p in (root/'support').rglob('*') if p.is_file()};assert paths==set(m)|{'MANIFEST.json'}
 for p,v in m.items():assert identity('support/'+p)==v,p
 return {'native_members_verified':51,'input_pins_verified':len(pins),'historical_files':90,'relationships':43,'support_manifest_files':len(m),'predecessor_archive':x['archive'],'limit':'Whole 261512053-byte predecessor archive not supplied; selected members and retained manifest freshly verified. Its whole-archive digest remains inherited retrieval evidence.'}
check('inheritance-pins-and-preservation',inheritance)
ns=load('candidate/namespace.json');historical=ns['historical_classes'];proposed=ns['prospective_classes']
a=load('native/retained/registers/fields.json');b=load('native/records/added-fields.json');native=a+b

def census():
 def tsv(p):return list(csv.DictReader(read('native/sources/'+p).decode().splitlines(),delimiter='\t'))
 nodes=tsv('producer/augmented-nodes.tsv');sf=tsv('definition-completion/security-fields.tsv');ff=tsv('definition-completion/security-framing-fields.tsv')
 tree=ast.parse(read('native/prior-code/model_kernel/catalog.py'));constants={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
 pieces={'inherited_producer_nodes':[r['node_id'] for r in nodes],'security_fields':[r['surface_id'] for r in sf],'security_records':['SECURITY:'+s+'.$record' for s in sorted({r['schema'] for r in sf})],'security_framing':[r['surface_id'] for r in ff],'custodian_roles':['CP2-CUSTODIAN:'+s for s in constants['ROLES']],'parsed_source_refs':['CP2-REF-PARSER:'+r['schema']+'.'+r['field']+'.'+p for r in sf if r['type'] in ['SOURCE-REF','LIST-SOURCE-REF'] for p in constants['REF_PARTS']],'record_parser':['CP2-RECORD-PARSER:'+p for p in constants['PARSER_FIELDS']],'reference_material':['CP2-REFERENCE-MATERIAL:'+p for p in constants['MATERIAL_FIELDS']]}
 base=[v for part in pieces.values() for v in part];assert len(base)==len(set(base))==4119
 assert base==load('native/sources/selected-contract.json')['field_label_surfaces']
 fld=[x['node_id'] for x in native];assert len(fld)==len(set(fld))==40924
 ledger=[json.loads(s) for s in gzip.decompress(read('native/candidate/ledger/node-duties.jsonl.gz')).splitlines()];ids=[r['field_class'] for r in ledger]
 assert ids==historical and len(ids)==len(set(ids))==45043
 assert set(ids)==set(base)|set(fld) and not set(base)&set(fld)
 assert ids==load('native/records/expanded-contract.json')['field_label_surfaces']
 assert len(ids)==load('native/records/candidate-delta.json')['counts']['surfaces'][1]
 assert not set(ids)&set(proposed) and len(set(proposed))==9339
 overlay=load('native/records/surface-delta.json');assert len(overlay)==32
 for d in overlay:
  assert d['old']['node_id']==d['new']['node_id'] and {k for k in d['old'] if d['old'][k]!=d['new'][k]}=={'owner_anchor'}
  assert ids[d['ordinal']]==d['new']['node_id'],d['ordinal']
 return {'retained_fields':len(a),'added_fields':len(b),'field_union':len(fld),'additional_base_classes':{k:len(v) for k,v in pieces.items()},'historical_classes':len(ids),'prospective_classes':len(proposed),'combined':len(ids)+len(proposed),'surface_overlay_rows':32,'extra_class_example':base[0]}
check('independent-45043-class-census-and-32-anchor-overlay',census)

def mapping():
 m=load('candidate/native-mapping.json');assert len(m['fields'])==len(native)
 sources={(x['native_reference'],x['sha256']):x['verified_archive_member'] for x in load('provenance/native-sources.json')};assert len(sources)==10
 assert m['source_resolution']==load('provenance/native-sources.json')
 for i,(mapped,row) in enumerate(zip(m['fields'],native)):
  origin='native/retained/registers/fields.json' if i<len(a) else 'native/records/added-fields.json';ix=i if i<len(a) else i-len(a)
  assert enc(mapped)==enc({'id':row['node_id'],'native':row,'origin':{'path':origin,'pointer':'/'+str(ix)}})
  path=sources[(row['source_file'],row['source_sha256'])];assert sha(read('native/'+path))==row['source_sha256']
 for d in m['exact_native_containers']:assert {'path':d['path'],**identity(d['path'])}==d
 assert m['canonical_schema'] is False
 return {'rows_roundtripped':len(native),'source_resolutions':10,'exact_native_containers':len(m['exact_native_containers']),'native_byte_identity':'verified separately against inheritance manifest'}
check('lossless-native-map-and-source-resolution',mapping)
fields=load('candidate/fields.json')['prospective'];by={r['template_id']:r for r in fields};bundle=load('support/declarations/static.json')
def declarations():
 assert len(fields)==len(by)==9339 and proposed==[x['id'] for x in fields]
 source_hashes={}
 for f,t in zip(fields,bundle['templates']):
  assert f['native_template']==t and f['template_id']==t['id'] and f['id']=='I164:PROSPECTIVE-META1.F'+sha(t['id'].encode())
  assert f['parent']==(by[t['parent']]['id'] if t['parent'] else None)
  assert f['identity_status']=='PROPOSED-CANDIDATE-ONLY' and t['canonical'] is False
  assert t['visibility']==t['dependency_classification']=='UNKNOWN' and t['custody']==['UNKNOWN']*7
  assert t['id']==t['record']+':'+t['selector']
  p='support/'+t['source']
  if p not in source_hashes:source_hashes[p]=sha(read(p))
  assert source_hashes[p]==t['source_sha256']
 s=load('candidate/schemas.json');forms=load('candidate/source-forms.json')['prospective'];assert len(s['prospective'])==len(forms)==59
 for record in s['prospective']:
  group=[f['id'] for f in fields if f['native_template']['record']==record]
  assert group==s['field_membership'][record]
  form=next(x for x in forms if x['record']==record);assert form['shape']==s['prospective'][record] and form['field_classes']==group
 for f in fields:assert s['guards'][f['template_id']]==f['native_template']['guard']
 # Independently derive two ABI shapes and stage parser key set from defining sources.
 abi=load('support/reference/contract/ABI.json')
 def typ(f):
  import re
  t=f['type'];m=re.fullmatch(r'(.*)\[(\d+)\]',t)
  if m:return {'tuple':[typ(dict(f,type=m[1])) for _ in range(int(m[2]))]}
  if t=='tuple':return {'object':{x['name']:typ(x) for x in f['components']}}
  assert t in ['uint256','bytes32','bytes'];return {'wire_type':'INTEGER' if t=='uint256' else 'STRING','abi_type':t}
 for method in ['signPetition','signPetitionWithZKProof']:
  fn=next(x for x in abi if x.get('name')==method and x['type']=='function');assert s['prospective']['ABI-'+method]=={x['name']:typ(x) for x in fn['inputs']}
 st=ast.parse(read('support/reference/retained/stage_carrier.py'));keys=next(ast.literal_eval(n.value) for n in st.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='KEYS' for x in n.targets))
 assert set(s['prospective']['STAGED-BINDINGS'])==set(keys)
 return {'rows':len(fields),'families':len(forms),'source_hashes':source_hashes,'fresh_additional_source_shapes':['both ABI methods','stage parser KEYS'],'coverage_limit':'Identity/mapping fidelity for all rows; independently derived completeness only within prior pinned SD-01 response domain plus explicitly checked ABI/stage shapes. No universal 59-family completeness claim.'}
check('9339-proposed-field-bindings-and-selected-source-shapes',declarations)

def cross_artifacts():
 prof=load('candidate/profile-binding.json');ident=load('candidate/identity.json')
 for n,v in ident['artifacts'].items():assert identity('candidate/'+n)==v,n
 for n,v in prof['metadata'].items():assert identity('candidate/'+n)==v,n
 assert ident['construction_code']=={'path':'tools/baseline.py',**identity('tools/baseline.py')}
 assert ident['input_pin_sha256']==sha(read('provenance/input-pins.json'))
 for d in prof['runtime']+prof['adapters']+prof['adopted_basis']+[prof['historical_profile']]:assert d=={'path':d['path'],**identity(d['path'])}
 ctx=load('candidate/contexts.json');assert [x['context'] for x in ctx['associations']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
 for x in ctx['associations']:assert x['class_directory']=='fields.json#/prospective' and x['canonical'] is False and x['status']=='NEW-CANDIDATE-ASSOCIATION'
 assert ctx['full_expansion'] is False and ctx['no_equivalence_between_contexts_inferred'] is True
 for d in ctx['historical_definitions']:assert d=={'path':d['path'],**identity(d['path'])}
 assert prof['canonical_registration'] is False and prof['actual_admission'] is False and prof['complete_model_binding'] is False
 return {'identity_artifacts':len(ident['artifacts']),'profile_metadata_artifacts':len(prof['metadata']),'runtime':len(prof['runtime']),'adapters':len(prof['adapters']),'contexts':2}
check('profile-context-and-exact-artifact-bindings',cross_artifacts)

def associations():
 assoc=load('candidate/associations.json');assert len(assoc['prospective'])==12
 for r in assoc['prospective']:
  d=r['source'];assert d=={'path':d['path'],**identity(d['path'])}
  nodes=ast.parse(read(d['path']))
  for anc in r['anchors']:assert any(isinstance(n,ast.FunctionDef) and n.name==anc['function'] and (n.lineno,n.end_lineno)==(anc['first_line'],anc['last_line']) for n in ast.walk(nodes))
  for e in r['endpoints']:assert by[e['template']]['id']==e['class']
  assert r['qualified_dependency']==r['visibility']=='UNKNOWN' and r['custody']==['UNKNOWN']*7
 duties=load('candidate/ledger-duties.json');assert len(duties['prospective_duties'])==12 and duties['full_ledger_bound'] is False
 assert {x['association'] for x in duties['prospective_duties']}=={x['id'] for x in assoc['prospective']}
 for x in duties['prospective_duties']:assert x['qualified_assessor'] is None and x['status'].startswith('METADATA-DECLARED')
 dirs=load('candidate/directories.json');status=load('candidate/status.json');prof=load('candidate/profile-binding.json')
 assert dirs['lifetime_acquisition_recovery_diagnostics']['bound'] is None and dirs['physical_storage']['bound'] is None and dirs['external_evidence']['bound'] is None
 assert 'final-binding' in dirs['lifetime_acquisition_recovery_diagnostics']['blocks']
 assert status['blockers']==prof['blockers']==duties['classification_duties'] and len(status['blockers'])==7
 assert status['canonical_registration']=='NOT-OCCURRED' and status['canonical_head'] is None and status['stream_identities']=='UNCOMPUTED' and status['actual_admission'] is False
 assert status['qualification'] is False and status['complete_immutable_model_binding'] is False
 return {'association_anchors_and_endpoints':12,'declared_ledger_duties':12,'blockers':status['blockers'],'limits':{k:v['max'] for k,v in dirs['local'].items()},'distinction':'anchor/endpoints mechanically checked; guard meaning assessed by source inspection; no qualified edge/observer classification'}
check('associations-ledger-and-propagated-blockers',associations)

def saved_evidence():
 r=load('results/focused.json');assert r['count']==len(r['fresh_checks'])==58 and all(x['status']=='PASS' for x in r['fresh_checks']) and len(r['saved_examples'])==12
 details=[]
 for x in r['saved_examples']:
  p='results/examples/'+x['name']+'.json';d=load(p);assert sha(read(p))==x['sha256'];assert d['fixture']=={'path':d['fixture']['path'],**identity(d['fixture']['path'])}
  assert d['profile_sha256']==sha(read('candidate/profile-binding.json'))
  fixture=load(d['fixture']['path']);blobs={ref:bytes.fromhex(raw) for ref,raw in fixture['blobs']}
  for key,klass in [('attempt_occurrences','ATTEMPT:'),('action_occurrences','ACTION:')]:
   for row in d[key]:
    raw=bytes.fromhex(row['exact_bytes_hex']);assert sha(raw)==row['reference'] and raw==blobs[row['reference']] and enc(row['parsed'])==raw and row['class']==by[klass]['id']
  for row in d['response_signature_joins']:assert row['candidate_class']==by['RESPONSE:/signature']['id']
  assert d['saved_evidence_only'] is True and d['new_lifecycle_executions']==0 and d['canonical_registration'] is False
  details.append({'name':x['name'],'actions':len(d['action_occurrences']),'attempts':len(d['attempt_occurrences']),'signature_joins':len(d['response_signature_joins']),'status':'supplied check PASS inspected; associations freshly compared to saved bytes, no lifecycle'})
 failure_members=[p for p in load('MANIFEST.json') if p.startswith('results/failures/')];assert len(failure_members)==6
 return {'recorded_checks':58,'saved_examples':details,'two_development_failures':{p:identity(p) for p in failure_members}}
check('58-supplied-checks-and-12-saved-export-association-records',saved_evidence)
print(json.dumps({'audit_groups':len(checks),'status':'PASS','seconds':time.monotonic()-started}))
