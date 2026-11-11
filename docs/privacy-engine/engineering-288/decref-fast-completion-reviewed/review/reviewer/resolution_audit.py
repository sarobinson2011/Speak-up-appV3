from bytes_only import *
p=B/'source/reference/I164-decref-public-source-resolution-1.zip'
pin=read(B/'source/DEPENDENCIES.json')['source_resolution']
assert fid(p)=={k:pin[k] for k in ('bytes','sha256')}
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 files={}
 for i in z.infolist():
  n=safe(i.filename);assert n not in files and not i.is_dir() and not i.flag_bits&1 and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG);files[n]=z.read(i)
 m=json.loads(files['MANIFEST.json'])['files']
 assert len(files)==226 and set(files)==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert ident(files[n])==pin,n
write(files,B/'resolution')
save(B/'resolution-archive-audit.json',{'identity':fid(p),'entries':226,'manifested_hashes':225,'CRC_safe_exact_membership_all_hashes':'PASS','schema':'MANIFEST.files','earlier_reader_failure':'Flat-manifest assumption rejected before extraction; zero candidate controls. Preserved in reviewer FAILURES.'})
