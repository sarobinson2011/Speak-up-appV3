# Privacy Engine Compatibility Target Model V1

STATE.md remains canonical.

---

# 1. Purpose of Compatibility Targets

A compatibility target identifies the published Privacy Engine protocol generation against which declared compatibility is made.

It provides a stable architectural reference for compatibility declarations.

It does not evaluate compatibility.

It does not establish compatibility.

It does not define protocol semantics.

---

# 2. Definition of a Compatibility Target

A Privacy Engine compatibility target is the bounded architectural identifier for one published Privacy Engine protocol generation used as the reference for declared compatibility.

A compatibility target identifies exactly one published protocol generation.

It exists only to identify the compatibility reference.

---

# 3. Compatibility Target Scope

A compatibility target is limited to identifying one published protocol generation.

It does not describe implementations.

It does not describe deployments.

It does not describe realization.

It does not describe certification.

---

# 4. Relationship to Published Protocol Generations

Every compatibility target identifies exactly one published protocol generation.

The published protocol generation remains the semantic authority.

The compatibility target merely references it.

> generation(T, G)

---

# 5. Relationship to Compatibility Statements

A compatibility statement references one compatibility target.

The compatibility target identifies the published protocol generation against which compatibility is declared.

> statement(S, I, T)

---

# 6. Relationship to Compatibility Profiles

A compatibility profile aggregates one or more compatibility statements.

Those compatibility statements may reference multiple compatibility targets.

The compatibility profile therefore aggregates declared compatibility across multiple published protocol generations without changing the identity of any compatibility target.

> profile(P)

> contains(P, S₁)

> contains(P, S₂)

---

# 7. Relationship to Implementations

Compatibility targets do not identify implementations.

Implementations reference compatibility targets only through compatibility statements.

Compatibility targets remain independent of implementation machinery.

---

# 8. Relationship to Protocol Realization

Compatibility targets are distinct from protocol realization.

A compatibility target identifies the declared compatibility reference.

Protocol realization determines whether an implementation preserves the published protocol semantics.

These relationships are independent.

> target(T, G)

≠

> realizes(I, G)

---

# 9. Relationship to Conformance Claims and Certification

Compatibility targets are distinct from conformance claims.

Compatibility targets are distinct from certification.

They neither assert nor evaluate realization.

They neither recognize nor reject compatibility.

They only identify the published protocol generation used as the declared compatibility reference.

> target(T, G)

≠

> claim(C, I, G)

≠

> status(S, I, G)

---

# 10. Compatibility Target Identity

A compatibility target possesses its own architectural identity.

That identity references exactly one published protocol generation.

It is not implementation identity.

It is not deployment identity.

It is not protocol identity.

---

# 11. Compatibility and Failure

A compatibility target neither succeeds nor fails.

Failure belongs to realization, conformance assessment, certification, or implementation.

A compatibility target remains a valid architectural reference regardless of compatibility outcome.

---

# 12. Protocol Authority

Compatibility targets do not define protocol semantics.

Compatibility targets do not acquire protocol authority.

Protocol authority always remains with the published protocol generation.

---

# 13. Conclusion

A Privacy Engine compatibility target is the bounded architectural identifier for one published protocol generation used as the reference for declared compatibility.

It identifies the compatibility reference.

It does not establish realization.

It does not establish certification.

It does not define protocol semantics.

Protocol authority always remains with the published protocol generation.
