# Privacy Engine Generation 2 Transition-State Equivalence Mapping and Profile Semantic Completion and Exact Construction-Basis Eighth Correction and Completion Determination V1

Identifier: PE-TRANSITION-STATE-EQUIVALENCE-MAPPING-AND-PROFILE-SEMANTIC-COMPLETION-AND-EXACT-CONSTRUCTION-BASIS-EIGHTH-CORRECTION-AND-COMPLETION-DETERMINATION-V1

Document version: V1

Engineering occurrence: Engineering[262]

Authority classification: development-authority-determination-non-protocol-non-publication

Status: exact proposed payload; author verification is recorded separately against its exact digest; not repository-materialized or independently accepted.

## 1. Scope and exact precedence

This eighth correction addresses E261-01 and E261-02 against Engineering[260]. Engineering[261] is the completed blocked independent review. Within the proposed successor construction basis, the marked E262 bodies and algorithms override conflicting E260/E258/E256/E254/E252/E250/E248/E246 text in that order, only within these bounded corrections; every unaffected inherited obligation remains. No prior committed artifact is edited. STATE.md remains the canonical implementation architecture and governance record. Published Generation 2 remains complete and immutable, M=0, I164 adoption not-performed and implementation readiness blocked-pending-published-successor-correction. The published G2 specification SHA-256 remains ffeaed785a34e8535d489ad6946dbdae3a55b441a0c94c8c05791eb33fd423e1.

The user authorized this bounded correction, its safe validation and repository completion workflow. That authorization does not appoint a real successor identity, mapping, profile, candidate, specification, publication, succession or adoption. The user-approved constant-edge-removal rule remains unchanged for correlation only, with complete evidence, prohibited parallel-path rejection, uniqueness and full-graph actor reconstruction.

## 2. Defect disposition register

| Finding | Governing correction and verification target |
|---|---|
| E261-01 | PRIVACY: re-admit the expression program; regenerate the complete privacy model; compare schemas, byfield, byid, relations and expression dependencies; structural mismatch is INVALID-PROFILE-SCHEMA. All subsequent component/composition scopes, owning-record joins, universe regeneration, evidence and graph checks use the same freshly regenerated model. Fully re-signed altered lookup evidence cannot pass. |
| E261-02 | TRACE: explicit section-body sets cover all inherited section assignments, including E246 section 12 and E248 section 12 atomicity. Exact block and parsed-cell rows name all governing ranges with one PRIMARY disposition and paired inverses. A clause-carrier audit records the exact text and complete collective destination set for every assigned block and cell. No unrecorded inter-body edge supplies closure. |

Engineering[261] report: SHA-256 d12844a9bb351fef4bbd4cf366ccd2cdd85e533dab150f3f5ebae034e12b83fb, 35942 bytes. E261 evidence archive: SHA-256 41e071dd8705f5b475accfb104ea39500a16d7e0420ef2bb165b750ded6eb53a, 4844963 bytes. Exact E260 payload: SHA-256 301efbbc1a0ed61a0564eaff8e4be8bb2287ddd583ab22825225b69dcf5a1887, 202316 bytes, 2568 LF.

E259-01 owning references, complete authorization digest and independently authenticated mapping facts remain required. E259-02 reserved identifiers and mutable expression-program re-admission remain required. E259-03 finding-level supplements remain; this correction extends their section-level closure. All E257, E255, E253, E251, D247/D249 and N01-N10 obligations remain, subject to their already recorded bounded corrections. The disproved E253 ownership arithmetic and unmatched-backtick diagnosis are not revived. V5 stays byte-identical; 745 retained plus 116 atoms gives 861 requirements, 2336 ownership rows and 3267 composition rows. All 40 serializers, 21 recovery rows, approved privacy graph rules and installation control transitions remain required.

The supplied corpus has 182 members; provenance has 71 Engineering records, 24 generic bindings and 109 changed-file identities (96 current, four historical-pack matches, nine unavailable historical versions). Supplied observations do not certify current remote state or every historical tree. The original N01-N10 report remains unavailable; its preserved definitions are neither discarded nor invented.

## 3. AUTHORITY

<!-- BEGIN E262-SEM-AUTHORITY -->
Published Generation 2 remains complete, immutable and unchanged. Correction can occur only through a distinct future successor. Privacy Engine is the implementation-independent authority. I164 is one bounded Speak-up-appV3 implementation; Speak Up is one application adapter and use case. Neither may define, narrow, repair, replace or become the protocol. M remains zero until separately authorized protocol-owned mappings and profiles exist.

These are proposed successor construction rules. They do not change published Generation 2, select a real successor identity, create a real candidate, perform a lifecycle act or adopt I164. Evaluation completion alone produces D and its occurrence evidence atomically. Failure produces none. Protocol semantic atomicity does not mandate a database, chain, transaction, implementation or runtime.

The procedure listings specify finite byte algorithms. Python notation and synthetic test adapters carry no protocol authority. A different implementation must reproduce the specified bytes and decisions. Synthetic source authority identifiers and test keys are author vectors only. Source authority, source-owned definitions, authenticated current facts, privacy-evidence appointment and installation authorization must be obtained from their separately governing source; possession of a key never appoints authority. A missing authority fact rejects admission and cannot be inferred from implementation behavior.
<!-- END E262-SEM-AUTHORITY -->

## 4. REGISTRY

<!-- BEGIN E262-SEM-REGISTRY -->
Registry identifier: {SUCCESSOR-NAMESPACE}-TRANSITION-MAPPING-REGISTRY-001.

Mapping identifier: {SUCCESSOR-NAMESPACE}-TMAP-{NNNNNN}.

Profile identifier: {SUCCESSOR-NAMESPACE}-TSE-PROFILE-{NNNNNN}-V0001.

The mapping and profile ordinals must be identical. One registry row binds exactly one mapping to exactly one profile. No mapping or profile can appear in more than one row. Replacement within one generation is prohibited.

The registry schema is:

registry_order, mapping_id, mapping_path, mapping_sha256, profile_id, profile_path, profile_sha256, applicability_definition_id, recovery_definition_id, status

Rows are ordered by registry_order contiguous from 000001 and equivalently by mapping_id byte order. status is closed-validated-normative-member. The empty serialization is exactly the header followed by LF and contains no data row. That empty registry authorizes zero transitions.


Mapping/profile byte admission precedes insertion. Registry order is ORD6 and unique mapping/profile ordinals agree. An admitted immutable profile is serialized as the container in E262-SEM-PRIVACY; its digest is computed before the mapping and registry that name it. Evidence of admission is external to that immutable container and signs its exact digest. M remains zero in this bounded 40-artifact construction. No sample mapping/profile is included as a candidate member.
<!-- END E262-SEM-REGISTRY -->

## 5. TYPES

<!-- BEGIN E262-SEM-TYPES -->
All text governed by this section is UTF-8 without BOM, Unicode NFC, LF-only, without trailing horizontal whitespace and with exactly one terminal LF. ASCII terminals are case-sensitive. Unsigned integers in text are canonical decimal: `0` or a non-zero digit followed by zero or more digits. Lowercase hexadecimal contains an even, non-zero number of characters from `0` through `9` and `a` through `f`.

The primitive type roots are exactly `PE-TSE-BOOL3`, `PE-TSE-BYTES`, `PE-TSE-ID` and `PE-TSE-UINT`. A derived type record has the exact TSV schema:

```text
type_order\ttype_id\tkind\telement_type_id\tfield_type_ids
```

`type_order` begins at `0001` and is contiguous. The four primitive roots occur first in the order shown. `kind` is `PRIMITIVE`, `SET` or `TUPLE`. A primitive row uses `NOT-APPLICABLE` in both final cells. A `SET` row names exactly one earlier type in `element_type_id` and uses `NOT-APPLICABLE` in `field_type_ids`. A `TUPLE` row uses `NOT-APPLICABLE` in `element_type_id` and names two or more earlier type IDs, comma-separated without spaces, in field order. Duplicate type IDs, forward references and cycles are invalid. There is no type whose literal identifier is `SET`.

Every typed value has one canonical octet encoding. `U32(n)` and `U64(n)` mean unsigned big-endian 32-bit and 64-bit encodings; overflow is invalid. `A(s)` means the ASCII bytes of `s`. `L32(x)` means `U32(len(x)) || x`; `L64(x)` means `U64(len(x)) || x`. The complete encoding is:

```text
A("TSEV1") || L32(A(type_id)) || kind_octet || L64(body)
```

The four primitive `kind_octet` values and bodies are:

| Type | Octet | Body |
|---|---|---|
| `PE-TSE-BOOL3` | `00` | `00` for FALSE, `01` for TRUE, `02` for UNRESOLVED |
| `PE-TSE-BYTES` | `01` | the represented octets, including the empty string when the owning component permits it |
| `PE-TSE-ID` | `02` | one nonempty ASCII identifier matching `[A-Za-z0-9][A-Za-z0-9._:#-]*`; its identity class applies its narrower grammar before encoding |
| `PE-TSE-UINT` | `03` | canonical decimal ASCII |

A derived `SET` uses `kind_octet = 10`. Its body is `U32(count)` followed by `L64(value)` for each distinct complete canonical element encoding, sorted by unsigned bytewise ascending order. A duplicate encoding is invalid. A derived `TUPLE` uses `kind_octet = 11`. Its body is `U32(field_count)` followed by `L64(value)` for each field in declared order. Each nested value must name the declared element or field type. These rules supply canonical bytes for every primitive and derived value.

The PE-TSE-EXPR-V2 grammar is the following complete ABNF; no Engineering[250] grammar is imported:

```text
expression = literal / argument / reference / tuple-expression / equal-expression / not-expression / and-expression / or-expression / member-expression / apply-expression / status-expression
literal = "literal(" type-id "," hex-bytes ")"
argument = "arg(" ord4 ")"
reference = "ref(" component-id "," side ")"
tuple-expression = "tuple(" type-id "," expression "," expression *( "," expression ) ")"
equal-expression = "equal(" expression "," expression ")"
not-expression = "not(" expression ")"
and-expression = "and(" expression *( "," expression ) ")"
or-expression = "or(" expression *( "," expression ) ")"
member-expression = "member(" expression "," definition-id ")"
apply-expression = "apply(" definition-id *( "," expression ) ")"
status-expression = status-op "(" component-id "," side ")"
status-op = "authoritative" / "available" / "valid" / "authenticated"
side = "AUTHORIZED" / "CURRENT"
ord4 = 4DIGIT
hex-bytes = 2HEXDIG *( 2HEXDIG )
```

ASCII space is prohibited inside an expression. `and` and `or` have at least one argument. `tuple` has at least two. `arg(0001)` denotes the first declared input; `0000`, an ordinal above the definition arity, or `arg` in a zero-input definition is invalid. `apply` evaluates argument expressions left-to-right, binds their canonical values to the callee's `arg` ordinals, and evaluates the callee in a new environment. No caller argument is visible except through those bindings.

`PE-TSE-SET` is a reserved built-in definition identifier and is not a definition record. It may occur only as `apply(PE-TSE-SET,<literal>...)` in a `SET` definition. Its arity is the number of literal arguments, including zero. All literals must have the output set type's element type; the result is the canonical set encoding above. `PE-TSE-SET` is forbidden in `definition_id`, source ownership and every other position.

E260 reserved-identifier completion: PE-TSE-SET is a reserved lexical identifier only for the admitted built-in apply position. Types, definitions, component/field/group IDs, source IDs/anchors, typed PE-TSE-ID values, Evaluation/Determination/read/evidence IDs and trusted appointment identifier fields must not equal it. Referenced type/definition names resolve only to admitted declarations. Opaque PE-TSE-BYTES data may contain arbitrary octets; this does not turn those octets into an identifier or prohibit documentary quotations. Literal SET is additionally forbidden as a type ID. The common identifier predicate and the admission/encoding callers below enforce this rule. Before any outer binding, revalidate_program rebuilds type declarations and the complete admitted program and checks its cached operation graph, so mutating a Python object cannot bypass declaration admission; source appointment cannot override it.

A literal is `literal(type-id,hex-bytes)`. `hex-bytes` decodes to one complete canonical typed-value encoding; its embedded `type_id` must equal the literal's `type-id`. A literal that is not canonical is invalid rather than normalized. `ref(component-id,side)` returns the component's authenticated represented value after its representation decoder, canonicalizer and normalizer have succeeded, as one complete canonical typed-value encoding of the component's `canonical_type_id`.

Definition records have the exact TSV schema:

```text
definition_order\tdefinition_id\tkind\tinput_type_ids\toutput_type_id\texpression\tsource_id\tsource_anchor
```

`definition_order` begins at `0001` and is contiguous. `kind` is `SET`, `CONDITION` or `FUNCTION`. `input_type_ids` is `NONE` or a comma-separated ordered list. A `SET` definition has `NONE` inputs, names an earlier derived type whose kind is `SET`, and has exactly one `apply(PE-TSE-SET,...)` expression. A `CONDITION` returns `PE-TSE-BOOL3`. A `FUNCTION` returns its declared type. Every definition names one owning successor source and anchor. Profile-local, implementation-owned and unresolved definitions are invalid. Admission uses the complete operation dependency graph generated by Profile._admit below, including member calls, every status stage and both component sides. Kahn traversal rejects any combined cycle. Definition IDs retain declared profile order for stable ordinals; it is the combined graph, not a contradictory reverse invocation ordering, that decides acyclicity.


Component records have the exact TSV schema:

```text
component_order\tcomponent_id\trepresented_type_id\trepresentation_decoder_definition_id\tcanonical_type_id\tcanonicalization_definition_id\tnormalization_definition_id\tauthority_source_id\tauthority_anchor\tavailability_condition_definition_id\tvalidity_condition_definition_id\tauthentication_definition_id\tprivacy_class\tobservability_class\tbinding_mode
```

`component_order` begins at `0001` and is contiguous. Every type and definition reference must resolve in the profile's closed type/definition tables. `privacy_class` is `PUBLIC`, `ACTION-BOUNDED` or `CONFIDENTIAL`. `observability_class` is `NONE`, `RESULT-ONLY` or `AUTHENTICATED-CONFIDENTIAL-COMPARISON-ONLY`. `binding_mode` is `CANONICAL-VALUE` or `BLINDED-SHA256-COMMITMENT`. The three condition/authentication definitions must return `PE-TSE-BOOL3`; decoder, canonicalizer and normalizer types must compose exactly from represented type to canonical type. `NONE` is forbidden in every component cell.

`apply` resolves either the reserved built-in above or one definition record, checks exact arity and input types, and evaluates it once in the bound argument environment. `member` requires a `SET` definition and compares complete canonical element encodings. `tuple(TYPE-ID,...)` constructs the explicitly named tuple type, including nested tuples, and requires its exact field count and types. The four status operators return `PE-TSE-BOOL3`. Failure, unavailable authority, failed authentication, invalid representation, noncanonical encoding, type failure or definition failure returns `NO-VALUE` for a non-Boolean result and `UNRESOLVED` for a Boolean result. `not`, `and` and `or` use Kleene strong three-valued truth tables. `equal` returns UNRESOLVED if either operand is NO-VALUE and otherwise compares complete canonical typed encodings. There are no other built-ins, references, substitutions, implicit conversions, collations, clocks, random sources or defaults.

The earlier scalar/profile ownership register remains:

Every profile contains the following scalar fields in this order:

profile-identifier, profile-version, governing-successor-generation, governing-mapping-identifier, profile-sha256-algorithm, projection-component-count, definition-count, equivalence-definition-id, material-conflict-definition-id, applicability-definition-id, determination-dependency-definition-id, comparison-timing-rule, execution-gate, commitment-gate, recovery-definition-id, privacy-classification, observability-classification

Field domains are:

- profile-identifier and governing-mapping-identifier use section 5 grammars and matching ordinals;
- profile-version is V0001;
- governing-successor-generation equals SUCCESSOR-GENERATION-ID;
- profile-sha256-algorithm is SHA-256;
- both counts are ORD6 canonical decimal counts matching their tables;
- every definition reference resolves uniquely within the profile;
- comparison-timing-rule is PRE-EXECUTION-AND-SEMANTIC-COMMITMENT;
- execution-gate and commitment-gate are EQUIVALENT-ONLY;
- privacy-classification is MINIMUM-ACTION-BOUNDED-NON-ACTOR;
- observability-classification is PUBLIC-RESULT-ONLY-NON-AUTHORITATIVE-DIAGNOSTICS.

The projection table schema is:

component_order, component_id, authoritative_source_id, authoritative_source_sha256, authoritative_source_anchor, component_type_definition_id, representation_definition_id, canonicalization_definition_id, normalization_definition_id, authorization_binding_mode, applicable_precondition_definition_ids, applicable_invariant_definition_ids, ordering_coordinate_definition_ids, dependency_coordinate_definition_ids, determination_dependency, equivalence_definition_id, immaterial_difference_definition_id, material_conflict_definition_id, authority_definition_id, availability_definition_id, validity_definition_id, authentication_definition_id, privacy_definition_id, observability_definition_id

component_order is contiguous ORD6. component_id uses LOCAL-ID and is unique. Definition lists are ordered comma-separated identifiers or NONE. authorization_binding_mode is CANONICAL-VALUE or BLINDED-SHA256-COMMITMENT. determination_dependency is INCLUDED or EXCLUDED and must agree with the determination-dependency definition.

The recovery table schema is:

recovery_order, stage, trigger, prerequisite_definition_id, disposition

stage is PRE-EXECUTION, EXECUTION or PRE-COMMITMENT. trigger is MATERIAL-CONFLICT, INDETERMINATE, EXECUTION-FAILURE or REVALIDATION-FAILURE. disposition is NEW-U-FROM-UNCHANGED-D or NEW-E-NEW-D-NEW-U. Rows are contiguous and must implement section 12's total function.

Profile validation rejects the profile unless every count, identity, digest, reference, type, expression, source anchor and cross-field constraint validates; the projection is proven minimal for the mapping; equivalence and conflict cannot both be true; every complete valid input is covered; every incomplete or untrusted evaluation becomes indeterminate; and no implementation-selected choice remains.


The E248 projection table describes the source-owned mapping obligations. Its component identity/order joins the E252 component program table one-to-one; canonical type, representation, canonicalization, normalization, conditions, source authority and binding mode must agree. E256 replaces E248's abbreviated recovery table with the exact 21-row function in E262-SEM-RECOVERY. The canonical spelling of the blinded mode is BLINDED-SHA256-COMMITMENT. CANONICAL-VALUE remains admitted. A legacy BLINDED-SHA256 input is migrated once at the component-mode boundary; serialized output always uses the canonical spelling.

The following complete executable notation governs V2 parsing, synthesis, all operation signatures, evaluation and occurrence bytes. Its dataclass defaults are confined to author fixtures; real source-owned rows must supply source and anchor explicitly and satisfy authenticated source ownership. ReadObject flags mean independently validated source facts, never assertions accepted from an unauthenticated caller. Invalid/missing source validation produces no successful Evaluation package; a comparison at a gate maps such validation failure to indeterminate under E262-SEM-COMPARISON.

### Constructor module: expr_v2.py

````python
"""E256 proposed deterministic expression/transcript construction.

This author model takes source-authenticated read objects as explicit inputs.
It does not appoint a source authority or infer authentication from a signature.
No profile or successor identity is selected by importing this module.
"""
from dataclasses import dataclass
from hashlib import sha256
import re
import json

NA='NOT-APPLICABLE'
B='PE-TSE-BOOL3';Y='PE-TSE-BYTES';I='PE-TSE-ID';U='PE-TSE-UINT'
PRIMITIVES=(B,Y,I,U)
ID=re.compile(r'[A-Za-z0-9][A-Za-z0-9._:#-]*\Z')
BUILTIN='PE-TSE-SET'
H=lambda b:sha256(b).hexdigest()
def need(ok,reason):
    if not ok:raise ValueError(reason)
def identifier(value):
    return isinstance(value,str) and bool(ID.fullmatch(value)) and value!=BUILTIN

def uint(n,width):
    need(isinstance(n,int) and 0<=n<1<<(8*width),'integer overflow')
    return n.to_bytes(width,'big')
def lp(b,width=8):return uint(len(b),width)+b
def tsv(header,rows):
    lines=[header,*rows]
    need(all(len(r)==len(header) for r in lines),'TSV arity')
    need(all(isinstance(c,str) and not any(x in c for x in '\t\r\n') for r in lines for c in r),'TSV cell')
    return ''.join('\t'.join(r)+'\n' for r in lines).encode()

class Types:
    def __init__(self,derived=()):
        self.rows={x:('PRIMITIVE',()) for x in PRIMITIVES}
        for name,kind,children in derived:
            need(identifier(name) and name not in self.rows and name!='SET','type identifier')
            need(kind in ('SET','TUPLE') and len(children)>=(1 if kind=='SET' else 2),'derived kind/arity')
            need(kind!='SET' or len(children)==1,'set arity')
            need(all(c in self.rows for c in children),'forward type')
            self.rows[name]=(kind,tuple(children))
    def encode(self,t,v):
        need(t in self.rows,'unknown type');kind,children=self.rows[t]
        if t==B:need(type(v)==int and v in (0,1,2),'BOOL3');octet=0;body=bytes([v])
        elif t==Y:need(isinstance(v,bytes),'BYTES');octet=1;body=v
        elif t==I:need(identifier(v),'ID');octet=2;body=v.encode('ascii')
        elif t==U:need(type(v)==int and v>=0,'UINT');octet=3;body=str(v).encode()
        elif kind=='SET':
            octet=16;values=sorted(v);need(len(values)==len(set(values)),'duplicate set value')
            for a in values:need(self.decode(a)[0]==children[0],'set element type')
            body=uint(len(values),4)+b''.join(lp(a) for a in values)
        else:
            octet=17;need(len(v)==len(children),'tuple arity')
            for a,c in zip(v,children):need(self.decode(a)[0]==c,'tuple field type')
            body=uint(len(v),4)+b''.join(lp(a) for a in v)
        return b'TSEV1'+lp(t.encode('ascii'),4)+bytes([octet])+lp(body)
    def decode(self,b):
        need(isinstance(b,bytes) and b.startswith(b'TSEV1'),'value header');pos=5
        def take(n):
            nonlocal pos
            need(pos+n<=len(b),'truncated value');v=b[pos:pos+n];pos+=n;return v
        def length(w):return int.from_bytes(take(w),'big')
        t=take(length(4)).decode('ascii');octet=take(1)[0];body=take(length(8));need(pos==len(b),'trailing value')
        need(t in self.rows,'value type');kind,children=self.rows[t]
        if t==B:need(len(body)==1 and body[0] in (0,1,2),'BOOL3 body');v=body[0]
        elif t==Y:v=body
        elif t==I:v=body.decode('ascii');need(bool(ID.fullmatch(v)),'ID body')
        elif t==U:need(bool(re.fullmatch(rb'0|[1-9][0-9]*',body)),'UINT body');v=int(body)
        else:
            need(len(body)>=4,'derived body');count=int.from_bytes(body[:4],'big');q=4;v=[]
            for _ in range(count):
                need(q+8<=len(body),'derived length');n=int.from_bytes(body[q:q+8],'big');q+=8
                need(q+n<=len(body),'derived data');v.append(body[q:q+n]);q+=n
            need(q==len(body),'derived trailing')
        # encode validates nested values, discriminator, canonical sort and grammar.
        need(self.encode(t,v)==b,'noncanonical value');return t,v

def parse(text):
    need(isinstance(text,str) and text.isascii() and not any(c.isspace() for c in text),'expression bytes')
    pos=0
    def atom():
        nonlocal pos
        start=pos
        while pos<len(text) and text[pos] not in ',()':pos+=1
        s=text[start:pos];need(bool(s),'empty expression token')
        if pos<len(text) and text[pos]=='(':
            pos+=1;args=[]
            if pos<len(text) and text[pos]!=')':
                while True:
                    args.append(atom())
                    if pos<len(text) and text[pos]==',':pos+=1;continue
                    break
            need(pos<len(text) and text[pos]==')','expression closing');pos+=1
            return (s,*args)
        return s
    value=atom();need(pos==len(text) and isinstance(value,tuple),'expression root');return value

@dataclass(frozen=True)
class Definition:
    id:str
    inputs:tuple
    output:str
    expression:tuple
    kind:str='FUNCTION'
    source:str='SYNTHETIC-SOURCE'
    anchor:str='synthetic-definition'

@dataclass(frozen=True)
class Component:
    id:str
    represented:str
    canonical:str
    decoder:str
    canonicalizer:str
    normalizer:str
    available:str
    valid:str
    authenticated:str
    source:str='SYNTHETIC-SOURCE'
    anchor:str='synthetic-component'

@dataclass(frozen=True)
class Field:
    id:str
    type:str
    equality:str
    source:str
    anchor:str

@dataclass(frozen=True)
class ReadObject:
    object_id:str
    value:bytes
    source:str
    anchor:str
    evidence_id:str
    evidence:bytes
    endpoint:bytes
    authoritative:bool=True
    valid:bool=True
    authenticated:bool=True

SIDES=('AUTHORIZED','CURRENT')
STAGES=('AUTHORITATIVE','AVAILABLE','VALID','AUTHENTICATED','DECODE','CANONICALIZE','NORMALIZE','PROJECT')
STATUSES={x.lower():x for x in STAGES[:4]}
EVENT_HEADER='event_order evaluation_id determination_id event_kind operation_id parent_event_order field_id object_id canonical_type_id canonical_sha256 authority_source_id authority_anchor authentication_evidence_id result'.split()
OP_HEADER='operation_order operation_id operation_kind expression_owner_id permitted_read_field_ids permitted_call_operation_ids owner_source_id owner_anchor'.split()

