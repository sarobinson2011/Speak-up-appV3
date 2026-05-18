# ADMISSION_DEPLOYMENT_FLOW_V0.md


Supporting historical V0 design document only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

This document reflects an earlier exploratory/stabilization phase of the enrollment architecture.

It must not be interpreted as redefining current canonical:

- M2 identity semantics
- continuity semantics
- Enrollment semantics
- TEMPEST semantics
- REFLECT semantics

Current canonical identity continuity is defined in:

- `STATE.md`
- `docs/CONTINUITY_CUSTODY_MODEL_V1.md`

Current locked interpretation:

- `memberSecret -> leaf -> nullifier`
- continuity = possession of the same original `memberSecret`
- wallets are runtime convenience handles only
- wallets are not identity, recovery, or continuity authorities

---

Status: Draft V0 deployment design  
Scope: Deployment and initialization flow only; no implementation in this document

## Purpose

Define the exact V0 deployment and initialization order for the unlinkable enrollment stack:

- `Poseidon1`
- `Poseidon2`
- `AnonymousMembershipRegistry`
- `AdmissionRegistry`

This document exists to prevent mis-wiring between logic contracts, proxy contracts, hashers, and post-deploy authorization.

---

# Design principles

- Use deterministic deployment order
- Link contracts using **proxy addresses**, not logic addresses
- Keep Poseidon helper contracts non-upgradeable
- Keep registries upgradeable using the existing OpenZeppelin proxy discipline
- Avoid partial initialization
- Make post-deploy validation explicit
- Preserve the separation between:
  - admission commitment hashing (`Poseidon1`)
  - anonymous membership tree hashing (`Poseidon2`)

---

# Components

## Non-upgradeable helper contracts

### Poseidon1
Used by `AdmissionRegistry` to derive:

- `admissionCommitment = Poseidon1(admissionSecret)`

### Poseidon2
Used by `AnonymousMembershipRegistry` for incremental Merkle tree hashing:

- `Poseidon2(left, right)`

## Upgradeable contracts

### AnonymousMembershipRegistry
Responsibilities:

- maintain anonymous membership leaves
- maintain incremental Merkle tree
- maintain root history
- allow only `AdmissionRegistry` to insert leaves

### AdmissionRegistry
Responsibilities:

- accept bonded admission-right funding
- activate anonymous membership via relayed secret opening
- allow refund of unused rights after lock period

## Upgradeability/admin

### ProxyAdmin
Owns and governs the upgradeable proxies.

### TransparentUpgradeableProxy
Used for:
- `AnonymousMembershipRegistry`
- `AdmissionRegistry`

---

# Deployment order

The following order is locked for V0.

## 1. Deploy Poseidon1

Deploy the non-upgradeable `Poseidon1` helper contract.

Output:
- `POSEIDON1_ADDRESS`

## 2. Deploy Poseidon2

Deploy the non-upgradeable `Poseidon2` helper contract.

Output:
- `POSEIDON2_ADDRESS`

## 3. Deploy AnonymousMembershipRegistry logic

Deploy the logic/implementation contract.

Output:
- `ANON_MEMBERSHIP_LOGIC_ADDRESS`

> Operator note: for current backend/runtime configuration, `ANON_MEMBERSHIP_PROXY_ADDRESS` is the canonical env variable. Legacy backend aliases `MEMBERSHIP_REGISTRY_ADDRESS` and `MEMBERSHIP_ADDRESS` may still be accepted temporarily during transition, but should not be used for new setup.

## 4. Deploy AdmissionRegistry logic

Deploy the logic/implementation contract.

Output:
- `ADMISSION_LOGIC_ADDRESS`

## 5. Deploy ProxyAdmin

Deploy the proxy admin used to manage registry proxies.

Output:
- `PROXY_ADMIN_ADDRESS`

## 6. Deploy AnonymousMembershipRegistry proxy

Deploy `TransparentUpgradeableProxy` pointing to `ANON_MEMBERSHIP_LOGIC_ADDRESS`.

Initialize via:

```text
initialize(owner, poseidon2)
```

Arguments:

- `owner`
- `POSEIDON2_ADDRESS`

Output:
- `ANON_MEMBERSHIP_PROXY_ADDRESS`

## 7. Deploy AdmissionRegistry proxy

Deploy `TransparentUpgradeableProxy` pointing to `ADMISSION_LOGIC_ADDRESS`.

Initialize via:

```text
initialize(owner, anonymousMembershipRegistry, admissionHasher, admissionBond, lockPeriod)
```

Arguments:

- `owner`
- `ANON_MEMBERSHIP_PROXY_ADDRESS`
- `POSEIDON1_ADDRESS`
- `admissionBond`
- `lockPeriod`

Output:
- `ADMISSION_PROXY_ADDRESS`

## 8. Post-deploy linkage

Call on the anonymous membership proxy:

```text
setAdmissionRegistry(ADMISSION_PROXY_ADDRESS)
```

This authorizes the admission registry to register anonymous membership leaves.

---

# Initializer surfaces

## AnonymousMembershipRegistry.initialize

```solidity
initialize(address initialOwner, address hasher_)
```

Expected values:

- `initialOwner` = governance/admin owner
- `hasher_` = `POSEIDON2_ADDRESS`

## AdmissionRegistry.initialize

