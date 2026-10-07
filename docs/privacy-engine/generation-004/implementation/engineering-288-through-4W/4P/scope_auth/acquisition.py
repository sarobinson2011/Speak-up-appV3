"""Bounded file-backed acquisition into the inherited exact-byte collector.

Local paths are transport, not source authority. Hashes bind bytes consumed from
one open descriptor. Size/mtime never establish identity. No full large stream
can enter this carrier: explicit local resource capability, not a protocol cap.
"""
import hashlib,os,stat
from pathlib import Path
from v4_ingest.records import exact,primitive,require,ValidationError
from admission_kernel.sources import MissingMaterial
MAX_OBJECT=16*1024*1024
MAX_TOTAL=64*1024*1024

def read_blob(base,entry):
    exact(entry,('path','bytes','sha256'));primitive('DIGEST',entry['sha256'])
    size=entry['bytes'];require(type(size) is int and 0<=size<=MAX_OBJECT,'source acquisition local byte capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    require(type(entry['path']) is str and entry['path'] and not Path(entry['path']).is_absolute() and '..' not in Path(entry['path']).parts,'relative source-object path')
    base=Path(base).resolve();path=(base/entry['path']).resolve()
    require(path.is_relative_to(base),'source-object path leaves acquisition directory')
    try:
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
        with os.fdopen(fd,'rb') as f:
            require(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'regular source object')
            h=hashlib.sha256();parts=[];count=0
            while True:
                b=f.read(min(65536,size-count+1))
                if not b:break
                count+=len(b);require(count<=size,'changed/oversize source object',category='INVALID-EVIDENCE-DIGEST');h.update(b);parts.append(b)
            require(count==size and h.hexdigest()==entry['sha256'],'exact acquired source byte identity',category='INVALID-EVIDENCE-DIGEST')
            return b''.join(parts)
    except OSError as e:raise MissingMaterial('source object unavailable: '+str(e)) from e

def acquire(manifest,base,failures=None):
    exact(manifest,('format','request','objects','bundles'))
    require(manifest['format']=='CP4E-FILE-ACQUISITION-V1','supported source acquisition carrier')
    q=dict(manifest['request']);require('materials' not in q and 'source_objects' not in q and 'bundles' not in q,'no shadow byte maps')
    q['materials']={};q['source_objects']={};q['bundles']={};receipt=[];total=0
    def attempt(fn):
        try:return fn()
        except (MissingMaterial,ValidationError,OSError,ValueError,KeyError,TypeError) as e:
            if failures is None:raise
            code='MISSING-EVIDENCE' if isinstance(e,(MissingMaterial,OSError)) else getattr(e,'category','INVALID-PROFILE-SCHEMA')
            failures.add(code,'file acquisition: '+str(e));return None
    def bounded(entry):
        nonlocal total
        size=entry['bytes'];require(type(size) is int and size>=0,'source byte count')
        total+=size;require(total<=MAX_TOTAL,'aggregate acquisition local capability',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        raw=read_blob(base,entry);receipt.append(entry);return raw
    for obj in manifest['objects']:
        def source(obj=obj):
            exact(obj,('directory','digest','blob'));require(obj['directory'] in ('materials','source_objects'),'source directory');primitive('DIGEST',obj['digest'])
            require(obj['digest'] not in q[obj['directory']],'duplicate source identity')
            raw=bounded(obj['blob']);require(hashlib.sha256(raw).hexdigest()==obj['digest'],'source map key identity',category='INVALID-EVIDENCE-DIGEST')
            q[obj['directory']][obj['digest']]=raw.hex()
        attempt(source)
    from v4_ingest.wire import FILES
    for scope,item in manifest['bundles'].items():
        def bundle(scope=scope,item=item):
            exact(item,('files','object_sha256'));exact(item['files'],FILES);files={}
            for name in FILES:
                raw=attempt(lambda:bounded(item['files'][name]))
                if raw is not None:files[name]=raw.hex()
            q['bundles'][scope]={'files':files,'object_sha256':item['object_sha256']}
        attempt(bundle)
    return q,{'exact_objects_acquired':len(receipt),'bytes_acquired':sum(e['bytes'] for e in receipt),'identities':receipt,'authentication_established_by_acquisition':False}
