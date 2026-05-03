# Shell Windows — Deterministic Context Extraction

## Definition

A *shell window* is a bounded, deterministic query executed against the live codebase or runtime environment to extract a precise slice of system state for inspection.

Examples:
- `rg` (code search)
- `sed` (targeted file window)
- `sqlite3` (database schema/state)
- `cast call` (on-chain state)

Shell windows are used to replace implicit context with explicit, reproducible state.

---

## Purpose

Shell windows serve four functions:

1. **Context Rehydration**
   - Reconstruct system state in long-running engineering threads
   - Avoid reliance on chat memory or assumptions

2. **Drift Prevention**
   - Ensure reasoning is grounded in actual repo state
   - Detect divergence between intended and actual behavior

3. **Auditability**
   - Provide reproducible evidence for claims about system behavior
   - Enable step-by-step verification of invariants

4. **Security Validation**
   - Prove absence of unintended linkage, leakage, or coupling
   - Validate invariants across all layers (contract, backend, frontend, DB)

---

## Method

Work proceeds in three steps:

1. **Extract**
   - Run a shell window:
     ```bash
     rg -n "pattern" path
     sed -n 'X,Yp' file
     sqlite3 db ".schema table"
     ```

2. **Classify**
   - Interpret results:
     - A: runtime risk
     - B: misleading/stale
     - C: historical
     - D: required/valid

3. **Act**
   - Apply minimal, targeted changes only where required

---

## Properties

Shell windows are:

- **Deterministic** — same input → same output
- **Bounded** — limited to a specific scope
- **Reproducible** — can be rerun at any time
- **Non-destructive** — read-only unless explicitly changing state

---

## Relationship to STATE.md

- STATE.md defines **intended invariants**
- Shell windows verify **actual system state**

Engineering proceeds by aligning the two.

---

## Example (Engineering[19])

Invariant:
> Anonymous actions must not be linkable across petitions by any reusable public identifier.

Shell windows used:

```bash
rg -n "admissionCommitment" ...
sed -n ...
sqlite3 ...