```solidity
initialize(
    address initialOwner,
    address anonymousMembershipRegistry_,
    address admissionHasher_,
    uint256 admissionBond_,
    uint256 lockPeriod_
)
```

Expected values:

- `initialOwner` = governance/admin owner
- `anonymousMembershipRegistry_` = `ANON_MEMBERSHIP_PROXY_ADDRESS`
- `admissionHasher_` = `POSEIDON1_ADDRESS`
- `admissionBond_` = chosen V0 bond amount
- `lockPeriod_` = chosen V0 refund lock duration

---

# Dependency graph

## Hashing dependencies

- `AdmissionRegistry` depends on `Poseidon1`
- `AnonymousMembershipRegistry` depends on `Poseidon2`

## Contract dependencies

- `AdmissionRegistry` depends on `AnonymousMembershipRegistry`
- `AnonymousMembershipRegistry` must whitelist `AdmissionRegistry`

## Proxy/linkage rule

All registry-to-registry references must use **proxy addresses**, not logic addresses.

---

# Why the order matters

## AnonymousMembershipRegistry must be initialized before AdmissionRegistry

Because `AdmissionRegistry.initialize(...)` requires the anonymous membership registry address.

## AnonymousMembershipRegistry cannot whitelist AdmissionRegistry until AdmissionRegistry proxy exists

Therefore:

- deploy anonymous membership proxy first
- deploy admission proxy second
- call `setAdmissionRegistry(...)` last

This is the only post-deploy authorization step required for V0 linkage.

---

# Expected deployed state after initialization

## AnonymousMembershipRegistry

- owner is set correctly
- hasher is `Poseidon2`
- tree is initialized
- initial root has been pushed into root history
- `admissionRegistry` is unset until linkage step
- after linkage, `admissionRegistry == ADMISSION_PROXY_ADDRESS`

## AdmissionRegistry

- owner is set correctly
- `anonymousMembershipRegistry == ANON_MEMBERSHIP_PROXY_ADDRESS`
- `admissionHasher == POSEIDON1_ADDRESS`
- `admissionBond` is set to configured V0 amount
- `lockPeriod` is set to configured V0 duration

---

# Post-deploy verification checklist

After deployment, verify all of the following.

## Hash helpers

- `Poseidon1` deployed successfully
- `Poseidon2` deployed successfully

## AnonymousMembershipRegistry

- proxy exists
- implementation address matches expected logic
- owner is correct
- hasher is `POSEIDON2_ADDRESS`
- current root is nonzero or matches expected initialized root semantics
- root history contains the current initialized root
- `admissionRegistry == ADMISSION_PROXY_ADDRESS`

## AdmissionRegistry

- proxy exists
- implementation address matches expected logic
- owner is correct
- `anonymousMembershipRegistry == ANON_MEMBERSHIP_PROXY_ADDRESS`
- `admissionHasher == POSEIDON1_ADDRESS`
- `admissionBond` matches configured value
- `lockPeriod` matches configured value

## Cross-linkage

- `AdmissionRegistry.activateMembership(...)` can register a leaf through the anonymous registry
- unauthorized callers cannot call `AnonymousMembershipRegistry.registerLeaf(...)`

---

# Minimal smoke test after deployment

A V0 deployment should pass this basic live flow:

1. derive `admissionCommitment` off-chain from `admissionSecret`
2. fund one admission right
3. derive `leaf` from `memberSecret`
4. call `activateMembership(commitment, secret, leaf)`
5. verify:
   - admission right status becomes `Activated`
   - anonymous registry leaf count increments
   - leaf is marked known
   - root changes
6. attempt refund after activation and confirm revert

Optional second smoke test:

1. fund a fresh admission right
2. wait until lock period expires
3. call refund
4. verify:
   - right status becomes `Refunded`
   - configured recipient receives bond amount

---

# Non-goals for this deployment doc

This document does not define:

- frontend enrollment flow
- relayer HTTP API details
- multisig ownership policy
- upgrade execution procedure
- monitoring/alerting
- production operational security controls
- deployment automation script format

Those may be documented separately.

---

# V0 implementation note
> Operator note: for current backend/runtime configuration, `ANON_MEMBERSHIP_PROXY_ADDRESS` is the canonical env variable. Legacy backend aliases `MEMBERSHIP_REGISTRY_ADDRESS` and `MEMBERSHIP_ADDRESS` may still be accepted temporarily during transition, but should not be used for new setup.
For V0, Poseidon helper contracts are treated as fixed deployed primitives.

The upgradeable surface begins at:

- `AnonymousMembershipRegistry`
- `AdmissionRegistry`

This keeps the cryptographic helpers simple and the stateful registries governable.

---

# Locked V0 deployment summary

```text
1. Deploy Poseidon1
2. Deploy Poseidon2
3. Deploy AnonymousMembershipRegistry logic
4. Deploy AdmissionRegistry logic
5. Deploy ProxyAdmin
6. Deploy AnonymousMembershipRegistry proxy and initialize(owner, Poseidon2)
7. Deploy AdmissionRegistry proxy and initialize(owner, AnonymousMembershipRegistry proxy, Poseidon1, bond, lockPeriod)
8. Call setAdmissionRegistry(AdmissionRegistry proxy) on AnonymousMembershipRegistry
9. Run post-deploy checks and smoke tests
```