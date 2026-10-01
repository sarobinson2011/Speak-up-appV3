# Adopted for unpublished G4 by S87

Steve authorized applying the same scheme to uniqueness on 2026-09-30. The exact active rule is sources/PE-G4-SOURCE-S87.md and privacy/cross_role_uniqueness.py. No further authorization of this extension is pending.

The original proposal below is retained as historical decision context; its former unadopted status is superseded.

# Separate public uniqueness decision — proposed, not adopted

The current S86 correction is correlation-only. Its positive fixture correctly retains UNIQUENESS-FAILURE. This was omitted from the author's preceding recommendation and must not be silently treated as authorized.

Exact proposed additional rule:

For the public uniqueness assessment only, equal public scalar bytes across distinct public roles shall not constitute a uniqueness failure for that pair when the same exact independently authenticated S86 semantic-separation evidence and complete edge-origin evidence authorize its correlation-only treatment. No same-role pair qualifies. Every other offending pair independently retains uniqueness failure. Source-established linkage, unknown evidence and mismatched scope or graph bindings do not qualify. The entire original graph remains in actor reconstruction, and all other admission requirements remain unchanged.

This is a second, explicit semantic change. It is not currently adopted, added to the normative inventory or implemented in the active procedure. The alternative is to retain the existing uniqueness rule and leave this cross-role candidate inadmissible. Neither alternative supplies missing actual source/observer evidence or implies profile admission.
