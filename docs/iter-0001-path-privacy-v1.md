# Agent Work Package — iter-0001-path-privacy-v1

Iteration: Path Privacy Hardening v1  
Branch: agent/iter-0001-path-privacy-v1  
Base anchor: baseline-v0 (tag) → commit e02aacdc0f10e6919d8a759d8829758b58e0367e  
Branch base: origin/main (must descend from baseline-v0)

---

## Objective

Remove wallet address from membership path retrieval requests.

Replace:
GET /api/membership/path?wallet=<address>

With:
GET /api/membership/path?leaf=<hex>

No circuit changes.  
No contract changes.  
No main branch edits.

---

## Rationale

Current baseline leaks wallet→membership index mapping to backend.

Requesting by leaf reduces direct deanonymization risk.

This is a privacy hardening iteration.

---

## Constraints

- Do NOT checkout main.
- Work only on agent branch.
- Maintain M2-only architecture.
- Keep changes minimal and reversible.
- Old endpoint may remain temporarily.

---

## Backend Requirements

1. Add leaf query support.
2. Accept 0x-prefixed hex.
3. Normalize to canonical field representation.
4. If both wallet and leaf provided:
   - Prefer leaf.
5. If neither provided:
   - Return 400.

Return payload unchanged except:
- wallet field optional or null.

---

## Frontend Requirements (not in scope for this backend step)

1. Compute:
   leaf = Poseidon1(memberSecret)
2. Request path using ?leaf=...
3. Maintain existing preflight checks.
4. Preserve deterministic UX.

---

## Tests

New wallet:
- connect → enroll → fetch path by leaf → sign works

Returning wallet:
- connect → path loads by leaf → sign works

Secret tampered:
- leaf not found OR preflight blocks signing

---

## Definition of Done

- Normal flow does not send wallet address to backend.
- Baseline sign loop passes.
- Single clean PR with clear commits.
- Branch pushed for human review.

---

## Future Work (Not in Scope)

- Snapshot distribution
- Client-side tree reconstruction
- Backend decentralization
