"""Current bound static metadata for MR-LAYOUT-01; no instance/stream expansion.
Retained predecessor compiler/procedure outputs are construction inputs to the
managed integration. Current derived outputs live separately to avoid recursive
content identities (a binding must not hash an artifact containing itself).
"""
import json,sys,copy,hashlib,io,zipfile,stat
from pathlib import Path
import semantic as s
import prospective_procedure as p
PATHS={'directory':'layout_outputs/directory.json','rules':'layout_outputs/rules.json','procedure':'layout_outputs/procedure.json'}
def derive(root):
 c=s.setup(Path(root));d=s.m.compile_candidate(c);r=s.compile_rules(c);v=p.count_only(d,r)
 return {'directory':d,'rules':r,'procedure':v}
def validate(root,values):
 # Reuse current authoritative derivation, including exact binding, rules,
 # guard/schema coverage and count/duty checks. No prior-success cache.
 expected=derive(root);s.m.same(values,expected,'LAYOUT-CONSUMER-SUBSTITUTION')
 return {'current_candidate_binding':expected['directory']['candidate_binding'],'metadata_counts':s.m.count_only(expected['directory'],s.setup(root)),'semantic_rule_count':len(expected['rules']['rules']),'procedure_duties':len(expected['procedure']['relation_duties']),'final_binding':'BLOCKED','actual_admission':False,'streams':'UNCOMPUTED'}
def main():
 root=Path(sys.argv[1]).resolve()
 if sys.argv[2]=='build':
  for key,value in derive(root).items():
   dest=root/PATHS[key];assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(s.m.enc(value))
  print('PASS current static directory/rule/procedure bindings; no full expansion')
 elif sys.argv[2]=='check':
  out=validate(root,{k:json.loads((root/v).read_bytes()) for k,v in PATHS.items()});print(json.dumps(out,indent=2))
 else:raise SystemExit('ROOT build|check')

# Current bounded preflight joins existing validators; no alternate fold/binder.
CURRENT_PINMAP={'bytes': 105378, 'sha256': 'dbc5b264232b5b3dc380712949dbe3506ee1e5c3a110106c056c593e38c26788'}
OBSERVATION_ORIGINS={'SYMBOLIC-U-ONE': {'kind': 'RETAINED-SAVED-EXECUTION', 'capture_archive_sha256': 'c1ecf45f8f0c0cc7b57c5549f3c2017443ddd68e245bf9bcfbed4f1ad4821712', 'capture_member': 'evidence/combined-ord.json', 'receipt_review_sha256': '320485ed017f5d39bd38ace5c1c4b09402425a8d3329b867054083039c280767', 'receipt_member': 'results/receipt-combined-ord.json', 'new_producer_execution': False}, 'SYMBOLIC-U-TWO': {'kind': 'RETAINED-SAVED-EXECUTION', 'capture_archive_sha256': 'c1ecf45f8f0c0cc7b57c5549f3c2017443ddd68e245bf9bcfbed4f1ad4821712', 'capture_member': 'evidence/combined-zk.json', 'receipt_review_sha256': '320485ed017f5d39bd38ace5c1c4b09402425a8d3329b867054083039c280767', 'receipt_member': 'results/receipt-combined-zk.json', 'new_producer_execution': False}}
CURRENT_FORMAT='I164-CURRENT-BOUNDED-INTEGRATION-1'
ACCEPTED_CONSUMER={'bytes':35124,'sha256':'2b4ccd7902d8e270ac8d4b22060d08d184dda1b0e6fcdccae781fd81eef902cc'}
# Immutable domain; ordering is read from the exact pinned candidate definition.
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
def current_contexts(root):
 import managed_coverage as mc
 declared=[v['context'] for v in mc.load(Path(root),'candidate/contexts.json')['associations']]
 mc.same(declared,list(CONTEXTS),'CURRENT-CONTEXT-DEFINITION')
 return declared

