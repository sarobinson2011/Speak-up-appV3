from pathlib import Path,PurePosixPath
import zipfile,io,hashlib,json,ast,difflib,collections,stat
W=Path(__file__).resolve().parents[2];P=W/'upload/I164-stored-failure-revocation-correspondence-1(1).zip';O=W/'sr-review/results'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def manifests(es):
 result=[]
 for n,b in es.items():
  if not n.endswith('MANIFEST.json'):continue
  m=json.loads(b);m=m.get('members',m);pre=n[:-len('MANIFEST.json')]
  if type(m) is not dict or not all(type(v) is dict and set(v)=={'bytes','sha256'} for v in m.values()):continue
  present=[];absent=[]
  for name,pin in m.items():
   if pre+name in es:assert ident(es[pre+name])==pin,(n,name);present.append(name)
   else:absent.append(name)
  result.append({'manifest':n,'present_verified':len(present),'absent':absent})
 return result
nested={}
def inspect(raw,label):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None;ns=z.namelist();assert len(ns)==len(set(ns))
  for i in z.infolist():
   p=PurePosixPath(i.filename);assert not p.is_absolute() and str(p)==i.filename and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  es={n:z.read(n) for n in ns}
  m=json.loads(es['MANIFEST.json']);m=m.get('members',m);assert set(es)==set(m)|{'MANIFEST.json'}
  for n,v in m.items():assert ident(es[n])==v,(label,n)
  record={'identity':ident(raw),'entries':len(ns),'CRC':'PASS','membership':'PASS','manifested_hashes':len(m),'manifest_audit':manifests(es)}
  if label:nested[label]=record
  for n,b in es.items():
   if n.endswith('.zip'):inspect(b,label+'!/'+n)
  return es,record
es,current=inspect(P.read_bytes(),'');oldm=json.loads(es['retained/owner/MANIFEST.json']);assert ident(es['retained/owner/MANIFEST.json'])=={'bytes':690980,'sha256':'5d3bd027372da6610ce1a05fec8fb75fcf19acb303b58692d61b038a5e6e1c4c'}
assert len(oldm)==2494 and {n[len('retained/owner/'):] for n in es if n.startswith('retained/owner/')}==set(oldm)|{'MANIFEST.json'}
for n,pin in oldm.items():assert ident(es['retained/owner/'+n])==pin
rm=json.loads(es['retained/review/MANIFEST.json']);assert ident(es['retained/review/MANIFEST.json'])=={'bytes':9380,'sha256':'1c08c019cada1d583b2e786f661327e74d65494f18e77d46d400692ec065c540'}
omit='input/I164-owner-lock-finalization-correspondence-1.zip'
assert {n[len('retained/review/'):] for n in es if n.startswith('retained/review/')}==(set(rm)|{'MANIFEST.json'})-{omit}
for n,pin in rm.items():
 if n!=omit:assert ident(es['retained/review/'+n])==pin
assert es['provenance/prior-review.json']==es['retained/review/CHECKPOINT.json']
def funcs(raw):
 s=raw.decode();t=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,aa=funcs(es['retained/owner/code/managed_coverage.py']);b,bb=funcs(es['code/managed_coverage.py']);assert len(a)==95 and aa==bb and all(b[k]==v for k,v in a.items());added=sorted(set(b)-set(a));changes=json.loads(es['provenance/changed-files.json']);assert added==changes['added_producer_functions']
diff=''
for n in ('code/managed_coverage.py','code/correspondence.py'):
 pins=changes['intentional_implementation_changes'][n];assert pins['current']==ident(es[n]) and pins['previous']==ident(es['retained/owner/'+n]);diff+=''.join(difflib.unified_diff(es['retained/owner/'+n].decode().splitlines(True),es[n].decode().splitlines(True),fromfile='reviewed-owner/'+n,tofile='stored-failure/'+n))
assert es['provenance/intentional.diff']==diff.encode()
sources={}
for n in ('prospective_entry.py','lab_bootstrap.py','live_connection.py'):
 assert es['source-evidence/'+n]==es['retained/owner/source-evidence/'+n];sources[n]=ident(es['source-evidence/'+n])
