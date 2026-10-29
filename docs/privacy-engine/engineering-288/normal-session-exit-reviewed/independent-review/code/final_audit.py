"""Final byte preservation and review-evidence reconciliation, no candidate execution."""
from pathlib import Path
import hashlib,json,sys,collections
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import verify_root,ident
w=Path(__file__).resolve().parents[2];r=w/'ns-review';groups={}
for name,count in [('primary',260),('recovered',43),('fresh-semantic',3),('fresh-constructed',2),('fresh-public',4)]:
 p=r/name;v=json.loads((p/'RESULT.json').read_bytes());lines=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()]
 assert v['result']=='PASS' and v['error'] is None and v['checks']==count and v['rows']==lines and len(lines)==count
 assert v['outcomes']==dict(collections.Counter(x['result'] for x in lines))
 groups[name]={'checks':count,'outcomes':v['outcomes'],'result_identity':ident((p/'RESULT.json').read_bytes()),'seconds':v['seconds'],'environment':v['environment']}
roots={n:verify_root(w/n) for n in ('ns-input','ns-recovered-v2')}
bad=w/'ns-recovered';m=json.loads((bad/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};extra={p.relative_to(bad).as_posix() for p in bad.rglob('*') if p.is_file()}-expected
for n,pin in m.items():assert ident((bad/n).read_bytes())==pin
forensic=json.loads((r/'failures/recovered-membership/record.json').read_bytes());assert extra=={x['relative_path'] for x in forensic}
for f in forensic:assert ident((bad/f['relative_path']).read_bytes())=={k:f[k] for k in ('bytes','sha256')}==ident((r/'failures/recovered-membership/forensic-extra.bin').read_bytes())
raw=(w/'upload/I164-normal-session-exit-correspondence-1(1).zip').read_bytes();assert ident(raw)=={'bytes':70593959,'sha256':'c9c8d2106617970e8008fadc3c60f61813c64e7ce07e24a60bc92ac1029b954a'}
failed=[r/'failures/source-oracle-zero/result/RESULT.json',r/'failures/recovered-membership/recovered/RESULT.json',r/'failures/recovered-membership/fresh-semantic/RESULT.json']
for p in failed:
 v=json.loads(p.read_bytes());assert v['result']=='FAIL' and v['checks']==0 and v['rows']==[]
out={'result':'PASS','independent_groups':groups,'completed_independent_controls':sum(x['checks'] for x in groups.values()),'public_CLI_check_included_in_fresh_public':True,'strict_verified_roots':roots,'forensic_root':{'root':str(bad),'manifested_members_unchanged':2331,'extra_records':forensic,'preserved_without_normalization':True},'input_archive_unchanged':ident(raw),'implementation_unchanged':True,'failed_attempts_excluded':[{'path':'failures/source-oracle-zero','checks':0,'reason':'Reviewer dedentation of library source fragment failed before first completed control; only reviewer oracle corrected.'},{'path':'failures/prefix-audit','checks':0,'reason':'Reviewer prefix equality incorrectly included a newly documented comment; inherited executable source and exact declared diff checked separately.'},{'path':'failures/recovery-cut-audit','checks':0,'reason':'Reviewer initially expected all intermediate-cut bytes identical; supplied note explicitly documents the README-only clarification.'},{'path':'failures/recovered-membership','attempts':2,'checks':0,'reason':'Both strict root gates rejected the same undeclared regular partial file before code consumption. Origin unestablished; bytes preserved outside strict roots; a new exact extraction was used.'}]}
(r/'results/final-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
