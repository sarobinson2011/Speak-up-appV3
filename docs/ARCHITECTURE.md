# Architecture Decisions & Rationale

## Core Design Decisions

### 0. UUPS Upgradeable Pattern

**Decision:** Use OpenZeppelin's UUPS (Universal Upgradeable Proxy Standard) for all contracts.

**Rationale:**
- Can upgrade contract logic without losing state or events
- Critical for M1 → M2 transition (swap authorizer logic)
- Bug fixes and improvements without redeployment
- Lower gas than Transparent Proxy pattern

**Trade-offs:**
- ✅ Upgradeability: Fix bugs, add features, swap authorizers
- ✅ State preservation: All data stays intact across upgrades
- ✅ Same addresses: Users/integrations don't need to update
- ✅ Lower cost: Upgrade function in implementation, not proxy
- ❌ Complexity: Must be careful with storage layout
- ❌ Admin trust: Owner can upgrade contracts

**Implementation:**
```
User → Proxy (storage) → Implementation (logic)
                              ↓ upgradeable
                         New Implementation
```

All contracts (PetitionRegistry, AttestationAuthorizer, ZKAuthorizer) use this pattern.

**Reference:** See [UPGRADES_GUIDE.md](./UPGRADES_GUIDE.md) for detailed UUPS documentation.

### 1. Pluggable Authorization via IAuthorizer

**Decision:** Abstract authorization into a pluggable interface rather than baking it into PetitionRegistry.

**Rationale:**
- V2 taught us that ZK verification is high-friction and slow to iterate on
- Want to ship M1 quickly with attestations, add ZK later
- Avoid rewriting core contract when upgrading authorization
- Different institutions may want different auth (SSO, NFT, ZK, etc.)

**Trade-offs:**
- ✅ Flexibility: swap auth mechanisms without state migration
- ✅ Clean separation: registry doesn't care about membership verification
- ❌ One extra external call per sign/comment (~2k gas)
- ❌ Requires admin trust to set correct authorizer

### 2. Nullifier Model: keccak256(memberSecret, petitionId, action)

**Decision:** Use simple keccak256 for M1, switch to Poseidon in M2 circuit.

**Rationale:**
- Keccak is cheap and available in Solidity/JS/TypeScript
- Easy to compute client-side without ZK libraries
- Domain separation ("SIGN" vs "COMMENT") prevents action collision
- Poseidon in M2 circuit reduces constraints (100 vs 100k for keccak in ZK)

**Trade-offs:**
- ✅ Simple client-side implementation
- ✅ No ZK toolchain needed for M1
- ❌ Different hash functions between M1 and M2 (but same bytes32 output)
- ❌ User must remember/store memberSecret securely

**Alternative considered:** Use public key + signature
- Rejected: reveals link between signatures on different petitions (same pubkey)

### 3. EIP-712 for Attestations

**Decision:** Use EIP-712 structured signing instead of EIP-191.

**Rationale:**
- EIP-712 includes domain separation (chainId, verifying contract)
- Prevents replay attacks across chains
- Prevents signature from being used on different contracts
- Standard format, wallet support

**Trade-offs:**
- ✅ Secure against replay and cross-chain misuse
- ✅ Human-readable signatures in wallets (better UX)
- ❌ Slightly more complex than raw signatures
- ❌ Requires computing domain separator

### 4. Comment Hash Instead of Full Text On-Chain

**Decision:** Store commentHash on-chain, full text off-chain.

**Rationale:**
- Comments can be long (100-1000 characters)
- Gas cost would be prohibitive (16 gas per byte = 16k-32k gas just for storage)
- Backend can moderate before anchoring hash
- Hash provides integrity proof without bloat

**Trade-offs:**
- ✅ Low gas cost (~20k instead of ~50k)
- ✅ Enables AI moderation before anchoring
- ❌ Requires off-chain storage (backend DB, IPFS, etc.)
- ❌ User must trust backend to serve correct comment for hash

**Alternative considered:** Store full text on-chain
- Rejected: too expensive, no benefit for most use cases

### 5. Separate Sign and Comment Nullifiers

**Decision:** Use different nullifiers for signing vs commenting (via domain separation).

**Rationale:**
- Want to allow one sign AND one comment per petition
- Single nullifier would only allow one action total
- Domain separation prevents confusion

**Trade-offs:**
- ✅ Flexible: user can sign, comment, or both
- ✅ Clear semantics: "SIGN" vs "COMMENT" domains
- ❌ More storage (2 mappings instead of 1)

**Alternative considered:** Single nullifier per petition
- Rejected: too restrictive, bad UX

### 6. Frozen State Model

**Decision:** Lock the on-chain state structure (mappings, events) before M1 launch.

**Rationale:**
- Enables M1 → M2 upgrade without state migration
- Events are the public API (indexers, analytics)
- Changing events breaks off-chain systems

**Trade-offs:**
- ✅ Smooth upgrade path
- ✅ No state migration needed
- ❌ Must get state model right upfront
- ❌ Can't easily add new fields later

### 7. Admin-Controlled Authorizer

**Decision:** Allow admin to update authorizer contract.

**Rationale:**
- Needed for M1 → M2 upgrade
- Allows emergency response if authorizer is compromised
- Keeps contracts simple (no governance)

**Trade-offs:**
- ✅ Flexible: can upgrade or rotate authorizer
- ✅ Simple: no complex governance
- ❌ Centralization risk: admin can switch to malicious authorizer
- ❌ Requires user trust

**Mitigation:** Consider timelock for production deployments.

---

