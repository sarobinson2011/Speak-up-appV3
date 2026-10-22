"""Exercise the retained pair enumerator on tiny compatible normalized groups only."""
import ast,sys,json
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);source=root/'native/code/expand_candidate.py'
def need(x,m):
 if not x:raise ValueError(m)
class G:
 def __init__(self,rows):self.rows=rows;self.parts=[(0,rows,True)]
 def entries(self,prefix=None):return iter(self.rows)
 def get(self,key):
  found=[(i,new) for i,r,p,new in self.rows if r==key];need(len(found)==1,'lookup');return found[0]
node=next(n for n in ast.parse(source.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='pairs');env={'need':need};exec(compile(ast.Module(body=[node],type_ignores=[]),'<retained pairs>','exec'),env)
results=[]
for rule,rows in [('SAME-RECORD',[(10,'a',None,True),(11,'b',None,True)]),('PARENT-RECORD',[(10,'x','a',True),(11,'y','b',True)]),('CARTESIAN',[(10,'x',None,True),(11,'y',None,True)])]:
 p={'rels':[{'from_node':'x','to_node':'y'}],'rules':[rule],'details':[None],'groups':{('x','SYMBOLIC-U-ONE'):G(rows),('y','SYMBOLIC-U-ONE'):G([(20,'a',None,True),(21,'b',None,True)])},'old_rel_n':0}
 pairs=list(env['pairs'](p,0,'SYMBOLIC-U-ONE'));expected=[(10,20),(11,21)] if rule!='CARTESIAN' else [(10,20),(10,21),(11,20),(11,21)];need(pairs==expected,'pairs');results.append({'rule':rule,'pairs':pairs,'result':'PASS'})
p['rules']=['NEAREST-DECLARED-ANCESTOR']
try:list(env['pairs'](p,0,'SYMBOLIC-U-ONE'))
except ValueError:results.append({'rule':'unlowered prospective operator','result':'REJECTED-AS-REQUIRED'})
else:raise AssertionError('unlowered operator accepted')
out.write_text(json.dumps({'checks':results,'scope':'fixture-normalized keys only; actual prospective full-model ranges/ledger remain unbound'},indent=2)+'\n');print('PASS',len(results))
