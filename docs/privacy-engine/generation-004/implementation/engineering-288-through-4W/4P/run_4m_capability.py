"""Bounded demonstration of retained semantic-document handle lifecycle boundary."""
import json,resource,tempfile
from pathlib import Path
from semantic_stream.storage import Store
soft,hard=resource.getrlimit(resource.RLIMIT_NOFILE);resource.setrlimit(resource.RLIMIT_NOFILE,(min(96,hard),hard))
s=Store();count=0;failure=None
try:
 for i in range(128):s.parse(s.write([(json.dumps({'n':i},separators=(',',':'))+'\n').encode()]));count+=1
except (OSError,Exception) as e:failure={'type':type(e).__name__,'detail':str(e)}
finally:
 s.close();resource.setrlimit(resource.RLIMIT_NOFILE,(soft,hard))
r={'result':'DEMONSTRATED-LIFECYCLE-BOUNDARY' if failure else 'NO-BOUNDARY-OBSERVED','completed_small_documents':count,'attempted_documents':128,'open_file_limit':min(96,hard),'failure':failure,'source':'semantic_stream/storage.py:Store.docs, Store.parse, Document.__init__','meaning':'Retained semantic indexes keep database connections open until whole invocation ends. Catalog maps themselves open readonly handles per operation. Complete metadata coverage is not complete actual-value acquisition.','full_stream_processed':False,'qualification_established':False}
Path('results/4M-semantic-handle-boundary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