def historical_members(base):
 """Verify actual archives, then read exact member bytes; no capture allowlist.
 Archive filenames are SHA256.zip under evidence_root/archives. The bytes are
 external recovery inputs, not candidate authority or a new capture attestation.
 """
 import managed_coverage as mc
 from pathlib import PurePosixPath
 archives={}
 for sha in {v[k] for v in OBSERVATION_ORIGINS.values() for k in ('capture_archive_sha256','receipt_review_sha256')}:
  path=Path(base)/'archives'/(sha+'.zip')
  mc.need(path.is_file(),'MISSING-HISTORICAL-ARCHIVE')
  raw=path.read_bytes();mc.need(hashlib.sha256(raw).hexdigest()==sha,'HISTORICAL-ARCHIVE-IDENTITY')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   names=z.namelist();mc.need(len(names)==len(set(names)),'HISTORICAL-DUPLICATE-MEMBER')
   for info in z.infolist():
    n=PurePosixPath(info.filename)
    mc.need(not info.is_dir() and not n.is_absolute() and '..' not in n.parts and not stat.S_ISLNK(info.external_attr>>16),'HISTORICAL-UNSAFE-MEMBER')
   mc.need(z.testzip() is None,'HISTORICAL-CRC')
   manifest=json.loads(z.read('MANIFEST.json'));mc.need(set(names)==set(manifest)|{'MANIFEST.json'},'HISTORICAL-MEMBERSHIP')
   for name,expected in manifest.items():
    b=z.read(name);mc.same({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},expected,'HISTORICAL-MANIFEST:'+name)
   wanted={v[k] for v in OBSERVATION_ORIGINS.values() for k,a in [('capture_member','capture_archive_sha256'),('receipt_member','receipt_review_sha256')] if v[a]==sha}
   archives[sha]=({'bytes':len(raw),'sha256':sha,'entries':len(names)},{n:z.read(n) for n in wanted})
 return archives

def bind_history(row,raw,archives):
 import managed_coverage as mc
 origin=OBSERVATION_ORIGINS[row['context']]
 provenance=row['provenance'];exact=provenance.get('kind')=='RETAINED-SAVED-EXECUTION'
 expected=origin if exact else {'kind':'NONORIGINAL-OBSERVATION','reference_origin':origin,'new_producer_execution':False}
 mc.same(provenance,expected,'OBSERVATION-PROVENANCE')
 bound={}
 for kind,ak,mk in [('capture','capture_archive_sha256','capture_member'),('receipt','receipt_review_sha256','receipt_member')]:
  archive,members=archives[origin[ak]];member=members[origin[mk]]
  if exact:mc.need(raw[kind]==member,'FALSE-EXACT-HISTORY:'+kind)
  bound[kind]={'archive':archive,'member':origin[mk],
   'member_identity':{'bytes':len(member),'sha256':hashlib.sha256(member).hexdigest()},
   'current_identity':{'bytes':len(raw[kind]),'sha256':hashlib.sha256(raw[kind]).hexdigest()},
   'byte_identical':raw[kind]==member}
 return {'claim':'EXACT-ARCHIVE-MEMBERS' if exact else 'NONORIGINAL; ARCHIVES ARE REFERENCES ONLY',
  'producer_execution_or_derivation_attested':False,'members':bound}

def check_current_inputs(root,inputs,evidence_root):
 import managed_coverage as mc
 root=Path(root).resolve();base=Path(evidence_root).resolve()
 mc.need(type(inputs) is dict and set(inputs)=={'format','root_members','observations'},'CURRENT-INPUT-STRUCTURE')
 mc.need(inputs['format']=='I164-CURRENT-INPUTS-1','CURRENT-INPUT-VERSION')
 pin_id=mc.identity(root,'provenance/layout-runtime-members.json');mc.same({k:pin_id[k] for k in ('bytes','sha256')},CURRENT_PINMAP,'CURRENT-PINMAP')
 pins=mc.load(root,'provenance/layout-runtime-members.json')
 mandatory=set(pins)|set(PATHS.values())|{'compiler/layout_consumers.py','provenance/layout-runtime-members.json'}
 mc.need(set(inputs['root_members'])==mandatory,'CURRENT-MANDATORY-MEMBERSHIP')
 # A submitted manifest does not supply expected producer/adapter identities.
 for name,pin in pins.items():
  ident=mc.identity(root,name);mc.same({k:ident[k] for k in ('bytes','sha256')},pin,'CURRENT-RUNTIME-PIN:'+name)
 ident=mc.identity(root,'compiler/managed_observations.py');mc.same({k:ident[k] for k in ('bytes','sha256')},ACCEPTED_CONSUMER,'ACCEPTED-CONSUMER-PIN')
 for name,expected in inputs['root_members'].items():
  path=root/name;mc.need(not path.is_symlink() and path.resolve().is_relative_to(root),'CURRENT-PATH')
  ident=mc.identity(root,name);mc.same({k:ident[k] for k in ('bytes','sha256')},expected,'CURRENT-MEMBER:'+name)
 contexts=current_contexts(root);archives=historical_members(base)
 rows=inputs['observations'];mc.need(type(rows) is list and len(rows)==2,'CURRENT-OBSERVATION-SET')
 mc.same([v['context'] for v in rows],contexts,'CURRENT-CONTEXT-COVERAGE')
 mc.same(sorted(v['method'] for v in rows),['signPetition','signPetitionWithZKProof'],'CURRENT-METHOD-COVERAGE')
 records=[]
 for row in rows:
  mc.need(set(row)=={'context','method','capture','receipt','provenance'},'CURRENT-OBSERVATION-FIELDS')
  data={};raw={}
  for kind in ['capture','receipt']:
   ident=row[kind];mc.need(set(ident)=={'path','bytes','sha256'},'EVIDENCE-IDENTITY')
   q=Path(ident['path']);mc.need(not q.is_absolute() and '..' not in q.parts,'EVIDENCE-PATH')
   q=base/q;mc.need(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(base),'MISSING-EVIDENCE')
   mc.same(mc.identity(base,ident['path']),ident,'EVIDENCE-IDENTITY:'+kind);raw[kind]=q.read_bytes();data[kind]=json.loads(raw[kind])
  mc.same(data['capture']['context'],row['context'],'OBSERVATION-CONTEXT')
  # Method comes from the authenticated retained intent, not the case label.
  head=json.loads(bytes.fromhex(data['capture']['after']['head']))
  methods={u['intent']['method'] for u in head['u'].values() if type(u.get('intent')) is dict}
  if not methods:
   # Runtime HEAD retains exact immutable intent by blob reference.
   blobs={k:bytes.fromhex(v) for k,v in data['capture']['after']['blobs']}
   methods={json.loads(blobs[u['intent']])['method'] for u in head['u'].values()}
  mc.same(sorted(methods),[row['method']],'OBSERVATION-SIGNING-METHOD')
  data['archival_evidence']=bind_history(row,raw,archives)
  records.append((copy.deepcopy(row),data))
 return records