## M1 vs M2 Trade-offs

### Why Start with M1 (Attestations)?

**Speed:**
- No ZK toolchain needed
- Simple backend signer
- Fast iteration on product features

**Reliability:**
- EIP-712 is battle-tested
- No verifier size limits
- No toolchain version sync issues

**Cost:**
- ~50k gas vs ~300k for ZK
- Lower barrier to entry

**Downsides:**
- Backend can see who signs/comments
- Backend could forge attestations if compromised
- Not "cryptographically private"

### When to Upgrade to M2 (ZK)?

**Triggers:**
- Institution requires strong privacy guarantees
- Backend has been compromised
- Regulatory pressure for operator-proof anonymity
- Product has proven itself, worth the complexity

**Requirements:**
- ZK circuit audited
- Verifier deployed and verified
- Membership tree infrastructure ready
- Frontend proof generation tested

---

## Security Model

### Trust Assumptions (M1)

**Users trust:**
- Backend to verify membership correctly
- Backend not to forge attestations
- Backend not to leak who signed/commented
- Smart contracts to enforce nullifier uniqueness

**Backend trusts:**
- Users not to share memberSecret
- Blockchain to finalize transactions

### Trust Assumptions (M2)

**Users trust:**
- ZK circuit correctness (via audit)
- Verifier contract correctness (via bb generation)
- Membership tree maintainer (for witnesses)
- Smart contracts to enforce nullifier uniqueness

**Backend trusts:**
- Users not to share memberSecret
- Blockchain to finalize transactions

**Key difference:** In M2, backend cannot forge proofs even if fully compromised.

---

## Gas Optimization Choices

### Storage Layout

**Decision:** Use nested mappings instead of arrays.

```solidity
// Chosen approach
mapping(uint256 => mapping(bytes32 => bool)) usedSignNullifier;

// Rejected: array of used nullifiers
bytes32[] usedNullifiers;
```

**Rationale:**
- O(1) lookup vs O(n) for array
- No need to iterate over past nullifiers
- Cheaper for most operations

### Event Encoding

**Decision:** Index petitionId and nullifier, don't index commentHash.

```solidity
event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier);
event PetitionCommented(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 commentHash);
```

**Rationale:**
- Can filter events by petition or nullifier
- CommentHash doesn't need to be searchable (use backend DB for that)
- Indexing costs extra gas (~375 gas per topic)

---

## Considered Alternatives

### Alternative 1: On-Chain Membership List

Instead of off-chain attestations, store member addresses on-chain.

```solidity
mapping(address => bool) public members;
```

**Rejected because:**
- Reveals who is a member on-chain (privacy leak)
- Expensive to update for large institutions
- Doesn't scale to dynamic membership

### Alternative 2: NFT-Based Membership

Require users to hold an NFT to prove membership.

```solidity
require(membershipNFT.balanceOf(msg.sender) > 0);
```

**Rejected because:**
- NFT ownership is public (links identity to signatures)
- NFT transfers break the model
- More complex, doesn't fit use case

### Alternative 3: Merkle Tree On-Chain (M1)

Store membership Merkle root on-chain for M1.

```solidity
bytes32 public membershipRoot;
function signPetition(bytes32[] proof, ...) { ... }
```

**Rejected because:**
- Adds complexity to M1 (should be simple)
- Still requires backend to generate proofs
- No advantage over attestations for M1
- Better to save this for M2

### Alternative 4: Multiple Comments Per Petition

Allow unlimited comments per user per petition.

**Rejected because:**
- Spam risk (even with moderation)
- Dilutes signal (petition comments should be high-quality)
- Harder to enforce rate limits anonymously
- One comment is enough for most use cases

---

## Future Considerations

### Potential M3 Features

1. **Delegated Signing:**
   - User authorizes another address to sign on their behalf
   - Useful for institutional members with changing staff

2. **Nullifier Rotation:**
   - Allow users to rotate memberSecret
   - Requires linking old/new secrets in membership tree
   - Prevents permanent identity loss if secret is leaked

3. **Multi-Institution Support:**
   - Single deployment, multiple institution roots
   - Each institution has its own membership tree
   - Petitions can be institution-specific or cross-institution

4. **Petition Expiry:**
   - Petitions close after a certain time
   - Prevents stale signatures from accumulating

5. **Signature Thresholds:**
   - Petition creator sets minimum signatures for "success"
   - On-chain verification of threshold reached

6. **Governance Integration:**
   - Successful petitions trigger governance proposals
   - On-chain voting based on signatures

### Known Limitations

1. **No signature removal:**
   - Once signed, cannot unsign
   - Nullifier is permanent
   - Could add "retract" feature with new nullifier domain

2. **No comment editing:**
   - CommentHash is immutable once anchored
   - Could allow multiple comments per user (remove nullifier check)

3. **Membership changes:**
   - M1: backend just stops issuing attestations for ex-members
   - M2: need to update Merkle tree, old proofs still valid
   - Consider expiring old Merkle roots

4. **Secret loss:**
   - If user loses memberSecret, they lose all history
   - No recovery mechanism (privacy vs recoverability trade-off)
   - Consider social recovery or secret backup schemes

---

## Conclusion

The V3 architecture prioritizes:
1. **Shipping quickly** (M1 attestations)
2. **Future flexibility** (pluggable auth)
3. **Clean upgrades** (frozen state model)
4. **User privacy** (nullifier-based anonymity)

It acknowledges that ZK is the end goal but recognizes that starting with ZK would slow product development. The architecture creates a clear path from simple to sophisticated without breaking changes.