class Profile:
    def __init__(self,types,definitions,components,fields,root_definition,root_fields,groups=()):
        self.types=types;self.defs={d.id:d for d in definitions};self.components={c.id:c for c in components}
        need(len(definitions)<=9999 and len(components)<=9999,'profile ordinal overflow')
        need(len(self.defs)==len(definitions) and len(self.components)==len(components),'duplicate profile ID')
        self.def_order={d.id:i for i,d in enumerate(definitions,1)}
        self.comp_order={c.id:i for i,c in enumerate(components,1)}
        self.fields={f.id:f for f in fields};need(len(self.fields)==len(fields),'duplicate field')
        self.root_definition=root_definition;self.root_fields=tuple(root_fields);self.groups=tuple(groups)
        self.ops={};self.graph={};self._admit()
    def dop(self,d):return 'PE-TSE-OP-DEFINITION-'+f'{self.def_order[d]:04}'
    def sop(self,c,side,stage):return f'PE-TSE-OP-COMPONENT-{self.comp_order[c]:04}-{side}-{stage}'
    def fid(self,c,side,part):return f'PE-TSE-FIELD-COMPONENT-{self.comp_order[c]:04}-{side}-{part}'
    def synth(self,e,env,owner):
        need(isinstance(e,tuple) and len(e)>0,'AST node');op,*a=e
        def sub(x):return self.synth(x,env,owner)
        if op=='literal':
            need(len(a)==2 and a[0] in self.types.rows and isinstance(a[1],str) and bool(re.fullmatch('[0-9a-f]+',a[1])) and len(a[1])%2==0,'literal')
            need(self.types.decode(bytes.fromhex(a[1]))[0]==a[0],'literal type');return a[0]
        if op=='arg':
            need(len(a)==1 and isinstance(a[0],str) and bool(re.fullmatch('[0-9]{4}',a[0])) and 1<=int(a[0])<=len(env),'argument');return env[int(a[0])-1]
        if op=='ref' or op in STATUSES:
            need(len(a)==2 and a[0] in self.components and a[1] in SIDES,'component reference');return self.components[a[0]].canonical if op=='ref' else B
        if op=='tuple':
            need(len(a)>=3 and a[0] in self.types.rows,'tuple type');kind,children=self.types.rows[a[0]]
            need(kind=='TUPLE' and tuple(sub(x) for x in a[1:])==children,'tuple check');return a[0]
        if op=='equal':need(len(a)==2 and sub(a[0])==sub(a[1]),'equal types');return B
        if op in ('not','and','or'):
            need(len(a)>0 and (op!='not' or len(a)==1) and all(sub(x)==B for x in a),'logical operands');return B
        if op=='member':
            need(len(a)==2 and a[1] in self.defs,'member definition');d=self.defs[a[1]]
            need(d.kind=='SET' and sub(a[0])==self.types.rows[d.output][1][0],'member type');return B
        if op=='apply':
            need(len(a)>=1,'apply arity')
            if a[0]=='PE-TSE-SET':
                need(owner.kind=='SET' and e==owner.expression,'SET position');kind,children=self.types.rows[owner.output]
                need(kind=='SET' and all(isinstance(x,tuple) and x[0]=='literal' and sub(x)==children[0] for x in a[1:]),'SET literals');return owner.output
            need(a[0] in self.defs,'callee');d=self.defs[a[0]]
            need(tuple(sub(x) for x in a[1:])==d.inputs,'callee arguments');return d.output
        raise ValueError('unknown operator')
    def _ast_targets(self,e):
        reads=set();calls=set();op,*a=e
        if op in ('ref',*STATUSES):calls.add(self.sop(a[0],a[1],'PROJECT' if op=='ref' else STATUSES[op]))
        elif op=='apply' and a[0]!='PE-TSE-SET':calls.add(self.dop(a[0]))
        elif op=='member':calls.add(self.dop(a[1]))
        for x in a:
            if isinstance(x,tuple):
                r,c=self._ast_targets(x);reads|=r;calls|=c
        return reads,calls
    def _admit(self):
        # The built-in token is not an identifier in any declared ownership,
        # type, field, component, group or occurrence identity position.
        for d in self.defs.values():
            need(all(identifier(x) for x in (d.id,d.source,d.anchor)),'definition identifiers')
        for c in self.components.values():
            need(all(identifier(x) for x in (c.id,c.source,c.anchor)),'component identifiers')
        for f in self.fields.values():
            need(all(identifier(x) for x in (f.id,f.source,f.anchor)),'field identifiers')
        for gid,_,_ in self.groups:need(identifier(gid),'group identifier')
        need(self.root_definition in self.defs and all(f in self.fields for f in self.root_fields),'root binding')
        need(tuple(self.fields[f].type for f in self.root_fields)==self.defs[self.root_definition].inputs,'root input signature')
        for d in self.defs.values():
            need(d.id!='PE-TSE-SET' and bool(ID.fullmatch(d.id)) and d.kind in ('FUNCTION','CONDITION','SET'),'definition header')
            need(all(t in self.types.rows for t in (*d.inputs,d.output)),'definition types')
            need(d.kind!='CONDITION' or d.output==B,'condition result')
            need(d.kind!='SET' or (not d.inputs and self.types.rows[d.output][0]=='SET' and d.expression[0:2]==('apply','PE-TSE-SET')),'SET definition')
            need(self.synth(d.expression,d.inputs,d)==d.output,'definition result')
            if d.kind=='SET':self.types.encode(d.output,[bytes.fromhex(x[2]) for x in d.expression[2:]])
        for c in self.components.values():
            need(c.represented in self.types.rows and c.canonical in self.types.rows,'component types')
            for name,ins,out in [(c.decoder,(c.represented,),c.canonical),(c.canonicalizer,(c.canonical,),c.canonical),(c.normalizer,(c.canonical,),c.canonical),(c.available,(B,),B),(c.valid,(B,),B),(c.authenticated,(B,),B)]:
                need(name in self.defs and self.defs[name].inputs==ins and self.defs[name].output==out,'stage signature')
            for side in SIDES:
                for part,t in [('REPRESENTATION',c.represented),('VALUE',c.canonical),*[(f'STATUS-{s}',B) for s in STAGES[:4]]]:
                    f=self.fid(c.id,side,part)
                    need(f in self.fields and self.fields[f].type==t,'component field')
        def add(op,kind,owner,reads,calls,source,anchor):
            need(op not in self.ops,'operation duplicate')
            self.ops[op]=(kind,owner,set(reads),set(calls),source,anchor);self.graph[op]=set(calls)
        root=self.defs[self.root_definition]
        add('PE-TSE-OP-ROOT','EVALUATION-ROOT',root.id,self.root_fields,[self.dop(root.id)],root.source,root.anchor)
        for d in self.defs.values():
            reads,calls=self._ast_targets(d.expression);add(self.dop(d.id),'DEFINITION',d.id,reads,calls,d.source,d.anchor)
        for c in self.components.values():
            for side in SIDES:
                for stage in STAGES:
                    reads=[];calls=[]
                    if stage in STAGES[:4]:
                        reads=[self.fid(c.id,side,'STATUS-'+stage)]
                        if stage!='AUTHORITATIVE':calls=[self.dop(getattr(c,stage.lower()))]
                    elif stage=='DECODE':reads=[self.fid(c.id,side,'REPRESENTATION')];calls=[self.dop(c.decoder)]
                    elif stage=='CANONICALIZE':calls=[self.sop(c.id,side,'DECODE'),self.dop(c.canonicalizer)]
                    elif stage=='NORMALIZE':calls=[self.sop(c.id,side,'CANONICALIZE'),self.dop(c.normalizer)]
                    else:
                        reads=[self.fid(c.id,side,'VALUE')]
                        calls=[self.sop(c.id,side,s) for s in (*STAGES[:4],'NORMALIZE')]
                    add(self.sop(c.id,side,stage),'COMPONENT-STAGE',c.id,reads,calls,c.source,c.anchor)
        seen_fields=set()
        for gid,fields,rule in self.groups:
            need(len(fields)>=2 and len(set(fields))==len(fields) and not seen_fields.intersection(fields),'identity group fields')
            need(all(f in self.fields for f in fields),'identity group field reference');seen_fields.update(fields)
            ts={self.fields[f].type for f in fields};need(len(ts)==1 and rule in self.defs,'identity group type')
            need(len({self.fields[f].equality for f in fields})==1,'identity group semantic equality')
            d=self.defs[rule];t=next(iter(ts));need(d.inputs==(t,t) and d.output==B,'identity rule signature')
            self.ops['PE-TSE-OP-ROOT'][3].add(self.dop(rule));self.graph['PE-TSE-OP-ROOT'].add(self.dop(rule))
        # The complete operation graph includes status-definition and ref-stage edges.
        pending={k:set(v) for k,v in self.graph.items()};self.topology=[]
        need(all(v in pending for edges in pending.values() for v in edges),'unknown operation edge')
        while pending:
            ready=sorted(k for k,v in pending.items() if not v)
            need(bool(ready),'combined operation cycle');k=ready[0];self.topology.append(k);del pending[k]
            for edges in pending.values():edges.discard(k)
        for d in self.defs.values():
            def walk(e):
                op,*a=e
                if op=='member':need(self.def_order[a[1]]<self.def_order[d.id],'definition forward reference')
                if op=='apply' and a[0]!='PE-TSE-SET':need(self.def_order[a[0]]<self.def_order[d.id],'definition forward reference')
                for x in a:
                    if isinstance(x,tuple):walk(x)
            walk(d.expression)
        # Identity and semantic equality rules are pure: no external read or stage.
        def pure(op):
            reachable=set();todo=[op]
            while todo:
                x=todo.pop()
                if x in reachable:continue
                reachable.add(x);need(self.ops[x][0]=='DEFINITION' and not self.ops[x][2],'impure equality');todo.extend(self.graph[x])
        for _,_,rule in self.groups:pure(self.dop(rule))
        for f in self.fields.values():
            need(f.type in self.types.rows and f.equality in self.defs,'field type/equality')
            d=self.defs[f.equality];need(d.inputs==(f.type,f.type) and d.output==B,'semantic equality signature');pure(self.dop(d.id))
    def operation_bytes(self):
        return tsv(OP_HEADER,[[f'{i:04}',op,kind,owner,','.join(sorted(reads)) or 'NONE',','.join(sorted(calls)) or 'NONE',source,anchor] for i,(op,(kind,owner,reads,calls,source,anchor)) in enumerate(self.ops.items(),1)])


def revalidate_program(program):
    """Re-admit declarative rows before outer binding; mutable Python caches
    are not evidence that the immutable serialized program was admitted.
    """
    rows=list(program.types.rows.items())
    need([name for name,_ in rows[:4]]==list(PRIMITIVES),'primitive order')
    types=Types([(name,kind,children) for name,(kind,children) in rows[4:]])
    need(list(types.rows.items())==rows,'canonical type declarations')
    rebuilt=Profile(types,list(program.defs.values()),list(program.components.values()),list(program.fields.values()),program.root_definition,program.root_fields,program.groups)
    for name in ('defs','components','fields','def_order','comp_order','ops','graph','topology'):
        need(getattr(program,name)==getattr(rebuilt,name),('program re-admission',name))
    return rebuilt

class Evaluation:
    def __init__(self,p,objects,eid='SYNTHETIC-E',did='SYNTHETIC-D'):
        need(identifier(eid) and identifier(did),'occurrence identifiers')
        self.p=p;self.objects=objects;self.eid=eid;self.did=did;self.events=[];self.stack=[]
        self.invocations={};self.values={};self.reads={};self.returns={};self.group_instances=[];self.completed=None
    def event(self,kind,op,parent,field=NA,obj=NA,t=NA,digest=NA,source=NA,anchor=NA,auth=NA,result=NA):
        order=f'{len(self.events)+1:06}'
        self.events.append([order,self.eid,self.did,kind,op,f'{parent:06}',field,obj,t,digest,source,anchor,auth,result]);return int(order)
    def value_cells(self,v):
        if v is None:return NA,NA,'NO-VALUE'
        t,x=self.p.types.decode(v);self.values[H(v)]=v
        return t,H(v),('FALSE','TRUE','UNRESOLVED')[x] if t==B else 'VALUE'
    def read(self,field):
        op,enter=self.stack[-1];need(field in self.p.ops[op][2],'unadmitted read');f=self.p.fields[field]
        o=self.objects.get(field);need(o is not None,'missing authenticated read object')
        need(o.authoritative and o.valid and o.authenticated,'invalid read validation')
        need((o.source,o.anchor)==(f.source,f.anchor),'read authority')
        need(identifier(o.object_id) and identifier(o.evidence_id) and bool(o.evidence) and bool(o.endpoint),'read evidence')
        need(self.p.types.decode(o.value)[0]==f.type,'read canonical type')
        t,dg,result=self.value_cells(o.value)
        n=self.event('READ',op,enter,field,o.object_id,t,dg,o.source,o.anchor,o.evidence_id,result)
        self.reads[n]=(field,o);return o.value
    def invoke(self,op,args=(),root=False):
        kind,owner,_,_,source,anchor=self.p.ops[op]
        need(all(a is not None for a in args),'unresolved argument environment')
        bundle=uint(len(args),4)+b''.join(lp(a) for a in args)
        encoded=self.p.types.encode(Y,bundle);dg=H(encoded);self.values[dg]=encoded
        if root:parent=0;obj=self.eid+'-INPUT-000000'
        else:
            caller,ce=self.stack[-1];need(op in self.p.ops[caller][3],'unadmitted call')
            parent=self.event('CALL',op,ce,obj=self.eid+f'-INPUT-{len(self.events)+1:06}',t=Y,digest=dg,source=source,anchor=anchor,result='ARGUMENTS')
            obj=self.events[parent-1][7]
        self.invocations[obj]=encoded
        enter=self.event('ENTER',op,parent,obj=obj,t=Y,digest=dg,source=source,anchor=anchor,result='ARGUMENTS')
        self.stack.append((op,enter))
        if kind=='EVALUATION-ROOT':
            values=[self.read(f) for f in self.p.root_fields]
            result=self.invoke(self.p.dop(self.p.root_definition),values)
            self.make_groups()
        elif kind=='DEFINITION':
            d=self.p.defs[owner];need(tuple(self.p.types.decode(a)[0] for a in args)==d.inputs,'invocation argument types')
            result=self.eval(d.expression,args,d)
        else:result=self.stage(op)
        t,dg,res=self.value_cells(result)
        ret=self.event('RETURN',op,enter,obj=self.eid+f'-OP-{enter:06}',t=t,digest=dg,source=source,anchor=anchor,result=res)
        self.returns[enter]=(ret,result);self.stack.pop();return result
    def missing(self,t):return self.p.types.encode(B,2) if t==B else None
    def eval(self,e,args,owner):
        op,*a=e;T=self.p.types
        def ev(x):return self.eval(x,args,owner)
        if op=='literal':return bytes.fromhex(a[1])
        if op=='arg':return args[int(a[0])-1]
        if op=='ref' or op in STATUSES:return self.invoke(self.p.sop(a[0],a[1],'PROJECT' if op=='ref' else STATUSES[op]))
        if op=='tuple':
            v=[ev(x) for x in a[1:]];return None if any(x is None for x in v) else T.encode(a[0],v)
        if op=='equal':
            left=ev(a[0]);right=ev(a[1]);return T.encode(B,2 if left is None or right is None else int(left==right))
        if op=='not':
            x=T.decode(ev(a[0]))[1];return T.encode(B,{0:1,1:0,2:2}[x])
        if op in ('and','or'):
            seen=[]
            for x in a:
                v=T.decode(ev(x))[1];seen.append(v)
                if (op=='and' and v==0) or (op=='or' and v==1):return T.encode(B,v)
            return T.encode(B,2 if 2 in seen else (1 if op=='and' else 0))
        if op=='member':
            v=ev(a[0]);s=self.invoke(self.p.dop(a[1]));return T.encode(B,2 if v is None or s is None else int(v in T.decode(s)[1]))
        if op=='apply':
            v=[ev(x) for x in a[1:]]
            if a[0]=='PE-TSE-SET':return T.encode(owner.output,v)
            d=self.p.defs[a[0]]
            return self.missing(d.output) if any(x is None for x in v) else self.invoke(self.p.dop(d.id),v)
        raise ValueError('unhandled admitted expression')
    def stage(self,op):
        _,cid,_,_,_,_=self.p.ops[op];c=self.p.components[cid]
        tail=op.split(f'-{self.p.comp_order[cid]:04}-',1)[1];side,stage=tail.split('-',1)
        def call(s):return self.invoke(self.p.sop(cid,side,s))
        if stage in STAGES[:4]:
            value=self.read(self.p.fid(cid,side,'STATUS-'+stage))
            return value if stage=='AUTHORITATIVE' else self.invoke(self.p.dop(getattr(c,stage.lower())),[value])
        if stage=='DECODE':return self.invoke(self.p.dop(c.decoder),[self.read(self.p.fid(cid,side,'REPRESENTATION'))])
        if stage in ('CANONICALIZE','NORMALIZE'):
            value=call('DECODE' if stage=='CANONICALIZE' else 'CANONICALIZE')
            return self.missing(c.canonical) if value is None else self.invoke(self.p.dop(c.canonicalizer if stage=='CANONICALIZE' else c.normalizer),[value])
        for s in STAGES[:4]:
            if self.p.types.decode(call(s))[1]!=1:return self.missing(c.canonical)
        value=call('NORMALIZE');expected=self.read(self.p.fid(cid,side,'VALUE'))
        return value if value==expected else self.missing(c.canonical)
    def make_groups(self):
        for gid,fields,rule in self.p.groups:
            members=[n for n,(f,o) in self.reads.items() if f in fields]
            if len(members)<2:continue
            for i,a in enumerate(members):
                for b in members[i+1:]:
                    x=self.reads[a][1];y=self.reads[b][1]
                    need((x.source,x.anchor,x.value)==(y.source,y.anchor,y.value),'alias authority/value mismatch')
                    result=self.invoke(self.p.dop(rule),[x.value,y.value])
                    need(self.p.types.decode(result)==(B,1),'identity rule failed')
            self.group_instances.append((gid,tuple(members)))
    def run(self):
        try:
            value=self.invoke('PE-TSE-OP-ROOT',root=True)
            need(value is not None and self.p.types.decode(value)!=(B,2),'Evaluation incomplete')
            t,dg,result=self.value_cells(value);root=self.p.defs[self.p.root_definition]
            self.event('DETERMINATION','PE-TSE-OP-ROOT',1,obj=self.did,t=t,digest=dg,source=root.source,anchor=root.anchor,result=result)
            transcript=tsv(EVENT_HEADER,self.events)
            package=self.graph_bytes(transcript,value)
            self.completed=dict(transcript=transcript,determination=value,**package)
            return self.completed
        except Exception:
            self.completed=None
            raise
    def graph_bytes(self,transcript,determination):
        T=self.p.types;nodes={};edges=[];alias={};group_rows=[]
        rid=lambda n:self.eid+f'-READ-{n:06}'
        for i,(gid,members) in enumerate(self.group_instances,1):
            ids=[rid(n) for n in members];representative=min(ids)
            for node in ids:alias[node]=representative
            group_rows.append([f'{i:06}',self.eid+f'-IG-{i:06}',gid,','.join(ids),'TRUE'])
        def node(id,kind,value,obj,source,anchor,equality,aliases=()):
            t,_=T.decode(value)
            envelope=b''.join(lp(x.encode(),4) for x in [id,obj,t,H(value),source,anchor,*aliases])
            nodes[id]=(kind,value,obj,source,anchor,equality,tuple(aliases),envelope)
        root=self.p.defs[self.p.root_definition]
        node(self.did,'DETERMINATION',determination,self.did,root.source,root.anchor,'BYTE-IDENTITY')
        tid=self.eid+'-TRANSCRIPT';node(tid,'TRANSCRIPT',T.encode(Y,transcript),tid,root.source,root.anchor,'BYTE-IDENTITY')
        def edge(a,b,k,n,field):edges.append([a,b,k,f'{n:06}',field])
        for event in self.events:
            n=int(event[0]);kind=event[3];op=event[4];parent=int(event[5])
            if kind=='ENTER':
                oid=self.eid+f'-OP-{n:06}';ret,value=self.returns[n];t,dg,_=self.value_cells(value)
                body=lp(op.encode(),4)+uint(n,8)+lp(t.encode(),4)+lp(dg.encode(),4)
                source,anchor=self.p.ops[op][4:]
                node(oid,'OPERATION',T.encode(Y,body),op,source,anchor,'BYTE-IDENTITY')
                if parent==0:edge(self.did,oid,'DEFINITION',n,'determination')
                else:
                    caller=int(self.events[parent-1][5]);edge(self.eid+f'-OP-{caller:06}',oid,'DEFINITION',parent,'callee')
            elif kind=='READ':
                field,o=self.reads[n];raw=rid(n);id=alias.get(raw,raw)
                if id not in nodes:
                    members=[r for r,a in alias.items() if a==id] or [raw]
                    objects=sorted({self.reads[int(r.rsplit('-',1)[1])][1].object_id for r in members})
                    node(id,'READ',o.value,','.join(objects),o.source,o.anchor,self.p.fields[field].equality,sorted(members))
                aid=self.eid+f'-AUTH-{n:06}';sid=self.eid+f'-SOURCE-{n:06}'
                node(aid,'AUTHENTICATION',T.encode(Y,o.evidence),o.evidence_id,o.source,o.anchor,'BYTE-IDENTITY')
                node(sid,'AUTHORITY',T.encode(Y,o.endpoint),o.source,o.source,o.anchor,'BYTE-IDENTITY')
                edge(self.eid+f'-OP-{parent:06}',id,'VALUE',n,'value');edge(id,aid,'AUTHENTICATION',n,'authentication');edge(id,sid,'AUTHORITY',n,'authority')
            elif kind=='DETERMINATION':edge(self.did,tid,'PRODUCTION',n,'transcript')
        seen=set();unique=[]
        for e in edges:
            need(e[0] in nodes and e[1] in nodes and e[0]!=e[1],'edge endpoints')
            if tuple(e) not in seen:seen.add(tuple(e));unique.append(e)
        graph={n:set() for n in nodes}
        for a,b,*_ in unique:graph[a].add(b)
        todo=[self.did];closure=set()
        def visit(n,active):
            need(n not in active,'occurrence graph cycle')
            if n in closure:return
            active.add(n)
            for x in sorted(graph[n]):visit(x,active)
            active.remove(n);closure.add(n)
        visit(self.did,set());need(closure==set(nodes),'orphan occurrence node')
        node_rows=[];value_rows=[]
        for i,(id,(kind,value,obj,source,anchor,eq,aliases,envelope)) in enumerate(nodes.items(),1):
            node_rows.append([f'{i:06}',id,','.join(aliases) or 'NONE',obj,kind,T.decode(value)[0],H(value),H(envelope),source,anchor,eq])
            value_rows.append([id,value.hex(),envelope.hex()])
        return dict(
            groups=tsv('group_order identity_group_id group_template_id member_read_occurrence_ids identity_rule_result'.split(),group_rows),
            nodes=tsv('node_order node_id alias_read_occurrence_ids source_object_ids node_class canonical_type_id canonical_sha256 envelope_sha256 authority_source_id authority_anchor semantic_equality_definition_id'.split(),node_rows),
            values=tsv('node_id canonical_value_hex metadata_envelope_hex'.split(),value_rows),
            edges=tsv('edge_order from_node_id to_node_id dependency_class transcript_event_order production_field'.split(),[[f'{i:06}',*r] for i,r in enumerate(unique,1)]),
            invocations=tsv('invocation_id canonical_arguments_hex'.split(),[[k,v.hex()] for k,v in self.invocations.items()]),
            dep=tsv(['node_id'],[[n] for n in sorted(closure)]))

def replay(profile,objects,package,eid='SYNTHETIC-E',did='SYNTHETIC-D'):
    expected=Evaluation(profile,objects,eid,did).run()
    need(set(package)==set(expected) and all(package[k]==v for k,v in expected.items()),'occurrence replay mismatch')
    return True

def unchanged(profile,package,refreshed_objects,node_validation):
    """BOOL3 unchangedness; complete fresh authority/validity/authentication status.

    node_validation is source-validated evidence, with exactly one 0/1/2 value
    per existing closure node. It does not derive current authority from logs.
    Missing fresh object means unavailable (2); a proved mismatch dominates (0).
    """
    import csv,io
    rows=lambda b:list(csv.DictReader(io.StringIO(b.decode()),delimiter='\t'))
    nodes=rows(package['nodes']);ids={n['node_id'] for n in nodes}
    need(set(node_validation)==ids and all(type(x)==int and x in (0,1,2) for x in node_validation.values()),'fresh node validation domain')
    oldvalues={r['node_id']:bytes.fromhex(r['canonical_value_hex']) for r in rows(package['values'])}
    events={r['event_order']:r for r in rows(package['transcript']) if r['event_kind']=='READ'}
    unresolved=False
    for n in nodes:
        status=node_validation[n['node_id']]
        if status==0:return 0
        if status==2:unresolved=True;continue
        if n['node_class']!='READ':continue
        prior=oldvalues[n['node_id']]
        for alias in n['alias_read_occurrence_ids'].split(','):
            event=events[alias.rsplit('-',1)[1]];o=refreshed_objects.get(event['field_id'])
            if o is None:unresolved=True;continue
            if not (o.authoritative and o.valid and o.authenticated):return 0
            if (o.object_id,o.source,o.anchor)!=(event['object_id'],event['authority_source_id'],event['authority_anchor']):return 0
            try:t,_=profile.types.decode(o.value)
            except (ValueError,UnicodeError):return 0
            if t!=n['canonical_type_id'] or H(o.value)!=n['canonical_sha256']:return 0
            runner=Evaluation(profile,{})
            result=runner.invoke(profile.dop(n['semantic_equality_definition_id']),[prior,o.value],root=True)
            truth=profile.types.decode(result)[1]
            if truth==0:return 0
            if truth==2:unresolved=True
    return 2 if unresolved else 1
````
<!-- END E262-SEM-TYPES -->

## 6. DEPENDENCY

<!-- BEGIN E262-SEM-DEPENDENCY -->
The expr_v2 module in E262-SEM-TYPES is the exact E256 dependency constructor. Its OP_HEADER and EVENT_HEADER are literal ordered schemas; permitted read fields and permitted call operations are separate columns. Operation IDs are generated by dop and sop, root first, definitions in declared order, then component order, AUTHORIZED before CURRENT and STAGES order. Root arguments are reads of root_fields in that order. Every invocation stores the full canonical argument bundle; ENTER/CALL/RETURN events name its digest and exact bytes remain in the arguments table.

Component PROJECT first tests AUTHORITATIVE, AVAILABLE, VALID and AUTHENTICATED, then NORMALIZE and the authenticated canonical VALUE field. DECODE reads REPRESENTATION; CANONICALIZE calls DECODE; NORMALIZE calls CANONICALIZE. Each named function receives the one typed result of its preceding stage. The authenticated VALUE must equal normalized bytes. Status fields are real READ occurrences with source and evidence edges. Member calls invoke the zero-input SET operation and are recorded even when returning an empty set.

The Evaluation methods define every event cell, not an issuer-selected subset. A skipped branch produces no events. Each READ has a distinct event occurrence ID, even when object IDs repeat. Group templates expand to actual matching READ occurrence IDs; at least two observed members are required to form an instance. The pure typed binary identity function checks every pair. Only identical canonical values, types and authority may collapse; the lowest occurrence ID is the representative. The values table preserves canonical typed bytes and a separate metadata envelope and digest. No metadata envelope is passed to the component semantic-equality function.

Evaluation.run constructs D, transcript, arguments, groups, nodes, values, edges and dependency closure as one package. replay regenerates every byte from the admitted program and authenticated input objects and requires exact equality. An extra/missing event, argument, node, edge, value or alias fails replay. A failed Evaluation exposes no completed package. immutable prior occurrences remain immutable.

unchanged evaluates the entire actual dependency closure with a complete fresh validation-status map. A proved difference or invalidity yields FALSE; otherwise any unavailable validation or equality yields UNRESOLVED; only every matched identity, type, authority, canonical digest and TRUE semantic equality yields TRUE. This is a sufficient unchanged-D test, not permission to repair a failed U. Admitted but unexecuted operations have no occurrence dependency node.
<!-- END E262-SEM-DEPENDENCY -->

## 7. PRIVACY