def validate_current(root,inputs,evidence_root):
 import managed_coverage as mc,managed_observations as mo
 root=Path(root).resolve();records=check_current_inputs(root,inputs,evidence_root)
 values={k:mc.load(root,v) for k,v in PATHS.items()}
 static=validate(root,values) # authoritative existing derivation and count checks
 c=s.setup(root);bundle=mc.read_bundle(root);mc.validate_bundle(root,bundle)
 outputs=[]
 for row,data in records:
  record=data['capture'];context=row['context']
  receipt=mo.validate_receipt(root,bundle,record,data['receipt'],context,root)
  export=record['after']
  occurrence=c.ingest(export,context,c.binding)
  # ingest constructs through the existing current candidate validator; no
  # caller-supplied occurrence or legacy receipt substitutes for this output.
  duty=p.consume(values['procedure'],values['directory'],values['rules'],occurrence,export)
  outputs.append({'capture':row['capture'],'receipt':row['receipt'],'provenance':row['provenance'],'context':context,'method':row['method'],
   'archival_evidence':data['archival_evidence'],'observed_source_identities':record['sources'],'observed_input_identities':record['inputs'],
   'accepted_occurrence_receipt':receipt,'candidate_binding':occurrence['binding'],
   'export_sha256':s.m.sha(s.m.enc(export)),'candidate_occurrence_sha256':s.m.sha(s.m.enc(occurrence)),
   'candidate_occurrences':len(occurrence['candidate_occurrences']),'authenticated_response_associations':len(occurrence['response_associations']),
   'mechanical_duty_result':duty,'candidate_blockers':occurrence['blockers']})
 # Detach the entire public result, including consumer receipt globals and inputs.
 return copy.deepcopy({'format':CURRENT_FORMAT,'scope':'BOUNDED-CURRENT-CANDIDATE-CORRESPONDENCE; NOT FULL MODEL',
  'consumed_inputs':inputs,'manifest_sha256':mc.digest(mc.enc(inputs)),
  'entry_points':['layout_consumers.validate','managed_coverage.validate_bundle','managed_observations.validate_receipt','candidate_pipeline.Candidate.ingest','prospective_procedure.consume'],
  'candidate_binding':c.binding,'contexts':current_contexts(root),'static_validation':static,'observations':outputs,
  'procedure_blockers':values['procedure']['blockers'],'managed_gaps_retained':mc.GAPS,
  'gap_disposition':{'runtime observation adapter for the new managed model records':'BOUNDED ACCEPTED CONSUMER CONNECTED; complete path coverage remains unestablished'},
  'coverage':'SAVED ORDINARY/ZK EXAMPLES ONLY; original source/provenance retained',
  'cardinalities':values['procedure']['counts'],'qualified_classifications':'UNKNOWN',
  'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY'})

def validate_current_result(root,inputs,evidence_root,result):
 import managed_coverage as mc
 mc.need(type(result) is dict and result.get('format')==CURRENT_FORMAT,'PARTIAL-OR-LEGACY-RESULT')
 mc.need(result.get('actual_admission') is False and result.get('canonical_registration') is False and result.get('full_expansion_ready') is False and result.get('final_binding')=='BLOCKED','CURRENT-SCOPE-ESCALATION')
 mc.same(result,validate_current(root,inputs,evidence_root),'CURRENT-RESULT-SUBSTITUTION')
 return True

if __name__=='__main__':main()

