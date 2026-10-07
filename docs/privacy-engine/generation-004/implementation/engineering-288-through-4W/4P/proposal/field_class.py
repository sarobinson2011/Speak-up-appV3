"""Decision-only prototype. NOT imported by production ingestion or admission."""
import re

def field_class_ref(value,exact_register):
    ordinary=r'[A-Za-z0-9][A-Za-z0-9._:#-]*'
    spelling=isinstance(value,str) and (re.fullmatch(ordinary,value,re.ASCII) or re.fullmatch(ordinary+r'\.\$record',value,re.ASCII))
    return bool(spelling and value in exact_register)
