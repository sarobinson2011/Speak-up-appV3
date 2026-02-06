# ZK Circuit Specification (Milestone 2)

## Overview

This document specifies the Noir circuits needed for Milestone 2 "Strong Privacy" mode. The circuits prove membership and nullifier derivation without revealing the user's identity to anyone, including the operator.

---

## Circuit: Sign Petition

### Purpose
Prove that a user is an eligible member and can sign petition N, without revealing which member they are.

### Private Inputs
- `member_secret: Field` - User's secret identifier
- `membership_path: [Field; TREE_DEPTH]` - Merkle proof of membership
- `membership_indices: [u1; TREE_DEPTH]` - Path indices for Merkle proof

### Public Inputs
- `petition_id: Field` - The petition being signed (converted from uint256)
- `nullifier: Field` - H(member_secret, petition_id, SIGN_DOMAIN)
- `membership_root: Field` - Root of membership Merkle tree

### Constraints

```noir
use dep::std;

// Domain separator for SIGN action
global SIGN_DOMAIN: Field = 0x5349474e; // "SIGN" in hex

fn main(
    // Private inputs
    member_secret: Field,
    membership_path: [Field; TREE_DEPTH],
    membership_indices: [u1; TREE_DEPTH],
    
    // Public inputs
    petition_id: pub Field,
    nullifier: pub Field,
    membership_root: pub Field
) {
    // 1. Verify nullifier derivation
    let computed_nullifier = std::hash::poseidon::bn254::hash_3([
        member_secret,
        petition_id,
        SIGN_DOMAIN
    ]);
    assert(nullifier == computed_nullifier);
    
    // 2. Verify membership in tree
    let member_leaf = std::hash::poseidon::bn254::hash_1([member_secret]);
    let computed_root = std::merkle::compute_merkle_root(
        member_leaf,
        membership_path,
        membership_indices
    );
    assert(membership_root == computed_root);
}
```

### Public Input Layout

When encoding for the Solidity verifier:

```javascript
publicInputs = [
  petitionId,      // bytes32 (convert uint256 to field)
  nullifier        // bytes32 (Poseidon hash output)
]
```

**Critical:** The PetitionRegistry will check:
- `publicInputs[0] == petitionId` (from function parameter)
- `publicInputs[1] == nullifier` (from function parameter)

So the circuit MUST output these in this exact order.

---

## Circuit: Comment on Petition

### Purpose
Prove that a user is an eligible member and can comment on petition N with comment hash C, without revealing which member they are.

### Private Inputs
- `member_secret: Field` - User's secret identifier
- `membership_path: [Field; TREE_DEPTH]` - Merkle proof of membership
- `membership_indices: [u1; TREE_DEPTH]` - Path indices for Merkle proof

### Public Inputs
- `petition_id: Field` - The petition being commented on
- `nullifier: Field` - H(member_secret, petition_id, COMMENT_DOMAIN)
- `comment_hash: Field` - Hash of the moderated comment content
- `membership_root: Field` - Root of membership Merkle tree

### Constraints

```noir
use dep::std;

// Domain separator for COMMENT action
global COMMENT_DOMAIN: Field = 0x434f4d4d454e54; // "COMMENT" in hex

fn main(
    // Private inputs
    member_secret: Field,
    membership_path: [Field; TREE_DEPTH],
    membership_indices: [u1; TREE_DEPTH],
    
    // Public inputs
    petition_id: pub Field,
    nullifier: pub Field,
    comment_hash: pub Field,
    membership_root: pub Field
) {
    // 1. Verify nullifier derivation
    let computed_nullifier = std::hash::poseidon::bn254::hash_3([
        member_secret,
        petition_id,
        COMMENT_DOMAIN
    ]);
    assert(nullifier == computed_nullifier);
    
    // 2. Verify membership in tree
    let member_leaf = std::hash::poseidon::bn254::hash_1([member_secret]);
    let computed_root = std::merkle::compute_merkle_root(
        member_leaf,
        membership_path,
        membership_indices
    );
    assert(membership_root == computed_root);
    
    // 3. Comment hash is public (no constraints needed, just in public inputs)
    // Backend will verify comment_hash = keccak256(approvedComment)
    // Circuit just ensures the same user can't comment twice (via nullifier)
}
```

### Public Input Layout

```javascript
publicInputs = [
  petitionId,      // bytes32
  nullifier,       // bytes32
  commentHash      // bytes32
]
```

**Critical:** The PetitionRegistry will check:
- `publicInputs[0] == petitionId`
- `publicInputs[1] == nullifier`
- `publicInputs[2] == commentHash`

