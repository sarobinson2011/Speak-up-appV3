import pathlib,json,zipfile,hashlib,shutil
P=pathlib.Path(__file__).resolve().parent;W=P.parent
H=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert 'PASS draft model/ledger' in (P/'results/build.log').read_text()
validation=json.loads((P/'results/recovered-validation.log').read_text());assert validation['metadata_correspondence'] is True and validation['actual_admission'] is False
assert len(json.loads((P/'results/final-focused.json').read_text()))==44
assert len(json.loads((P/'results/process.json').read_text()))==5
summary={'implementation_author':'SU-Engineering[288C]','independent_review':'PENDING for new draft connection','incorporated_review':{'bytes':29809796,'entries':56,'sha256':'3b852fdb9a1af1aa441923182600762059107ae197659c08511ec7491fdf9052','fresh_independent_controls':98,'additional_full_CLI':1,'supplied_construction_controls':40,'supplied_author_review_controls':77,'reviews_rerun':False},'focused_controls':44,'fresh_process_negatives':5,'construction':'PASS actual emitted-input procedure consumption and reviewed SOURCE-ONLY path','recovered_fresh_process_validation':validation,'candidate_changes':[],'full_expansion':False,'readiness':'BLOCKED','final_binding':'BLOCKED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','admission':False}
(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2))
stage=P/'delivery';stage.mkdir(exist_ok=False)
for n in ['code','outputs','results','failures']:shutil.copytree(P/n,stage/n)
for n in ['REPORT.md','RECOVERY.md','AUTHORIZATION.txt','CHANGED-IDENTITIES.json','SUMMARY.json','recover.py','audit.py','package.py']:shutil.copyfile(P/n,stage/n)
(stage/'inputs').mkdir();shutil.copyfile(P/'independent-review/inputs/integration.zip',stage/'inputs/source-only-integration.zip')
(stage/'provenance').mkdir()
for n in ['REPORT.md','SUMMARY.json','RECOVERY.md']:
 shutil.copyfile(P/'independent-review'/n,stage/'provenance'/('independent-'+n))
m={str(f.relative_to(stage)):H(f.read_bytes()) for f in sorted(stage.rglob('*')) if f.is_file()}
(stage/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
zp=W/'Engineering-288C-I164-source-only-model-ledger-inputs.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,9) as z:
 for f in sorted(stage.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(stage)))
fresh=P/'fresh-extraction'
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
 assert set(z.namelist())==set(m)|{'MANIFEST.json'};z.extractall(fresh)
for n,v in m.items():assert H((fresh/n).read_bytes())==v
om=json.loads((fresh/'outputs/MANIFEST.json').read_bytes());assert set(om)|{'MANIFEST.json'}=={f.name for f in (fresh/'outputs').iterdir()}
for n,v in om.items():assert H((fresh/'outputs'/n).read_bytes())==v
v={'file':str(zp),**H(zp.read_bytes()),'entries':len(m)+1,'CRC':'PASS','fresh_extraction_membership_and_manifests':'PASS'}
(P/'package-verification.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2))
