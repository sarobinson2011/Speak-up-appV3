from pathlib import Path,PurePosixPath
import zipfile,io,hashlib,json,ast,difflib,collections,stat
W=Path(__file__).resolve().parents[2];P=W/'upload/I164-callback-exception-stored-failure-correspondence-1(1).zip';O=W/'cb-review/results'
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
es,current=inspect(P.read_bytes(),'')
assert current['identity']=={'bytes':84555031,'sha256':'0a39361622d3c05c7f46b258bfd7570d632ab57ee87317103cacce1f52822255'} and current['entries']==2807
priorraw=(W/'upload/I164-stored-failure-revocation-correspondence-1(1).zip').read_bytes();reviewraw=(W/'Formal-Lab6-I164-stored-failure-revocation-independent-review.zip').read_bytes()
assert ident(priorraw)=={'bytes':76307999,'sha256':'cd36a49cf2366c95aa96d8407e182eec716e6e77d261a1b0908ec250266230bf'}
assert ident(reviewraw)=={'bytes':78909450,'sha256':'7ea2c551a2f6cf12472bf4a2396b4f2146763deb4fff9a3420a25cea9e13d0cf'}
with zipfile.ZipFile(io.BytesIO(priorraw)) as z:prior={n:z.read(n) for n in z.namelist()}
with zipfile.ZipFile(io.BytesIO(reviewraw)) as z:review={n:z.read(n) for n in z.namelist()}
assert len(prior)==2661 and {n[len('retained/stored/'):] for n in es if n.startswith('retained/stored/')}==set(prior)
assert all(es['retained/stored/'+n]==b for n,b in prior.items())
omit='input/I164-stored-failure-revocation-correspondence-1.zip';assert review[omit]==priorraw
assert {n[len('retained/review/'):] for n in es if n.startswith('retained/review/')}==set(review)-{omit}
assert all(es['retained/review/'+n]==b for n,b in review.items() if n!=omit)
assert es['provenance/prior-review.json']==review['CHECKPOINT.json']
def funcs(raw):
 s=raw.decode();tree=ast.parse(s);return {n.name:ast.get_source_segment(s,n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))},[ast.dump(n,include_attributes=False) for n in tree.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
a,aa=funcs(prior['code/managed_coverage.py']);b,bb=funcs(es['code/managed_coverage.py']);assert len(a)==100 and aa==bb and all(b[k]==v for k,v in a.items());changes=json.loads(es['provenance/changed-files.json']);added=sorted(set(b)-set(a));assert added==changes['added_producer_functions'] and changes['inherited_functions_classes_unchanged']==len(a)
diff=''
for n in ('code/managed_coverage.py','code/correspondence.py'):
 pins=changes['intentional_implementation_changes'][n];assert pins['current']==ident(es[n]) and pins['previous']==ident(prior[n]);diff+=''.join(difflib.unified_diff(prior[n].decode().splitlines(True),es[n].decode().splitlines(True),fromfile='reviewed-stored/'+n,tofile='callback-failure/'+n))
assert es['provenance/intentional.diff']==diff.encode()
sources={}
for n in ('prospective_entry.py','lab_bootstrap.py','live_connection.py'):
 assert es['source-evidence/'+n]==prior['source-evidence/'+n];sources[n]=ident(es['source-evidence/'+n])
old=json.loads(prior['results/correction/stored-failure-revocation.json']);new=json.loads(es['results/primary/callback-stored-failure.json'])
assert all(new[k]==v for k,v in old.items() if k not in ('format','contexts','extension_components'))
assert new['prior_stored_failure_components']==old['extension_components'] and new['prior_stored_failure_receipt']==ident(prior['results/correction/stored-failure-revocation.json'])
assert len(new['contexts'])==len(old['contexts'])==2
for x,y in zip(old['contexts'],new['contexts']):assert set(y)==set(x)|{'callback_stored_failure_correspondence'} and all(y[k]==v for k,v in x.items())
assert [r['context'] for r in new['contexts']]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
obpaths=[n for n,p in json.loads(es['MANIFEST.json']).items() if p==new['unchanged_obligations']];assert obpaths
for n in obpaths:assert [v['id'] for v in json.loads(es[n])['obligations']]==[f'O{i:02}' for i in range(1,12)]
assert new['inventory_unknown_totals']==4 and new['lifetime_unknown_totals']==14
cut=json.loads(es['provenance/recovery-cut-manifest.json']);assert len(cut)==2788 and all(ident(es[n])==v for n,v in cut.items())
supplied={}
for name,count in [('primary',423),('recovered',70),('public',4)]:
 p='results/'+name+'/';r=json.loads(es[p+'RESULT.json']);logs=[json.loads(s) for s in es[p+'progress.jsonl'].decode().splitlines()];assert r['result']=='PASS' and r['error'] is None and r['checks']==count and r['rows']==logs and len(logs)==count
 supplied[name]={'checks':count,'outcomes':dict(collections.Counter(x['result'] for x in logs)),'result_identity':ident(es[p+'RESULT.json']),'labels':[x['check'] for x in logs],'inspected_not_rerun':True}
failed=json.loads(es['failures/initial-membership/results/RESULT.json']);assert failed['checks']==0 and failed['error'] and failed['result']=='FAIL';fe=json.loads(es['failures/initial-membership/EVIDENCE.json']);extra=fe['extra_entries'];assert len(extra)==1
assert ident(es['failures/initial-membership/undeclared-partial.bin'])=={k:extra[0][k] for k in ('bytes','sha256')}
result={'result':'PASS','current':current,'reused_prior_outer_identity':ident(priorraw),'reused_prior_review_outer_identity':ident(reviewraw),'retained_predecessor_members':len(prior),'retained_review_noninput_members':len(review)-1,'all_predecessor_member_bytes_equal_original':True,'nested_archive_occurrences':nested,'source_identities':sources,'inherited_producer_functions':len(a),'added_functions':added,'inherited_nonfunction_AST_unchanged':True,'declared_changes_and_exact_diff':'PASS','all_prior_receipt_fields_historical_identities_relationships_ordinals_normal_branch':'UNCHANGED','new_receipt':ident(es['results/primary/callback-stored-failure.json']),'obligations_identity':new['unchanged_obligations'],'obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'supplied':supplied,'supplied_zero_assertion_attempt':{'result_identity':ident(es['failures/initial-membership/results/RESULT.json']),'assertions':0,'excluded':True,'partial':fe},'supplied_recovery_cut_unchanged_nonmanifest_members':len(cut),'supplied_recovery_cut_outer_freshly_verified':False,'historical_compact_manifest_qualifications':'Preserved; absent/rebased items listed in manifest audit; original outer ZIPs not inferred from recompression.'}
(O/'composition.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('current','nested_archive_occurrences','supplied','supplied_zero_assertion_attempt')},indent=2));print('nested archives',len(nested),'interpretable manifests',len(current['manifest_audit'])+sum(len(v['manifest_audit']) for v in nested.values()))