---

## Membership Tree Design

### Tree Structure

Use a Sparse Merkle Tree with Poseidon hash:

```
Root
  ├─ Branch
  │   ├─ Leaf: H(member_secret_1)
  │   └─ Leaf: H(member_secret_2)
  └─ Branch
      ├─ Leaf: H(member_secret_3)
      └─ Empty (0)
```

### Leaf Computation

```javascript
// User's leaf in the tree
memberLeaf = poseidon([memberSecret])
```

### Tree Depth

Recommended: `TREE_DEPTH = 20` (supports up to 1M members)

For smaller institutions: `TREE_DEPTH = 10` (supports up to 1K members)

### Root Management

The membership root should be:
1. **Stored on-chain** (in a MembershipRegistry contract), OR
2. **Stored off-chain** and passed as public input (with governance to freeze old roots)

For V3, we recommend **option 1**:

```solidity
contract MembershipRegistry {
    bytes32 public currentRoot;
    mapping(bytes32 => bool) public validRoots; // support multiple valid roots
    
    function updateRoot(bytes32 newRoot) external onlyAdmin {
        validRoots[newRoot] = true;
        currentRoot = newRoot;
    }
}
```

Then ZKAuthorizer can check:
```solidity
function authorizeSign(...) {
    // ... decode proof and publicInputs
    
    // Extract membership root from circuit public inputs (if included)
    // OR fetch from MembershipRegistry
    bytes32 membershipRoot = membershipRegistry.currentRoot();
    
    // Verify proof
    require(verifier.verify(proof, publicInputs), "Invalid proof");
}
```

---

## Field Element Conversions

### Solidity uint256 → Noir Field

Noir uses the BN254 scalar field (~254 bits). Solidity `uint256` is 256 bits.

For `petitionId` (which is typically a small counter like 1, 2, 3...):
```javascript
// No conversion needed - just use the value
publicInputs[0] = ethers.toBeHex(petitionId, 32);
```

For `nullifier` and `commentHash` (which are keccak256 outputs):
```javascript
// These are 256-bit values, may exceed field modulus
// Option 1: Use Poseidon hash instead of keccak256 for nullifiers
// Option 2: Modulo reduce: value % FIELD_MODULUS (NOT RECOMMENDED - loses security)

// RECOMMENDED: In Noir, compute nullifiers with Poseidon:
nullifier = poseidon([member_secret, petition_id, DOMAIN])

// In Solidity contract, store as bytes32 (no conversion needed)
```

### Keccak256 vs Poseidon

**Keccak256** (EVM-native):
- Pro: Easy to compute in Solidity and TypeScript
- Con: Expensive to verify in ZK circuits (~100k constraints)

**Poseidon** (ZK-native):
- Pro: Cheap in ZK circuits (~100 constraints)
- Con: Not native to EVM (need Solidity implementation for fallback)

**Recommendation for V3:**
- Use **Poseidon for nullifiers** (computed in circuit and verified on-chain as bytes32)
- Use **keccak256 for commentHash** (computed off-chain, passed as public input)

---

## Proof Generation Flow

### Client-Side (Browser)

```javascript
import { Noir } from '@noir-lang/noir_js';
import { BarretenbergBackend, UltraHonkBackend } from '@noir-lang/backend_barretenberg';

async function generateSignProof(memberSecret, petitionId) {
  // 1. Fetch membership witness from backend or local storage
  const witness = await fetchMembershipWitness(memberSecret);
  
  // 2. Load compiled circuit
  const circuit = await fetch('/circuits/sign_petition.json').then(r => r.json());
  
  // 3. Prepare inputs
  const inputs = {
    member_secret: memberSecret,
    membership_path: witness.path,
    membership_indices: witness.indices,
    petition_id: petitionId,
    nullifier: computeNullifier(memberSecret, petitionId, 'SIGN'),
    membership_root: witness.root
  };
  
  // 4. Generate proof with UltraHonk
  const backend = new UltraHonkBackend(circuit);
  const noir = new Noir(circuit, backend);
  
  const { witness: witnessData } = await noir.execute(inputs);
  const proof = await backend.generateProof(witnessData);
  
  return proof; // { proof: Uint8Array, publicInputs: string[] }
}

function computeNullifier(memberSecret, petitionId, domain) {
  // Use Poseidon (same as circuit)
  return poseidon([memberSecret, petitionId, domainToField(domain)]);
}
```

### Server-Side (Faster, but less trustless)

Alternatively, users can request the backend to generate proofs:

