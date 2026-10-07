"""Retained S70/S71 wire domains, without semantic evidence admission.

Helpers check representability before encoding. Row orders use minimum width;
closed comparison ordinals are separate. No full pair/graph construction here.
"""
import re
import unicodedata
from .records import require, primitive, digest, profile_identity, ValidationError

SCALAR_MODULUS = 21888242871839275222246405745257275088548364400416034343698204186575808495617
SIGN_DOMAIN = b'PE-TSE-PRIVACY-EVIDENCE-V2\n'
OBJECT_DOMAIN = b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'
PROFILE_DOMAIN = b'PE-TSE-IMMUTABLE-PROFILE-V1\n'
FILES = ('evidence.tsv', 'tokens.tsv', 'links.tsv', 'signature.txt')
MEMBERS = ('SOURCE-OWNED-BODY', 'EXPRESSION-PROGRAM', 'PRIVACY')
TOKEN_HEADER = 'token_order surface_id action_context_id token_id token_sha256 exposure permitted_reuse_class'.split()
LINK_HEADER = 'link_order from_token_id to_token_id relation_order relation_class'.split()
EVIDENCE_HEADER = 'evidence_id evidence_kind profile_id profile_sha256 scope_id component_id surface_template_sha256 relation_template_sha256 tokens_sha256 links_sha256 correlation_result uniqueness_result actor_reconstruction_result issued_by algorithm'.split()


