"""Bounded, noncanonical input to later expand/bind/finalize stages.
Does not construct the full symbolic model or assign source classifications.
"""
from common import *
from register import validate_register,BLOCKERS

def potential_equal(left,right):
 for r in [left,right]:boolean(r['arbitrary']);digest(r['symbolic_digest'])
 return left['arbitrary'] or right['arbitrary'] or left['symbolic_digest']==right['symbolic_digest']

def declarations(reg):
 validate_register(reg)
 spec=json.loads((ROOT/'reference/SCHEMA-SPEC.json').read_text())
 return {'format':'I164-RETRY3-MODEL-INPUT-1','schemas':spec['groups'],
  'fields':reg['fields'],'source_forms':sorted({r['source_file'] for r in reg['fields']}),
  'custody_columns':7,'custody_status':'UNKNOWN',
  'symbolic_context_requirement':{'count':2,'identities':'MUST-BIND-RETAINED-CONTEXTS','expansion':'NOT-EXECUTED'},
  'potential_equality':'left.arbitrary OR right.arbitrary OR equal symbolic_digest',
  'inherited_relationships_sha256':reg['relationships_43_sha256'],
  'local_directories':{'U':64,'stage':1,'attempt':102,'shared_slots_plus_holds':16,'stage_queries':2086,'extra_queries':16,'stage_backups':85,'events':12000,'blobs_arithmetic_envelope':460,'journal':384000,'shared_owners':4096},
  'lifetime_acquisition_directory':'UNESTABLISHED','canonical_registration':False,
  'full_expansion_permitted':False,'blockers':BLOCKERS,'actual_admission':False}

def validate_declarations(value,reg):same(value,declarations(reg),'MODEL-DECLARATION-SUBSTITUTION');return value

def occurrence_relations(rows):
 # Only exact observed containment. No speculative equality or authority edges.
 ids={r['id'] for r in rows};need(len(ids)==len(rows),'DUPLICATE-OCCURRENCE')
 return [{'from':r['id'],'to':r['parent'],'kind':'EXACT-OBSERVED-CONTAINMENT','qualified':False} for r in rows if r['parent'] is not None and r['parent'] in ids]
