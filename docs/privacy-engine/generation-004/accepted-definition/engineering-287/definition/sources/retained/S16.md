# Privacy Engine Deprecation & Migration Model V1

STATE.md remains canonical.

This document is supporting documentation only.

If any conflict exists between this document and STATE.md, STATE.md wins.

---

# 1. Purpose of Deprecation

Protocol generations exist indefinitely as published semantic contracts.

Deprecation does not redefine a protocol generation.

It publishes its lifecycle status.

Deprecation allows protocol evolution while preserving explicit historical protocol identity.

---

# 2. Definition of Deprecation

A deprecated protocol generation:

- remains completely defined
- remains uniquely identifiable
- remains semantically unchanged
- remains historically valid

Deprecation communicates that future protocol evolution is expected to occur through another protocol generation.

Deprecation is therefore a lifecycle attribute, not a semantic modification.

---

# 3. Supported Deprecated Generations

A deprecated generation may remain supported.

Support status is independent of protocol identity.

While supported, a deprecated generation continues to publish:

- protocol identity
- protocol surface
- compatibility relationships
- conformance requirements
- migration contract

Supporting a deprecated generation does not permit semantic drift.

A supported deprecated generation remains the same protocol generation.

---

# 4. Protocol Migration

Protocol migration is the published transition from one protocol generation to another.

Migration describes protocol generations.

It does not describe:

- implementations
- deployments
- infrastructure
- rollout strategy

Migration exists to preserve explicit protocol lineage.

---

# 5. Migration Compatibility

Migration and compatibility are independent concepts.

Compatibility asks:

> Are externally relied-upon protocol semantics preserved?

Migration asks:

> What published protocol generation succeeds another?

Neither implies the other.

Possible relationships include:

| Compatibility | Migration |
|---------------|-----------|
| Compatible | No migration required |
| Compatible | Migration published |
| Incompatible | Migration published |
| Incompatible | No migration |

Compatibility remains determined solely by invariant preservation.

Migration never establishes compatibility.

---

# 6. Retirement

A protocol generation may eventually be retired.

Retirement changes lifecycle status only.

Retirement does not:

- redefine protocol semantics
- remove protocol identity
- invalidate historical conformance
- alter compatibility history

Retired generations remain permanently published as historical protocol contracts.

---

# 7. Responsibilities of Protocol Authors

Authors of every protocol generation must publish explicit lifecycle information.

Lifecycle publication must not rely upon implementation behavior.

Every protocol generation must preserve explicit relationships with previous published generations.

Protocol authors must never redefine an existing protocol generation.

If semantics change, a new protocol generation must be published.

---

# 8. Published Migration Contract

Every protocol generation should publish:

- protocol generation identifier
- lifecycle status
- predecessor generation(s), where applicable
- successor generation(s), where known
- compatibility relationship(s)
- migration relationship(s)
- retirement status

This information forms the published migration contract.

It exists independently of implementation.

---

# 9. Conclusion

Protocol identity is permanent.

Compatibility preserves protocol identity.

Versioning identifies protocol generations.

Deprecation publishes lifecycle status.

Migration publishes protocol lineage.

Retirement concludes lifecycle status without altering protocol semantics.

Together these provide explicit protocol evolution while preserving stable semantic contracts across generations.