def uint(n, bits):
    require(type(n) is int and type(bits) is int and bits in (32, 64) and 0 <= n < 2**bits, f'U{bits} overflow/type')
    return n.to_bytes(bits // 8, 'big')


def lp(raw, bits=64):
    require(type(raw) is bytes, 'octets required')
    return uint(len(raw), bits) + raw


def scalar(x):
    require(type(x) is int and 0 <= x < SCALAR_MODULUS, 'strict scalar domain; no field reduction')
    return x


def public_inputs(n, a, r):
    return tuple(scalar(v) for v in (n, a, r))


def row_order(n):
    require(type(n) is int and n > 0, 'positive one-based row order')
    return f'{n:06}'  # Minimum width; 1000000 is valid.


def ord6(n, allow_zero=False):
    require(type(n) is int and (0 if allow_zero else 1) <= n <= 999999, 'closed ORD6 domain')
    return f'{n:06}'


def model_wire_limits(token_count, largest_index, relation_order, pair_count, header_bytes):
    """Arithmetic representability only; does not claim model completeness.

    Callers supply actual counts later. U32 index permits 2**32 indexed tokens.
    Count/byte values used by L64 are U64. No table allocation is performed.
    """
    require(type(token_count) is int and 0 <= token_count <= 2**32, 'U32-indexed token count')
    if token_count:
        uint(largest_index, 32)
        require(largest_index == token_count - 1, 'contiguous largest index')
    else:
        require(largest_index is None, 'empty index sentinel')
    ord6(relation_order, allow_zero=True)
    uint(pair_count, 64)
    uint(header_bytes, 64)
    size = header_bytes + 8 * pair_count
    uint(size, 64)
    return size


class Reader:
    def __init__(self, raw):
        require(type(raw) is bytes, 'wire octets required')
        self.raw, self.pos = raw, 0

    def take(self, n):
        require(type(n) is int and 0 <= n <= len(self.raw) - self.pos, 'truncated wire value')
        result = self.raw[self.pos:self.pos + n]
        self.pos += n
        return result

    def number(self, bits=64):
        return int.from_bytes(self.take(bits // 8), 'big')

    def blob(self, bits=64):
        return self.take(self.number(bits))

    def end(self):
        require(self.pos == len(self.raw), 'trailing wire bytes')


def encode_container(members):
    require(isinstance(members, dict) and list(members) == list(MEMBERS), 'exact ordered three-member container')
    for v in members.values():
        require(type(v) is bytes and v, 'nonempty member octets')
    return PROFILE_DOMAIN + b''.join(lp(k.encode('ascii')) + lp(v) for k, v in members.items())


def decode_container(raw):
    from semantic_stream.storage import Blob
    if isinstance(raw, Blob):
        pos=0
        def take(n):
            nonlocal pos
            out=raw.slice(pos,n);pos+=n;return out
        def number():return int.from_bytes(take(8).small(), 'big')
        require(take(len(PROFILE_DOMAIN))==PROFILE_DOMAIN,'profile domain')
        out={}
        for name in MEMBERS:
            require(take(number())==name.encode(),'profile member order/name')
            out[name]=take(number());require(len(out[name])>0,'empty immutable member')
        require(pos==len(raw),'trailing wire bytes');return out
    rd = Reader(raw)
    require(rd.take(len(PROFILE_DOMAIN)) == PROFILE_DOMAIN, 'profile domain')
    members = {}
    for name in MEMBERS:
        require(rd.blob() == name.encode('ascii'), 'profile member order/name')
        members[name] = rd.blob()
        require(members[name], 'empty immutable member')
    rd.end()
    return members  # Raw member bytes only; no profile validation/admission.


def _files(files):
    require(isinstance(files, dict) and set(files) == set(FILES) and all(type(v) is bytes for v in files.values()), 'exact four-file V2 object')


def signature_preimage(files):
    _files(files)
    return SIGN_DOMAIN + b''.join(files[n] for n in FILES[:3])


def object_preimage(files):
    _files(files)
    return OBJECT_DOMAIN + b''.join(lp(files[n]) for n in FILES)


def object_digest(files):
    return digest(object_preimage(files))


def signature_line(raw):
    require(type(raw) is bytes, 'signature bytes')
    try:
        line = raw.decode('ascii')
    except UnicodeError as e:
        raise ValidationError('ASCII signature line required') from e
    match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._:#-]*) ([0-9a-f]{128})\n', line, re.ASCII)
    require(match is not None, 'exact authority-space-signature-LF grammar')
    return match[1], bytes.fromhex(match[2])


def verify_signature(files, public_key, authority_id):
    """Cryptographic byte authentication ONLY; caller key confers no appointment."""
    _files(files)
    primitive('ID', authority_id)
    require(type(public_key) is bytes and len(public_key) == 32, 'Ed25519 32-byte public key')
    issuer, sig = signature_line(files['signature.txt'])
    require(issuer == authority_id, 'signature authority identity mismatch')
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(sig, signature_preimage(files))
    except InvalidSignature as e:
        raise ValidationError('invalid Ed25519 signature', category='BYTE-AUTHENTICATION') from e
    return {'bytes_authenticated': True, 'source_authority_established': False, 'profile_admitted': False}


def read_table(raw, header):
    require(type(raw) is bytes, 'TSV bytes')
    try:
        text = raw.decode('utf-8')
    except UnicodeError as e:
        raise ValidationError('UTF-8 TSV required') from e
    require(text.endswith('\n') and '\r' not in text and not text.startswith('\ufeff') and unicodedata.normalize('NFC', text) == text, 'TSV UTF-8/NFC/no-BOM/no-CR/terminal-LF')
    lines = text[:-1].split('\n')
    require(lines[0] == '\t'.join(header), 'exact TSV header')
    rows = []
    for line in lines[1:]:
        cells = line.split('\t')
        require(len(cells) == len(header) and all(c and not c.endswith(' ') for c in cells), 'exact nonempty TSV cells; no blank rows/trailing space')
        rows.append(dict(zip(header, cells)))
    return rows


def ingest_tables(files, *, stream_links=False):
    """Parse fixed V2 tables, local syntax/joins/digests; no regenerated universe."""
    _files(files)
    e = read_table(files['evidence.tsv'], EVIDENCE_HEADER)
    ts = read_table(files['tokens.tsv'], TOKEN_HEADER)
    ls = None if stream_links else read_table(files['links.tsv'], LINK_HEADER)
    require(len(e) == 1, 'sole evidence row')
    row = e[0]
    for k, v in row.items():
        if k.endswith('sha256'):
            primitive('DIGEST', v, 'evidence.' + k)
        elif k.endswith('result'):
            require(v in ('PASS', 'FAIL'), 'result enum', 'evidence.' + k)
        elif k == 'evidence_kind':
            require(v in ('ADMISSION-COMPONENT', 'ADMISSION-COMPOSITION', 'COMPONENT', 'COMPOSITION'), 'evidence kind')
        elif k == 'algorithm':
            require(v == 'ED25519-RFC8032', 'signature algorithm')
        else:
            primitive('ID', v, 'evidence.' + k)
    authority, _ = signature_line(files['signature.txt'])
    profile_identity(row['profile_id'])
    composition = row['evidence_kind'].endswith('COMPOSITION')
    require((row['component_id'] == 'NOT-APPLICABLE') == composition, 'component/kind join')
    expected_scope = row['profile_id'] + ('#ADMISSION-V1' if row['evidence_kind'].startswith('ADMISSION-') else '#OCCURRENCE-SET-' + digest(files['tokens.tsv']))
    expected_id = row['profile_id'] + '#' + row['evidence_kind'] + '-' + ('ALL' if composition else row['component_id'])
    require(row['scope_id'] == expected_scope and row['evidence_id'] == expected_id, 'owning evidence identity/scope constructor')
    require(authority == row['issued_by'], 'signature/evidence issuer mismatch')
    require(row['tokens_sha256'] == digest(files['tokens.tsv']) and row['links_sha256'] == digest(files['links.tsv']), 'table digest mismatch')
    ids = set()
    for i, t in enumerate(ts, 1):
        require(t['token_order'] == row_order(i), 'contiguous token order')
        primitive('ID', t['action_context_id'])
        for k in ('surface_id','token_id'):
            require(bool(t[k]) and all(33<=ord(c)<=126 for c in t[k]), 'model-derived token/surface identifier framing')
        primitive('DIGEST', t['token_sha256'])
        require(t['token_id'] not in ids, 'duplicate token identity')
        ids.add(t['token_id'])
        require(t['exposure'] in ('PUBLIC', 'ACTION-BOUNDED', 'CONFIDENTIAL', 'PRIVATE-ACTOR'), 'exposure enum')
        require(t['permitted_reuse_class'] in ('NONE', 'GENERATION-CONSTANT'), 'reuse enum')
    if not stream_links:
        tuples = []
        for i, l in enumerate(ls, 1):
            require(l['link_order'] == row_order(i), 'contiguous link order')
            require(l['from_token_id'] in ids and l['to_token_id'] in ids, 'orphan link token')
            require(re.fullmatch(r'[0-9]{6}', l['relation_order']) is not None, 'closed relation ORD6')
            primitive('ID', l['relation_class'])
            if l['relation_order'] == '000000':
                require(l['relation_class'] == 'EQUALS', 'zero relation order is potential equality')
            tuples.append(tuple(l[k] for k in LINK_HEADER[1:]))
        require(tuples == sorted(set(tuples)), 'unique lexical signed link tuples')
    return {'evidence': row, 'tokens': ts, 'links': ls, 'object_sha256': object_digest(files),
            'byte_authentication_checked': False, 'link_validation_deferred': stream_links, 'model_validation_complete': False, 'profile_admitted': False}
