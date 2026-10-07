"""Exact interval coverage and model potential stripes; no pair enumeration."""
from collections import Counter
from v4_ingest.records import require


def normalized(ranges, low, high):
    require(isinstance(ranges, list), 'coverage range list')
    out=[]
    for r in ranges:
        require(isinstance(r, list) and len(r)==2 and all(type(x) is int for x in r), 'integer half-open coverage interval')
        a,b=r;require(low<=a<b<=high, 'coverage interval outside exact model domain', category='INCOMPLETE-EVIDENCE-UNIVERSE')
        require(not out or out[-1][1]<a, 'canonical disjoint non-adjacent coverage intervals')
        out.append([a,b])
    return out


def union(parts):
    out=[]
    for a,b in sorted(r for part in parts for r in part):
        if out and a<=out[-1][1]:out[-1][1]=max(out[-1][1],b)
        else:out.append([a,b])
    return out


def contains(ranges, value):
    return any(a<=value<b for a,b in ranges)


def potential_stripe_counts(tokens):
    """Count all legal j>i for every i in O(N), preserving exact predicate."""
    fixed=Counter(t['symbolic_digest'] for t in tokens if not t['arbitrary'])
    arbitrary=sum(t['arbitrary'] for t in tokens);result=[]
    for i,t in enumerate(tokens):
        if t['arbitrary']:
            arbitrary-=1;result.append(len(tokens)-i-1)
        else:
            fixed[t['symbolic_digest']]-=1;result.append(arbitrary+fixed[t['symbolic_digest']])
    return result


def weighted_count(ranges, weights):
    return sum(sum(weights[a:b]) for a,b in ranges)