old=json.loads(es['retained/owner/results/primary/owner-lock-finalization.json']);new=json.loads(es['results/correction/stored-failure-revocation.json'])
assert all(new[k]==v for k,v in old.items() if k not in ('format','contexts','extension_components'))
assert new['prior_owner_finalization_components']==old['extension_components'] and new['prior_owner_finalization_receipt']==ident(es['retained/owner/results/primary/owner-lock-finalization.json'])
for x,y in zip(old['contexts'],new['contexts']):assert set(y)==set(x)|{'stored_failure_revocation_correspondence'} and all(y[k]==v for k,v in x.items())
assert [r['context'] for r in new['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
assert new['inventory_unknown_totals']==4 and new['lifetime_unknown_totals']==14
ob=[n for n,p in json.loads(es['MANIFEST.json']).items() if p==new['unchanged_obligations']];assert len(ob)==1
assert [v['id'] for v in json.loads(es[ob[0]])['obligations']]==[f'O{i:02}' for i in range(1,12)]
mapping=json.loads(es['provenance/initial-member-map.json'])['members'];assert len(mapping)==2596
for n,p in mapping.items():assert ident(es[p['retained_path']])=={k:v for k,v in p.items() if k!='retained_path'},n
initial_manifest=json.loads(es[mapping['MANIFEST.json']['retained_path']]);assert set(mapping)==set(initial_manifest)|{'MANIFEST.json'}
for n,p in initial_manifest.items():assert ident(es[mapping[n]['retained_path']])==p
cut=json.loads(es['provenance/corrected-cut-manifest.json']);assert len(cut)==2643 and all(ident(es[n])==v for n,v in cut.items())
supplied={}
for label,path,count in [('current-focused','results/correction/',66),('current-recovered','results/final-recovered/',37),('current-fresh','results/final-fresh/',3),('earlier-primary','results/primary/',366),('earlier-recovered','failures/helper-escape-gap/baseline-recovered/',75),('earlier-fresh','failures/helper-escape-gap/baseline-fresh/',2),('earlier-constructed','failures/helper-escape-gap/baseline-constructed/',2),('earlier-public','failures/helper-escape-gap/baseline-public/',3)]:
 r=json.loads(es[path+'RESULT.json']);logs=[json.loads(l) for l in es[path+'progress.jsonl'].decode().splitlines()];assert r['result']=='PASS' and r['error'] is None and r['checks']==count and r['rows']==logs and len(logs)==count
 supplied[label]={'checks':count,'outcomes':dict(collections.Counter(v['result'] for v in logs)),'result_identity':ident(es[path+'RESULT.json']),'labels':[v['check'] for v in logs],'inspected_not_rerun':True}
failed=json.loads(es['failures/source-arity/results/RESULT.json']);assert failed['checks']==0 and failed['result']=='FAIL';interrupt=json.loads(es['retained/owner/failures/derive-attempt-1/ATTEMPT.json']);assert interrupt['completed_assertions']==0 and interrupt['cause']=='UNESTABLISHED'
result={'result':'PASS','current':current,'predecessor_manifest_reused_verified_identity':ident(es['retained/owner/MANIFEST.json']),'retained_predecessor_members':2495,'retained_prior_review_noninput_members':68,'predecessor_outer_archive_freshly_verified':False,'prior_review_outer_archive_freshly_verified':False,'nested_archive_occurrences':nested,'source_identities':sources,'inherited_producer_functions':len(a),'added_functions':added,'nonfunction_AST_preserved':True,'declared_changes_and_exact_diff':'PASS','original_evidence_prior_context_fields_identities_relationships_ordinals_preserved':True,'original_obligations_identity':new['unchanged_obligations'],'obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'receipt':ident(es['results/correction/stored-failure-revocation.json']),'initial_exact_member_tree_reconstruction':len(mapping),'initial_outer_archive_newly_verified':False,'corrected_cut_nonmanifest_members_unchanged':len(cut),'corrected_cut_outer_archive_newly_verified':False,'supplied':supplied,'supplied_failed_zero_assertion_attempt':{'identity':ident(es['failures/source-arity/results/RESULT.json']),'checks':0,'excluded':True},'prior_interruption':interrupt,'historical_manifest_absences':'Unchanged compact/forensic predecessor qualifications, individually listed; original ZIP bytes not reconstructed by recompression.'}
(O/'composition.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('current','nested_archive_occurrences','supplied')},indent=2));print('nested archives',len(nested),'interpretable manifests',len(current['manifest_audit'])+sum(len(v['manifest_audit']) for v in nested.values()))
