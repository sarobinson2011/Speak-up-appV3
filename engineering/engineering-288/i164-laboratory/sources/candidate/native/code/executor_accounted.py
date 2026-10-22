"""Active candidate wrapper. Retained executor remains historical, unchanged."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'retained/kernel/candidate/executor'))
from session import Session as HistoricalSession
from allowances import Allowances,wire,H,need
class Session(HistoricalSession):
 def __init__(self,*args,allowances,**kw):
  if not isinstance(allowances,Allowances):raise ValueError('shared pilot authority required')
  self.allowances=allowances;super().__init__(*args,**kw)
  binding={'pilot':allowances.pilot,'accounting_code':H((ROOT/'code/allowances.py').read_bytes()),'wrapper_code':H(Path(__file__).read_bytes()),'policy':H((ROOT/'records/approval.json').read_bytes())}
  try:
   if kw.get('create'):
    self.db.execute('CREATE TABLE allowance_binding(raw BLOB)');self.db.execute('INSERT INTO allowance_binding VALUES (?)',(wire(binding),))
   need(self.db.execute('SELECT raw FROM allowance_binding').fetchone()[0]==wire(binding),'changed accounting/pilot binding')
  except BaseException:self.close();raise
 def status(self,request_id):
  return self.allowances.governed('status',request_id,lambda:super(Session,self).status())
 def backup(self,path,request_id):
  # Retirement and accounting are separate; a job backup never contains quota authority.
  return self.allowances.governed('backup',request_id,lambda:super(Session,self).backup(path))
