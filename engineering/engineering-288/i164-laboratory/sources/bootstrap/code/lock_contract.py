"""Strict hash-pinned uv lock subset actually supplied by the host addendum.
No URLs, editable requirements, options other than SHA256 hashes, markers or
version ranges are accepted. No installation or hash rewriting.
"""
import re

def parse_lock(text):
 out={};pending=[]
 for line in text.splitlines():
  s=line.strip()
  if not s or s.startswith('#'):
   if pending:raise ValueError('COMMENT-OR-BLANK-IN-CONTINUATION')
   continue
  more=s.endswith('\\');s=s[:-1].rstrip() if more else s
  if '\\' in s:raise ValueError('UNSUPPORTED-ESCAPE')
  pending.extend(s.split())
  if more:continue
  m=re.fullmatch(r'([A-Za-z0-9_.-]+)==([0-9]+(?:\.[0-9]+)*)',pending[0])
  if not m:raise ValueError('UNSUPPORTED-REQUIREMENT')
  name=re.sub(r'[-_.]+','-',m[1]).lower()
  if name in out:raise ValueError('DUPLICATE-REQUIREMENT')
  hashes=[]
  for word in pending[1:]:
   h=re.fullmatch(r'--hash=sha256:([0-9a-f]{64})',word)
   if not h:raise ValueError('UNSUPPORTED-HASH-OPTION')
   if h[1] in hashes:raise ValueError('DUPLICATE-HASH')
   hashes.append(h[1])
  if not hashes:raise ValueError('MISSING-HASHES')
  out[name]={'version':m[2],'hashes':hashes};pending=[]
 if pending:raise ValueError('UNFINISHED-CONTINUATION')
 if not out:raise ValueError('EMPTY-LOCK')
 return out
