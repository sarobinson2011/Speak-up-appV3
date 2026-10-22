"""DynamoDB wire adapter plus OFFLINE SQLite contract simulator. No client creation."""
import sqlite3,json
from anchor import Blocked,need,parse,enc,sha
class DynamoContract:
 def __init__(self,client,descriptor,namespace):
  # A future service injects its configured SDK client. This file loads no credentials.
  self.client=client;self.descriptor=descriptor;self.namespace=namespace
 def identity(self):
  x=self.client.describe_table(TableName=self.descriptor['table_arn'])['Table']
  need(x['TableStatus']=='ACTIVE' and not x.get('Replicas'),'SINGLE-REGION-ACTIVE-REQUIRED')
  need(x['TableArn']==self.descriptor['table_arn'] and x['TableId']==self.descriptor['table_id'],'TABLE-INCARNATION')
  return dict(self.descriptor)
 def key(self,k):return {'pk':{'S':self.namespace+'#'+k}}
 def get(self,k):
  self.identity();r=self.client.get_item(TableName=self.descriptor['table_arn'],Key=self.key(k),ConsistentRead=True)
  return bytes(r['Item']['v']['B']) if 'Item' in r else None
 def item(self,k,v):return {**self.key(k),'v':{'B':v}}
 def create(self,raw):
  self.identity();self.client.put_item(TableName=self.descriptor['table_arn'],Item=self.item('HEAD',raw),ConditionExpression='attribute_not_exists(pk)')
 def request(self,old,new,puts):
  need(len(puts)<=98,'TRANSACTION-COUNT')
  for v in [new,*puts.values()]:need(type(v) is bytes and len(v)<=300000,'DDB-ITEM-BOUND')
  table=self.descriptor['table_arn']
  actions=[{'Put':{'TableName':table,'Item':self.item('HEAD',new),'ConditionExpression':'#v = :old','ExpressionAttributeNames':{'#v':'v'},'ExpressionAttributeValues':{':old':{'B':old}}}}]
  actions += [{'Put':{'TableName':table,'Item':self.item(k,v),'ConditionExpression':'attribute_not_exists(pk)'}} for k,v in sorted(puts.items())]
  # Permanent OP record, not this API's 10-minute token, enforces long-lived idempotence.
  return {'TransactItems':actions}
 def commit(self,old,new,puts,fault=None):
  need(fault is None,'NO-PRODUCTION-FAULT-HOOK');self.identity()
  try:self.client.transact_write_items(**self.request(old,new,puts))
  except Exception as ex:raise TimeoutError('DDB outcome must be resolved; no automatic retry') from ex
class SimulatedBackend:
 """No AWS guarantees. Fixture state is fully writable by the harness owner."""
 def __init__(self,path,descriptor):
  self.descriptor=dict(descriptor);self.available=True;self.stale=None
  self.db=sqlite3.connect(path,isolation_level=None,timeout=2)
  self.db.execute('PRAGMA journal_mode=DELETE');self.db.execute('PRAGMA synchronous=FULL')
  self.db.execute('CREATE TABLE IF NOT EXISTS objects(k TEXT PRIMARY KEY,v BLOB NOT NULL)')
 def identity(self):
  if not self.available:raise OSError('SIMULATED-UNAVAILABLE')
  return dict(self.descriptor)
 def get(self,k):
  self.identity()
  if k=='HEAD' and self.stale is not None:return self.stale
  row=self.db.execute('SELECT v FROM objects WHERE k=?',(k,)).fetchone();return row[0] if row else None
 def create(self,raw):
  self.identity()
  try:self.db.execute('INSERT INTO objects VALUES (?,?)',('HEAD',raw))
  except sqlite3.IntegrityError as ex:raise Blocked('EXISTING-ANCHOR-NO-RESET') from ex
 def commit(self,old,new,puts,fault=None):
  self.identity()
  if fault=='before':raise TimeoutError('SIMULATED-before-commit')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   row=self.db.execute('SELECT v FROM objects WHERE k=?',('HEAD',)).fetchone();need(row and row[0]==old,'CAS-CONFLICT')
   for k,v in puts.items():self.db.execute('INSERT INTO objects VALUES (?,?)',(k,v))
   if fault=='partial':raise OSError('SIMULATED-crash-before-head')
   self.db.execute('UPDATE objects SET v=? WHERE k=?',(new,'HEAD'));self.db.execute('COMMIT')
  except BaseException:
   if self.db.in_transaction:self.db.execute('ROLLBACK')
   raise
  if fault=='ack_loss':raise TimeoutError('SIMULATED-commit-acknowledgement-lost')
 def close(self):self.db.close()
