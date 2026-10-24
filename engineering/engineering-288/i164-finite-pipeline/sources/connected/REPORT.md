# CF-01 correction — bounded connected finite receipt

Implementation author: SU-Engineering[288C]. Independent closure remains pending.

## Incorporated review and original witness

The supplied independent review verifies as 34,472,947 bytes, 76 entries,
SHA-256 633f343a9301c3311bbd9779fcef826cc97c396595f404fa4423eac5d2528201.
CRC, exact archive membership and every manifest member were checked. Its exact
embedded author checkpoint also verifies (13,433,845 bytes, 181 entries,
525fa0fe01c52266557ed025c4474bef02c74a6d7d4fa6f38d8c2c4a70b159e6).
The review's 19 focused controls and eight post-chain checks remain separate from
its full fault-injected chain and the 48 supplied author controls it inspected.
No completed component review suite was rerun. Prior component support is retained.

CF-01 is the attribution/correspondence distinction: the old connection correctly
hashed a modified `04-ledger/result.json` but did not establish its claims against
the ledger. The exact original witness changes only contexts[0].node_duties from
9,339 to 0. Old `output_bindings()` freshly reproduced acceptance against the
review's actual saved stage outputs, while the actual ledger still has 9,339 node
duties. The original public-run false receipt, original/mutated summary, recipe,
review harness and findings are copied byte-for-byte with archive-member provenance.
The prior full public-run witness is inspected retained evidence, not a new rerun.

## Minimal correction and governing source

Only inherited runtime file `code/connect.py` changes. Existing stage validators,
worker, recovery machinery, archive pins, candidate and draft sources are unchanged.
`ledger/code/ledger.py::summary` defines the redundant summary contract;
`::main` adds the exact emitted ledger byte identity. Both source and ledger
CONTRACT.md are copied with exact identities for inspection.

After existing selected-byte, model/acquisition, verification-receipt, context and
obligation checks, the correction parses one exact ledger-byte snapshot and derives:

| Summary claim | Validated source |
| --- | --- |
| Context name and order | ledger.contexts in their validated order |
| node_duties | number of node-duty entries, including empty directories |
| relation_duties | number of relation-duty entries, including zero-count duties |
| fold_duties | number of n-ary fold-duty entries |
| token_members | sum of occurrence-key memberships in node duties |
| edge_members | sum of ordered-edge memberships in relation duties |
| binding | exact validated model/acquisition binding |
| ledger identity | byte length and SHA-256 of the same validated ledger bytes |
| source_only_obligations | length of the preserved SOURCE-ONLY obligation set |
| qualification, canonical rebinding, final binding, admission | validated ledger fields |
| status string | unchanged source-fixed mechanical-summary status |

The entire redundant summary must equal that derived envelope, with exact JSON
types, key set and context ordering. Missing/extra fields, altered values and
coordinated substitutions reject. The final receipt takes ledger_contexts from
the derived value, never from submitted summary metadata. The identity attached
to the summary is computed from the actual checked summary bytes. Equivalent JSON
serialization remains allowed, with its own truthful byte identity.

No 9,339/9,376/12/2,376/2,368 fixture constants supply validation expectations.
The public chain still validates the ledger through its unchanged public API;
`output_bindings()` remains an internal linkage helper requiring validated inputs.
The correction does not make that helper a standalone ledger authenticator.

## Adjacent summary assessment

The other reported context counts come from the output-verification receipt,
which is already compared in full with the embedded verification receipt of the
exact validated ledger. They cannot be altered in both places without changing
ledger bytes and failing the selected-ledger/public validation path. Input-stage
validation is consumed by existing APIs; its unused metadata is not promoted to
new final-receipt claims. No unrelated component contract is reopened.

## Fresh checks and preservation

Results distinguish fresh CF-01 linkage controls, fresh subprocess/recovered-code
controls, the clean actual connected run and the corrected full fault-injection
run. In the latter, all four original stage functions/subprocesses execute before
the one summary mutation. Successful component stages are not confused with a
successful final receipt: the corrupted summary must reject and no receipt may
be written. This is constructed offline fault injection, not an assertion of
corruption on Steve's host or adversarial-runtime assurance.

Original selected bundle/model/ledger bytes, both contexts, all O01–O11 collections
and their status lists remain unchanged. Exact 666-member candidate and 163-member
draft manifests are checked through the same existing preflight. Historical
identities, relationships, ordinals and prior scoped findings are preserved.
No database connection, request, session operation, acquisition, lifecycle,
completed-review suite, global expansion, canonical rebinding or policy change.

Recovery rejected undeclared partial files. Their bytes and failed attempts are
preserved outside strict input roots; membership was not weakened. One early
continuation failed before writing its path journal, leaving six retained byte
objects without established original path mappings; this development evidence
gap is stated in failures/earlier-continuation-note.txt, not filled by inference.
The later journal records additional paths and identities before moving them.
All required exact declared inputs then verified. Premature harness commands
failed on the absent configuration before any stages executed; logs are retained.

SOURCE-ONLY unchanged. Production/lifetime bounds, operational ownership, custody,
rollback resistance, real-storage durability and qualification remain unresolved.
Readiness/final binding BLOCKED; backup KERNEL-ONLY; streams UNCOMPUTED; admission
disabled. Decision B and the unapproved retention boundary remain unchanged.
