# DIRECTION.md — Speak-up-appV3 (M2-only) Baseline Direction

Last updated: 2026-02-27 (Europe/London)

This file exists to stop the Engineering[n] loop. It’s the practical, operational “what we built / how it behaves / what to do next” for the M2-only MVP baseline.

STATE.md remains canonical for architecture invariants. This file is the *execution* direction and checklist.

---

## 1) MVP Baseline (what “done” means)

Speak-up-appV3 is now **M2-only**:

- Client-side Groth16 proof generation (in-browser)
- On-chain verification (Aurora testnet)
- Membership eligibility via Merkle tree (Poseidon)
- Uniqueness enforced by **nullifier** (one sign per petition per member)
- No JWT, no email verification, no attester/permit flow
- Backend is an indexer/convenience API for membership paths (not an authority)

### The critical operational rule (identity stability)

**Per-wallet secret is generated once and stored locally. It never auto-rotates.**

- Local secret key:
  - `su_memberSecret_v1:wallet:<addrLower>`
- Membership leaf must match:
  - `leaf = Poseidon1(memberSecret)`
- If secret is missing for a wallet that is already enrolled on-chain:
  - That wallet is **dead for signing on this device** (acceptable for MVP)
- If secret exists but leaf mismatch:
  - UI shows **Secret mismatch** and signing is disabled

---

## 2) Expected UX flows (how the app should behave)

### A) New wallet flow (fresh wallet)

1. Connect wallet
2. Frontend generates/stores `memberSecret` in localStorage (one-time)
3. Open a petition details page
4. If not enrolled:
   - Status shows **Not enrolled**
   - **Enroll (one-time)** button is available
   - Sign button disabled
5. Click **Enroll (one-time)**:
   - Sends tx to `MembershipRegistry.registerLeaf(leaf)` with exact bond
   - After enrollment, backend indexer eventually serves `/api/membership/path?wallet=...`
6. Once membership path loads and leaf matches:
   - Status becomes **Ready**
   - **Sign with Strong Privacy (ZK)** becomes enabled
7. Sign:
   - Client generates Groth16 proof
   - Contract verifies proof
   - Nullifier is recorded/checked → prevents double-sign

### B) Existing wallet already signed a petition

- Petition details show **Already signed (Strong Privacy)**
- Sign button stays disabled permanently for that wallet+petition
- Enrollment state is independent (you can be enrolled and still “already signed” for a petition)

### C) Wallet has no membership path (404 from backend)

- This is normal if not enrolled or not indexed yet.
- UX should guide user to **Enroll (one-time)**.
- After enrollment, the path should load shortly after (or after a refresh).

### D) Wallet has missing secret

- Status: **Secret missing for this wallet (cannot sign from this device)**
- Sign button disabled
- Enroll may still appear depending on wallet state, but signing is blocked by missing secret.

---

## 3) What is authoritative

- **Authoritative truth:** smart contracts on Aurora testnet.
- Backend:
  - Convenience/indexer that returns Merkle paths for enrolled wallets.
  - If backend is wrong/out of date, signing won’t work (proof won’t verify).
- Frontend:
  - Generates secret and proofs; does not “trust itself” — it must match on-chain leaf and contract checks.

---

## 4) Immediate next tasks (tiny + deterministic)

### Task 1 — Confirm enrollment UX is stable (Option B “Enroll” button)

Goal: any brand-new funded wallet can go:

Connect → Enroll → Path loads → Sign

Checklist:
- [ ] New wallet connects, secret is stored under correct localStorage key
- [ ] Petition details show **Not enrolled** and Enroll button
- [ ] Enroll tx succeeds (uses `registerBondWei()` from chain)
- [ ] After backend indexes, petition details shows Sign enabled
- [ ] Signing succeeds and “Already signed” shows afterwards

If any step fails:
- log membershipPath response and leafMatches check in console
- ensure backend is running + up to date (indexer catches the event)

### Task 2 — Draw a baseline line (MVP commit point)

Once the above passes consistently (your “five pass” test), freeze baseline with:

- docs updated (STATE.md + ZK_CIRCUIT_SPEC.md)
- remove M1/UI remnants
- cleanup dead files
- commit with a clear message: “M2-only baseline: stable identity + enroll/sign UX”

---

## 5) Cleanup checklist (no logic changes)

### A) Remove obvious stray files at repo root

You already found:
- `./mvp_identity_fix.patch`  → remove (it was an intermediate scratch)

Command:
```bash
rm -f ./mvp_identity_fix.patch