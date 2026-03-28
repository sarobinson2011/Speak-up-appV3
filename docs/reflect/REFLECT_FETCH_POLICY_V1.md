# REFLECT_FETCH_POLICY_V1

## Fetch Stages

1. Root metadata (sequential)
2. Manifest (sequential)
3. Chunks + connector (parallel)

---

## Parallel Model

- 3 chunk fetches in parallel
- 1 connector fetch in parallel from separate mirror

---

## Constraints

- no cross-object dependency
- fallback is per-object
- no global reshuffle