<!-- BEGIN E262-SEM-PRIVACY -->
This section replaces the incomplete owning-schema and admission constructors. The six fixed schema registers and component field registers are defined by SCHEMAS and PrivacyProfile.schemas below. Field order is exact. AUTHORIZATION-HEADER uses its inherited 14 field values; its canonical authorization header remains the inherited field_order/field_name/field_value TSV, not a new commitment encoding. RECOVERY-RESULT.disposition encodes U classification ACTIVE, PRE-TRANSITION-FAILURE, TRANSITION-FAILURE or COMMITTED from the 21-row function; it is not a substitute for that function's authorization/E/D permissions. COMPONENT rows expose represented/canonical octets as lowercase hex. In canonical-value mode blind/opening are NOT-APPLICABLE. In blinded mode opening is L64(canonical bytes) followed by 32 raw blind octets, represented as lowercase hex. Source authentication of the opening remains mandatory.

Approved correlation amendment: regenerate the complete multigraph. For correlation reachability alone remove equality edges whose endpoints carry the same permitted non-NONE constant reuse class, validated from the owning literal or bounded-enumeration domain. Reject any remaining path joining PUBLIC tokens from distinct U contexts. No token or relation is removed from evidence. Parallel prohibited paths still reject. Uniqueness is unchanged. Actor reconstruction uses the full graph, including allowed constant equality edges. The user explicitly approved this bounded replacement of E254 section 4; the old any-mixed-path predicate is retained only for regression comparison and is not the governing procedure.

Owning constants are only the literal or closed-domain fields assigned by PrivacyProfile, with exact field/value checks in owning_records. Component IDs, types and ordinals are constants only within the immutable admitted profile. All other fields have NONE reuse. Public observability comprises only U and one of the five classification literals. Co-observed public fields have an explicit join. expression_relations conservatively traverses every AST branch, member and apply, and propagates argument dependencies; the issuer cannot choose relation rows.

Privacy label owner_source_id resolves the immutable profile namespace plus -SOURCE-SNN. Each privacy-schema-SCHEMA anchor is a virtual typed endpoint to the matching fixed schema register definition, or to the component schema generator for COMPONENT-ORD4, inside that source’s PRIVACY range. privacy-relation-constructor is the virtual typed endpoint to PrivacyProfile._relations in S70’s PRIVACY range. Virtual endpoints are digest-and-byte-range-bound; they are not nonexistent HTML anchors.

Static admission precedes registry insertion and is separate from occurrence evidence. It uses exactly two distinct symbolic U contexts, every owning field occurrence and potential equality of every arbitrary nonconstant cell. This conservative abstraction may reject safe profiles; it cannot be weakened by successful sampled occurrences. Occurrence evidence instead uses all exact authenticated owning records in the supplied comparison scope. Every nonconstant observable action record in that scope must be supplied; an unproven completeness boundary is invalid. Hash collision evidence rejects authorization; no digest assumption makes equality mathematically injective.

The canonical immutable profile container has the exact ordered members SOURCE-OWNED-BODY, EXPRESSION-PROGRAM and PRIVACY. Each member is L64(ASCII member name) followed by L64(exact bytes), after PE-TSE-IMMUTABLE-PROFILE-V1 and LF. SOURCE-OWNED-BODY is the canonical source-owned scalar and projection record serialization, not issuer prose: the 17 scalar fields above as field: SP value LF in their stated order, followed by the canonical projection TSV above and the exact 21-row recovery TSV. Counts and references bind the program; independently authenticated source ownership, projection minimality, comparison coverage and disjointness are admission prerequisites. No occurrence evidence belongs inside the profile. EXPRESSION-PROGRAM and PRIVACY canonical JSON generation is specified below; immutable bytes are final before the outside evidence signs their digest.

E258 cross-representation admission and occurrence joins: for each component ordinal, the expression-program component, source-owned projection row and privacy component register must agree on component identity, canonical type and binding mode before the outer profile can be admitted. Regeneration of internally inconsistent bytes is not validation. The earliest structural inconsistency is INVALID-PROFILE-SCHEMA.

Occurrence validation consumes a source-authenticated complete comparison-history list for each supplied U context. Its exact values are `{U-ID}-TSE-CMP-{ORD6}` contiguous from 000001; the current owning comparison attempt is the final list member. The authorization header's generation and mapping must equal the validated immutable source-owned body. A comparison-result row repeats the current attempt cells exactly. A recovery comparison event must use the same stage and result; execution-failure follows PRE-EXECUTION equivalent; revalidation-failure follows PRE-COMMITMENT indeterminate; commitment-success follows PRE-COMMITMENT equivalent. Public classification is the comparison result for comparison and commitment-success events, pre-transition-failure for that disposition, and transition-failure for the remaining terminal failure disposition. Missing authenticated history or a failed join is INVALID-ACTION-CONTEXT and cannot be repaired by regenerating signatures.

E260 owning-reference completion: authorization header successor-state-relation-definition-id must resolve in program.defs before evidence can pass. It must equal the relation selected by the independently authenticated immutable mapping. The authenticated_mapping input is an exact ordered fact view with MAPPING_FACT_FIELDS below. It is extracted from the governing mapping after independent source authentication, not appointed by a privacy signer and not a new mapping artifact or serializer. Its generation, mapping ID/digest, profile ID/digest, selected relation ID and exact input/output type signature are checked against the immutable body, header and admitted program. The relation is a source-owned CONDITION or FUNCTION returning PE-TSE-BOOL3; its argument types remain exactly source-defined. No new fixed arity or implementation-selected relation is introduced. Source ownership and anchor adequacy remain mandatory before this view is admitted. Missing, extra, unauthenticated or inconsistent mapping facts cannot be substituted with header assertions and yield INVALID-ACTION-CONTEXT.

The remaining owning-reference audit distinguishes decidable joins from external facts. Component IDs/types/order/modes, profile/scalar/projection references, generation/mapping/profile binding, complete authorization digest, occurrence-local comparison history, result/recovery attempt identity and outcome joins are checked mechanically. Comparison history is bounded to the six-digit ORD6 domain. Q0/current-state facts and coordinate values require independently authenticated protocol sources; their truth cannot be reconstructed from digest spelling or a privacy signature. The exact authorization byte constructor below permits the comparison attempt's authorization_sha256 to be recomputed, without adding that digest to its own preimage. No privacy PASS constitutes execution permission, and diagnostic inconsistency does not mutate an authoritative result.

E262 canonical decision model: the caller's Python profile and program objects are untrusted representations. Admission rebuilds the program from its declarative records and rebuilds the complete privacy model from those validated declarations. Schemas, byfield, byid, relations and expression dependencies must equal the regenerated structures; any mismatch contributes INVALID-PROFILE-SCHEMA, the earliest failure in ORDER. Existing byte, digest and surface-label checks remain. After checking the supplied outer binding, the validator discards the supplied profile for decision purposes. All subsequent authority, component/composition scope, owning-schema, occurrence, universe, label, disclosure, signature and graph checks consume the same fresh canonical model. No partially validated cache influences a result. Failure collection retains the existing ordered precedence. This does not authenticate source truth, appoint authority or prove external scope completeness.

The trusted privacy appointment is supplied outside the profile/evidence by the source authority: authority_id, algorithm, public_key, key_fingerprint_sha256, owner_source_id, owner_anchor. Exact appointment equality is tested before signature verification. No self-signed appointment is admitted. The unchanged V2 signed-payload and object-digest preimages are implemented below, without a self digest. Both admission and occurrence require a component bundle for every component plus composition; kind/scope cannot be interchanged. validate_closed is the governing integrated entrypoint. Lower-level validate is only its evidence subroutine. All detectable failures are collected and the earliest code in ORDER wins; a later malformed context cannot mask earlier invalid authentication. The failure-subset test tests ordering, not semantic completeness by itself.

### Constructor module: privacy_v2.py

````python
"""Proposed E256 finite privacy schema and evidence constructors.

Admission uses an explicit conservative two-context symbolic universe; occurrence
validation uses exact field bytes. Evidence is outside the immutable profile.
Correlation uses the user's approved constant-edge amendment. Actor testing
retains the complete graph, including permitted constant equality edges.
"""
from expr_v2 import H,lp,tsv,need,NA
from dataclasses import dataclass
from itertools import combinations,product
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from cryptography.exceptions import InvalidSignature
import json,re

SCHEMAS={
'AUTHORIZATION-HEADER':'serialization-domain successor-generation-id mapping-id mapping-sha256 profile-id profile-sha256 authorization-id transition-occurrence-id determination-id authorized-state-id successor-state-relation-definition-id ordering-coordinate-set-digest dependency-coordinate-set-digest component-count'.split(),
'COMPONENT-BINDING':'component_order component_id binding_mode canonical_type_id authorization_context_digest bound_value'.split(),
'COMPARISON-ATTEMPT':'comparison_attempt_id generation_id mapping_id mapping_sha256 profile_id profile_sha256 authorization_id authorization_sha256 transition_occurrence_id determination_id authorized_state_id authorized_state_sha256 current_state_id current_state_sha256 stage result failure_code'.split(),
'COMPARISON-RESULT':'comparison_attempt_id transition_occurrence_id result failure_code'.split(),
'RECOVERY-RESULT':'transition_occurrence_id comparison_attempt_id stage event unchanged_d_sufficiency disposition'.split(),
'OBSERVABILITY-OUTPUT':'transition_occurrence_id classification'.split(),
}
LABEL_HEADER='label_order schema_id field_order field_name exposure action_context_rule permitted_reuse_class derived_from_field_ids derivation_class owner_source_id owner_anchor'.split()
SURFACE_HEADER='surface_order surface_id record_class field_name exposure action_context_rule permitted_reuse_class derived_from_surface_ids derivation_class owner_source_id owner_anchor'.split()
REL_HEADER='relation_order from_surface_id to_surface_id relation_class condition_definition_id owner_source_id owner_anchor'.split()
TOKEN_HEADER='token_order surface_id action_context_id token_id token_sha256 exposure permitted_reuse_class'.split()
LINK_HEADER='link_order from_token_id to_token_id relation_order relation_class'.split()
EVIDENCE_HEADER='evidence_id evidence_kind profile_id profile_sha256 scope_id component_id surface_template_sha256 relation_template_sha256 tokens_sha256 links_sha256 correlation_result uniqueness_result actor_reconstruction_result issued_by algorithm'.split()
ORDER=['INVALID-PROFILE-SCHEMA','PROFILE-DIGEST-MISMATCH','INVALID-EVIDENCE-AUTHORITY','MISSING-EVIDENCE','INVALID-EVIDENCE-AUTHENTICATION','INVALID-EVIDENCE-DIGEST','INVALID-SURFACE-LABELS','INVALID-ACTION-CONTEXT','INCOMPLETE-EVIDENCE-UNIVERSE','COMPONENT-COUNT-MISMATCH','UNNECESSARY-COMPONENT','PUBLIC-PRIVATE-VALUE','REUSABLE-IDENTIFIER','OPENING-DISCLOSURE','UNIQUENESS-FAILURE','CORRELATION-FAILURE','ACTOR-RECONSTRUCTION-RISK','COMPONENT-FAILURE']
SCHEMA_OWNER={'AUTHORIZATION-HEADER':'S71','COMPONENT-BINDING':'S71','COMPARISON-ATTEMPT':'S72','COMPARISON-RESULT':'S72','RECOVERY-RESULT':'S72','OBSERVABILITY-OUTPUT':'S72'}
PUBLIC_CLASSES={'equivalent','material-conflict','indeterminate','pre-transition-failure','transition-failure'}
MODES={'CANONICAL-VALUE':'CANONICAL-VALUE','BLINDED-SHA256':'BLINDED-SHA256-COMMITMENT','BLINDED-SHA256-COMMITMENT':'BLINDED-SHA256-COMMITMENT'}

@dataclass(frozen=True)
class PrivacyComponent:
    id:str
    mode:str
    canonical_type:str
    necessity:str='PREDICATE-INPUT'
    privacy:str='CONFIDENTIAL'

@dataclass(frozen=True)
class Surface:
    order:int
    schema:str
    field:str
    exposure:str
    reuse:str
    domain:str
    component:str=NA
    @property
    def id(self):return f'PE-TSE-SURFACE-{self.order:06}'
    @property
    def field_id(self):return self.schema+'.'+self.field

