# REFLECT Cross-State Mixing Review V1

STATE.md remains canonical.

## Objective

Determine whether REFLECT currently permits material from one publication state to be combined with material from another publication state while still producing an accepted result.

## Conclusion

No runtime path was found that permits cross-state mixing to be accepted.

Current classification:

    runtime safe
    dedicated regression test missing

## Evidence

State identity is bound by publication-state digest.

Acquisition plans preserve the selected state digest and selected target before retrieval or fallback.

Connector and chunk coherence is enforced by:

- connector digest agreement
- descriptor digest agreement
- connector chunk-entry digest agreement
- chunk digest recomputation
- offset and size agreement

Reconstruction only occurs after publication objects verify.

Acquisition rejects publication material whose descriptor content digest does not match the selected target content digest.

Continuation/fallback retries against the same target. It does not select a new state.

Therefore:

    connector(A) + chunks(B) -> reject

and:

    publication(A) + selected target(B) -> reject

under the reviewed runtime paths.

## Gap

Existing tests cover digest mismatch, wrong publication, continuation, fallback, and tampered publication-state digest.

The missing regression is an explicit two-state fixture attempting:

    connector(A) + chunks(B)

and:

    publication(A) + selected target(B)

## Next Slice

Engineering[62] should be a bounded regression harness only.

No new REFLECT semantics.
No runtime behavior changes unless a test exposes a real bug.
