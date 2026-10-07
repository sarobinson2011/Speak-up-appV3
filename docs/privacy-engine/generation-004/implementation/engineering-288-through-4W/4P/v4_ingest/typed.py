"""S70 generic canonical TSEV1 value codec. No expressions or PE-TSE runtime."""
import re
from .records import primitive, require, ValidationError
from .wire import Reader, uint, lp

ROOTS = {'PE-TSE-BOOL3': 0, 'PE-TSE-BYTES': 1, 'PE-TSE-ID': 2, 'PE-TSE-UINT': 3}


class Codec:
    """Derived types are inserted in declaration order as (SET/TUPLE, children)."""
    def __init__(self, derived=()):
        self.types = {k: ('PRIMITIVE', ()) for k in ROOTS}
        for name, kind, children in derived:
            primitive('ID', name)
            require(name != 'SET' and name not in self.types, 'unique type ID')
            require(kind in ('SET', 'TUPLE') and type(children) in (list, tuple), 'derived type declaration')
            require(len(children) == 1 if kind == 'SET' else len(children) >= 2, 'derived arity')
            require(all(c in self.types for c in children), 'types require earlier children; no cycles')
            self.types[name] = kind, tuple(children)

    def encode(self, name, value):
        require(name in self.types, 'declared type required')
        kind, children = self.types[name]
        if kind == 'PRIMITIVE':
            tag = ROOTS[name]
            if name == 'PE-TSE-BOOL3':
                require(type(value) is str and value in ('FALSE', 'TRUE', 'UNRESOLVED'), 'BOOL3 symbolic value')
                body = bytes([('FALSE', 'TRUE', 'UNRESOLVED').index(value)])
            elif name == 'PE-TSE-BYTES':
                require(type(value) is bytes, 'BYTES octets')
                body = value
            elif name == 'PE-TSE-ID':
                primitive('ID', value)
                body = value.encode('ascii')
            else:
                primitive('UINT', value)
                body = str(value).encode('ascii')
        else:
            require(type(value) in (list, tuple), 'derived sequence')
            if kind == 'SET':
                tag = 0x10
                values = sorted(self.encode(children[0], v) for v in value)
                require(len(set(values)) == len(values), 'duplicate canonical SET element')
            else:
                tag = 0x11
                require(len(value) == len(children), 'TUPLE field count')
                values = [self.encode(t, v) for t, v in zip(children, value)]
            body = uint(len(values), 32) + b''.join(lp(v) for v in values)
        return b'TSEV1' + lp(name.encode('ascii'), 32) + bytes([tag]) + lp(body)

    def decode(self, raw, expected):
        require(expected in self.types, 'declared expected type')
        rd = Reader(raw)
        require(rd.take(5) == b'TSEV1', 'typed domain')
        require(rd.blob(32) == expected.encode('ascii'), 'exact type identity')
        tag, body = rd.take(1)[0], rd.blob()
        rd.end()
        kind, children = self.types[expected]
        if kind == 'PRIMITIVE':
            require(tag == ROOTS[expected], 'primitive kind octet')
            if expected == 'PE-TSE-BOOL3':
                require(body in (b'\x00', b'\x01', b'\x02'), 'canonical BOOL3 octet')
                value = ('FALSE', 'TRUE', 'UNRESOLVED')[body[0]]
            elif expected == 'PE-TSE-BYTES':
                value = body
            else:
                try:
                    text = body.decode('ascii')
                except UnicodeError as e:
                    raise ValidationError('typed ASCII body required') from e
                if expected == 'PE-TSE-ID':
                    primitive('ID', text)
                    value = text
                else:
                    require(re.fullmatch(r'0|[1-9][0-9]*', text) is not None, 'canonical UINT decimal')
                    try:
                        value = int(text)
                    except ValueError as e:
                        raise ValidationError('integer exceeds local implementation capacity', category='RESOURCE-LIMIT') from e
        else:
            require(tag == (0x10 if kind == 'SET' else 0x11), 'derived kind octet')
            br = Reader(body)
            count = br.number(32)
            require(count <= (len(body) - br.pos) // 8, 'impossible derived count')
            if kind == 'TUPLE':
                require(count == len(children), 'tuple count')
            encoded = [br.blob() for _ in range(count)]
            br.end()
            if kind == 'SET':
                require(encoded == sorted(set(encoded)), 'unique bytewise sorted SET')
            value = [self.decode(b, children[0] if kind == 'SET' else children[i]) for i, b in enumerate(encoded)]
        require(self.encode(expected, value) == raw, 'noncanonical typed value')
        return value