class PrivacyProfile:
    def __init__(self,id,components,appointment,public_output=False,expression_dependencies=()):
        need(isinstance(id,str) and id.isascii() and id,'profile identity')
        need(len({c.id for c in components})==len(components),'component duplicate')
        need(type(public_output)==bool,'output exposure policy')
        self.id=id;self.components=tuple(components);self.appointment=dict(appointment);self.public_output=public_output
        self.expression_dependencies=tuple(expression_dependencies)
        self.schemas={k:list(v) for k,v in SCHEMAS.items()}
        for n,c in enumerate(components,1):
            need(c.mode in MODES and c.privacy in ('PUBLIC','ACTION-BOUNDED','CONFIDENTIAL','PRIVATE-ACTOR'),'component policy')
            self.schemas[f'COMPONENT-{n:04}']=['represented_value','canonical_value','blind','opening']
        self.surfaces=[]
        for schema,fields in self.schemas.items():
            for name in fields:
                exposure='PUBLIC' if schema=='OBSERVABILITY-OUTPUT' and public_output else 'CONFIDENTIAL'
                reuse='NONE';domain='OPAQUE';component=NA
                if name.replace('-','_')=='transition_occurrence_id':domain='ACTION-IDENTITY'
                if name in ('result','classification','failure_code','stage','event','unchanged_d_sufficiency','disposition','binding_mode','serialization-domain','canonical_type_id','component_id','component_order','component-count'):
                    reuse='GENERATION-CONSTANT';domain='CONSTANT:'+schema+'.'+name
                if schema.startswith('COMPONENT-0'):
                    c=components[int(schema[-4:])-1];component=c.id;domain='COMPONENT:'+c.id+'.'+name
                    if name in ('represented_value','canonical_value') and c.privacy in ('PUBLIC','PRIVATE-ACTOR'):exposure=c.privacy
                self.surfaces.append(Surface(len(self.surfaces)+1,schema,name,exposure,reuse,domain,component))
        self.byfield={s.field_id:s for s in self.surfaces};self.byid={s.id:s for s in self.surfaces}
        self.relations=self._relations()
        self.labels,self.surface_bytes,self.relation_bytes=self._tables()
        payload={'format':'PE-TSE-PRIVACY-PROFILE-CONSTRUCTION-V1','profile_id':id,
                 'components':[c.__dict__ for c in components],'appointment':appointment,'public_output':public_output,
                 'schemas':self.schemas,'expression_dependencies':self.expression_dependencies,
                 'labels_sha256':H(self.labels),'surfaces_sha256':H(self.surface_bytes),'relations_sha256':H(self.relation_bytes)}
        # This canonical JSON is the privacy subobject, not a replacement for the
        # complete future mapping/profile serializer. An outer digest binds it.
        self.bytes=(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
        self.sha256=H(self.bytes)
        self.binding_sha256=self.sha256
    def _relations(self):
        triples=set()
        def add(a,b,k):
            need(a in self.byfield and b in self.byfield,'relation field reference')
            if a!=b:triples.add((self.byfield[a].id,self.byfield[b].id,k))
        # Every same-named identity reference has a source-defined relationship.
        aliases={}
        for s in self.surfaces:aliases.setdefault(s.field.replace('-','_'),[]).append(s.field_id)
        for name,fields in aliases.items():
            if name.endswith('_id'):
                for a,b in combinations(fields,2):add(a,b,'REFERENCES')
        for n,c in enumerate(self.components,1):
            prefix=f'COMPONENT-{n:04}.'
            add(prefix+'represented_value',prefix+'canonical_value','DERIVES')
            add(prefix+'canonical_value','COMPONENT-BINDING.bound_value','ENCODES')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':
                add(prefix+'blind','COMPONENT-BINDING.bound_value','ENCODES')
                add(prefix+'canonical_value',prefix+'opening','ENCODES');add(prefix+'blind',prefix+'opening','ENCODES')
        for s in self.surfaces:
            if s.schema=='AUTHORIZATION-HEADER':add(s.field_id,'COMPONENT-BINDING.authorization_context_digest','DERIVES')
        add('COMPONENT-BINDING.authorization_context_digest','COMPONENT-BINDING.bound_value','ENCODES')
        add('COMPARISON-ATTEMPT.result','COMPARISON-RESULT.result','REFERENCES')
        add('COMPARISON-ATTEMPT.failure_code','COMPARISON-RESULT.failure_code','REFERENCES')
        add('COMPARISON-RESULT.result','OBSERVABILITY-OUTPUT.classification','DERIVES')
        add('COMPARISON-RESULT.failure_code','OBSERVABILITY-OUTPUT.classification','DERIVES')
        # Each entry is generated by the source-owned expression-AST walker,
        # identifying an exact input surface and output surface, not issuer prose.
        for a,b,k in self.expression_dependencies:
            need(k in ('REFERENCES','EQUALS','AUTHENTICATES','DERIVES'),'AST relation class');add(a,b,k)
        # Public fields co-observed in one output are observable joins.
        for schema in self.schemas:
            public=[s.field_id for s in self.surfaces if s.schema==schema and s.exposure=='PUBLIC']
            for a,b in combinations(public,2):add(a,b,'OBSERVABLY-JOINABLE')
        return sorted(triples)
    def _tables(self):
        labels=[];surfaces=[]
        for s in self.surfaces:
            namespace=self.id.split('-TSE-PROFILE-',1)[0] if '-TSE-PROFILE-' in self.id else 'SYNTHETIC'
            owner=namespace+'-SOURCE-'+SCHEMA_OWNER.get(s.schema,'S70');anchor='privacy-schema-'+s.schema.lower()
            derived=sorted(a for a,b,k in self.relations if b==s.id and k in ('DERIVES','ENCODES'))
            # Multiple derivation mechanisms remain separate relation rows; labels
            # declare the conservative DERIVES union, which is independently exact.
            dfields=[self.byid[a].field_id for a in derived];kind='DERIVES' if derived else NA
            labels.append([f'{s.order:06}',s.schema,f'{self.schemas[s.schema].index(s.field)+1:04}',s.field,s.exposure,'OCCURRENCE-U',s.reuse,','.join(dfields) or 'NONE',kind,owner,anchor])
            surfaces.append([f'{s.order:06}',s.id,s.schema,s.field,s.exposure,'OCCURRENCE-U',s.reuse,','.join(derived) or 'NONE',kind,owner,anchor])
        namespace=self.id.split('-TSE-PROFILE-',1)[0] if '-TSE-PROFILE-' in self.id else 'SYNTHETIC'
        relations=[[f'{i:06}',a,b,k,'ALWAYS',namespace+'-SOURCE-S70','privacy-relation-constructor'] for i,(a,b,k) in enumerate(self.relations,1)]
        return tsv(LABEL_HEADER,labels),tsv(SURFACE_HEADER,surfaces),tsv(REL_HEADER,relations)
    def schema_bytes(self):
        return tsv('schema_order schema_id field_order field_name'.split(),[[f'{i:04}',schema,f'{j:04}',f] for i,(schema,fields) in enumerate(self.schemas.items(),1) for j,f in enumerate(fields,1)])

@dataclass(frozen=True)
class Token:
    id:str
    surface:str
    context:str
    digest:str
    exposure:str
    reuse:str
    record:int

def universe(profile,contexts,admission=False):
    """contexts: ordered U -> schema -> exact ordered record dictionaries.

    Admission uses exactly two symbolic contexts. It instantiates every schema
    and permits potential equality among all non-fresh non-constant cells.
    That is deliberately conservative; PASS is not sampled occurrence success.
    """
    if admission:
        need(contexts is None,'admission context injection')
        contexts={f'{profile.id}-ADMISSION-U-{i:06}':None for i in (1,2)}
    else:
        need(isinstance(contexts,dict) and len(contexts)>0 and len(contexts)==len(set(contexts)),'action contexts')
        need(all(isinstance(c,str) and c and c.isascii() for c in contexts),'action context ID')
    tokens=[]
    for context,records in sorted(contexts.items()):
        if not admission:need(set(records)==set(profile.schemas),'owning schema universe')
        for schema,fields in profile.schemas.items():
            count=len(profile.components) if schema=='COMPONENT-BINDING' else 1
            if not admission:need(len(records[schema])==count,'record count')
            for j in range(count):
                if not admission:need(list(records[schema][j])==fields,'field order/universe')
                for f in fields:
                    s=profile.byfield[schema+'.'+f]
                    if admission:
                        value=('FRESH:'+context if s.domain=='ACTION-IDENTITY' else 'CONSTANT:'+s.domain if s.reuse!='NONE' else 'ARBITRARY').encode()
                    else:
                        value=records[schema][j][f];need(isinstance(value,str) and value and not any(x in value for x in '\t\r\n'),'field value')
                        if s.domain=='ACTION-IDENTITY':need(value==context,'action identity binding')
                        if schema=='OBSERVABILITY-OUTPUT' and f=='classification':need(value in PUBLIC_CLASSES,'public classification')
                        value=value.encode()
                    tokens.append(Token(f'TOKEN-{len(tokens)+1:06}',s.id,context,H(value),s.exposure,s.reuse,j+1))
    links=set()
    for order,(a,b,k) in enumerate(profile.relations,1):
        for x in tokens:
            if x.surface!=a:continue
            for y in tokens:
                if y.surface!=b or x.context!=y.context:continue
                sx=profile.byid[x.surface];sy=profile.byid[y.surface]
                # Generic binding fields instantiate only their owning component.
                if sx.schema=='COMPONENT-BINDING' and sy.component!=NA and profile.components[x.record-1].id!=sy.component:continue
                if sy.schema=='COMPONENT-BINDING' and sx.component!=NA and profile.components[y.record-1].id!=sx.component:continue
                links.add((x.id,y.id,f'{order:06}',k))
    for x,y in combinations(tokens,2):
        sx=profile.byid[x.surface];sy=profile.byid[y.surface]
        arbitrary=lambda s:s.domain!='ACTION-IDENTITY' and s.reuse=='NONE'
        possible=admission and (arbitrary(sx) or arbitrary(sy))
        if x.digest==y.digest or possible:links.add((x.id,y.id,'000000','EQUALS'))
    # Complete equality relation, including runtime matches, is never issuer-selected.
    return tokens,sorted(links)

def checks(tokens,links,*,inherited=False):
    byid={t.id:t for t in tokens};need(len(byid)==len(tokens),'duplicate token')
    graph={t.id:[] for t in tokens}
    for a,b,order,k in links:
        need(a in byid and b in byid and a!=b,'link endpoint')
        allowed=k=='EQUALS' and byid[a].reuse==byid[b].reuse and byid[a].reuse!='NONE'
        graph[a].append((b,allowed));graph[b].append((a,allowed))
    public=[t for t in tokens if t.exposure=='PUBLIC']
    uniqueness=not any(x.context!=y.context and x.digest==y.digest and not (x.reuse==y.reuse and x.reuse!='NONE') for x,y in combinations(public,2))
    # Preserve E254's any-edge-distinct-simple-path rule, including parallel edges.
    def bad_path(start,end):
        stack=[(start,frozenset([start]),False)]
        while stack:
            n,seen,bad=stack.pop()
            if n==end:
                if bad:return True
                continue
            for nxt,allowed in sorted(graph[n],reverse=True):
                if nxt not in seen:stack.append((nxt,seen|{nxt},bad or not allowed))
        return False
    if inherited:
        correlation=not any(bad_path(x.id,y.id) for x,y in combinations(public,2) if x.context!=y.context)
    else:
        correlation=True;remaining=set(graph)
        while remaining:
            visited=set();todo=[min(remaining)]
            while todo:
                n=todo.pop()
                if n in visited:continue
                visited.add(n);todo.extend(x for x,allowed in graph[n] if not allowed and x not in visited)
            remaining-=visited
            if len({byid[n].context for n in visited if byid[n].exposure=='PUBLIC'})>1:correlation=False;break
    actors={t.id for t in tokens if t.exposure=='PRIVATE-ACTOR'}
    actor=True
    for t in public:
        visited=set();todo=[t.id]
        while todo:
            n=todo.pop()
            if n in visited:continue
            visited.add(n);todo.extend(x for x,_ in graph[n] if x not in visited)
        if visited&actors:actor=False;break
    return {'correlation':correlation,'uniqueness':uniqueness,'actor_reconstruction':actor}

def token_bytes(tokens):
    return tsv(TOKEN_HEADER,[[f'{i:06}',t.surface,t.context,t.id,t.digest,t.exposure,t.reuse] for i,t in enumerate(tokens,1)])
def link_bytes(links):return tsv(LINK_HEADER,[[f'{i:06}',*row] for i,row in enumerate(links,1)])

def evidence(profile,tokens,links,key,admission=False,component=NA):
    if component!=NA:
        seed={t.id for t in tokens if profile.byid[t.surface].component==component};need(bool(seed),'component evidence scope')
        changed=True
        while changed:
            old=len(seed)
            for a,b,_,_ in links:
                if a in seed or b in seed:seed.update([a,b])
            changed=len(seed)!=old
        tokens=[t for t in tokens if t.id in seed];links=[r for r in links if r[0] in seed and r[1] in seed]
    tests=checks(tokens,links);tb=token_bytes(tokens);lb=link_bytes(links)
    kind=('ADMISSION-' if admission else '')+('COMPOSITION' if component==NA else 'COMPONENT')
    scope=profile.id+('#ADMISSION-V1' if admission else '#OCCURRENCE-SET-'+H(tb))
    eid=profile.id+'#'+kind+'-'+('ALL' if component==NA else component)
    row=[eid,kind,profile.id,profile.binding_sha256,scope,component,H(profile.surface_bytes),H(profile.relation_bytes),H(tb),H(lb),*['PASS' if tests[k] else 'FAIL' for k in ['correlation','uniqueness','actor_reconstruction']],profile.appointment['authority_id'],'ED25519-RFC8032']
    eb=tsv(EVIDENCE_HEADER,[row]);signed=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+eb+tb+lb
    sb=(profile.appointment['authority_id']+' '+key.sign(signed).hex()+'\n').encode()
    files={'evidence.tsv':eb,'tokens.tsv':tb,'links.tsv':lb,'signature.txt':sb}
    digest=H(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(lp(files[n]) for n in files))
    return files,digest

def validate(profile,trusted_appointment,files,digest,expected_tokens,expected_links,*,admission=False,component=NA,labels=None,components_pass=True):
    """Ordered fail selection; expected universe is independently regenerated.

    Full source appointment and complete outer profile identity must be validated
    before calling this subobject validator. No key possession appoints authority.
    """
    def fail(code):return ('FAIL',code)
    import csv,io
    try:
        need(isinstance(profile,PrivacyProfile),'profile object')
        need(profile.sha256==H(profile.bytes),'profile digest')
    except Exception:return fail('INVALID-PROFILE-SCHEMA')
    if profile.appointment!=trusted_appointment:return fail('INVALID-EVIDENCE-AUTHORITY')
    try:
        pk=bytes.fromhex(trusted_appointment['public_key'])
        need(len(pk)==32 and H(pk)==trusted_appointment['key_fingerprint_sha256'] and trusted_appointment['algorithm']=='ED25519-RFC8032','appointment key')
    except Exception:return fail('INVALID-EVIDENCE-AUTHORITY')
    if not files or set(files)!={'evidence.tsv','tokens.tsv','links.tsv','signature.txt'}:return fail('MISSING-EVIDENCE')
    try:
        line=files['signature.txt'].decode('ascii');a,s=line.rstrip('\n').split(' ')
        need(line.endswith('\n') and line.count('\n')==1 and a==trusted_appointment['authority_id'] and bool(re.fullmatch('[0-9a-f]{128}',s)),'signature line')
        signed=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+files['evidence.tsv']+files['tokens.tsv']+files['links.tsv']
        Ed25519PublicKey.from_public_bytes(pk).verify(bytes.fromhex(s),signed)
    except Exception:return fail('INVALID-EVIDENCE-AUTHENTICATION')
    computed=H(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n'+b''.join(lp(files[n]) for n in ['evidence.tsv','tokens.tsv','links.tsv','signature.txt']))
    if digest!=computed:return fail('INVALID-EVIDENCE-DIGEST')
    if labels is not None and labels!=profile.labels:return fail('INVALID-SURFACE-LABELS')
    try:
        rows=list(csv.DictReader(io.StringIO(files['evidence.tsv'].decode()),delimiter='\t'));need(len(rows)==1,'evidence rows');r=rows[0]
        if r['profile_sha256']!=profile.binding_sha256 or r['profile_id']!=profile.id:return fail('PROFILE-DIGEST-MISMATCH')
        tokens=expected_tokens;links=expected_links
        if component!=NA:
            seed={t.id for t in tokens if profile.byid[t.surface].component==component}
            while True:
                old=len(seed)
                for a,b,_,_ in links:
                    if a in seed or b in seed:seed.update([a,b])
                if len(seed)==old:break
            tokens=[t for t in tokens if t.id in seed];links=[r for r in links if r[0] in seed and r[1] in seed]
        kind=('ADMISSION-' if admission else '')+('COMPOSITION' if component==NA else 'COMPONENT')
        scope=profile.id+('#ADMISSION-V1' if admission else '#OCCURRENCE-SET-'+H(token_bytes(tokens)))
        need(r['evidence_kind']==kind and r['scope_id']==scope and r['component_id']==component,'evidence scope')
        need(r['surface_template_sha256']==H(profile.surface_bytes) and r['relation_template_sha256']==H(profile.relation_bytes),'template digests')
        need(files['tokens.tsv']==token_bytes(tokens) and files['links.tsv']==link_bytes(links),'universe equality')
        need(r['tokens_sha256']==H(files['tokens.tsv']) and r['links_sha256']==H(files['links.tsv']),'data digests')
    except Exception:return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    if any(c.necessity not in ('PREDICATE-INPUT','AUTHORIZATION-BINDING','ORDERING-COORDINATE','DEPENDENCY-COORDINATE') for c in profile.components):return fail('UNNECESSARY-COMPONENT')
    if any(c.privacy=='PRIVATE-ACTOR' for c in profile.components):return fail('PUBLIC-PRIVATE-VALUE')
    tests=checks(tokens,links)
    eid=profile.id+'#'+kind+'-'+('ALL' if component==NA else component)
    expected_row=[eid,kind,profile.id,profile.binding_sha256,scope,component,H(profile.surface_bytes),H(profile.relation_bytes),H(token_bytes(tokens)),H(link_bytes(links)),*['PASS' if tests[k] else 'FAIL' for k in ['correlation','uniqueness','actor_reconstruction']],profile.appointment['authority_id'],'ED25519-RFC8032']
    if files['evidence.tsv']!=tsv(EVIDENCE_HEADER,[expected_row]):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    for k,code in [('uniqueness','UNIQUENESS-FAILURE'),('correlation','CORRELATION-FAILURE'),('actor_reconstruction','ACTOR-RECONSTRUCTION-RISK')]:
        if not tests[k]:return fail(code)
    if any(r[k+'_result']!=('PASS' if tests[k] else 'FAIL') for k in tests):return fail('INCOMPLETE-EVIDENCE-UNIVERSE')
    if component==NA and not components_pass:return fail('COMPONENT-FAILURE')
    return ('PASS','NONE')
````

### Constructor module: profile_body.py

````python
"""Exact scalar/projection/recovery serialization for a future owning profile.

Authenticated source ownership and source-defined predicate adequacy are verified
before this byte constructor; this module never appoints those source authorities.
"""
from expr_v2 import need,tsv,NA,B
import re
SCALARS='profile-identifier profile-version governing-successor-generation governing-mapping-identifier profile-sha256-algorithm projection-component-count definition-count equivalence-definition-id material-conflict-definition-id applicability-definition-id determination-dependency-definition-id comparison-timing-rule execution-gate commitment-gate recovery-definition-id privacy-classification observability-classification'.split()
PROJECTION='component_order component_id authoritative_source_id authoritative_source_sha256 authoritative_source_anchor component_type_definition_id representation_definition_id canonicalization_definition_id normalization_definition_id authorization_binding_mode applicable_precondition_definition_ids applicable_invariant_definition_ids ordering_coordinate_definition_ids dependency_coordinate_definition_ids determination_dependency equivalence_definition_id immaterial_difference_definition_id material_conflict_definition_id authority_definition_id availability_definition_id validity_definition_id authentication_definition_id privacy_definition_id observability_definition_id'.split()
RECOVERY='recovery_order stage event unchanged_d_sufficiency u_classification authorization_disposition evaluation_required determination_required authorization_required u_required execute_permission commit_permission'.split()

def recovery_rows():
    rows=[]
    def add(stage,event,suff):
        if event=='commitment-success':tail=['COMMITTED','CONSUMED','SAME','SAME','NONE','NONE','PROHIBIT','COMPLETE']
        elif event=='equivalent':tail=['ACTIVE','PRESERVE','SAME','SAME','SAME','SAME','PERMIT' if stage=='PRE-EXECUTION' else 'PROHIBIT','PERMIT' if stage=='PRE-COMMITMENT' else 'PROHIBIT']
        else:tail=['PRE-TRANSITION-FAILURE' if stage=='PRE-EXECUTION' else 'TRANSITION-FAILURE','TERMINALLY-STALE','SAME' if suff=='TRUE' else 'NEW','SAME' if suff=='TRUE' else 'NEW-ON-SUCCESSFUL-COMPLETION','NEW','NEW','PROHIBIT','PROHIBIT']
        rows.append([f'{len(rows)+1:04}',stage,event,suff,*tail])
    for stage,events in [('PRE-EXECUTION',['equivalent','material-conflict','indeterminate']),('EXECUTION',['execution-failure']),('PRE-COMMITMENT',['equivalent','material-conflict','indeterminate','revalidation-failure']),('COMMITMENT',['commitment-success'])]:
        for event in events:
            for suff in ([NA] if event in ('equivalent','commitment-success') else ['TRUE','FALSE','UNRESOLVED']):add(stage,event,suff)
    return rows

def owning_body(scalars,projection,program,privacy,source_identities):
    """source_identities maps authenticated source IDs to exact SHA-256.

    Existence and contents of source anchors are checked against those supplied
    immutable sources before admission. No digest alone supplies authority.
    """
    need(list(scalars)==SCALARS,'scalar order')
    for v in scalars.values():need(isinstance(v,str) and v and not any(c in v for c in '\t\r\n'),'scalar bytes')
    m=re.fullmatch(r'(.+)-TSE-PROFILE-([0-9]{6})-V0001',scalars['profile-identifier'])
    need(m and int(m[2])>0 and scalars['profile-identifier']==privacy.id,'profile grammar')
    need(scalars['governing-mapping-identifier']==m[1]+'-TMAP-'+m[2],'mapping ordinal')
    need(bool(re.fullmatch(r'PE-PROTOCOL-GENERATION-[0-9]{3}',scalars['governing-successor-generation'])),'generation grammar')
    fixed={'profile-version':'V0001','profile-sha256-algorithm':'SHA-256','comparison-timing-rule':'PRE-EXECUTION-AND-SEMANTIC-COMMITMENT','execution-gate':'EQUIVALENT-ONLY','commitment-gate':'EQUIVALENT-ONLY','privacy-classification':'MINIMUM-ACTION-BOUNDED-NON-ACTOR','observability-classification':'PUBLIC-RESULT-ONLY-NON-AUTHORITATIVE-DIAGNOSTICS'}
    need(all(scalars[k]==v for k,v in fixed.items()),'scalar fixed domains')
    need(scalars['projection-component-count']==f'{len(program.components):06}' and scalars['definition-count']==f'{len(program.defs):06}','scalar counts')
    for f in ('equivalence-definition-id','material-conflict-definition-id','applicability-definition-id','determination-dependency-definition-id','recovery-definition-id'):
        need(scalars[f] in program.defs and program.defs[scalars[f]].output==B,'scalar definition reference')
    need(len(projection)==len(program.components)==len(privacy.components),'projection count')
    for i,(r,c,p) in enumerate(zip(projection,program.components.values(),privacy.components),1):
        need(list(r)==PROJECTION and r['component_order']==f'{i:06}' and r['component_id']==c.id==p.id,'projection identity')
        need(p.canonical_type==c.canonical,'cross-representation canonical type')
        need(r['authoritative_source_id']==c.source and r['authoritative_source_anchor']==c.anchor,'source owner')
        need(source_identities.get(c.source)==r['authoritative_source_sha256'] and bool(re.fullmatch('[0-9a-f]{64}',r['authoritative_source_sha256'])),'source digest binding')
        for f,expected in [('component_type_definition_id',c.canonical),('representation_definition_id',c.decoder),('canonicalization_definition_id',c.canonicalizer),('normalization_definition_id',c.normalizer),('availability_definition_id',c.available),('validity_definition_id',c.valid),('authentication_definition_id',c.authenticated)]:need(r[f]==expected,'component program binding')
        mode='BLINDED-SHA256-COMMITMENT' if p.mode=='BLINDED-SHA256' else p.mode
        need(r['authorization_binding_mode']==mode and r['determination_dependency'] in ('INCLUDED','EXCLUDED'),'projection domain')
        for f in ('applicable_precondition_definition_ids','applicable_invariant_definition_ids','ordering_coordinate_definition_ids','dependency_coordinate_definition_ids'):
            ids=[] if r[f]=='NONE' else r[f].split(',')
            need(len(ids)==len(set(ids)) and all(x in program.defs for x in ids),'projection definition list')
            need(ids==sorted(ids,key=program.def_order.get),'projection definition order')
        for f in ('equivalence_definition_id','immaterial_difference_definition_id','material_conflict_definition_id','authority_definition_id','privacy_definition_id','observability_definition_id'):
            need(r[f] in program.defs and program.defs[r[f]].output==B,'projection predicate')
    return ''.join(f'{k}: {scalars[k]}\n' for k in SCALARS).encode()+tsv(PROJECTION,[[r[k] for k in PROJECTION] for r in projection])+tsv(RECOVERY,recovery_rows())

def validate_body(data,program,privacy,source_identities):
    need(isinstance(data,bytes) and data.endswith(b'\n') and b'\r' not in data,'body bytes')
    lines=data.decode().splitlines();need(len(lines)>=17+1+len(program.components)+22,'body length')
    scalars={}
    for k,line in zip(SCALARS,lines[:17]):
        need(line.startswith(k+': '),'scalar line');scalars[k]=line[len(k)+2:]
    need(lines[17].split('\t')==PROJECTION,'projection header')
    projection=[]
    for line in lines[18:18+len(program.components)]:
        row=line.split('\t');need(len(row)==len(PROJECTION),'projection row');projection.append(dict(zip(PROJECTION,row)))
    need(data==owning_body(scalars,projection,program,privacy,source_identities),'canonical complete owning body')
    return scalars,projection
````

### Constructor module: privacy_admission.py

````python
"""Closed author-side admission/occurrence constructor for the E256 privacy model.

The immutable owning profile bytes and its source-appointed authority are inputs,
not objects this procedure may appoint. The caller must first validate the outer
profile against its governing source. This constructor binds that exact digest,
regenerates all privacy tables and evaluates both evidence scopes.
"""
from privacy_v2 import *
from expr_v2 import PRIMITIVES,Types,parse,identifier,B,revalidate_program
from profile_body import validate_body
import csv,io,unicodedata

FAILURES=tuple(ORDER)
FAILURE_INDEX={name:i for i,name in enumerate(FAILURES)}
def first_failure(failures):
    need(set(failures)<=set(FAILURES),'undeclared privacy failure')
    return min(failures,key=FAILURE_INDEX.get) if failures else 'NONE'

def expression_relations(program,components):
    """Conservative exact AST relation algorithm, including unused branches.

    arg flows come from caller operands; entry arguments range over component
    represented/canonical inputs. This over-approximation may reject a safe
    profile, but does not use a sampled execution to prove admission.
    """
    index={c.id:i for i,c in enumerate(components,1)}
    need(set(program.components)==set(index),'component program identity')
    result=set();all_inputs=set()
    for i in index.values():all_inputs.update([f'COMPONENT-{i:04}.represented_value',f'COMPONENT-{i:04}.canonical_value'])
    def walk(e,arguments):
        op,*a=e
        if op=='literal':return set()
        if op=='arg':return set(arguments[int(a[0])-1])
        if op=='ref' or op in ('available','authoritative','valid','authenticated'):
            field=f'COMPONENT-{index[a[0]]:04}.canonical_value'
            if op=='authenticated':result.add((field,'COMPARISON-ATTEMPT.result','AUTHENTICATES'))
            else:result.add((field,'COMPARISON-ATTEMPT.result','REFERENCES'))
            return {field}
        if op=='apply':
            inputs=[walk(x,arguments) for x in a[1:]]
            if a[0]=='PE-TSE-SET':return set().union(*inputs)
            return walk(program.defs[a[0]].expression,inputs)
        if op=='member':
            return walk(a[0],arguments)|walk(program.defs[a[1]].expression,[])
        children=[walk(x,arguments) for x in a if isinstance(x,tuple)]
        if op=='equal':
            for left in children[0]:
                for right in children[1]:
                    if left!=right:result.add((left,right,'EQUALS'))
        return set().union(*children)
    for definition in program.defs.values():
        sources=walk(definition.expression,[all_inputs for _ in definition.inputs])
        for source in sources:result.add((source,'COMPARISON-ATTEMPT.result','DERIVES'))
    return tuple(sorted(result))

def bind_program(profile,program):
    relations=expression_relations(program,profile.components)
    return PrivacyProfile(profile.id,profile.components,profile.appointment,profile.public_output,relations)

def bind_outer(profile,program,source_owned_body,source_identities):
    """Exact future-profile container; no occurrence/admission evidence member.

    source_owned_body is the already validated source-owned mapping/profile
    scalar body, including its existing identities, predicates and recovery
    bindings. This function neither invents nor validates those authority facts.
    The profile's governing source must validate that body before admission.
    """
    revalidate_program(program)
    need(isinstance(source_owned_body,bytes) and source_owned_body,'owning profile body')
    validate_body(source_owned_body,program,profile,source_identities)
    structures={'types':list(program.types.rows.items()),'definitions':[d.__dict__ for d in program.defs.values()],
                'components':[c.__dict__ for c in program.components.values()],'fields':[f.__dict__ for f in program.fields.values()],
                'root_definition':program.root_definition,'root_fields':program.root_fields,'groups':program.groups}
    pb=(json.dumps(structures,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
    members=[('SOURCE-OWNED-BODY',source_owned_body),('EXPRESSION-PROGRAM',pb),('PRIVACY',profile.bytes)]
    outer=b'PE-TSE-IMMUTABLE-PROFILE-V1\n'+b''.join(lp(name.encode())+lp(data) for name,data in members)
    profile.binding_sha256=H(outer)
    profile.outer_bytes=outer
    profile.source_identities=dict(source_identities)
    profile.source_owned_body=source_owned_body
    return outer

def read_tsv(b,header):
    need(isinstance(b,bytes) and b.endswith(b'\n') and not b.startswith(b'\xef\xbb\xbf') and b'\r' not in b,'TSV bytes')
    s=b.decode('utf-8');need(unicodedata.normalize('NFC',s)==s,'TSV NFC')
    lines=[line.split('\t') for line in s[:-1].split('\n')]
    need(lines and lines[0]==header and all(len(r)==len(header) and all(c for c in r) for r in lines),'TSV schema')
    return [dict(zip(header,r)) for r in lines[1:]]

MAPPING_FACT_FIELDS='generation_id mapping_id mapping_sha256 profile_id profile_sha256 successor_state_relation_definition_id successor_state_relation_input_type_ids successor_state_relation_output_type_id'.split()

def mapping_facts(profile,program,facts,scalars):
    """Facts are extracted from an independently authenticated immutable mapping.

    This view neither serializes nor appoints a mapping. Its definition role and
    signature are source-owned; the validator joins them to the admitted profile.
    """
    need(isinstance(facts,dict) and list(facts)==MAPPING_FACT_FIELDS,'mapping fact fields')
    for name,value in facts.items():
        need(isinstance(value,str) and value and value.isascii() and not any(c in value for c in '\t\r\n'),'mapping fact cell')
        if name.endswith('_sha256'):need(bool(re.fullmatch('[0-9a-f]{64}',value)),'mapping fact digest')
        if name.endswith('_id'):need(identifier(value),'mapping fact identifier')
    need(facts['generation_id']==scalars['governing-successor-generation'] and facts['mapping_id']==scalars['governing-mapping-identifier'],'mapping fact governing identity')
    need(facts['profile_id']==profile.id and facts['profile_sha256']==profile.binding_sha256,'mapping fact profile binding')
    relation=facts['successor_state_relation_definition_id']
    need(relation in program.defs,'mapping relation reference')
    definition=program.defs[relation]
    need(facts['successor_state_relation_input_type_ids']==(','.join(definition.inputs) or 'NONE'),'mapping relation input signature')
    need(facts['successor_state_relation_output_type_id']==definition.output==B,'mapping relation output signature')
    need(definition.kind in ('CONDITION','FUNCTION') and definition.source in profile.source_identities,'mapping relation source/role')
    return facts

def authorization_bytes(record):
    h=record['AUTHORIZATION-HEADER'][0]
    header=tsv(['field_order','field_name','field_value'],[[f'{i:04}',f,h[f]] for i,f in enumerate(SCHEMAS['AUTHORIZATION-HEADER'],1)])
    bindings=tsv(SCHEMAS['COMPONENT-BINDING'],[[r[f] for f in SCHEMAS['COMPONENT-BINDING']] for r in record['COMPONENT-BINDING']])
    return header+bindings

def owning_records(profile,contexts,program,comparison_history,authenticated_mapping):
    """Validate the complete six-schema occurrence records before tokenization.

    IDs/digests are authenticated protocol inputs, not inferred state. All known
    constants, scalar grammars, component ordinals and redundant bindings are
    checked here. Unknown record kinds and extra/missing fields are rejected.
    """
    need(isinstance(contexts,dict) and contexts,'contexts')
    need(isinstance(comparison_history,dict) and set(comparison_history)==set(contexts),'comparison history domain')
    scalars,_=validate_body(profile.source_owned_body,program,profile,profile.source_identities)
    facts=mapping_facts(profile,program,authenticated_mapping,scalars)
    for u,record in contexts.items():
        need(isinstance(u,str) and bool(re.fullmatch('[A-Za-z0-9][A-Za-z0-9._:#-]*',u)),'context ID')
        need(set(record)==set(profile.schemas),'owning schemas')
        for schema,fields in profile.schemas.items():
            count=len(profile.components) if schema=='COMPONENT-BINDING' else 1
            need(isinstance(record[schema],list) and len(record[schema])==count,'owning cardinality')
            for r in record[schema]:
                need(isinstance(r,dict) and list(r)==fields,'owning field order')
                for name,value in r.items():
                    need(isinstance(value,str) and value and unicodedata.normalize('NFC',value)==value and not any(c in value for c in '\t\r\n'),'owning cell')
                    n=name.replace('-','_')
                    if n.endswith(('_sha256','_digest')):need(bool(re.fullmatch('[0-9a-f]{64}',value)),'owning digest')
                    if n.endswith('_id'):need(identifier(value),'owning ID')
                    if n=='transition_occurrence_id':need(value==u,'owning U')
        h=record['AUTHORIZATION-HEADER'][0];attempt=record['COMPARISON-ATTEMPT'][0]
        result=record['COMPARISON-RESULT'][0];recovery=record['RECOVERY-RESULT'][0];obs=record['OBSERVABILITY-OUTPUT'][0]
        need(h['serialization-domain']=='PE-TSE-AUTHORIZATION-V1','authorization domain')
        need(h['successor-state-relation-definition-id'] in program.defs,'authorization relation reference')
        for header_name,fact_name in [('successor-generation-id','generation_id'),('mapping-id','mapping_id'),('mapping-sha256','mapping_sha256'),('profile-id','profile_id'),('profile-sha256','profile_sha256'),('successor-state-relation-definition-id','successor_state_relation_definition_id')]:
            need(h[header_name]==facts[fact_name],'authorization/mapping fact join')
        need(attempt['authorization_sha256']==H(authorization_bytes(record)),'complete authorization digest')
        need(h['profile-id']==profile.id and attempt['profile_id']==profile.id,'profile ID binding')
        need(h['successor-generation-id']==scalars['governing-successor-generation'],'generation/profile binding')
        need(h['mapping-id']==scalars['governing-mapping-identifier'],'mapping/profile binding')
        need(h['profile-sha256']==profile.binding_sha256,'immutable profile binding')
        need(h['successor-generation-id']==attempt['generation_id'],'generation binding')
        need(h['component-count']==f'{len(profile.components):06}','component count')
        for hn,an in [('mapping-id','mapping_id'),('mapping-sha256','mapping_sha256'),('profile-sha256','profile_sha256'),('authorization-id','authorization_id'),('determination-id','determination_id'),('authorized-state-id','authorized_state_id')]:
            need(h[hn]==attempt[an],'attempt authorization binding')
        need(attempt['stage'] in ('PRE-EXECUTION','PRE-COMMITMENT'),'attempt stage')
        need(attempt['result'] in ('equivalent','material-conflict','indeterminate'),'attempt result')
        history=comparison_history[u]
        need(isinstance(history,list) and 0<len(history)<=999999 and all(isinstance(x,str) for x in history),'comparison history')
        need(history==[f'{u}-TSE-CMP-{i:06}' for i in range(1,len(history)+1)],'comparison history contiguous')
        need(attempt['comparison_attempt_id']==history[-1],'current comparison history binding')
        comparison_codes={'NONE','INVALID-IDENTITY','UNREGISTERED-IDENTITY','DIGEST-MISMATCH','INVALID-PROFILE','INVALID-AUTHORIZATION','INVALID-OPENING','UNAUTHENTICATED-STATE','INCONSISTENT-BOTH-TRUE','INCOMPLETE-PROFILE-COVERAGE','UNRESOLVED-REQUIRED-INPUT'}
        need(attempt['failure_code'] in comparison_codes,'comparison code')
        need((attempt['result']=='indeterminate')==(attempt['failure_code']!='NONE'),'result failure binding')
        for n in ['comparison_attempt_id','transition_occurrence_id','result','failure_code']:need(result[n]==attempt[n],'result attempt binding')
        need(recovery['comparison_attempt_id']==attempt['comparison_attempt_id'],'recovery attempt binding')
        need(recovery['stage'] in ('PRE-EXECUTION','EXECUTION','PRE-COMMITMENT','COMMITMENT'),'recovery stage')
        need(recovery['unchanged_d_sufficiency'] in ('TRUE','FALSE','UNRESOLVED',NA),'recovery sufficiency')
        key=(recovery['stage'],recovery['event'],recovery['unchanged_d_sufficiency'])
        admitted={('PRE-EXECUTION','equivalent',NA):'ACTIVE',('PRE-COMMITMENT','equivalent',NA):'ACTIVE',('COMMITMENT','commitment-success',NA):'COMMITTED'}
        for stage,event in [('PRE-EXECUTION','material-conflict'),('PRE-EXECUTION','indeterminate'),('EXECUTION','execution-failure'),('PRE-COMMITMENT','material-conflict'),('PRE-COMMITMENT','indeterminate'),('PRE-COMMITMENT','revalidation-failure')]:
            for sufficiency in ('TRUE','FALSE','UNRESOLVED'):admitted[stage,event,sufficiency]='PRE-TRANSITION-FAILURE' if stage=='PRE-EXECUTION' else 'TRANSITION-FAILURE'
        need(key in admitted and recovery['disposition']==admitted[key],'recovery lookup')
        comparison_events=('equivalent','material-conflict','indeterminate')
        if recovery['event'] in comparison_events:
            need(recovery['stage']==attempt['stage'] and recovery['event']==attempt['result'],'recovery comparison binding')
        elif recovery['event']=='execution-failure':
            need(recovery['stage']=='EXECUTION' and attempt['stage']=='PRE-EXECUTION' and attempt['result']=='equivalent','execution failure binding')
        elif recovery['event']=='revalidation-failure':
            need(recovery['stage']=='PRE-COMMITMENT' and attempt['stage']=='PRE-COMMITMENT' and attempt['result']=='indeterminate','revalidation failure binding')
        else:
            need(recovery['event']=='commitment-success' and recovery['stage']=='COMMITMENT' and attempt['stage']=='PRE-COMMITMENT' and attempt['result']=='equivalent','commitment success binding')
        need(obs['classification'] in PUBLIC_CLASSES,'observability classification')
        if recovery['event'] in comparison_events or recovery['event']=='commitment-success':observable=attempt['result']
        else:observable='pre-transition-failure' if recovery['disposition']=='PRE-TRANSITION-FAILURE' else 'transition-failure'
        need(obs['classification']==observable,'observability result binding')
        header_bytes=tsv(['field_order','field_name','field_value'],[[f'{i:04}',f,h[f]] for i,f in enumerate(SCHEMAS['AUTHORIZATION-HEADER'],1)])
        for i,(binding,c) in enumerate(zip(record['COMPONENT-BINDING'],profile.components),1):
            need(binding['component_order']==f'{i:04}' and binding['component_id']==c.id and binding['canonical_type_id']==c.canonical_type,'component row binding')
            need(binding['binding_mode']==MODES[c.mode] and binding['authorization_context_digest']==H(header_bytes),'binding mode/context')
            need(bool(re.fullmatch('[0-9a-f]+',binding['bound_value'])) and len(binding['bound_value'])%2==0,'bound value')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':need(len(binding['bound_value'])==64,'commitment length')
            values=record[f'COMPONENT-{i:04}'][0]
            for name,value in values.items():
                if name in ('blind','opening') and MODES[c.mode]=='CANONICAL-VALUE':
                    need(value==NA,'canonical mode has no opening');continue
                need(bool(re.fullmatch('(?:[0-9a-f]{2})+',value)),'component value hex')
            canonical=bytes.fromhex(values['canonical_value']);represented=bytes.fromhex(values['represented_value'])
            need(program.types.decode(canonical)[0]==c.canonical_type,'canonical type')
            need(program.types.decode(represented)[0]==program.components[c.id].represented,'represented type')
            if MODES[c.mode]=='BLINDED-SHA256-COMMITMENT':
                need(len(values['blind'])==64,'blind length');blind=bytes.fromhex(values['blind'])
                opening=lp(canonical)+blind
                need(bytes.fromhex(values['opening'])==opening,'opening serialization')
                preimage=lp(b'PE-TSE-COMPONENT-COMMITMENT-V1')+bytes.fromhex(binding['authorization_context_digest'])+lp(c.id.encode())+lp(c.canonical_type.encode())+lp(canonical)+blind
                need(binding['bound_value']==H(preimage),'commitment preimage')
            else:need(binding['bound_value']==canonical.hex(),'canonical binding value')
    return contexts

def appointment_valid(appointment,trusted):
    try:
        need(appointment==trusted,'external appointment')
        need(set(trusted)=={'authority_id','algorithm','public_key','key_fingerprint_sha256','owner_source_id','owner_anchor'},'appointment fields')
        key=bytes.fromhex(trusted['public_key'])
        need(len(key)==32 and trusted['algorithm']=='ED25519-RFC8032' and H(key)==trusted['key_fingerprint_sha256'],'appointed key')
        need(all(isinstance(x,str) and x for x in trusted.values()),'appointment values')
        need(all(identifier(trusted[k]) for k in ('authority_id','owner_source_id','owner_anchor')),'appointment identifiers')
        return True
    except (ValueError,KeyError,TypeError):return False

def validate_closed(profile,program,trusted,evidence_objects,*,admission,contexts=None,comparison_history=None,authenticated_mapping=None,outer_profile_bytes=None,outer_profile_sha256=None):
    """Total ordered decision over structural, authority, evidence and policy gates.

    A bundle contains COMPOSITION plus every component, with no extras. Values
    are (four-file-object, object-digest). Admission and occurrence kinds cannot
    be interchanged. An optional outer binding must supply both exact bytes and
    digest; the privacy subobject remains the signed model identity in these
    author vectors. Full admission requires the outer binding produced by
    bind_outer; the lower-level subobject validator remains usable for vectors.
    """
    failures=set()
    try:
        program=revalidate_program(program)
        regenerated=bind_program(profile,program)
        validate_body(profile.source_owned_body,program,profile,profile.source_identities)
        regenerated_outer=bind_outer(regenerated,program,profile.source_owned_body,profile.source_identities)
        if regenerated_outer!=getattr(profile,'outer_bytes',None):failures.add('PROFILE-DIGEST-MISMATCH')
        if regenerated.bytes!=profile.bytes or regenerated.relation_bytes!=profile.relation_bytes:failures.add('INVALID-PROFILE-SCHEMA')
        if regenerated.labels!=profile.labels or regenerated.surface_bytes!=profile.surface_bytes or regenerated.surfaces!=profile.surfaces:failures.add('INVALID-SURFACE-LABELS')
        if H(profile.bytes)!=profile.sha256:failures.add('PROFILE-DIGEST-MISMATCH')
        # Every derived decision-bearing structure must agree. A malformed
        # cache is structural/schema failure, before signature or graph policy.
        for name in ('schemas','byfield','byid','relations','expression_dependencies'):
            if getattr(profile,name,None)!=getattr(regenerated,name):
                failures.add('INVALID-PROFILE-SCHEMA')
    except Exception:return ('FAIL','INVALID-PROFILE-SCHEMA')
    if not isinstance(outer_profile_bytes,bytes) or H(outer_profile_bytes)!=outer_profile_sha256 or outer_profile_sha256!=profile.binding_sha256 or outer_profile_bytes!=getattr(profile,'outer_bytes',None):failures.add('PROFILE-DIGEST-MISMATCH')
    # From here onward all scopes, universes, owning joins and policy checks
    # consume the same freshly rebuilt model, never the supplied caches.
    profile=regenerated
    if not appointment_valid(profile.appointment,trusted):failures.add('INVALID-EVIDENCE-AUTHORITY')
    expected={NA,*[c.id for c in profile.components]}
    if not isinstance(evidence_objects,dict) or set(evidence_objects)!=expected:failures.add('MISSING-EVIDENCE')
    try:
        if not admission:owning_records(profile,contexts,program,comparison_history,authenticated_mapping)
        tokens,links=universe(profile,contexts,admission=admission)
    except Exception:
        failures.add('INVALID-ACTION-CONTEXT');tokens=[];links=[]
    if any(c.necessity not in ('PREDICATE-INPUT','AUTHORIZATION-BINDING','ORDERING-COORDINATE','DEPENDENCY-COORDINATE') for c in profile.components):failures.add('UNNECESSARY-COMPONENT')
    if any(c.privacy=='PRIVATE-ACTOR' for c in profile.components):failures.add('PUBLIC-PRIVATE-VALUE')
    for s in profile.surfaces:
        if s.field in ('blind','opening') and s.exposure!='CONFIDENTIAL':failures.add('OPENING-DISCLOSURE')
        if s.exposure=='PUBLIC' and s.domain=='ACTION-IDENTITY' and s.reuse!='NONE':failures.add('REUSABLE-IDENTIFIER')
    if len(profile.components)!=len(program.components):failures.add('COMPONENT-COUNT-MISMATCH')
    # Collect independently testable failures before applying priority. In
    # particular, bad context cannot hide an earlier bad signature. The lower
    # verifier checks appointment before using its key.
    component_failed=False
    for component in [c.id for c in profile.components]+[NA]:
        try:
            if not isinstance(evidence_objects,dict) or component not in evidence_objects:continue
            files,digest=evidence_objects[component]
            # Byte equality below verifies every signed cell, including claimed results.
            verdict,code=validate(profile,trusted,files,digest,tokens,links,admission=admission,component=component,components_pass=not component_failed)
            if verdict!='PASS':
                failures.add(code)
                if component!=NA:component_failed=True
            r=read_tsv(files['evidence.tsv'],EVIDENCE_HEADER)
            need(len(r)==1,'evidence row count')
            if r[0]['profile_sha256']!=profile.binding_sha256 or r[0]['profile_id']!=profile.id:failures.add('PROFILE-DIGEST-MISMATCH')
        except Exception:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    return ('FAIL',first_failure(failures)) if failures else ('PASS','NONE')
````
<!-- END E262-SEM-PRIVACY -->

## 8. AUTHORIZATION

<!-- BEGIN E262-SEM-AUTHORIZATION -->
An authorization is the concatenation of the complete canonical header TSV and the complete COMPONENT-BINDING TSV, each with its exact header and terminal LF, with no separator or additional prefix between them. The component table has one ordered row per projection component. SHA-256 of these complete bytes is the comparison attempt authorization_sha256; it is not a field in its own preimage. The original header context digest and blinded-component preimage remain unchanged. The header schema is:

field_order, field_name, field_value

Its exact rows, in order, are:

0001 serialization-domain PE-TSE-AUTHORIZATION-V1
0002 successor-generation-id SUCCESSOR-GENERATION-ID
0003 mapping-id mapping identifier
0004 mapping-sha256 mapping digest
0005 profile-id profile identifier
0006 profile-sha256 profile digest
0007 authorization-id authorization identifier
0008 transition-occurrence-id U identifier
0009 determination-id D identifier
0010 authorized-state-id Q0 identifier
0011 successor-state-relation-definition-id profile definition reference
0012 ordering-coordinate-set-digest coordinate-set digest defined in this block
0013 dependency-coordinate-set-digest coordinate-set digest defined in this block
0014 component-count ORD6 count

Each literal label and value is UTF-8 NFC. The canonical header bytes are the canonical TSV header field_order, field_name, field_value plus those rows and one terminal LF. authorization-context-digest is SHA-256 of those bytes.

Ordering and dependency coordinate sets use schema coordinate_order, coordinate_definition_id, canonical_value_hex. Rows are contiguous, definition-unique and definition-order sorted. The set digest is SHA-256 of the complete canonical TSV including header and terminal LF. Empty sets are header-only TSVs, not omitted values.

The component-binding schema is:

component_order, component_id, binding_mode, canonical_type_id, authorization_context_digest, bound_value

For CANONICAL-VALUE, bound_value is lowercase hexadecimal of the exact normalized canonical bytes. For BLINDED-SHA256-COMMITMENT, it is the commitment digest from E262-SEM-COMMITMENT. The authorization is valid only when all profile components appear once in profile order and the context digest equals the recomputed header digest.
<!-- END E262-SEM-AUTHORIZATION -->

## 9. COMMITMENT

<!-- BEGIN E262-SEM-COMMITMENT -->
The algorithm identifier is PE-TSE-SHA256-COMMITMENT-V1. Its protocol-owned algorithm is SHA-256 as defined by FIPS PUB 180-4. An implementation convention cannot substitute or reinterpret it.

The blind is exactly 32 octets produced by a cryptographically secure random-bit generator whose security claim includes at least 256 bits of input entropy. It must be independently generated for each component and authorization, retained only as confidential opening material, never reused, never derived from actor, enrollment, admission, action, state or other blinds, and never disclosed outside an authorized comparison or independent privacy-validation boundary.

The commitment preimage contains, in order:

1. UTF-8 bytes PE-TSE-COMPONENT-COMMITMENT-V1;
2. authorization-context-digest as 32 raw octets;
3. component identifier UTF-8 bytes;
4. canonical type identifier UTF-8 bytes;
5. canonical component bytes;
6. the 32 raw blind octets.

Items 1, 3, 4 and 5 are encoded as unsigned 64-bit big-endian byte length followed by the exact bytes. Items 2 and 6 are raw fixed 32-octet values without length prefixes. The commitment is SHA-256 of the complete preimage and is textually represented by 64 lowercase hexadecimal characters.

Opening supplies the canonical component bytes and blind through the confidential comparison boundary. Verification recomputes the context digest, preimage and commitment; authenticates the opening source; and requires exact digest equality. The opened authorized value is then evaluated against the independently obtained current value using the profile's equivalence, immaterial-difference and material-conflict definitions. Commitment equality is neither required nor sufficient for semantic equivalence.

Missing, malformed, unauthenticated or mismatched openings, invalid algorithms, canonicalization failure and detected collision evidence produce indeterminate and prohibit execution and commitment. An observed pair of distinct preimages with equal digest invalidates every affected authorization and requires a future-generation algorithm change. Without such evidence, the commitment establishes computational binding only under SHA-256 collision resistance; it does not prove mathematical injectivity, actor identity, admission, provenance, broader state correctness or any unencoded fact.
<!-- END E262-SEM-COMMITMENT -->

## 10. COMPARISON

<!-- BEGIN E262-SEM-COMPARISON -->
Procedure identifier: PE-TSE-COMPARISON-V2.

Each comparison attempt identity is `{U-ID}-TSE-CMP-{ORD6}`. Ordinals begin `000001` and are contiguous within U. The exact attempt fields, in order, are attempt ID; generation ID; mapping ID and digest; profile ID and digest; authorization ID and digest; U ID; D ID; Q0 ID and digest; current-state ID and digest; stage; result; failure code. Stage is `PRE-EXECUTION` or `PRE-COMMITMENT`. Result is `equivalent`, `material-conflict` or `indeterminate`.

Evaluation executes in this order: validate identity grammar, registered relationships and digests; validate profile, authorization, opening evidence and state authentication; evaluate equivalence expression `EQ`; evaluate sufficient-conflict expressions in profile order, producing `MC=TRUE` if any is TRUE, `MC=FALSE` if all are FALSE and `MC=UNRESOLVED` otherwise; then select the first matching row:

| Condition | Result | Failure code |
|---|---|---|
| identity, relationship, digest, profile, authorization, opening or authentication failure | indeterminate | the exact validation failure |
| `EQ=TRUE` and `MC=TRUE` | indeterminate | `INCONSISTENT-BOTH-TRUE` |
| `MC=TRUE` | material-conflict | `NONE` |
| `EQ=TRUE` and `MC=FALSE` | equivalent | `NONE` |
| `EQ=FALSE` and `MC=FALSE` | indeterminate | `INCOMPLETE-PROFILE-COVERAGE` |
| otherwise | indeterminate | `UNRESOLVED-REQUIRED-INPUT` |

The closed comparison failure codes, in order, are `NONE`, `INVALID-IDENTITY`, `UNREGISTERED-IDENTITY`, `DIGEST-MISMATCH`, `INVALID-PROFILE`, `INVALID-AUTHORIZATION`, `INVALID-OPENING`, `UNAUTHENTICATED-STATE`, `INCONSISTENT-BOTH-TRUE`, `INCOMPLETE-PROFILE-COVERAGE` and `UNRESOLVED-REQUIRED-INPUT`. Every attempt produces one immutable result and one code. Only equivalent permits the next gate. An independently sufficient authenticated conflict remains material-conflict despite unrelated unresolved input. No validation failure yields equivalence or absence of a result.

Evaluation failure and comparison indeterminacy are distinct. A comparison returns one immutable classification and code; unsuccessful Evaluation cannot manufacture D or an authoritative dependency graph. Comparison at commitment and the commitment decision form one indivisible protocol-semantic boundary. No implementation transaction is elevated to protocol authority.
<!-- END E262-SEM-COMPARISON -->

## 11. RECOVERY

<!-- BEGIN E262-SEM-RECOVERY -->
The recovery TSV uses the literal header given below. It has exactly 21 data rows. There is no `ANY` token in serialized output.

| Order | Stage | Event | D sufficiency | U classification | Authorization | Evaluation | D | Authorization required | U required | Execute | Commit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0001 | PRE-EXECUTION | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PERMIT | PROHIBIT |
| 0002 | PRE-EXECUTION | material-conflict | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0003 | PRE-EXECUTION | material-conflict | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0004 | PRE-EXECUTION | material-conflict | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0005 | PRE-EXECUTION | indeterminate | TRUE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0006 | PRE-EXECUTION | indeterminate | FALSE | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0007 | PRE-EXECUTION | indeterminate | UNRESOLVED | PRE-TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0008 | EXECUTION | execution-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0009 | EXECUTION | execution-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0010 | EXECUTION | execution-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0011 | PRE-COMMITMENT | equivalent | NOT-APPLICABLE | ACTIVE | PRESERVE | SAME | SAME | SAME | SAME | PROHIBIT | PERMIT |
| 0012 | PRE-COMMITMENT | material-conflict | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0013 | PRE-COMMITMENT | material-conflict | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0014 | PRE-COMMITMENT | material-conflict | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0015 | PRE-COMMITMENT | indeterminate | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0016 | PRE-COMMITMENT | indeterminate | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0017 | PRE-COMMITMENT | indeterminate | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0018 | PRE-COMMITMENT | revalidation-failure | TRUE | TRANSITION-FAILURE | TERMINALLY-STALE | SAME | SAME | NEW | NEW | PROHIBIT | PROHIBIT |
| 0019 | PRE-COMMITMENT | revalidation-failure | FALSE | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0020 | PRE-COMMITMENT | revalidation-failure | UNRESOLVED | TRANSITION-FAILURE | TERMINALLY-STALE | NEW | NEW-ON-SUCCESSFUL-COMPLETION | NEW | NEW | PROHIBIT | PROHIBIT |
| 0021 | COMMITMENT | commitment-success | NOT-APPLICABLE | COMMITTED | CONSUMED | SAME | SAME | NONE | NONE | PROHIBIT | COMPLETE |

The lookup key is the exact triple `(stage,event,unchanged_d_sufficiency)`. For `equivalent` and `commitment-success`, sufficiency must be `NOT-APPLICABLE`; for every other event it must be TRUE, FALSE or UNRESOLVED. Exactly one row therefore matches every admitted event. Unmatched or multiply matched input is invalid and yields no permission. `NEW-ON-SUCCESSFUL-COMPLETION` retains the Engineering[250] meaning. No failed U may be repaired, resumed, reactivated or committed.

The exact recovery header, with spaces below denoting TAB, is:

```text
recovery_order stage event unchanged_d_sufficiency u_classification authorization_disposition evaluation_required determination_required authorization_required u_required execute_permission commit_permission
```

The Markdown table above supplies its 21 rows in order without transformation. An indeterminate comparison does not prove substantive state conflict or invalidity. The terminal stale authorization follows the failed bounded U disposition; it does not retrospectively alter D or a prior successful Evaluation. New Evaluation produces new D only on successful completion. No failed U is resumed, repaired, reactivated or committed.
<!-- END E262-SEM-RECOVERY -->

## 12. REQUIREMENTS

<!-- BEGIN E262-SEM-REQUIREMENTS -->
REQDATA-V4 retains its historical identity: 44811 bytes, 211 LF, SHA-256 58f90e18a3ddd950cd053cdd2ffa7426f5057c0af30dae78450a2ae16e3dd837. V5 changes exactly four normative-text cells: TSEPROF-003 input and its one atom replace PE-TSE-EXPR-V1 with PE-TSE-EXPR-V2; STALEAUTH-002 input and its one atom replace “the section 7 comparison” with “the PE-TSE-COMPARISON-V2 procedure”. Each old token must occur exactly once. The stream header becomes PE-TSE-REQDATA-V5. No other cell changes.

V5: 44831 bytes, 211 LF, SHA-256 10b16fdcbe7ee2fb701836ea51a1c0111930a58b36ec03293c9527ac4ff1ce72. The constructor below preserves the 92 inputs, 116 atoms, 745 retained requirements, 861 final rows and strengths 565 MUST / 278 MUST NOT / 18 MAY. It uses the literal expansion register, not a prose splitter. N01's two TSEAPP atoms and N02's four complete STALEAUTH atoms are preserved. N10's existing 50 RF/16 SF allocation is unchanged by these version/reference substitutions.

Ownership is by distinct SNN per requirement, never by source-anchor segment. The 184 atom anchor segments contain 18 excess source occurrences and yield 166 ownership rows. Retained rows yield 2170, total 2336. Composition has 70 + 2336 + 861 = 3267 rows. Source-local requirements include retained rows and atoms. Source and inventory serializers are sibling consumers of this external dataset, never consumers of each other's output.

### Constructor module: construction.py

````python
"""Noncanonical E256 construction work. No repository or lifecycle operations."""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter

BASE = Path(__file__).resolve().parent.parent / 'eng260-input'
CORPUS = BASE.parent / 'corpus'
PREFIX = 'PRIVACY_ENGINE_GENERATION_2_TRANSITION_STATE_EQUIVALENCE_MAPPING_AND_PROFILE_SEMANTIC_COMPLETION_AND_EXACT_CONSTRUCTION_BASIS_'
H = lambda b: hashlib.sha256(b).hexdigest()

def doc(suffix):
    return (CORPUS/'docs'/(PREFIX+suffix+'_DETERMINATION_V1.md')).read_text()

def section(text, number):
    m = re.search(r'^## '+str(number)+r'\. .*?\n(.*?)(?=^## [0-9]+\. |\Z)', text, re.M|re.S)
    if not m:
        raise ValueError(('missing section', number))
    return m[1]

def table(text):
    # Used only for the inspected E248 input and E252 expansion registers;
    # no unescaped inner pipe occurs in their cells.
    return [[c.strip() for c in l.strip('|').split('|')] for l in text.splitlines() if l.startswith('|')]

def tsv(header, rows):
    rows = [header, *rows]
    if any(len(row)!=len(header) or any(any(c in str(v) for c in '\t\r\n') for v in row) for row in rows):
        raise ValueError('invalid TSV cell or arity')
    return ''.join('\t'.join(map(str,row))+'\n' for row in rows).encode()

TRANSFORMS = {
    'TSEPROF-003': ('PE-TSE-EXPR-V1', 'PE-TSE-EXPR-V2'),
    'STALEAUTH-002': ('the section 7 comparison', 'the PE-TSE-COMPARISON-V2 procedure'),
}

def migrate(id, text):
    if id not in TRANSFORMS:
        return text
    old, new = TRANSFORMS[id]
    if text.count(old)!=1:
        raise ValueError(('migration source multiplicity', id, text.count(old)))
    return text.replace(old,new)

def dataset(e248, e252, version):
    inputs=[r for r in table(section(e248,14)) if len(r)==4 and r[0].startswith('{SUCCESSOR-NAMESPACE}-')]
    inputs=[[r[0].removeprefix('{SUCCESSOR-NAMESPACE}-'), *r[1:]] for r in inputs]
    expansions={r[0]:re.findall(r'`([^`]+)`',r[1]) for r in table(section(e252,7)) if len(r)==2 and r[0] in {i[0] for i in inputs}}
    families=dict(re.findall(r'^(RF-\d\d) (SF-\d\d)$',e252,re.M))
    modal=lambda s:re.findall(r'\b(?:MUST NOT|MUST|MAY)\b',s)
    inrows=[]; atoms=[]
    for i,(id,text,src,rf) in enumerate(inputs,1):
        value=migrate(id,text) if version==5 else text
        inrows.append([f'{i:04}',id,value,src,rf,str(len(modal(text)))])
        expanded=expansions.get(id,[text])
        assert len(expanded)==len(modal(text))
        for j,a in enumerate(expanded,1):
            a=migrate(id,a) if version==5 else a
            assert len(modal(a))==1
            atoms.append([f'{len(atoms)+1:04}',id+(f'-A{j:02}' if id in expansions else ''),id,modal(a)[0],a,src,rf,families[rf],'EXPLICIT-CONJUNCT-OF-INPUT' if id in expansions else 'IDENTICAL-LEXICAL-OBLIGATION'])
    b=f'PE-TSE-REQDATA-V{version}\n'.encode()+tsv('input_order input_id normative_text source_anchor_expression rf modal_count'.split(),inrows)+tsv('atom_order atom_id input_id strength normative_text source_anchor_expression rf sf conservation_class'.split(),atoms)
    return b,inrows,atoms

def construct(out):
    out.mkdir(parents=True,exist_ok=True)
    e248=doc('CORRECTION_AND_COMPLETION');e252=doc('THIRD_CORRECTION_AND_COMPLETION')
    v4,oldinputs,oldatoms=dataset(e248,e252,4)
    assert H(v4)=='58f90e18a3ddd950cd053cdd2ffa7426f5057c0af30dae78450a2ae16e3dd837'
    v5,inputs,atoms=dataset(e248,e252,5)
    assert len(inputs)==92 and len(atoms)==116
    changes=[]
    for name,olds,news in [('INPUT',oldinputs,inputs),('ATOM',oldatoms,atoms)]:
        for a,b in zip(olds,news):
            for col,(av,bv) in enumerate(zip(a,b)):
                if av!=bv:
                    assert col==(2 if name=='INPUT' else 4)
                    changes.append([name,a[0],a[1],col,av,bv])
    assert len(changes)==4
    g2=list(csv.DictReader((CORPUS/'docs/privacy-engine/generation-002/candidate/specification/COMPLETE_NORMATIVE_REQUIREMENT_INVENTORY_V1.tsv').open(),delimiter='\t'))
    g2=[r for r in g2 if r['order']!='end']; assert len(g2)==749
    ns='{SUCCESSOR-NAMESPACE}'
    replaced={'PE-G2-COMMIT-004',*(f'PE-G2-STALEAUTH-00{i}' for i in [2,3,4])}
    def convert(tokens):
        norm=[];support=[]
        for s in tokens:
            if s=='S01':support.append('STATE')
            elif s=='S02':support.append(ns+'-COMPOSITION-MAP-001')
            elif s=='PE-G2-SEMANTIC-DIFFERENCE-001':support.append(ns+'-TSE-SEMANTIC-DIFFERENCE-001')
            else:
                assert re.fullmatch(r'S\d\d',s) and 3<=int(s[1:])<=72
                norm.append(ns+'-SOURCE-'+s)
        return [', '.join(dict.fromkeys(a)) or 'NONE' for a in (norm,support)]
    def atomrow(a):
        _,id,inp,strength,text,src,rf,sf,_=a
        norm,support=convert([s.split(' ',1)[0] for s in src.split('; ')])
        cond=text[:text.index(',')+1] if text.startswith(('When ','For ')) else 'ALWAYS'
        rid=ns+'-'+id
        return [rid,rid.lower(),rf,sf,strength,'applicable' if cond=='ALWAYS' else 'conditional',cond,text,norm,support,'revised' if 'PE-G2-'+inp in replaced else 'new','PE-G2-'+inp if 'PE-G2-'+inp in replaced else 'NONE','NOT-APPLICABLE','NOT-APPLICABLE']
    final=[]
    for r in g2:
        if r['successor_identifier'] in replaced:
            final.extend(atomrow(a) for a in atoms if 'PE-G2-'+a[2]==r['successor_identifier'])
        else:
            norm,support=convert(r['sources'].split(', '));id=r['successor_identifier'].replace('PE-G2-',ns+'-',1)
            final.append([id,id.lower(),r['rf'],r['sf'],r['strength'],'applicable',r['applicability'],r['normative_text'],norm,support,'unchanged',r['successor_identifier'],'NOT-APPLICABLE','NOT-APPLICABLE'])
    final.extend(atomrow(a) for a in atoms if 'PE-G2-'+a[2] not in replaced)
    assert len(final)==861 and len({r[0] for r in final})==861
    for old in g2:
        if old['successor_identifier'] in replaced:continue
        row=next(r for r in final if r[11]==old['successor_identifier'])
        assert [row[2],row[3],row[4],row[6],row[7]]==[old['rf'],old['sf'],old['strength'],old['applicability'],old['normative_text']]
    owns=[];counts={f'S{i:02}':[0,0] for i in range(3,73)}
    for i,r in enumerate(final,1):
        for src in r[8].split(', '):
            if src=='NONE':continue
            owns.append([f'{len(owns)+1:06}',f'{i:04}',r[0],src])
            counts[src[-3:]][0 if r[10]=='unchanged' else 1]+=1
    excess=Counter()
    for a in atoms:
        seg=[s.split(' ',1)[0] for s in a[5].split('; ')]
        excess[a[2]]+=len(seg)-len(set(seg))
    excess={k:v for k,v in excess.items() if v}
    assert sum(excess.values())==18
    assert len(owns)==2336
    assert sum(x[0] for x in counts.values())==2170 and sum(x[1] for x in counts.values())==166
    files={
        'REQDATA-V5.tsv':v5,
        'migration-cells.tsv':tsv('table order id zero_based_column old_text new_text'.split(),changes),
        'symbolic-inventory-V5.tsv':tsv('requirement_order requirement_id requirement_anchor rf_family sf_family strength applicability condition_text normative_text normative_source_ids supporting_reference_ids treatment predecessor_requirement_id mapping_id profile_id'.split(),[[f'{i:04}',*r] for i,r in enumerate(final,1)]),
        'ownership.tsv':tsv('ownership_order requirement_order requirement_id source_id'.split(),owns),
        'source-allocations.tsv':tsv('source retained atoms total'.split(),[[s,*v,sum(v)] for s,v in counts.items()]),
        'excess-segments.tsv':tsv(['input_id','excess_segments'],list(excess.items())),
    }
    # Do not claim actual composition or source/specification endpoints from row counts.
    info={'scope':'parameterized requirement/ownership audit; not a successor candidate',
          'input_count':len(inputs),'atom_count':len(atoms),'inventory_count':len(final),
          'strengths':dict(Counter(r[4] for r in final)),
          'retained_ownership':2170,'atom_ownership':166,'total_ownership':len(owns),
          'composition_expected_arithmetic':70+len(owns)+len(final),
          'rf':len({r[2] for r in final}),'sf':len({r[3] for r in final}),
          'files':{k:{'sha256':H(b),'bytes':len(b),'lf':b.count(b'\n')} for k,b in files.items()}}
    for name,b in files.items(): (out/name).write_bytes(b)
    (out/'construction-results.json').write_text(json.dumps(info,indent=2)+'\n')
    return info

if __name__=='__main__':
    print(json.dumps(construct(Path(__file__).resolve().parent/'results'),indent=2))
````
<!-- END E262-SEM-REQUIREMENTS -->

## 13. SERIALIZERS

<!-- BEGIN E262-SEM-SERIALIZERS -->
This is the complete replacement source/40-artifact constructor. The exact 40-path/classification/H1 register is E248 section 16; 66 predecessor byte identities are E248 section 13. The supplied immutable input corpus is hash-checked before use. The algorithm consumes those closed registers mechanically. Four later-authorized identity parameters are required; no real values are selected here. Default literal symbols produce non-installable author vectors only. Synthetic test substitutions are visibly isolated from any real generation.

The closed semantic import register for EACH of the 16 revised and four new sources is, in this exact order: AUTHORITY, REGISTRY, TYPES, DEPENDENCY, PRIVACY, AUTHORIZATION, COMMITMENT, COMPARISON, RECOVERY. Every import is the exact body between the unique corresponding E256 BEGIN/END markers. This deliberately supersedes selective E252 source imports: every source carries the complete closed semantic book so no imported rule depends on omitted semantic prose. Program modules are dependencies within that same book. Inherited predecessor-derived source bodies remain token-conserved beneath an explicit subordinate heading. If those historical bodies conflict, the complete E256 book and V5 atomic requirement table take precedence. Fifty preserved sources are byte-identical references, never rewritten.

Template staging is typed and single-pass. Only an explicitly selected template AST executes controls. Imported code fences, normative blocks and replacement values are opaque literal strings; text resembling {{NAME}} inside an imported block never executes. prefix, book, source and construct_one are the complete sequence register, including exact headings and separators. There is no recursive scan over inserted text. Unknown executable substitutions reject. The only single-brace parameter replacements are the five named tokens in Constructor.sub; GGG is derived from the authorized generation identifier. Source/allocation rows are final inventory order filtered by ownership.

A preserved source root is a virtual endpoint ROOT:source-id, bound to path, SHA-256 and full byte span; it does not imply a physical HTML anchor. Constructed sources and specification also have physical prefix anchors. SF and RF anchors use the lowercased namespace followed by lowercased family ID. Requirement anchors come from the inventory. Every anchor/reference must resolve by the typed endpoint rules, not by assuming all anchors are physical.

Instrumented get records each generated artifact byte read. The manifest uses that measured direct relation, not the obsolete asserted 150-edge register. Artifact 0030 reads 0029 and all constructed source bytes; 0038 reads all identities/inventories it consumes plus the actual S70 semantic bytes. Row 0040 alone uses SELF in digest/size/LF cells. No dependency computes its own digest. The trace artifact follows specification construction; status follows trace; package manifest is last. All 40 serializers are below.

### Constructor module: artifact_construction.py

````python
"""E256 symbolic 40-member byte constructor with instrumented direct reads.

Identity strings remain literal symbols. These outputs cannot be installed as
a real candidate. Four authorized identity values are still required later.
"""
from pathlib import Path
import csv,io,json,re,unicodedata,importlib.util
from collections import defaultdict
from construction import BASE,CORPUS,doc,section,table,construct,H
from expr_v2 import need,tsv,NA

WORK=Path(__file__).parent
PARAM={'SUCCESSOR-NAMESPACE':'{SUCCESSOR-NAMESPACE}','SUCCESSOR-GENERATION-ID':'{SUCCESSOR-GENERATION-ID}',
       'SUCCESSOR-GENERATION-LABEL':'{SUCCESSOR-GENERATION-LABEL}','SUCCESSOR-VERSION':'{SUCCESSOR-VERSION}','GGG':'{GGG}'}
CORE=('AUTHORITY','REGISTRY','TYPES','DEPENDENCY','PRIVACY','AUTHORIZATION','COMMITMENT','COMPARISON','RECOVERY')
ORDER=[2,3,4,5,6,7,*range(8,29),34,35,36,29,30,37,32,38,31,33,39,1,40]

def read_rows(b):return list(csv.DictReader(io.StringIO(b.decode()),delimiter='\t'))
def cell(s):return s.replace('\\','\\\\').replace('|','\\|')
def mdtable(header,rows):return '| '+' | '.join(header)+' |\n|'+ '|'.join('---' for _ in header)+'|\n'+''.join('| '+' | '.join(cell(str(c)) for c in r)+' |\n' for r in rows)
def render(template,values):
    """One pass over the template AST; replacement text is opaque literal data."""
    return re.sub(r'\{\{([A-Za-z0-9_-]+)\}\}',lambda m:values[m[1]],template)
def block(payload,name):
    start=f'<!-- BEGIN E262-{name} -->\n';end=f'<!-- END E262-{name} -->\n'
    need(payload.count(start)==payload.count(end)==1,('marked range',name))
    return payload.split(start,1)[1].split(end,1)[0]

class Constructor:
    def __init__(self,payload,parameters=None):
        self.param=dict(PARAM)
        if parameters is not None:
            need(set(parameters)==set(PARAM)-{'GGG'},'exactly four identity parameters')
            need(all(isinstance(v,str) and v.isascii() and v and not any(x in v for x in '\t\r\n{}') for v in parameters.values()),'identity parameter bytes')
            self.param.update(parameters);self.param['GGG']=parameters['SUCCESSOR-GENERATION-ID'].rsplit('-',1)[1]
        def substitute(text):
            text=re.sub(r'\{(SUCCESSOR-NAMESPACE|SUCCESSOR-GENERATION-ID|SUCCESSOR-GENERATION-LABEL|SUCCESSOR-VERSION|GGG)\}',lambda m:self.param[m[1]],text)
            return text.replace('{successor-namespace}',self.param['SUCCESSOR-NAMESPACE'].lower())
        self.sub=substitute
        self.payload=payload;self.blocks={k:self.sub(block(payload,'SEM-'+k)) for k in CORE}
        self.inventory=[];self.sources={};self.artifacts={};self.dependencies=defaultdict(set);self.active=None
        e248=doc('CORRECTION_AND_COMPLETION');self.e252=doc('THIRD_CORRECTION_AND_COMPLETION')
        for r in table(section(e248,16)):
            if len(r)==5 and re.fullmatch('[0-9]{4}',r[0]):
                n=int(r[0]);path,id,h1=r[2:];h1=h1.split('; ',1)[0] if h1.startswith('# ') else ''
                if n==5:id='{SUCCESSOR-GENERATION-ID}'
                self.inventory.append(dict(order=n,classification='NORMATIVE' if r[1]=='N' else 'EVIDENCE-ONLY',path=self.sub(path),id=self.sub(id),h1=self.sub(h1)))
        need(len(self.inventory)==40,'inventory')
        self.meta={r['order']:r for r in self.inventory}
        for r in table(section(e248,13)):
            if len(r)==5 and re.fullmatch('S[0-9]{2}',r[0]):
                slot,id,path,digest,treatment=r;b=(CORPUS/path).read_bytes();need(H(b)==digest,('predecessor digest',slot))
                self.sources[slot]=dict(slot=slot,path=path,digest=digest,bytes=b,treatment=treatment,id=id)
        need(len(self.sources)==66,'source register')
        self.source_art={self.meta[n]['id'][-3:]:n for n in range(8,28)}
        self.reqbytes=self.sub((WORK/'results/symbolic-inventory-V5.tsv').read_text()).encode();self.reqs=read_rows(self.reqbytes)
        family=(CORPUS/'docs/privacy-engine/generation-002/candidate/specification/SUCCESSOR_SECTION_AND_FAMILY_INVENTORY_V1.tsv').read_bytes()
        self.sf=[r for r in read_rows(family) if r['record_type']=='sf']
        self.rf=[r for r in read_rows(family) if r['record_type']=='rf']
        need(len(self.sf)==16 and len(self.rf)==50,'family register')
        self.source_ranges={};self.spec_ranges={}
    def get(self,n):
        need(n in self.artifacts,('prerequisite incomplete',self.active,n))
        if self.active is not None:self.dependencies[self.active].add(n)
        return self.artifacts[n]
    def prefix(self,n):
        m=self.meta[n]
        return f'<a id="{m["id"].lower()}"></a>\n{m["h1"]}\n\nIdentifier:\n{m["id"]}\n\nDocument version:\nV1\n\nSuccessor generation:\n{self.param["SUCCESSOR-GENERATION-ID"]}\n\nStatus:\nunreviewed-unpublished-non-authoritative\n\n'
    def template_after(self,needle):
        tail=section(self.e252,11).split(needle,1)[1];return tail.split('```text\n',1)[1].split('```',1)[0]
    def book(self,owner):
        pieces=[];offset=0;ranges={}
        for name in CORE:
            heading=f'<a id="{owner.lower()}-sem-{name.lower()}"></a>\n### E262-SEM-{name}\n\n'
            body=self.blocks[name];piece=heading+body+'\n'
            start=offset+len(heading.encode());ranges[name]=(start,start+len(body.encode()))
            pieces.append(piece);offset+=len(piece.encode())
        return ''.join(pieces),ranges
    def source(self,n):
        slot=self.meta[n]['id'][-3:];identifier=self.meta[n]['id'];prefix=self.prefix(n)
        if slot in self.sources:
            old=self.sources[slot];prefix+=f'Predecessor source identifier:\nPE-G2-SOURCE-{slot}\n\nPredecessor source SHA-256:\n{old["digest"]}\n\n'
        prefix+='## Complete Governing Transition-State Equivalence Semantics\n\n'
        book,ranges=self.book(identifier)
        self.source_ranges[slot]={k:(a+len(prefix.encode()),b+len(prefix.encode())) for k,(a,b) in ranges.items()}
        out=prefix+book+'## Successor Atomic Requirements\n\n'
        requirements=[r for r in self.reqs if identifier in r['normative_source_ids'].split(', ')]
        out+=mdtable(['Requirement','Strength','Applicability','Condition','Normative text','RF','SF'],[[r[k] for k in ['requirement_id','strength','applicability','condition_text','normative_text','rf_family','sf_family']] for r in requirements])+'\n'
        if slot in self.sources:
            text=self.sources[slot]['bytes'].decode();need(unicodedata.normalize('NFC',text)==text,'predecessor NFC')
            lines=text.splitlines();h1=next(i for i,line in enumerate(lines) if re.match(r'^ {0,3}# ',line));body='\n'.join(lines[h1+1:])
            converted='\n'.join(l.rstrip(' \t') for l in body.splitlines()).strip('\n')+'\n'
            need(re.findall(r'\S+',body)==re.findall(r'\S+',converted),'predecessor token conservation')
            out+='## Predecessor-Derived Body\n\n'+converted+'\n'
        out+=f'Candidate status: unreviewed-unpublished-non-authoritative\nEnd of source: {identifier}\n'
        return out.rstrip('\n').encode()+b'\n'
    def source_info(self,slot):
        sid=self.param['SUCCESSOR-NAMESPACE']+'-SOURCE-'+slot
        if slot in self.source_art:
            n=self.source_art[slot];b=self.get(n);path=self.meta[n]['path'];digest=H(b)
            old=self.sources.get(slot)
            return sid,path,digest,b,old
        old=self.sources[slot];return sid,old['path'],old['digest'],old['bytes'],old
    def sections(self):
        root=self.meta[38]['id'];rows=[]
        # Root title is exact inventory H1 content; no constructor-selected title.
        groups=[('ROOT',root,self.meta[38]['h1'][2:],NA,self.reqs)]
        for r in self.sf:
            id=r['identifier'];groups.append(('SF',id,r['title'],root,[q for q in self.reqs if q['sf_family']==id]))
        for r in self.rf:
            id=r['identifier'];groups.append(('RF',id,r['title'],r['parent_identifier'],[q for q in self.reqs if q['rf_family']==id]))
        for i,(kind,id,title,parent,qs) in enumerate(groups,1):
            need(bool(qs),'empty family');rows.append([f'{i:04}',kind,id,title,parent,qs[0]['requirement_order'],qs[-1]['requirement_order'],str(len(qs))])
        return tsv('record_order record_class identifier title parent_identifier first_requirement last_requirement requirement_count'.split(),rows)
    def composition(self):
        spec=self.meta[38]['id'];root=spec.lower();edges=[]
        for i in range(3,73):
            slot=f'S{i:02}';sid,path,dg,b,old=self.source_info(slot)
            edges.append(['SOURCE-DEFINES-SPECIFICATION',sid,spec,'ROOT:'+sid,root])
        for q in read_rows(self.get(34)):
            for sid in q['normative_source_ids'].split(', '):edges.append(['REQUIREMENT-OWNED-BY-SOURCE',q['requirement_id'],sid,q['requirement_anchor'],'ROOT:'+sid])
            edges.append(['REQUIREMENT-COMPOSED-INTO-SPECIFICATION',q['requirement_id'],spec,q['requirement_anchor'],q['requirement_anchor']])
        rel=['SOURCE-DEFINES-SPECIFICATION','REQUIREMENT-OWNED-BY-SOURCE','REQUIREMENT-COMPOSED-INTO-SPECIFICATION']
        edges.sort(key=lambda r:(rel.index(r[0]),*r[1:]));need(len(edges)==3267,'composition count')
        return tsv('composition_order relation from_id to_id from_anchor to_anchor normative_status'.split(),[[f'{i:06}',*r,'normative'] for i,r in enumerate(edges,1)])
    def specification(self):
        reqs=read_rows(self.get(34));self.get(32);self.get(36)
        identity=self.get(37);self.get(29);self.get(30)
        out=self.prefix(38)+'## Specification Identity\n\n'+f'Specification identity artifact: {self.meta[37]["id"]}\nSpecification identity SHA-256: {H(identity)}\nSpecification identifier: {self.meta[38]["id"]}\nSpecification version: {self.param["SUCCESSOR-VERSION"]}\nGoverning generation: {self.param["SUCCESSOR-GENERATION-ID"]}\n\n'
        for sf in self.sf:
            out+=f'<a id="{self.param["SUCCESSOR-NAMESPACE"].lower()}-{sf["identifier"].lower()}"></a>\n## {sf["identifier"]} — {sf["title"]}\n\n'
            for rf in self.rf:
                if rf['parent_identifier']!=sf['identifier']:continue
                out+=f'<a id="{self.param["SUCCESSOR-NAMESPACE"].lower()}-{rf["identifier"].lower()}"></a>\n### {rf["identifier"]} — {rf["title"]}\n\n'
                data=[]
                for q in reqs:
                    if q['rf_family']==rf['identifier']:data.append([f'<a id="{q["requirement_anchor"]}"></a> {q["requirement_id"]}',*[q[k] for k in ['strength','applicability','condition_text','normative_text','normative_source_ids','supporting_reference_ids']]])
                out+=mdtable(['Requirement','Strength','Applicability','Condition','Normative text','Normative sources','Supporting references'],data)+'\n'
        # The exact semantic ranges come from S70's constructed bytes, not a
        # second unsupervised rendering of the input blocks.
        s70=self.get(25);out+='## Complete Transition-State Equivalence Semantics\n\n'
        for name,(a,b) in self.source_ranges['S70'].items():
            text=s70[a:b].decode();need(text==self.blocks[name],'source semantic import')
            out+=f'<a id="{self.meta[38]["id"].lower()}-sem-{name.lower()}"></a>\n### E262-SEM-{name}\n\n'
            start=len(out.encode());out+=text;self.spec_ranges[name]=(start,len(out.encode()));out+='\n'
        return out.rstrip('\n').encode()+b'\n'
    def construct_one(self,n):
        self.active=n
        if 8<=n<=27:return self.source(n)
        if n in (1,2,4,5,6,7,33,37):
            if n==1:
                for d in (31,33,39):self.get(d)
                body=self.template_after('`MD-STATUS-V3` body:')
            elif n==2:body=self.template_after('Artifact 0002 uses:')
            elif n==4:body=self.template_after('Artifact 0004 uses:')
            elif n==5:body=self.template_after('`MD-IDENTITY-V3` body:')
            elif n==6:body=self.template_after('Artifact 0006 uses:')
            elif n==7:body=self.template_after('Artifact 0007 uses:')
            elif n==33:
                for d in (28,29,34,38):self.get(d)
                body=self.template_after('`MD-CLOSED-SET-V3` body:')
            else:
                self.get(5);body=self.template_after('`MD-SPEC-IDENTITY-V3` body:')
            return (self.prefix(n)+render(body,self.param)).encode()
        if n==3:
            book,_=self.book(self.meta[n]['id']);return (self.prefix(n)+'## Complete Corrected Semantics\n\n'+book+block(self.payload,'SEM-REQUIREMENTS')+block(self.payload,'SEM-SERIALIZERS')).encode()
        if n==28:return tsv('registry_order mapping_id mapping_path mapping_sha256 profile_id profile_path profile_sha256 applicability_definition_id recovery_definition_id status'.split(),[])
        if n==34:return self.reqbytes
        if n==35:
            qs=read_rows(self.get(34));reasons={'unchanged':'BYTE-PRESERVED','revised':'MODAL-ATOMIZED-REVISION','new':'MODAL-ATOMIZED-ADDITION'}
            return tsv('classification_order successor_requirement_id predecessor_requirement_id classification reason'.split(),[[r['requirement_order'],r['requirement_id'],r['predecessor_requirement_id'],r['treatment'],reasons[r['treatment']]] for r in qs])
        if n==36:self.get(34);return self.sections()
        if n==29:
            rows=[]
            for i in range(3,73):
                slot=f'S{i:02}';sid,path,dg,b,old=self.source_info(slot)
                if slot not in self.source_art:treatment,method,relation='unchanged-immutable-source-input','sha256-fixed-predecessor-bytes','identical-to-immutable-source-by-reference'
                elif old:treatment,method,relation='successor-revised-source','sha256-constructed-canonical-bytes','successor-revision-of'
                else:treatment,method,relation='successor-new-source','sha256-constructed-canonical-bytes','new-successor-source'
                rows.append([f'{i-2:04}',slot,sid,path,treatment,method,dg,old['path'] if old else NA,old['digest'] if old else NA,relation])
            return tsv('source_order source_slot source_identifier successor_path treatment identity_method successor_sha256 predecessor_path predecessor_sha256 predecessor_relationship'.split(),rows)
        if n==30:
            rows=[]
            for i,r in enumerate(read_rows(self.get(29)),1):
                _,_,_,b,_=self.source_info(r['source_slot']);rows.append([f'{i:04}',r['source_slot'],r['source_identifier'],r['successor_path'],H(b),str(len(b)),str(b.count(b'\n')),r['treatment']])
            rows.append(['0071','END',self.meta[30]['id'],NA,NA,'70',NA,'COUNT'])
            return tsv('manifest_order source_slot source_id path sha256 bytes lf_count treatment'.split(),rows)
        if n==32:return self.composition()
        if n==38:return self.specification()
        if n==31:
            rows=[]
            for i,(kind,d,count) in enumerate([('REGISTRY',28,'0'),('REQUIREMENTS',34,'861'),('SECTIONS',36,'67'),('COMPOSITION',32,'3267'),('SPECIFICATION-IDENTITY',37,NA),('SPECIFICATION',38,'861')],1):
                rows.append([f'{i:04}',kind,self.meta[d]['id'],self.meta[d]['path'],H(self.get(d)),count,'closed-validated-normative-member'])
            return tsv('manifest_order semantic_class semantic_id path sha256 row_count status'.split(),rows)
        if n==39:return self.trace()
        if n==40:
            rows=[]
            for d in range(1,41):
                m=self.meta[d]
                if d==40:dg=length=lf='SELF';deps=','.join(self.meta[k]['id'] for k in range(1,40))
                else:
                    b=self.get(d);dg=H(b);length=str(len(b));lf=str(b.count(b'\n'));deps=','.join(self.meta[k]['id'] for k in sorted(self.dependencies[d])) or 'NONE'
                rows.append([f'{d:04}',m['id'],m['classification'],m['path'],dg,length,lf,deps])
            return tsv('artifact_order artifact_id classification path sha256 bytes lf_count dependency_ids'.split(),rows)
        raise ValueError(('missing constructor',n))
    def trace(self):
        from semantic_trace import construct_trace
        return construct_trace(self)
    def run(self,out):
        out.mkdir(parents=True,exist_ok=True)
        for n in ORDER:
            b=self.construct_one(n);need(isinstance(b,bytes) and b.endswith(b'\n') and b'\r' not in b,('canonical artifact',n))
            self.artifacts[n]=b
            target=out/self.meta[n]['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
        self.active=None
        need(len(self.artifacts)==40 and sum(m['classification']=='NORMATIVE' for m in self.inventory)==36,'artifact classification')
        positions={n:i for i,n in enumerate(ORDER)}
        for n,deps in self.dependencies.items():need(all(positions[d]<positions[n] for d in deps),('dependency order',n,deps))
        # Preserve source bytes without inserting markup. Each virtual root spans
        # byte 0 through EOF, paired with the byte identity in the source register.
        roots=[]
        for i in range(3,73):
            slot=f'S{i:02}';sid,path,dg,b,old=self.source_info(slot)
            roots.append(['ROOT:'+sid,path,'0',str(len(b)),dg])
        (out.parent/'source-virtual-roots.tsv').write_bytes(tsv('endpoint path start end sha256'.split(),roots))
        report={'scope':'symbolic non-installable 40-member byte vectors; not a real successor candidate',
                'artifacts':[{**self.meta[n],'sha256':H(b),'bytes':len(b),'lf':b.count(b'\n'),'direct_reads':sorted(self.dependencies[n])} for n,b in sorted(self.artifacts.items())],
                'direct_edge_count':sum(map(len,self.dependencies.values())),'trace':self.trace_report,
                'source_count':70,'composition_rows':len(read_rows(self.artifacts[32])),'section_rows':len(read_rows(self.artifacts[36]))}
        (out.parent/'construction-results.json').write_text(json.dumps(report,indent=2)+'\n');return report
````
<!-- END E262-SEM-SERIALIZERS -->

## 14. TRACE

<!-- BEGIN E262-SEM-TRACE -->
Trace scope is every block and every parsed table cell of E243, E244, B245 canonical, E246, D247, E248, D249, E250, D251, E252, D253, E254, D255, D257, D259, D261, the historical E256, E258 and E260 payloads and this E262 payload. Root input hashes and exact section/defect-to-body assignments appear below. PRIMARY is exactly one forward relation per such endpoint; its paired inverse is mandatory. SUPPLEMENTAL covers source realization, specification realization, requirements, composition, registry and family assignments. Self retention has retained-only status and is never counted as semantic resolution.

A block endpoint has its original parser half-open byte range and hash. A cell endpoint has its physical carrier-row span, 1-based parsed cell ordinal and hash of decoded parsed cell UTF-8 bytes; it is a typed cell selector, not a fictitious substring byte range. RANGE destinations exclude delimiter lines and contain actual rule/constructor bodies. Source/specification destinations must resolve to independently constructed bytes and exact range equality. Root comments or headings cannot satisfy realization. Inverse relation names and row pair IDs are exhaustively defined below. Control-only REQUIREMENTS, SERIALIZERS, TRACE, MARKDOWN and INSTALLATION bodies govern construction, not transition execution, and therefore use artifact/procedure destinations instead of pretending to be imported protocol clauses.

Inherited finding resolution register: FINDING_BODIES specifies every required governing body for all 62 prior/current findings across the eight D roots. Its first-class primary class is separately fixed by DEFECT_MAP; every remaining named body yields an explicit supplemental resolved-by edge and paired inverse. All blocks and parsed cells in each finding receive those supplemental destinations. SECTION_MULTI similarly closes composite subjects in earlier determination sections. No unrecorded transitive prose reference counts as a resolution edge. The tuple-selection D253 endpoint reaches TYPES; the D255 binding-mode endpoint reaches TYPES, PRIVACY and AUTHORIZATION as well as REQUIREMENTS. The D247 and D257 supplements remain. The audit serializes each finding block and its complete required body set, verifies that every declared finding was parsed, and rejects any missing required resolution pair. This checks construction against the audited semantic assignment register; independent semantic review remains required and is not replaced by a fixed row count.

D253, D255, D257 and D259 defect ranges begin at their exact ### E253-NN / ### E255-NN / ### E257-NN / ### E259-NN headings and end immediately before the next heading of that level or above outside a fenced block. This uses parsed blocks so quoted Markdown does not alter the governing range. Other roots use the explicit closed section/defect register. Historical metadata with no changed obligation is retained; it is not claimed corrected merely from endpoint cardinality. D247 uses its exact numbered defect paragraphs, including its missing terminal LF.

E262 section-obligation closure: SECTION_BODIES is the exact collective governing-body set for every assigned determination section, including the complete E260 basis. Each original block and parsed cell retains exactly one PRIMARY disposition and receives explicit supplements to every other required body. An edge names a member of the collective resolution set; it does not assert that one member alone resolves every clause in a composite paragraph, table row or code block. A section's individual obligations are covered by the union of its explicit destinations. In particular E246-PARA-000256 has a corrected-by edge to COMPARISON, which contains the indivisible commitment boundary, as well as its retained RECOVERY primary. E248 section 12 has the same explicit COMPARISON supplement. Existing recovery, dependency, privacy, typing, authorization and finding-level destinations are retained.

The audit is exhaustive over parsed clause carriers: section-obligation-audit.tsv records root, section, endpoint, collective bodies and JSON-escaped exact block/cell text. No normative-keyword filtering or sentence splitting can omit a clause. Embedded complete constructor fences remain indivisible code carriers. The constructor verifies the entire declared section domain was encountered and every required block/cell edge exists. This supplies inspectable clause-level evidence; independent semantic judgment must still check that each obligation is actually carried by at least one named body. Headings, row counts, mere mentions and inferred transitive prose edges are not semantic proof. Control-only REQUIREMENTS/SERIALIZERS/TRACE/MARKDOWN/INSTALLATION destinations remain procedure ranges, not invented protocol-source realization.

### Constructor module: semantic_trace.py

````python
"""Closed span-based trace construction; retention is not realization."""
from artifact_construction import *

ROOT_HASHES={
'E243':'97f5201adbed45395a1cbc0d3db2fd6a8419d36d687a1bfe25c901e99c9c59d3',
'E244':'d57807fc9da70a5a0cfa4a37897256b336fc18dba2aa987d97ad5d5146e99f30',
'E246':'a191d11525b254374731562f40fd2be142fa00d8c89c03441bc0b694c66cb493',
'E248':'1f5b59b0ff4720ee142a42017f13e543e1a3973fd81113ca86ca2ead43834a73',
'E250':'558747f7091ab5e5f597a3f3fba3acb987ea28dfd652e7e691e81371d2b5ccf2',
'E252':'7bffea0286c19cc8c1f560ab694849814823e0566d0a6dc8f1118e6a949b3343',
'E254':'2b3193b69df04c335c88e5078b2defb6784a73d707192a6208eda7ff48b0fae6',
'E258':'8878dede83870f9f8409a0a6470abea5ba45b651dbe61211459cf10f68d5f04e',
'E256':'7b7f176275567cc9e1daf3e52234d24feffa8ff5d22748e280c13d11ffb57a57',
'D247':'35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5',
'D249':'636899f5426b8a70065b7f7193bba8ef1d0542e10c2ecc014a90cea39990bb37',
'D251':'ae67f309c7d13a656d0e5d66a89ad016eb64910a464897def54116e02cef940b',
'D253':'8d73384f9f6a32103d7fb8c419527faf11514ae3110465f7c8b84a072e43683b',
'D255':'f008dc4d42c9859704bf9dd349a50fa2813a75b7ba64ac2570b6425047cf3e0a',
'D257':'a3ecf60ed54f845bc24dd7502fc8e48876484d67eaa04334393f84fede9e0c5d',
'E260':'301efbbc1a0ed61a0564eaff8e4be8bb2287ddd583ab22825225b69dcf5a1887',
'D261':'d12844a9bb351fef4bbd4cf366ccd2cdd85e533dab150f3f5ebae034e12b83fb',
'D259':'2861bdfa95840126b7b8b44d44c987f7c58c670b1fa7d9dba3b675dd4bc7bc41'}
SECTION_MAP={
'E243':{7:'REGISTRY',8:'REGISTRY',9:'TYPES',10:'AUTHORIZATION',11:'COMPARISON',12:'COMPARISON',13:'RECOVERY',14:'RECOVERY',15:'COMPARISON',16:'PRIVACY'},
'E244':{9:'REGISTRY',10:'REGISTRY',11:'TYPES',12:'AUTHORIZATION',13:'COMPARISON',14:'COMPARISON',15:'RECOVERY',16:'RECOVERY',17:'COMPARISON',18:'PRIVACY'},
'E246':{6:'REGISTRY',7:'TYPES',8:'TYPES',9:'COMPARISON',10:'AUTHORIZATION',11:'RECOVERY',12:'RECOVERY',13:'PRIVACY',14:'SERIALIZERS',15:'REQUIREMENTS',16:'TRACE',17:'SERIALIZERS',18:'TRACE',19:'TRACE'},
'E248':{3:'SERIALIZERS',4:'REGISTRY',5:'REGISTRY',6:'TYPES',7:'COMPARISON',8:'AUTHORIZATION',9:'COMMITMENT',10:'PRIVACY',11:'DEPENDENCY',12:'RECOVERY',13:'SERIALIZERS',14:'REQUIREMENTS',15:'TRACE',16:'SERIALIZERS',17:'SERIALIZERS',18:'SERIALIZERS',19:'INSTALLATION'},
'E250':{2:'TYPES',3:'COMPARISON',4:'COMPARISON',5:'PRIVACY',6:'DEPENDENCY',7:'RECOVERY',8:'SERIALIZERS',9:'REQUIREMENTS',10:'TRACE',11:'MARKDOWN',12:'SERIALIZERS',13:'SERIALIZERS',14:'INSTALLATION'},
'E252':{2:'TYPES',3:'PRIVACY',4:'DEPENDENCY',5:'RECOVERY',6:'SERIALIZERS',7:'REQUIREMENTS',8:'COMPARISON',9:'MARKDOWN',10:'TRACE',11:'SERIALIZERS',12:'SERIALIZERS',13:'INSTALLATION',14:'TRACE'},
'E254':{2:'REQUIREMENTS',3:'DEPENDENCY',4:'PRIVACY',5:'MARKDOWN',6:'TRACE',7:'INSTALLATION',8:'SERIALIZERS',9:'TRACE',10:'TRACE'},
'E256':{3:'AUTHORITY',4:'REGISTRY',5:'TYPES',6:'DEPENDENCY',7:'PRIVACY',8:'AUTHORIZATION',9:'COMMITMENT',10:'COMPARISON',11:'RECOVERY',12:'REQUIREMENTS',13:'SERIALIZERS',14:'TRACE',15:'MARKDOWN',16:'INSTALLATION'}}
SECTION_MAP['E258']=dict(SECTION_MAP['E256'])
SECTION_MAP['E260']=dict(SECTION_MAP['E256'])
DEFECT_MAP={
'D247':['TYPES','COMPARISON','AUTHORIZATION','PRIVACY','DEPENDENCY','RECOVERY','SERIALIZERS','REQUIREMENTS','TRACE','SERIALIZERS','INSTALLATION'],
'D249':['TYPES','COMPARISON','PRIVACY','DEPENDENCY','RECOVERY','SERIALIZERS','REQUIREMENTS','TRACE','MARKDOWN','TRACE','SERIALIZERS','SERIALIZERS','INSTALLATION'],
'D251':['TYPES','PRIVACY','DEPENDENCY','RECOVERY','SERIALIZERS','REQUIREMENTS','MARKDOWN','TRACE','SERIALIZERS','SERIALIZERS','INSTALLATION'],
'D253':['REQUIREMENTS','REQUIREMENTS','DEPENDENCY','PRIVACY','MARKDOWN','TRACE','INSTALLATION','SERIALIZERS'],
'D255':['REQUIREMENTS','REQUIREMENTS','SERIALIZERS','MARKDOWN','TRACE','REQUIREMENTS','DEPENDENCY','PRIVACY','INSTALLATION','SERIALIZERS'],
'D257':['PRIVACY','PRIVACY','TYPES','TRACE'],
'D259':['PRIVACY','TYPES','TRACE'],'D261':['PRIVACY','TRACE']}
# Exhaustive finding-to-body sets, audited against all 60 D247-D259 findings.
# Each set includes its primary class. All additional classes become explicit
# supplemental resolution edges for both blocks and their parsed cell endpoints.
FINDING_BODIES={
'D247':[
 ('TYPES','REGISTRY','PRIVACY','DEPENDENCY','RECOVERY'),('COMPARISON',),
 ('AUTHORIZATION','COMMITMENT','PRIVACY','COMPARISON'),('PRIVACY','COMMITMENT'),
 ('DEPENDENCY','TYPES','RECOVERY'),('RECOVERY',),('SERIALIZERS','REQUIREMENTS'),
 ('REQUIREMENTS',),('TRACE',),('SERIALIZERS',),('INSTALLATION','SERIALIZERS')],
'D249':[
 ('TYPES',),('COMPARISON',),('PRIVACY','TYPES'),('DEPENDENCY','TYPES'),
 ('RECOVERY',),('SERIALIZERS','REQUIREMENTS'),('REQUIREMENTS',),('TRACE','MARKDOWN'),
 ('MARKDOWN',),('TRACE',),('SERIALIZERS',),('SERIALIZERS','REQUIREMENTS'),('INSTALLATION','SERIALIZERS')],
'D251':[
 ('TYPES',),('PRIVACY','TYPES'),('DEPENDENCY','TYPES'),('RECOVERY',),
 ('SERIALIZERS',),('REQUIREMENTS',),('MARKDOWN',),('TRACE',),
 ('SERIALIZERS','REQUIREMENTS'),('SERIALIZERS',),('INSTALLATION',)],
'D253':[
 ('REQUIREMENTS',),('REQUIREMENTS',),('DEPENDENCY','TYPES'),('PRIVACY','COMMITMENT'),
 ('MARKDOWN',),('TRACE',),('INSTALLATION',),('SERIALIZERS','REQUIREMENTS')],
'D255':[
 ('REQUIREMENTS',),('REQUIREMENTS','SERIALIZERS'),('SERIALIZERS',),('MARKDOWN',),
 ('TRACE',),('REQUIREMENTS','TYPES','PRIVACY','AUTHORIZATION'),('DEPENDENCY','TYPES'),
 ('PRIVACY','TYPES','AUTHORIZATION','COMMITMENT'),('INSTALLATION',),('SERIALIZERS','TRACE','REQUIREMENTS')],
'D257':[
 ('PRIVACY','TYPES'),('PRIVACY','AUTHORIZATION','COMPARISON','RECOVERY'),('TYPES',),('TRACE',)],
'D259':[
 ('PRIVACY','AUTHORIZATION','TYPES'),('TYPES','PRIVACY'),('TRACE','TYPES','PRIVACY','REQUIREMENTS')],
}
FINDING_BODIES['D261']=[('PRIVACY','TYPES'),('TRACE','COMPARISON','RECOVERY')]
MULTI_RESOLUTION={}
for root,bodysets in FINDING_BODIES.items():
    need(len(bodysets)==len(DEFECT_MAP[root]),('finding body count',root))
    for ordinal,names in enumerate(bodysets,1):
        need(len(names)==len(set(names)) and DEFECT_MAP[root][ordinal-1] in names,'finding primary body')
        MULTI_RESOLUTION[root,ordinal]=tuple(n for n in names if n!=DEFECT_MAP[root][ordinal-1])
# Section-level composite subjects also receive explicit destination sets.
SECTION_MULTI={
('E243',9):('REGISTRY','PRIVACY','DEPENDENCY','RECOVERY'),
('E244',11):('REGISTRY','PRIVACY','DEPENDENCY','RECOVERY'),
('E246',7):('PRIVACY','DEPENDENCY','RECOVERY'),('E246',8):('PRIVACY','DEPENDENCY','RECOVERY'),
('E246',10):('COMMITMENT',),('E246',11):('DEPENDENCY','TYPES'),
('E248',6):('PRIVACY','DEPENDENCY','RECOVERY'),('E248',8):('COMMITMENT',),
('E248',10):('TYPES',),('E248',11):('TYPES',),
('E250',6):('TYPES',),('E252',4):('TYPES',),('E254',3):('TYPES',),
('E256',6):('TYPES',),('E258',6):('TYPES',),
}

# Complete section-body register. Each value is the union of governing bodies
# required by the individual obligations in that section. Edges name the
# collective resolution set; they do not claim each body alone covers the whole
# section. Primary assignments remain unchanged. No implicit transitive edge.
SECTION_ADDITIONS={
'E243':{7:'AUTHORITY,TYPES,AUTHORIZATION,COMPARISON,RECOVERY',8:'AUTHORITY,SERIALIZERS,TRACE',9:'COMPARISON,AUTHORIZATION',10:'TYPES,COMMITMENT',11:'AUTHORITY,TYPES,AUTHORIZATION',12:'TYPES',13:'COMPARISON',14:'DEPENDENCY',15:'AUTHORITY',16:'AUTHORITY,COMMITMENT'},
'E244':{9:'AUTHORITY,TYPES,AUTHORIZATION,COMPARISON,RECOVERY',10:'AUTHORITY,SERIALIZERS,TRACE',11:'COMPARISON,AUTHORIZATION',12:'TYPES,COMMITMENT',13:'AUTHORITY,TYPES,AUTHORIZATION',14:'TYPES',15:'COMPARISON',16:'DEPENDENCY',17:'AUTHORITY',18:'AUTHORITY,COMMITMENT'},
'E246':{6:'AUTHORITY',7:'REGISTRY,AUTHORITY,SERIALIZERS,TRACE',8:'REGISTRY,COMPARISON,AUTHORIZATION',9:'AUTHORITY,TYPES,AUTHORIZATION,COMMITMENT,PRIVACY',10:'TYPES,PRIVACY,COMPARISON',11:'AUTHORITY',12:'COMPARISON,AUTHORITY',13:'AUTHORITY,COMMITMENT',14:'REQUIREMENTS',15:'SERIALIZERS',16:'MARKDOWN',17:'REGISTRY,REQUIREMENTS',18:'AUTHORITY',19:'AUTHORITY,REGISTRY,REQUIREMENTS,SERIALIZERS,INSTALLATION'},
'E248':{3:'TYPES,MARKDOWN',4:'TYPES,AUTHORITY',5:'AUTHORITY',6:'REGISTRY,AUTHORIZATION,COMPARISON',7:'TYPES,AUTHORIZATION,COMMITMENT,PRIVACY',8:'TYPES,DEPENDENCY',9:'AUTHORIZATION,TYPES,PRIVACY,COMPARISON',10:'AUTHORITY,AUTHORIZATION,COMMITMENT',11:'AUTHORITY,RECOVERY',12:'COMPARISON,DEPENDENCY',13:'AUTHORITY,REQUIREMENTS,REGISTRY,TYPES,DEPENDENCY,PRIVACY,AUTHORIZATION,COMMITMENT,COMPARISON,RECOVERY',14:'SERIALIZERS',15:'MARKDOWN',16:'REGISTRY',17:'REQUIREMENTS,TRACE,REGISTRY',18:'REQUIREMENTS,TRACE',19:'SERIALIZERS,AUTHORITY'},
'E250':{2:'AUTHORITY',3:'REGISTRY,TYPES,PRIVACY,DEPENDENCY,RECOVERY,AUTHORITY',4:'AUTHORIZATION,COMMITMENT,PRIVACY,TYPES',5:'TYPES,AUTHORIZATION,COMMITMENT,AUTHORITY',6:'RECOVERY,AUTHORITY',7:'DEPENDENCY,COMPARISON',8:'REQUIREMENTS',9:'SERIALIZERS',10:'MARKDOWN',11:'TRACE',12:'REQUIREMENTS,TRACE,REGISTRY',13:'REQUIREMENTS',14:'AUTHORITY,SERIALIZERS'},
'E252':{2:'AUTHORITY',3:'TYPES,AUTHORIZATION,COMMITMENT,AUTHORITY',4:'RECOVERY,AUTHORITY',5:'DEPENDENCY,COMPARISON',6:'REQUIREMENTS',7:'SERIALIZERS',8:'TYPES,PRIVACY,AUTHORIZATION,COMMITMENT',9:'TRACE',10:'MARKDOWN,REQUIREMENTS,SERIALIZERS',11:'REQUIREMENTS,TRACE,REGISTRY',12:'REQUIREMENTS',13:'AUTHORITY,SERIALIZERS',14:'TYPES,PRIVACY,DEPENDENCY,RECOVERY,COMPARISON,REQUIREMENTS,SERIALIZERS,MARKDOWN,INSTALLATION'},
'E254':{2:'SERIALIZERS',3:'AUTHORITY,RECOVERY',4:'TYPES,AUTHORIZATION,COMMITMENT,AUTHORITY',5:'TRACE',6:'MARKDOWN,SERIALIZERS,REQUIREMENTS',7:'AUTHORITY,SERIALIZERS',8:'REQUIREMENTS,TRACE,REGISTRY',9:'AUTHORITY,REQUIREMENTS,TYPES,DEPENDENCY,PRIVACY,AUTHORIZATION,COMMITMENT,COMPARISON,RECOVERY,MARKDOWN,INSTALLATION,SERIALIZERS',10:'REQUIREMENTS,TYPES,DEPENDENCY,PRIVACY,MARKDOWN,INSTALLATION,SERIALIZERS'},
}
# The E256/E258/E260 sections have the same complete semantic-book partition.
# Embedded profile/occurrence validation additionally owns cross-body joins.
for root in ('E256','E258','E260'):
    SECTION_ADDITIONS[root]={3:'REGISTRY',4:'AUTHORITY',5:'AUTHORITY',6:'RECOVERY,AUTHORITY',7:'TYPES,REGISTRY,AUTHORITY,AUTHORIZATION,COMMITMENT,COMPARISON,RECOVERY',8:'TYPES,COMMITMENT,DEPENDENCY',9:'AUTHORIZATION,TYPES,PRIVACY,COMPARISON',10:'TYPES,PRIVACY,AUTHORIZATION,COMMITMENT,AUTHORITY',11:'DEPENDENCY,COMPARISON',12:'SERIALIZERS',13:'REQUIREMENTS,TRACE,REGISTRY',14:'MARKDOWN,REQUIREMENTS,SERIALIZERS',15:'TRACE',16:'AUTHORITY,SERIALIZERS'}
# Complete literal requirement registers span the entire semantic book. Their
# REQUIREMENTS primary supplies conservation/serialization; the explicit core
# supplements carry each atom's protocol rule, including atomicity table cells.
for root,number in [('E246',15),('E248',14),('E250',9),('E252',7),('E254',2),('E256',12),('E258',12),('E260',12)]:
    SECTION_ADDITIONS[root][number]+=','+','.join(CORE)
SECTION_BODIES={}
for root,sections in SECTION_MAP.items():
    need(set(SECTION_ADDITIONS[root])==set(sections),'complete section audit domain')
    for number,primary_name in sections.items():
        names=tuple(dict.fromkeys((primary_name,*SECTION_MULTI.get((root,number),()),*SECTION_ADDITIONS[root][number].split(','))))
        SECTION_BODIES[root,number]=names
        SECTION_MULTI[root,number]=tuple(n for n in names if n!=primary_name)

INVERSE={'authority-retained':'authority-retained-inverse','corrected-by':'corrects','resolved-by':'resolves','realized-in':'realizes','assigned-to':'contains-assignment','composed-in':'contains-composition','specified-at':'specifies','covers-cell':'cell-of'}

def construct_trace(c):
    spec=importlib.util.spec_from_file_location('e256_markdown_parser',BASE/'review/parser.py');parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
    files=list((CORPUS/'docs').glob('*.md'))+list((BASE/'upload').glob('*.md'))
    byhash={H(p.read_bytes()):p.read_bytes() for p in files}
    roots={k:byhash[h] for k,h in ROOT_HASHES.items()}
    b245=next((BASE/'review').glob('B245-CANONICAL-V1.tsv'),None)
    if b245:roots['B245-CANONICAL-V1']=b245.read_bytes()
    else:
        e250=doc('SECOND_CORRECTION_AND_COMPLETION')
        rows=[r for r in table(section(e250,10)) if len(r)==3 and re.fullmatch('B0[1-9]',r[0])]
        roots['B245-CANONICAL-V1']=tsv('blocker_id subject required_closure'.split(),rows)
    need(H(roots['B245-CANONICAL-V1'])=='cbcab0d6899e9f82aa2fc9a26ad3c3d034c79d976a448626396d2df85062b32d','B245 digest')
    roots['E262']=c.payload.encode();endpoints={};primary=[];forward=[];root_counts={};assignments=[];seen_findings=set();section_assignments=[];seen_sections=set()
    def endpoint(id,root,start,end,b,kind):
        need(id not in endpoints,('duplicate endpoint',id));need(0<=start<=end<=len(b),'endpoint range')
        endpoints[id]=(root,str(start),str(end),H(b[start:end]),kind)
    def relation(a,b,kind,scope='SUPPLEMENTAL'):
        need(kind in INVERSE,'relation kind');forward.append((scope,a,b,kind))
    # Resolution destinations are exact nonempty body ranges, never heading-only.
    payload=roots['E262'];resolutions={}
    for name in (*CORE,'REQUIREMENTS','SERIALIZERS','TRACE','MARKDOWN','INSTALLATION'):
        marker=f'<!-- BEGIN E262-SEM-{name} -->\n'.encode();start=payload.index(marker)+len(marker)
        end=payload.index(f'<!-- END E262-SEM-{name} -->\n'.encode(),start)
        need(any(e['kind'] not in ('HEAD','BREAK') for e in parser.parse(payload[start:end])),'empty semantic resolution')
        id='E262-RANGE-SEM-'+name;endpoint(id,'E262',start,end,payload,'RANGE');resolutions[name]=id
    for root,b in roots.items():
        eps=parser.parse(b);section_number=None;defect=None;block_count=cell_count=0
        for i,e in enumerate(eps,1):
            id=f'{root}-{e["kind"]}-{i:06}';start,end=e['start'],e['end'];text=e['bytes'].decode();kind=e['kind']
            endpoint(id,root,start,end,b,kind);block_count+=1
            if kind=='HEAD':
                if text.startswith('## '):
                    m=re.match(r'## ([0-9]+)\. ',text);section_number=int(m[1]) if m else None;defect=None
                if text.startswith('### '):
                    m=re.match(r'### (?:(?:E(?:25[3579]|261)-)([0-9]{2})|([0-9]+)\.)',text)
                    defect=int(m[1] or m[2]) if m else None
                    if root=='D261':
                        m=re.match(r'### E261-([0-9]{2}) ',text);defect=int(m[1]) if m else None
            if root=='D247':
                m=re.match(r'([0-9]+)\. \*\*',text)
                if m:defect=int(m[1])
            name=SECTION_MAP.get(root,{}).get(section_number)
            if defect and root in DEFECT_MAP and defect<=len(DEFECT_MAP[root]):name=DEFECT_MAP[root][defect-1]
            if root=='B245-CANONICAL-V1':name='TRACE'
            if root=='E262':
                name=next((k for k,v in resolutions.items() if int(endpoints[v][1])<=start and end<=int(endpoints[v][2])),None)
            if defect and root in DEFECT_MAP:
                seen_findings.add((root,defect))
                assignments.append((root,defect,id,FINDING_BODIES[root][defect-1]))
            if (root,section_number) in SECTION_BODIES:
                seen_sections.add((root,section_number))
                section_assignments.append((root,section_number,id,SECTION_BODIES[root,section_number],text))
            target=resolutions[name] if name else id
            kindrel='resolved-by' if root.startswith('D') and name else 'corrected-by' if name else 'authority-retained'
            relation(id,target,kindrel,'PRIMARY');primary.append(id)
            extras=MULTI_RESOLUTION.get((root,defect),()) if defect and root in DEFECT_MAP else SECTION_MULTI.get((root,section_number),())
            for extra in extras:
                destination=resolutions[extra]
                if destination!=target:relation(id,destination,kindrel,'SUPPLEMENTAL')
            # Cell endpoint domain uses the exact parsed cell text; its physical
            # carrier is the row span and cell ordinal, not a guessed byte slice.
            for j,celltext in enumerate(e.get('cells',[]),1):
                cid=f'{id}-CELL-{j:03}';endpoint(cid,root,start,end,b,'CELL-'+str(j));cell_count+=1
                endpoints[cid]=(root,str(start),str(end),H(celltext.encode()),'CELL-'+str(j))
                relation(cid,target,kindrel,'PRIMARY');primary.append(cid);relation(id,cid,'covers-cell')
                if (root,section_number) in SECTION_BODIES:
                    section_assignments.append((root,section_number,cid,SECTION_BODIES[root,section_number],celltext))
                for extra in extras:
                    if resolutions[extra]!=target:relation(cid,resolutions[extra],kindrel,'SUPPLEMENTAL')
        root_counts[root]={'blocks':block_count,'cells':cell_count}
    # Every semantic body realizes actual source bytes, and the specification
    # copies the same range. No self-retention edge is counted as realization.
    for slot,n in sorted(c.source_art.items()):
        b=c.get(n);sid=c.meta[n]['id'];endpoint('ROOT:'+sid,f'A{n:04}',0,len(b),b,'ROOT')
        for name,(a,z) in c.source_ranges[slot].items():
            id=sid+'#SEM-'+name;endpoint(id,f'A{n:04}',a,z,b,'RANGE')
            need(b[a:z]==c.blocks[name].encode(),'source range bytes')
            relation(resolutions[name],id,'realized-in')
    specbytes=c.get(38);specid=c.meta[38]['id'];endpoint('SPEC:ROOT','A0038',0,len(specbytes),specbytes,'ROOT')
    for name,(a,z) in c.spec_ranges.items():
        id='SPEC:SEM-'+name;endpoint(id,'A0038',a,z,specbytes,'RANGE')
        need(specbytes[a:z]==c.blocks[name].encode(),'spec range bytes')
        relation(resolutions[name],id,'realized-in')
        for slot in c.source_art:relation(c.param['SUCCESSOR-NAMESPACE']+'-SOURCE-'+slot+'#SEM-'+name,id,'specified-at')
    for i in range(3,69):
        slot=f'S{i:02}'
        if slot in c.source_art:continue
        old=c.sources[slot];sid=c.param['SUCCESSOR-NAMESPACE']+'-SOURCE-'+slot;endpoint('ROOT:'+sid,slot,0,len(old['bytes']),old['bytes'],'ROOT')
    reqbytes=c.get(34);offset=len(reqbytes.splitlines(keepends=True)[0]);req_ids={}
    for r,line in zip(read_rows(reqbytes),reqbytes.splitlines(keepends=True)[1:]):
        id='REQ:'+r['requirement_id'];endpoint(id,'A0034',offset,offset+len(line),reqbytes,'ROW');offset+=len(line);req_ids[r['requirement_id']]=id
        anchor=f'<a id="{r["requirement_anchor"]}"></a>'.encode();a=specbytes.index(anchor);z=specbytes.index(b'\n',a)+1
        dest='SPEC:'+r['requirement_id'];endpoint(dest,'A0038',a,z,specbytes,'REQUIREMENT');relation(id,dest,'specified-at')
        for sid in r['normative_source_ids'].split(', '):
            relation(id,'ROOT:'+sid,'assigned-to')
            slot=sid[-3:]
            if slot in c.source_art:
                n=c.source_art[slot];source=c.get(n)
                needle=('| '+r['requirement_id']+' |').encode();a=source.index(needle);z=source.index(b'\n',a)+1
                local=sid+'#REQ-'+r['requirement_id'];endpoint(local,f'A{n:04}',a,z,source,'REQUIREMENT')
                relation(id,local,'realized-in');relation(local,dest,'specified-at')
    # Every section/family row resolves to the physical specification section,
    # and every requirement is assigned to both its RF and SF row.
    sections=c.get(36);offset=len(sections.splitlines(keepends=True)[0]);family_ids={}
    for r,line in zip(read_rows(sections),sections.splitlines(keepends=True)[1:]):
        id='FAMILY:'+r['identifier'];endpoint(id,'A0036',offset,offset+len(line),sections,'ROW');offset+=len(line)
        if r['record_class']=='ROOT':relation(id,'SPEC:ROOT','specified-at');continue
        family_ids[r['identifier']]=id
        anchor=f'<a id="{c.param["SUCCESSOR-NAMESPACE"].lower()}-{r["identifier"].lower()}"></a>'.encode()
        a=specbytes.index(anchor);level=b'\n## ' if r['record_class']=='SF' else b'\n### '
        heading=specbytes.index(level,a);next_anchor=specbytes.find(b'\n<a id=',heading+len(level))
        # The endpoint contains the actual family heading and at least its first
        # normative child row/body. It is structural, not a semantic resolution.
        z=next_anchor if next_anchor!=-1 else len(specbytes)
        dest='SPEC:FAMILY:'+r['identifier'];endpoint(dest,'A0038',a,z,specbytes,'SECTION')
        relation(id,dest,'specified-at')
    for r in read_rows(reqbytes):
        for k in ('rf_family','sf_family'):relation(req_ids[r['requirement_id']],family_ids[r[k]],'assigned-to')
    comp=c.get(32);offset=len(comp.splitlines(keepends=True)[0])
    for row,line in zip(read_rows(comp),comp.splitlines(keepends=True)[1:]):
        id='COMPOSITION:'+row['composition_order'];endpoint(id,'A0032',offset,offset+len(line),comp,'ROW');offset+=len(line)
        a=req_ids.get(row['from_id'],'ROOT:'+row['from_id']);relation(a,id,'composed-in')
        dest='SPEC:'+row['from_id'] if row['from_id'] in req_ids else 'SPEC:ROOT'
        relation(id,dest,'specified-at')
    # Registry zero-member semantics get both a source semantic realization and
    # a concrete header-only artifact endpoint, rather than an assertion count.
    registry=c.get(28);endpoint('REGISTRY:EMPTY','A0028',0,len(registry),registry,'EMPTY-REGISTRY');relation(resolutions['REGISTRY'],'REGISTRY:EMPTY','realized-in')
    for a,info in endpoints.items():
        if info[-1]=='RANGE' and a.startswith('E262-RANGE'):
            need(any(x==a and kind=='realized-in' for _,x,y,kind in forward) or a in [resolutions[k] for k in ['REQUIREMENTS','SERIALIZERS','TRACE','MARKDOWN','INSTALLATION']],'missing realization')
    need(len(primary)==len(set(primary)),'primary uniqueness')
    need(seen_findings==set(MULTI_RESOLUTION),'finding inventory completeness')
    resolution_pairs={(a,b) for _,a,b,k in forward if k in ('resolved-by','corrected-by')}
    for root,ordinal,id,names in assignments:
        for name in names:need((id,resolutions[name]) in resolution_pairs,('finding resolution missing',id,name))

    need(seen_sections==set(SECTION_BODIES),'section inventory completeness')
    for root,number,id,names,clause in section_assignments:
        for name in names:need((id,resolutions[name]) in resolution_pairs,('section obligation destination missing',id,name))

    forward=sorted(set(forward),key=lambda r:(r[0]!='PRIMARY',r[1],r[3],r[2]));rows=[]
    for scope,a,b,kind in forward:
        need(a in endpoints and b in endpoints,('dangling trace',a,b))
        order=len(rows)+1;status='retained-only' if kind=='authority-retained' else 'resolved-body' if kind in ('corrected-by','resolved-by') else 'realized' if kind in ('realized-in','specified-at') else 'structural'
        rows.append([f'{order:06}',scope,'FORWARD',a,b,kind,f'{order+1:06}',status])
        rows.append([f'{order+1:06}',scope,'REVERSE',b,a,INVERSE[kind],f'{order:06}',status])
    for i in range(0,len(rows),2):
        a,b=rows[i:i+2];need(a[3]==b[4] and a[4]==b[3] and a[6]==b[0] and b[6]==a[0],'trace inverse')
    c.trace_endpoints=endpoints
    c.trace_report={'roots':root_counts,'primary_endpoints':len(primary),'declared_endpoints':len(endpoints),'forward_relations':len(forward),'paired_rows':len(rows),'heading_only_resolution_destinations':0}
    audit=WORK/'results/complete-construction';audit.mkdir(exist_ok=True)
    (audit/'semantic-assignment-audit.tsv').write_bytes(tsv('review finding endpoint required_bodies'.split(),[[root,f'{ordinal:02}',id,','.join(names)] for root,ordinal,id,names in assignments]))
    (audit/'section-obligation-audit.tsv').write_bytes(tsv('root section endpoint collective_bodies exact_text_json'.split(),[[root,str(number),id,','.join(names),json.dumps(clause,ensure_ascii=True)] for root,number,id,names,clause in section_assignments]))
    (audit/'trace-endpoints.tsv').write_bytes(tsv('endpoint root start end sha256 kind'.split(),[[k,*v] for k,v in sorted(endpoints.items())]))
    return tsv('trace_order scope direction from_endpoint to_endpoint relation inverse_trace_order coverage_status'.split(),rows)
````
<!-- END E262-SEM-TRACE -->

## 15. MARKDOWN

<!-- BEGIN E262-SEM-MARKDOWN -->
The canonical block/cell scanner is the supplied E255 diagnostic parser with SHA-256 be8d12e93dc70b68443a6739382d2fd8dff9bab53f223bb98c947dc55018d58c. E256 adopts its exact parse and cells algorithms as construction notation, without treating its diagnostic driver as authority. The valid unmatched-backtick continuation has two cells and remains TROW. A separately supplied three-cell continuation is rejected from the two-column table. The complete physical-byte coverage and D247 missing-final-LF reconstruction tests are retained. Trace imports the exact parser bytes; no repaired expected result changes the scanner.

````python
from pathlib import Path
import re,hashlib,unicodedata,json
# Preserve slices; escaped bytes skipped and exact matching backtick runs only.
def cells(line):
 s=line.rstrip('\n');sep=[];i=0
 while i<len(s):
  if s[i]=='\\':i+=2;continue
  if s[i]=='`':
   j=i
   while j<len(s) and s[j]=='`':j+=1
   n=j-i;k=j;end=None
   while k<len(s):
    if s[k]=='\\':k+=2;continue
    if s[k]=='`':
     q=k
     while q<len(s) and s[q]=='`':q+=1
     if q-k==n:end=q;break
     k=q
    else:k+=1
   if end is not None:i=end;continue
   i=j;continue
  if s[i]=='|':sep.append(i)
  i+=1
 cuts=[-1]+sep+[len(s)];out=[s[a+1:b].strip(' ') for a,b in zip(cuts,cuts[1:])]
 if sep and not out[0]:out=out[1:]
 if sep and not out[-1]:out=out[:-1]
 return out,len(sep)
def parse(b):
 t=b.decode('utf-8');assert not t.startswith('\ufeff') and '\r' not in t and unicodedata.normalize('NFC',t)==t
 ls=t.splitlines(keepends=True); offsets=[0]
 for x in ls:offsets.append(offsets[-1]+len(x.encode()))
 assert b==b''.join(x.encode() for x in ls)
 def blank(i):return not ls[i].rstrip('\n').strip(' \t')
 def basic(i):
  s=ls[i].rstrip('\n')
  m=re.fullmatch(r' {0,3}(`{3,})([^`]*)',s) or re.fullmatch(r' {0,3}(~{3,})([^~]*)',s)
  if m:return ('FENCE',m.group(1))
  if re.fullmatch(r' {0,3}\$\$ *',s):return ('FORMULA',None)
  if re.fullmatch(r' {0,3}\$\$.+\$\$ *',s):return ('FORMULA1',None)
  if re.fullmatch(r' {0,3}#{1,6} .+',s):return ('HEAD',None)
  if any(re.fullmatch(' {0,3}'+re.escape(ch)+'(?: *'+re.escape(ch)+'){2,} *',s) for ch in '*-_'):return ('BREAK',None)
  if i+1<len(ls) and not blank(i) and not blank(i+1):
   a,_=cells(ls[i]);d,_=cells(ls[i+1])
   if len(a)==len(d)>0 and all(re.fullmatch(r':?-{3,}:?',x) for x in d):return ('TABLE',len(a))
  m=re.match(r'^( {0,3})(?:[-*+] |[0-9]{1,9}\. )',s)
  if m:return ('LIST',len(m.group(1))+2)
  if s.startswith('    '):return ('LINE',None)
  return ('PARA',None)
 eps=[];gaps=[];i=0
 def emit(k,a,z):eps.append({'kind':k,'start':offsets[a],'end':offsets[z],'line':a+1,'bytes':b[offsets[a]:offsets[z]],'cells':cells(ls[a])[0] if k in ('THEAD','TDELIM','TROW') else []})
 while i<len(ls):
  if blank(i):gaps.append((offsets[i],offsets[i+1]));i+=1;continue
  k,v=basic(i);a=i;i+=1
  if k=='FENCE':
   while i<len(ls) and not re.fullmatch(r' {0,3}'+re.escape(v[0])+'{'+str(len(v))+r',} *',ls[i].rstrip('\n')):i+=1
   if i==len(ls):raise ValueError(('UNCLOSED-FENCE',a+1))
   i+=1
  elif k=='FORMULA':
   while i<len(ls) and not re.fullmatch(r' {0,3}\$\$ *',ls[i].rstrip('\n')):i+=1
   if i==len(ls):raise ValueError(('UNCLOSED-FORMULA',a+1))
   i+=1
  elif k=='FORMULA1':k='FORMULA'
  elif k=='TABLE':
   emit('THEAD',a,a+1);emit('TDELIM',i,i+1);i+=1
   while i<len(ls) and not blank(i):
    c,p=cells(ls[i])
    if not p:break
    if len(c)!=v:raise ValueError(('INVALID-TABLE-CELL-COUNT',i+1,len(c),v))
    emit('TROW',i,i+1);i+=1
   continue
  elif k=='LIST':
   while i<len(ls):
    j=i
    while j<len(ls) and blank(j):j+=1
    if j<len(ls) and len(ls[j])-len(ls[j].lstrip(' '))>=v:i=j+1
    else:break
  elif k=='PARA':
   while i<len(ls) and not blank(i) and basic(i)[0]=='PARA':i+=1
  emit(k,a,i)
 spans=sorted([(e['start'],e['end']) for e in eps]+gaps)
 assert b==b''.join(b[a:z] for a,z in spans)
 return eps
if __name__=='__main__':
 R=Path('review/corpus');U=Path('upload')
 roots={'E243':'97f5201adbed45395a1cbc0d3db2fd6a8419d36d687a1bfe25c901e99c9c59d3','E244':'d57807fc9da70a5a0cfa4a37897256b336fc18dba2aa987d97ad5d5146e99f30','E246':'a191d11525b254374731562f40fd2be142fa00d8c89c03441bc0b694c66cb493','E248':'1f5b59b0ff4720ee142a42017f13e543e1a3973fd81113ca86ca2ead43834a73','E250':'558747f7091ab5e5f597a3f3fba3acb987ea28dfd652e7e691e81371d2b5ccf2','E252':'7bffea0286c19cc8c1f560ab694849814823e0566d0a6dc8f1118e6a949b3343','D247':'35f2ce9bb84aaec7e3d5dfecb341d3d04cadb65060d89028a4e70a08e731bcc5','D249':'636899f5426b8a70065b7f7193bba8ef1d0542e10c2ecc014a90cea39990bb37','D251':'ae67f309c7d13a656d0e5d66a89ad016eb64910a464897def54116e02cef940b','D253':'8d73384f9f6a32103d7fb8c419527faf11514ae3110465f7c8b84a072e43683b','E254':'2b3193b69df04c335c88e5078b2defb6784a73d707192a6208eda7ff48b0fae6'}
 files={hashlib.sha256(p.read_bytes()).hexdigest():p for p in list(R.rglob('*.md'))+list(U.glob('Engineering-*-*review*.md'))}
 out={}
 for name,sha in roots.items():
  b=files[sha].read_bytes()
  try:
   eps=parse(b);out[name]={'blocks':len(eps),'cells':sum(len(e['cells']) for e in eps)}
   for i,e in enumerate(eps,1):e['id']=f'{name}-{e["kind"]}-{i:06}';e['sha256']=hashlib.sha256(e['bytes']).hexdigest();e['text']=e.pop('bytes').decode()
   Path('review/'+name+'-endpoints.json').write_text(json.dumps(eps,indent=2))
  except Exception as e:out[name]={'error':str(e)}
 print(json.dumps(out,indent=2));Path('review/parser-results.json').write_text(json.dumps(out,indent=2))
 for s in ['| A | B |\n| --- | --- |\n| `x | y |\n','| A | B |\n| --- | --- |\n| x | y | z |\n','```abnf\na = b\n```\nAfter.\n','- item\n  continuation\n\nParagraph.\n','$$\nx+y\n$$\n---\n    indented\n','# Final','| A | B |\n| --- | --- |\n| x\\|y | `p|q` |\n']:
  try:print('VECTOR',repr(s),[e['kind'] for e in parse(s.encode())])
  except Exception as e:print('VECTOR',repr(s),str(e))
 print('CELLS',cells('| `x | y |'))
````
<!-- END E262-SEM-MARKDOWN -->

## 16. INSTALLATION

<!-- BEGIN E262-SEM-INSTALLATION -->
Installation remains distinct from protocol execution. The inherited E252 section 13 outside-attempt authority binding, nine-line authorization bytes, signature algorithm, destination digest, prior-manifest admission and durable PREPARE-before-mutation guarantees remain mandatory. This block supplies the complete corrected control transition algorithm. It does not provide installation authorization or assert filesystem durability from an in-memory test.

The initial eight dispatch cells are unchanged: either operation with IDENTICAL-COMPLETE is a verified no-op; INSTALL admits ABSENT and rejects DIFFERENT-COMPLETE/PARTIAL-INVALID; REPLACE admits DIFFERENT-COMPLETE and rejects ABSENT/PARTIAL-INVALID. A partial destination is recoverable only through an independently valid matching attempt, not through initial reclassification. Foreign bytes, malformed or unauthenticated rows, missing prior blobs and unsupported durable atomic append/mutation capability reject before any mutation.

Append one signed RECOVERY-BEGIN before recovery work; it is a one-way barrier, never a retry loop. New closed entry kinds are RECOVERY-BEGIN, CANCEL-CREATE and CANCEL-REPLACE. RECOVERY-BEGIN uses zero path fields, NOT-APPLICABLE prior fields, package digest and RECOVERING result. CANCEL copies its pending forward PREPARE path/prior/candidate cells and uses NOT-APPLIED result. All other digest/signature/chain preimages remain unchanged. Checkpoints are forward-only and never restarted during recovery.

For pending forward intent, exact candidate bytes take precedence over exact prior bytes, even if both equal. Append APPLY for candidate; otherwise append CANCEL for exact prior; otherwise block without mutation. For pending rollback, prior equality takes precedence: append APPLY-ROLLBACK immediately; otherwise exact candidate permits the one prepared rollback mutation and subsequent APPLY; otherwise block. Resolve every pending intent before preparing another path. Roll back the largest remaining applied ordinal. Terminal ROLLED-BACK requires exact original bytes/absence and no pending or outstanding applied path. Re-entry from every valid prefix repeats the same deterministic next transition.

The integer rank is implemented by measure: nonterminal base 1, weight 3 per outstanding applied path; a pending rollback replaces its path weight with 2 before mutation or 1 after restoration; pending forward adds 4; absence of the recovery barrier adds 1; terminal rank 0. Each permitted recovery step strictly decreases rank. Appending rollback PREPARE cannot increase it. Equal prior/candidate paths already satisfy the after-restoration weight, preserving strict decrease. External corruption yields a blocked result, not a claimed decreasing mutation. Finite crashes can resume at any durable prefix; an environment that fails indefinitely cannot be promised liveness.

The listing's synthetic path-i.bin and package/prior digest adapters stand for the exact candidate path and prior manifest bytes admitted above. Only the control state/row transition algorithm is normative; live installers must bind those adapters to the 40-member manifest and externally authorized byte identities. No live installer is executed by this correction.

### Constructor module: install_model.py

````python
"""Proposed E256 recovery model: synthetic bytes, signed logs, no filesystem mutation.

This implements installation control only, not Privacy Engine transaction semantics.
The caller supplies an already verified external authority binding and byte manifests.
Full authorization admission remains outside this module's test coverage.
"""
from dataclasses import dataclass, field
import copy
import hashlib
import json
from functools import lru_cache, cached_property
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

H=lambda b:hashlib.sha256(b).hexdigest()
NA='NOT-APPLICABLE'
HEADER='entry_order entry_type attempt_id path_order relative_path prior_state prior_sha256 candidate_sha256 result_state previous_entry_sha256 entry_sha256 authority_id signature'.split()

class Invalid(ValueError): pass

def require(ok,reason):
    if not ok: raise Invalid(reason)

@lru_cache(maxsize=65536)
def verified_signature(public_bytes, signature, digest):
    # Pure memoization by every cryptographic input; altered bytes never hit.
    Ed25519PublicKey.from_public_bytes(public_bytes).verify(signature,digest)

@dataclass
class Model:
    old: tuple
    new: tuple
    state: list
    log: list=field(default_factory=list)
    # Isolated test key. This is never real installation authority.
    key: object=field(default_factory=lambda:Ed25519PrivateKey.from_private_bytes(bytes(range(32))))
    aid: str='SYNTHETIC-AUTH'
    attempt: str='SYNTHETIC-AUTH-ATTEMPT-000001'

    def clone(self):
        return Model(self.old,self.new,list(self.state),copy.deepcopy(self.log),self.key,self.aid,self.attempt)

    @property
    def mode(self): return 'CREATE' if all(x is None for x in self.old) else 'REPLACE'
    @cached_property
    def package(self): return H(b'PACKAGE\n'+b''.join(f'{i:06}\t{H(b)}\n'.encode() for i,b in enumerate(self.new,1)))
    @cached_property
    def prior(self): return 'ABSENT' if self.mode=='CREATE' else H(b'PRIOR\n'+b''.join(f'{i:06}\t{H(b)}\n'.encode() for i,b in enumerate(self.old,1)))
    @cached_property
    def public_bytes(self): return self.key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)

    def cells(self,kind,i,applied):
        """The first nine cells; chain and signature are constructed separately."""
        zero=i is None
        ps=NA;ph=NA;ch=self.package;result='PRESENT'
        if kind=='BEGIN':
            ps='ABSENT' if self.mode=='CREATE' else 'DIFFERENT-COMPLETE';ph=self.prior
        elif kind=='RECOVERY-BEGIN':result='RECOVERING'
        elif kind=='CHECKPOINT':
            ch=H(b'PE-TSE-INSTALL-CHECKPOINT-V1\n'+b''.join(f'{j+1:06}\t{H(self.new[j])}\n'.encode() for j in sorted(applied)))
        elif kind.startswith('TERMINAL-'):
            result=kind.removeprefix('TERMINAL-');kind='TERMINAL'
        elif not zero:
            if 'ROLLBACK-' in kind:
                ps='PRESENT';ph=H(self.new[i]);ch='ABSENT' if self.old[i] is None else H(self.old[i])
                result='INTENT-RECORDED' if kind.startswith('PREPARE-') else ('REMOVED' if self.old[i] is None else 'RESTORED')
            else:
                ps='ABSENT' if self.old[i] is None else 'PRESENT';ph='ABSENT' if self.old[i] is None else H(self.old[i]);ch=H(self.new[i])
                result='INTENT-RECORDED' if kind.startswith('PREPARE-') else 'NOT-APPLIED' if kind.startswith('CANCEL-') else 'PRESENT'
        return [f'{len(self.log)+1:06}',kind,self.attempt,'000000' if zero else f'{i+1:06}',NA if zero else f'path-{i+1:04}.bin',ps,ph,ch,result]

    def append(self,kind,i=None):
        replay=self.replay()
        first=self.cells(kind,i,replay['applied'])+[self.log[-1][10] if self.log else '0'*64]
        digest=H(b'PE-TSE-INSTALL-ENTRY-V1\n'+('\t'.join(first)+'\n').encode())
        self.log.append(first+[digest,self.aid,self.key.sign(bytes.fromhex(digest)).hex()])
        self.replay()

    def replay(self):
        applied=set();rolled=set();pending=None;recovery=False;terminal=None;next_i=0;checkpoint_due=False;prev='0'*64
        # Derive state only from signed records; do not trust cached sets/checkpoints.
        for order,r in enumerate(self.log,1):
            require(len(r)==13,'arity')
            require(r[0]==f'{order:06}' and r[2]==self.attempt and r[9]==prev and r[11]==self.aid,'identity or chain')
            dg=H(b'PE-TSE-INSTALL-ENTRY-V1\n'+('\t'.join(r[:10])+'\n').encode())
            require(dg==r[10],'digest')
            try:verified_signature(self.public_bytes,bytes.fromhex(r[12]),bytes.fromhex(dg))
            except (InvalidSignature,ValueError):raise Invalid('signature')
            require(terminal is None,'after terminal')
            k=r[1]; i=None if r[3]=='000000' else int(r[3])-1
            require(i is None or 0<=i<len(self.new),'path ordinal')
            saved=self.log;self.log=self.log[:order-1]
            try:expected=self.cells('TERMINAL-'+r[8] if k=='TERMINAL' else k,i,applied)
            finally:self.log=saved
            require(r[:9]==expected,'entry cells')
            if order==1:
                require(k=='BEGIN' and i is None,'first BEGIN')
            elif k=='RECOVERY-BEGIN':
                require(not recovery and i is None,'duplicate recovery');recovery=True;checkpoint_due=False
            elif k=='PREPARE-'+self.mode:
                require(not recovery and pending is None and not checkpoint_due and i==next_i,'forward prepare')
                pending=(k,i)
            elif k=='APPLY-'+self.mode:
                require(pending==('PREPARE-'+self.mode,i),'forward apply pairing')
                pending=None;applied.add(i);next_i+=1;checkpoint_due=not recovery
            elif k=='CANCEL-'+self.mode:
                require(recovery and pending==('PREPARE-'+self.mode,i),'cancel pairing')
                pending=None
            elif k=='CHECKPOINT':
                require(not recovery and pending is None and checkpoint_due and i is None,'checkpoint position')
                checkpoint_due=False
            elif k.startswith('PREPARE-ROLLBACK-'):
                require(recovery and pending is None and applied and i==max(applied),'rollback order')
                require(k==('PREPARE-ROLLBACK-REMOVE' if self.mode=='CREATE' else 'PREPARE-ROLLBACK-RESTORE'),'rollback kind')
                pending=(k,i)
            elif k.startswith('APPLY-ROLLBACK-'):
                require(recovery and pending==('PREPARE-'+k.removeprefix('APPLY-'),i),'rollback apply pairing')
                pending=None;applied.remove(i);rolled.add(i)
            elif k=='TERMINAL':
                require(pending is None and i is None,'terminal pending')
                if r[8]=='COMPLETE':require(not recovery and len(applied)==len(self.new) and not checkpoint_due,'complete state')
                elif r[8]=='ROLLED-BACK':require(recovery and not applied,'rollback state')
                else:raise Invalid('terminal outside model')
                terminal=r[8]
            else:raise Invalid('invalid entry kind or order')
            prev=dg
        return dict(applied=applied,rolled=rolled,pending=pending,recovery=recovery,terminal=terminal,next_i=next_i,checkpoint_due=checkpoint_due)

    def verify_bytes(self,r):
        p=r['pending']
        for i,current in enumerate(self.state):
            if p and p[1]==i:
                require(current==self.old[i] or current==self.new[i],'pending foreign bytes')
            else:
                require(current==(self.new[i] if i in r['applied'] else self.old[i]),'foreign bytes')

    def measure(self):
        r=self.replay();self.verify_bytes(r)
        if r['terminal']:return 0
        # One pending forward intent may add at most one applied path (weight 3).
        # Unprepared rollback path=3; prepared before mutation=2; postmutation=1.
        weight=3*len(r['applied'])+1
        if r['pending']:
            k,i=r['pending']
            if 'ROLLBACK' in k:weight-=3;weight+=1 if self.state[i]==self.old[i] else 2
            else:weight+=4
        if not r['recovery']:weight+=1
        return weight

    def recover_step(self):
        r=self.replay();self.verify_bytes(r)
        if r['terminal']:return 'TERMINAL'
        if not r['recovery']:
            self.append('RECOVERY-BEGIN');return 'RECOVERY-BEGIN'
        if r['pending']:
            k,i=r['pending']
            if 'ROLLBACK' in k:
                if self.state[i]==self.old[i]:
                    self.append(k.replace('PREPARE-','APPLY-',1),i);return 'ROLLBACK-APPLY'
                # The existing signed PREPARE is the authorization for this mutation.
                self.state[i]=self.old[i];return 'ROLLBACK-MUTATION'
            if self.state[i]==self.new[i]:
                self.append('APPLY-'+self.mode,i);return 'FORWARD-APPLY'
            self.append('CANCEL-'+self.mode,i);return 'FORWARD-CANCEL'
        if r['applied']:
            self.append('PREPARE-ROLLBACK-'+('REMOVE' if self.mode=='CREATE' else 'RESTORE'),max(r['applied']));return 'ROLLBACK-PREPARE'
        self.append('TERMINAL-ROLLED-BACK');return 'ROLLED-BACK'

    def finish_recovery(self,collect=False):
        samples=[];history=[]
        for _ in range(4*len(self.new)+10):
            before=self.measure()
            terminal=self.replay()['terminal']
            if terminal:
                require(tuple(self.state)==(self.new if terminal=='COMPLETE' else self.old),'terminal byte mismatch');return samples,history
            step=self.recover_step();after=self.measure()
            require(after<before,('nondecreasing progress',step,before,after))
            history.append([step,before,after])
            if collect:samples.append(self.clone())
        raise Invalid('step bound exceeded')

def test():
    stats={}
    for mode in ['CREATE','REPLACE']:
        new=tuple(f'candidate-{i}'.encode() for i in range(40))
        old=tuple(None for _ in new) if mode=='CREATE' else tuple(v if i%2==0 else f'prior-{i}'.encode() for i,v in enumerate(new))
        m=Model(old,new,list(old));m.append('BEGIN');prefixes=[m.clone()]
        for i in range(40):
            m.append('PREPARE-'+mode,i);prefixes.append(m.clone())
            m.state[i]=new[i];prefixes.append(m.clone())
            m.append('APPLY-'+mode,i);prefixes.append(m.clone())
            m.append('CHECKPOINT');prefixes.append(m.clone())
        m.append('TERMINAL-COMPLETE');assert tuple(m.state)==new
        recovered=0;steps=0;reentries=0
        for p in prefixes:
            done,history=p.finish_recovery(collect=True);recovered+=1;steps+=len(history)
            # Restart from each actual recovery boundary once on the complete
            # forward prefix. Other prefix recoveries still check each rank drop.
            if len(p.log)>0 and recovered==len(prefixes):
                for q in done:
                    q.finish_recovery();reentries+=1
            before=copy.deepcopy(p.log);p.finish_recovery();assert p.log==before
        reject=0
        for which in ['tamper','authority','foreign','duplicate-recovery','wrong-signature']:
            p=prefixes[0].clone()
            # prefixes have been recovered in place, so use a new valid base.
            p=Model(old,new,list(old));p.append('BEGIN')
            if which=='tamper':p.log[0][9]='1'*64
            elif which=='authority':p.aid='OTHER'
            elif which=='foreign':p.state[0]=b'foreign'
            elif which=='wrong-signature':p.log[0][-1]='0'*128
            else:
                p.append('RECOVERY-BEGIN')
                try:p.append('RECOVERY-BEGIN')
                except Invalid:reject+=1;continue
                raise AssertionError('duplicate recovery accepted')
            prior=list(p.state)
            try:p.recover_step()
            except Invalid:reject+=1
            else:raise AssertionError(('invalid accepted',which))
            assert p.state==prior
        stats[mode]=dict(forward_interruption_prefixes=recovered,strict_progress_steps=steps,recovery_reentry_boundaries=reentries,invalid_no_mutation_cases=reject,equal_individual_paths=sum(a==b for a,b in zip(old,new)))
    return stats

if __name__=='__main__':
    result=test()
    print(json.dumps(result,indent=2))
    (Path(__file__).parent/'results/install-model-results.json').write_text(json.dumps(result,indent=2)+'\n')
````
<!-- END E262-SEM-INSTALLATION -->

## 17. Author construction and next gate

The separate author report and fresh executed evidence bind this exact payload by SHA-256, bytes and LF count. Author PASS is not independent acceptance. Four real identity inputs remain deferred. Symbolic and synthetic artifacts are non-installable review vectors; M=0.

The supplied repository checkpoint is Engineering[260] commit a0df08f94657849b10177798a3c934fa350d9ca9, parent 0557a207255d99f5f314d4b9f141074cd2220274. No actual Engineering[262] repository commit or remote update is claimed here. The completion workflow verifies that checkpoint, preserves every prior corpus member, commits only this supporting document, verifies the two lightweight tags and remote main, and packages Engineering[263] from the actual committed bytes. Engineering[263] performs a fresh complete independent review. Published G2 remains immutable and unchanged; M=0; I164 adoption not-performed; readiness blocked-pending-published-successor-correction. No real successor identity, mapping, profile, candidate, specification, publication, succession or adoption follows from author verification.
