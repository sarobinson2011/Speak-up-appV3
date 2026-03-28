# REFLECT_SELECTION_POLICY_V1

## State Selection

Client deterministically selects the highest recent valid publication state.

---

## Validity Criteria

Selected state must:

- pass all validity checks
- be fully fetchable
- preserve structural separation

---

## No External Influence

- mirrors do not suggest state
- no randomness required
- selection is fully client-derived