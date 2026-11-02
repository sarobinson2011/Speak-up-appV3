"""Independent source/language expectations for the new slice only."""
import ast
from common import identity
ORDER=['inner-handler-departure-attempt','inner-handler-exit-complete','selected-loop-body-complete','final-iterator-advance-attempt','ordinary-iterator-exhaustion','cleanup-loop-complete']
NORMAL={s:('exhausted' if i==4 else 'normal') for i,s in enumerate(ORDER)}
def derive(raw):
 tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=next(n for n in ast.walk(fn) if isinstance(n,ast.ExceptHandler) and n.name=='e')
 assert ast.unparse(outer.type)=='BaseException'
 loop=next(n for n in outer.body if isinstance(n,ast.For));guard,=loop.body;protected,=guard.body;handler,=protected.handlers
 assert loop.lineno==169 and handler.lineno==172
 assert not loop.orelse and not guard.orelse and not protected.orelse and not protected.finalbody
 assert ast.unparse(loop.target)=='(name, obj)' and isinstance(loop.iter,ast.List)
 pairs=[]
 for item in loop.iter.elts:
  assert isinstance(item,ast.Tuple) and len(item.elts)==2
  label,ref=item.elts;assert type(label.value) is str and isinstance(ref,ast.Name);pairs.append([label.value,ref.id])
 assert pairs==[['raw','raw'],['managed','managed']]
 assert ast.unparse(guard.test)=='obj is not None'
 assert handler.name=='close_error' and ast.unparse(handler.type)=='BaseException'
 assert [ast.unparse(n) for n in protected.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"]
 stmt,=handler.body
 assert ast.unparse(stmt)=="details['cleanup'].append([name, type(close_error).__name__, str(close_error)])"
 assert not any(isinstance(n,(ast.Break,ast.Continue,ast.Return,ast.Yield,ast.YieldFrom)) for n in ast.walk(loop))
 pos=outer.body.index(loop);following=outer.body[pos+1]
 assert isinstance(following,ast.Try) and following.lineno==174
 def point(n):return {'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(raw.decode(),n),'source':identity(raw)}
 points=[handler,handler,guard,loop,loop.iter,loop]
 return {'order':ORDER.copy(),'normal_outcomes':NORMAL.copy(),'ordered_inputs':pairs,'entry_count':2,'selected_index':1,'next_index':2,'stages':{s:point(n) for s,n in zip(ORDER,points)},'loop':point(loop),'handler':point(handler),'stop_before':point(following.body[0].value),'target_names':['name','obj'],'caught_name':'close_error','outer_caught_name':'e','source_guards':['outer BaseException handler','exact two-entry for','obj is not None','inner BaseException handler'],'aggregate_departure':'Caught-name clearing and outer handled-exception restoration; no internal opcode order or physical destruction inferred','language_reference':'https://docs.python.org/3.12/reference/compound_stmts.html#the-for-statement; #except-clause'}