```javascript
// POST /api/proof/sign
{
  "petitionId": 1,
  "membershipProof": "..." // SSO token
}

// Backend:
// 1. Verify user is member
// 2. Fetch user's memberSecret from DB (encrypted)
// 3. Generate proof server-side
// 4. Return proof to user
// 5. User submits proof on-chain
```

This is faster but requires trusting the backend not to leak secrets.

---

## Verifier Deployment

### Generate Verifier Contract

```bash
# After compiling Noir circuit
nargo compile

# Generate UltraHonk verifier
bb write_vk -b ./target/sign_petition.json
bb contract -b ./target/sign_petition.json -o UltraHonkVerifier.sol

# Deploy with Foundry
forge create UltraHonkVerifier --private-key $PRIVATE_KEY
```

### Verifier Size Issues

UltraHonk verifiers can exceed EIP-170 (24KB contract size limit).

**Solutions:**
1. **Split into libraries** (recommended):
   ```solidity
   library VerifierLib1 { ... }
   library VerifierLib2 { ... }
   contract UltraHonkVerifier {
       function verify(...) external view {
           VerifierLib1.verifyPart1(...);
           VerifierLib2.verifyPart2(...);
       }
   }
   ```

2. **Use older proof system** (UltraPlonk instead of UltraHonk):
   - Smaller verifier (~15KB)
   - Slower proving time
   - Still secure

3. **Optimize circuit** (reduce number of gates):
   - Use native Noir types instead of arrays where possible
   - Minimize field operations
   - Use lookup tables for repeated operations

---

## Testing Strategy

### 1. Unit Test Circuits

```bash
# Test Noir circuit logic
nargo test
```

### 2. Test Proof Generation

```javascript
// Generate proof locally
const proof = await generateSignProof(testMemberSecret, testPetitionId);
console.log('Proof size:', proof.proof.length, 'bytes');
console.log('Public inputs:', proof.publicInputs);
```

### 3. Test On-Chain Verification

```solidity
// Foundry test
function testZKAuthorization() public {
    // Generate proof off-chain (or with FFI)
    (bytes memory proof, bytes32[] memory publicInputs) = generateProof();
    
    // Encode authData
    bytes memory authData = abi.encode(proof, publicInputs);
    
    // Should succeed
    vm.prank(user);
    registry.signPetition(1, nullifier, authData);
    
    // Should fail on double-sign
    vm.expectRevert();
    registry.signPetition(1, nullifier, authData);
}
```

### 4. Gas Benchmarking

```javascript
// Measure gas cost of proof verification
const tx = await registry.signPetition(petitionId, nullifier, authData);
const receipt = await tx.wait();
console.log('Gas used:', receipt.gasUsed.toString());

// Expected: 250k-350k for UltraHonk, 150k-250k for UltraPlonk
```

---

## Migration Path: M1 → M2

### Phase 1: Dual Mode (Both Active)

Deploy ZKAuthorizer alongside AttestationAuthorizer:

```solidity
// Registry can accept EITHER attestation OR proof
// Frontend toggle: "Standard Privacy" vs "Strong Privacy"
```

### Phase 2: Deprecate Attestations

After sufficient testing:

```solidity
registry.setAuthorizer(zkAuthorizer);
// Now ONLY ZK proofs work
```

### Phase 3: Remove Attestation Backend

Shut down attestation service, keep only:
- Membership registry (for tree updates)
- AI moderation (for comments)

---

## Open Questions for M2 Design

1. **Membership tree updates:**
   - How often to update (daily? weekly?)?
   - Support proofs against old roots?
   - How to handle member removal?

2. **Secret rotation:**
   - Should users be able to change memberSecret?
   - If yes, need to link old/new secrets in tree

3. **Gas optimization:**
   - Is UltraHonk too expensive (~300k gas)?
   - Consider UltraPlonk (~200k gas) or Groth16 (~250k gas)?

4. **Proof generation:**
   - Client-side (slower, trustless) vs server-side (faster, trusted)?
   - Provide both options?

5. **Membership verification:**
   - Email/SSO → merkle tree mapping?
   - Who controls the tree?
   - Decentralize tree management?

---

## Summary

The M2 ZK circuits are designed to be **drop-in replacements** for the M1 attestation system:

- **Same nullifier model** (domain-separated per action)
- **Same public inputs** (petitionId, nullifier, commentHash)
- **Same on-chain state** (usedSignNullifier, usedCommentNullifier)
- **Same events** (PetitionSigned, PetitionCommented)

Only the **authorization mechanism** changes:
- M1: ECDSA signature verification
- M2: ZK proof verification

This architectural separation ensures M1 can ship quickly, and M2 can be added later without breaking changes.

