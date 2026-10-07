"""Acquire source-rooted exact dependency bytes without inventing source truth."""
from v4_ingest.records import parse,exact,primitive,digest,require
from admission_kernel.sources import MissingMaterial

def payload(provider,ref):
    result=provider.payload(ref);active=set();done=set();stack=[(ref['material_sha256'],False)]
    while stack:
        key,leave=stack.pop()
        if leave:active.remove(key);done.add(key);continue
        if key in done:continue
        require(key not in active,'cyclic source material dependencies',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        raw=provider.materials.get(key)
        if raw is None:raise MissingMaterial('scope dependency bytes '+key)
        require(digest(raw)==key,'scope dependency byte digest',category='INVALID-EVIDENCE-DIGEST')
        obj=parse(raw);exact(obj,('format','payload','dependencies'))
        require(obj['format']=='CP3-LAB-MATERIAL-V1' and isinstance(obj['dependencies'], list),'supported complete source dependency grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
        active.add(key);stack.append((key,True))
        for dep in obj['dependencies']:primitive('DIGEST',dep);stack.append((dep,False))
    return result
