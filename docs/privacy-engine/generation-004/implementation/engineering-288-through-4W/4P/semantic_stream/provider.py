"""Exact inherited source-specific invocation codecs, streamed without hex copies."""
from admission_kernel.sources import FiniteLabProvider,MissingMaterial
from v4_ingest.records import canonical,digest,parse,exact,require,primitive,_source_refs
from .storage import Blob,Memory,Hex,encode

class StreamingProvider(FiniteLabProvider):
 def __init__(self,trusted,materials,sources,store):
  super().__init__(trusted,materials,sources);self.store=store;self.invocation_receipts=__import__('semantic_stream.lifetime',fromlist=['BoundedLog']).BoundedLog()
 def invocation(self,argument,security,model_digest):
  # Disk-backed exact dependency/consumed directory; no resident Blob map.
  import sqlite3
  path=self.store.path('invocation-closure');db=sqlite3.connect(path);db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file')
  db.execute('create table consumed(k text primary key,kind text,done integer) without rowid');db.execute('create index pending on consumed(done,k)')
  def add(key,kind):db.execute('insert or ignore into consumed values(?,?,0)',(key,kind))
  premises=self.trusted['premises']
  try:
   for _,ref in _source_refs([argument,security]):
    self.raw(ref)
    for kind in ('source','material'):add(ref[kind+'_sha256'],kind)
   for name in argument['premise_ids']:
    require(name in premises,'missing qualified reduction premise',category='INCOMPLETE-EVIDENCE-UNIVERSE');self.raw(premises[name]);add(premises[name]['material_sha256'],'material')
   while True:
    row=db.execute('select k,kind from consumed where done=0 limit 1').fetchone()
    if row is None:break
    key,kind=row
    if kind=='material':
     raw=self.materials.get(key)
     if raw is None:raise MissingMaterial('invocation dependency bytes '+key)
     require(digest(raw)==key,'invocation dependency digest',category='INVALID-EVIDENCE-DIGEST');obj=parse(raw);exact(obj,('format','payload','dependencies'))
     require(obj['format']=='CP3-LAB-MATERIAL-V1' and isinstance(obj['dependencies'],list),'supported complete dependency grammar')
     for dep in obj['dependencies']:primitive('DIGEST',dep);add(dep,'source' if dep in self.sources else 'material')
    db.execute('update consumed set done=1 where k=?',(key,))
   count=db.execute('select count(*) from consumed').fetchone()[0];db.commit()
   def consumed_parts():
    yield b'{';first=True
    for key,kind in db.execute('select k,kind from consumed order by k'):
     raw=(self.sources if kind=='source' else self.materials)[key]
     require(digest(raw)==key,'reopened invocation material byte identity',category='INVALID-EVIDENCE-DIGEST')
     if not first:yield b','
     first=False;yield b'"'+key.encode()+b'":';yield from encode(raw.hex())
    yield b'}\n'
   consumed_bytes=self.store.write(consumed_parts())
  finally:db.close();path.unlink(missing_ok=True)
  def cb(v):
   def chunks():yield from encode(v);yield b'\n'
   return self.store.write(chunks())
  parts=[('argument',cb(argument)),('security',cb(security)),('model-digest',self.store.write([model_digest.encode()])),
         ('consumed-source-bytes',consumed_bytes),
         ('premise-directory',cb({n:premises[n] for n in argument['premise_ids']}))]
  codec=self.trusted['mechanism']['invocation_codec']
  if codec=='NAMED-L64-V1':
   def chunks():
    yield b'CP3-LAB-ASSESSMENT-A\n'
    for name,b in parts:
     n=name.encode();yield len(n).to_bytes(8,'big');yield n;yield len(b).to_bytes(8,'big');yield from b.chunks()
   result=self.store.write(chunks())
  elif codec=='CANONICAL-JSON-V1':result=cb({'mechanism':'CP3-LAB-ASSESSMENT-B','inputs':{n:b.hex() for n,b in parts}})
  else:require(False,'unsupported exact source-specific invocation grammar',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  self.invocation_receipts.append({'argument_id':argument['argument_id'],'bytes':len(result),'sha256':digest(result),'dependency_count':count,'competence_established':False})
  return result

 def _distribution(self,world,db,name):
  from fractions import Fraction
  db.execute('create table '+name+' (key text primary key,n text,d text)')
  total=Fraction()
  for key,p in world['distribution']:
   if self.store.tick:self.store.tick()
   primitive('BYTES',key);primitive('RATIONAL',p)
   require(type(key) is str,'finite outcome scalar capability exceeded',category='INCOMPLETE-EVIDENCE-UNIVERSE')
   q=Fraction(*p);require(q>0,'genuine positive normalized world support')
   try:db.execute('insert into '+name+' values(?,?,?)',(key,str(q.numerator),str(q.denominator)))
   except __import__('sqlite3').IntegrityError:require(False,'duplicate finite outcome')
   total+=q;require(total.denominator.bit_length()<=1048576,'finite arithmetic capability exceeded',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  require(total==1,'genuine positive normalized world support')

 @staticmethod
 def _collision_key(value):
  # Preserve the inherited Python hash/equality domains: bool and int compare
  # equal; None and strings remain distinct. Containers were never hashable.
  if type(value) in (bool,int):return 'n:'+str(int(value))
  if value is None:return 'null'
  require(type(value) is str,'finite collision scalar capability exceeded',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  return 's:'+value

 def nonvacuity(self,experiment):
  # Source roles and exact correspondence remain separate from arithmetic.
  self.role('non-vacuity')
  a,b=self.payload(experiment['left_world']),self.payload(experiment['right_world'])
  keys=('world_id','protected_alternative','distribution','schedule','leakage','target','coalition','occurrences')
  exact(a,keys);exact(b,keys)
  require(a['target']==b['target']==experiment['target_id'] and a['coalition']==b['coalition']==experiment['coalition_id'],'world target/coalition join',category='INVALID-ACTION-CONTEXT')
  if a['protected_alternative']==b['protected_alternative'] or a['world_id']==b['world_id'] or a['occurrences']<1 or b['occurrences']<1 or a['schedule']!=b['schedule'] or a['leakage']!=b['leakage']:
   return {'status':'INVALID','bound':None,'reason':'NV2 degenerate/mismatched source scope'}
  import sqlite3
  db=sqlite3.connect(self.store.root/('assessment-'+str(self.store.count)));self.store.count+=1
  db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file')
  try:
   if experiment['kind']=='COLLISION':
    require(len(a['distribution'])>=2,'nonempty distinct relation-valid finite tuples',category='INVALID-ACTION-CONTEXT')
    db.execute('create table tuples(k text primary key)')
    for row in a['distribution']:
     require(isinstance(row,list) and len(row)==2,'finite canonical input tuples',category='INVALID-ACTION-CONTEXT')
     try:db.execute('insert into tuples values(?)',(self._collision_key(row[1]),))
     except sqlite3.IntegrityError:require(False,'distinct finite canonical input tuples',category='INVALID-ACTION-CONTEXT')
   else:
    self._distribution(a,db,'l');self._distribution(b,db,'r')
  finally:db.close()
  return {'status':'VALID','bound':None,'reason':'finite complete-support contract; independent adequacy is a LAB hypothesis'}

 def evaluate(self,argument,experiment,artifacts):
  from fractions import Fraction
  from .storage import unhex
  require(argument['certificate_artifact_ids'],'certificate absent',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  require(len(argument['certificate_artifact_ids'])==1,'LAB checker supports one complete certificate, not a generic PASS',category='INCOMPLETE-EVIDENCE-UNIVERSE')
  c=parse(unhex(artifacts[argument['certificate_artifact_ids'][0]]['exact_bytes']))
  exact(c,('format','experiment_id','left_world','right_world','premise_ids'))
  if c['format']!='CP3-FINITE-DISTRIBUTION-CERTIFICATE-V1':return {'status':'UNAVAILABLE','bound':None,'reason':'unsupported exact finite certificate'}
  if c['experiment_id']!=experiment['experiment_id'] or c['premise_ids']!=argument['premise_ids']:return {'status':'INVALID','bound':None,'reason':'certificate experiment/premise mismatch'}
  left,right=self.payload(experiment['left_world']),self.payload(experiment['right_world'])
  if c['left_world']!=left or c['right_world']!=right:return {'status':'INVALID','bound':None,'reason':'certificate differs from source-owned worlds'}
  nv=self.nonvacuity(experiment)
  if nv['status']!='VALID':return nv
  import sqlite3
  db=sqlite3.connect(self.store.root/('distance-'+str(self.store.count)));self.store.count+=1
  db.execute('pragma cache_size=-256');db.execute('pragma temp_store=file')
  try:
   if experiment['kind']=='COLLISION':
    db.execute('create table counts(k text primary key,n integer)');n=0
    for k,_ in left['distribution']:
     if self.store.tick:self.store.tick()
     db.execute('insert into counts values(?,1) on conflict(k) do update set n=n+1',(self._collision_key(k),));n+=1
    numerator=sum(v*(v-1)//2 for v, in db.execute('select n from counts'));q=Fraction(numerator,n*(n-1)//2)
   else:
    self._distribution(left,db,'l');self._distribution(right,db,'r');q=Fraction()
    for ln,ld,rn,rd in db.execute('select l.n,l.d,r.n,r.d from l left join r using(key) union all select null,null,r.n,r.d from r left join l using(key) where l.key is null'):
     q+=abs((Fraction(int(ln),int(ld)) if ln is not None else Fraction())-(Fraction(int(rn),int(rd)) if rn is not None else Fraction()))
     require(q.denominator.bit_length()<=1048576,'finite arithmetic capability exceeded',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    q/=2
  finally:db.close()
  return {'status':'VALID','bound':[q.numerator,q.denominator],'reason':'exact finite whole-view distribution; no primitive-security claim'}
