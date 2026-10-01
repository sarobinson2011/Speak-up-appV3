"""Exact UNION budget calculation. Does not qualify source facts or grant admission."""
from fractions import Fraction

def rational(value):
 if type(value) is not list or len(value)!=2 or any(type(x) is not int for x in value) or value[1]<=0 or not 0<=value[0]<=value[1]:raise ValueError('canonical probability pair')
 from math import gcd
 if gcd(*value)!=1:raise ValueError('noncanonical rational')
 return Fraction(*value)

def policy_maximum(value):
 limit=rational(value)
 if limit>=1:raise ValueError('computational maximum must be strictly below one')
 return limit

def union_budget(terms,maximum):
 limit=policy_maximum(maximum)
 if type(terms) is not list or not terms:raise ValueError('complete nonempty term list required')
 total=Fraction(0);seen=set()
 for t in terms:
  if type(t) is not dict or set(t)!={'argument_id','bound','multiplicity'}:raise ValueError('exact budget term')
  if type(t['argument_id']) is not str or not t['argument_id'] or t['argument_id'] in seen:raise ValueError('term identity')
  seen.add(t['argument_id'])
  if type(t['multiplicity']) is not int or t['multiplicity']<=0:raise ValueError('multiplicity')
  total+=rational(t['bound'])*t['multiplicity']
 total=min(total,Fraction(1))
 return {'bound':[total.numerator,total.denominator],'budget_result':'WITHIN' if total<=limit else 'EXCEEDED','source_facts_qualified':False,'profile_admitted':False}
