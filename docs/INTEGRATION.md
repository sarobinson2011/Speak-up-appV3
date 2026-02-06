# Speak-Up V3 Integration Guide

## Current Deployment (Aurora Testnet)

**Contracts:** See [CONTRACT_ADDRESSES.md](./CONTRACT_ADDRESSES.md) for deployed addresses  
**Setup:** See [WORKING_COMMANDS.md](./WORKING_COMMANDS.md) for tested commands  
**Upgrades:** See [UPGRADES_GUIDE.md](./UPGRADES_GUIDE.md) for UUPS pattern details

This guide focuses on **integration patterns** for backend and frontend.

---

## Overview

This document describes how to integrate the Speak-Up V3 smart contracts with your backend and frontend.

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    PetitionRegistry                     │
│  (Core contract - STABLE across M1 and M2)             │
│                                                         │
│  - Manages petitions, signatures, comments             │
│  - Enforces nullifier uniqueness                       │
│  - Emits stable events                                 │
│  - Delegates authorization to pluggable authorizer     │
└────────────────────┬────────────────────────────────────┘
                     │ calls
                     ▼
          ┌──────────────────────┐
          │    IAuthorizer       │
          └──────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌────────────────────┐  ┌────────────────────┐
│ AttestationAuth    │  │   ZKAuthorizer     │
│   (Milestone 1)    │  │   (Milestone 2)    │
│                    │  │                    │
│ - EIP-712 sigs     │  │ - ZK proofs        │
│ - Backend trust    │  │ - No backend trust │
│ - Fast, cheap      │  │ - Cryptographic    │
└────────────────────┘  └────────────────────┘
```

---

## Milestone 1: Attestation-Based Flow

### User Flow: Signing a Petition

```
1. User authenticates with backend (SSO/email/etc.)
2. Backend verifies membership eligibility
3. User generates nullifier client-side: H(memberSecret, petitionId, "SIGN")
4. User requests attestation from backend
5. Backend signs permit using EIP-712
6. User submits transaction to PetitionRegistry.signPetition()
```

### User Flow: Commenting on a Petition

```
1. User authenticates with backend
2. User writes comment, generates nullifier: H(memberSecret, petitionId, "COMMENT")
3. User submits comment to backend
4. Backend moderates with AI (GPT-4)
5. If approved, backend computes commentHash, signs permit
6. User submits transaction to PetitionRegistry.commentOnPetition()
```

---

## Backend Integration (M1)

### 1. EIP-712 Message Signing

#### Sign Permit Structure

```javascript
const signPermitType = {
  SignPermit: [
    { name: 'action', type: 'bytes32' },
    { name: 'petitionId', type: 'uint256' },
    { name: 'nullifier', type: 'bytes32' },
    { name: 'expiry', type: 'uint256' }
  ]
};

const domain = {
  name: 'SpeakUpV3',
  version: '1',
  chainId: 1313161555, // Aurora testnet
  verifyingContract: PETITION_REGISTRY_ADDRESS
};

const SIGN_ACTION = ethers.keccak256(ethers.toUtf8Bytes('SIGN'));

const permitMessage = {
  action: SIGN_ACTION,
  petitionId: 1,
  nullifier: '0x1234...', // from user
  expiry: Math.floor(Date.now() / 1000) + 3600 // 1 hour
};

// Sign with backend private key
const signature = await backendSigner.signTypedData(
  domain,
  signPermitType,
  permitMessage
);

// Split signature
const sig = ethers.Signature.from(signature);
const authData = ethers.AbiCoder.defaultAbiCoder().encode(
  ['uint256', 'uint8', 'bytes32', 'bytes32'],
  [permitMessage.expiry, sig.v, sig.r, sig.s]
);

// Return authData to user
```

#### Comment Permit Structure

```javascript
const commentPermitType = {
  CommentPermit: [
    { name: 'action', type: 'bytes32' },
    { name: 'petitionId', type: 'uint256' },
    { name: 'nullifier', type: 'bytes32' },
    { name: 'commentHash', type: 'bytes32' },
    { name: 'expiry', type: 'uint256' }
  ]
};

const COMMENT_ACTION = ethers.keccak256(ethers.toUtf8Bytes('COMMENT'));

const permitMessage = {
  action: COMMENT_ACTION,
  petitionId: 1,
  nullifier: '0x5678...', // from user
  commentHash: ethers.keccak256(ethers.toUtf8Bytes(commentText)),
  expiry: Math.floor(Date.now() / 1000) + 3600
};

// Sign and encode as above
```

### 2. Backend API Endpoints

#### POST /api/petition/sign-permit

Request:
```json
{
  "petitionId": 1,
  "nullifier": "0x1234...",
  "membershipProof": "..." // SSO token, email verification, etc.
}
```

Response:
```json
{
  "authData": "0xabcd...", // encoded (expiry, v, r, s)
  "expiry": 1234567890
}
```

#### POST /api/petition/comment

Request:
```json
{
  "petitionId": 1,
  "nullifier": "0x5678...",
  "commentText": "This petition is important because...",
  "membershipProof": "..."
}
```

Response (after AI moderation):
```json
{
  "approved": true,
  "commentHash": "0x9abc...",
  "authData": "0xdef0...",
  "expiry": 1234567890
}
```

---

## Frontend Integration (M1)

### 1. Nullifier Generation

```javascript
import { ethers } from 'ethers';

// User generates a secret once and stores it (localStorage/encrypted)
const memberSecret = ethers.hexlify(ethers.randomBytes(32));

// Compute nullifier for signing
function computeSignNullifier(memberSecret, petitionId) {
  return ethers.keccak256(
    ethers.solidityPacked(
      ['bytes32', 'uint256', 'string'],
      [memberSecret, petitionId, 'SIGN']
    )
  );
}

// Compute nullifier for commenting
function computeCommentNullifier(memberSecret, petitionId) {
  return ethers.keccak256(
    ethers.solidityPacked(
      ['bytes32', 'uint256', 'string'],
      [memberSecret, petitionId, 'COMMENT']
    )
  );
}
```

### 2. Sign Petition Flow

```javascript
async function signPetition(petitionId) {
  // 1. Compute nullifier
  const nullifier = computeSignNullifier(memberSecret, petitionId);
  
  // 2. Request attestation from backend
  const response = await fetch('/api/petition/sign-permit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      petitionId,
      nullifier,
      membershipProof: await getMembershipProof() // SSO token
    })
  });
  
  const { authData, expiry } = await response.json();
  
  // 3. Submit transaction
  const tx = await petitionRegistry.signPetition(
    petitionId,
    nullifier,
    authData
  );
  
  await tx.wait();
  console.log('Petition signed anonymously!');
}
```

### 3. Comment on Petition Flow

```javascript
async function commentOnPetition(petitionId, commentText) {
  // 1. Compute nullifier
  const nullifier = computeCommentNullifier(memberSecret, petitionId);
  
  // 2. Submit comment to backend for moderation
  const response = await fetch('/api/petition/comment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      petitionId,
      nullifier,
      commentText,
      membershipProof: await getMembershipProof()
    })
  });
  
  const { approved, commentHash, authData, expiry } = await response.json();
  
  if (!approved) {
    throw new Error('Comment was rejected by moderation');
  }
  
  // 3. Submit transaction
  const tx = await petitionRegistry.commentOnPetition(
    petitionId,
    nullifier,
    commentHash,
    authData
  );
  
  await tx.wait();
  console.log('Comment posted anonymously!');
}
```

---

## Milestone 2: ZK Proof Flow (Future)

### User Flow Changes

When "Strong Privacy" mode is enabled:

```
1. User authenticates (to get membership tree witness)
2. User generates proof CLIENT-SIDE using Noir + bb.js
3. User submits transaction directly (no backend attestation needed)
```

### Frontend Changes

```javascript
// Toggle in UI
const [privacyMode, setPrivacyMode] = useState('standard'); // 'standard' | 'private'

async function signPetition(petitionId) {
  const nullifier = computeSignNullifier(memberSecret, petitionId);
  
  let authData;
  
  if (privacyMode === 'standard') {
    // M1: Get attestation from backend
    const { authData: attestation } = await requestSignPermit(petitionId, nullifier);
    authData = attestation;
  } else {
    // M2: Generate ZK proof
    const proof = await generateSignProof({
      memberSecret,
      petitionId,
      membershipWitness // from backend or local storage
    });
    authData = encodeProofData(proof);
  }
  
  // Same contract call!
  const tx = await petitionRegistry.signPetition(petitionId, nullifier, authData);
  await tx.wait();
}
```

### ZK Proof Generation (Skeleton)

```javascript
import { Noir } from '@noir-lang/noir_js';
import { BarretenbergBackend } from '@noir-lang/backend_barretenberg';

async function generateSignProof({ memberSecret, petitionId, membershipWitness }) {
  // Load Noir circuit
  const circuit = await fetch('/circuits/sign_circuit.json').then(r => r.json());
  const noir = new Noir(circuit);
  
  // Prepare inputs
  const inputs = {
    member_secret: memberSecret,
    petition_id: petitionId,
    membership_root: membershipWitness.root,
    membership_path: membershipWitness.path,
    // ... other witness data
  };
  
  // Generate proof
  const backend = new BarretenbergBackend(circuit);
  const { proof, publicInputs } = await noir.generateProof(inputs);
  
  // Encode for contract
  return ethers.AbiCoder.defaultAbiCoder().encode(
    ['bytes', 'bytes32[]'],
    [proof, publicInputs]
  );
}
```

---

## Deployment Guide

### 1. Deploy Contracts (M1)

```javascript
// 1. Deploy AttestationAuthorizer
const AttestationAuthorizer = await ethers.getContractFactory('AttestationAuthorizer');
const attestationAuth = await AttestationAuthorizer.deploy(
  ATTESTER_ADDRESS,     // backend signer
  ADMIN_ADDRESS,        // governance
  PETITION_REGISTRY_PLACEHOLDER // will use CREATE2 or predict address
);

// 2. Deploy PetitionRegistry
const PetitionRegistry = await ethers.getContractFactory('PetitionRegistry');
const registry = await PetitionRegistry.deploy(
  attestationAuth.target,
  ADMIN_ADDRESS
);

console.log('PetitionRegistry:', registry.target);
console.log('AttestationAuthorizer:', attestationAuth.target);
```

### 2. Upgrade to ZK (M2)

```javascript
// 1. Deploy UltraHonk verifier (generated by bb)
const verifier = await deployVerifier(); // from bb-generated contract

// 2. Deploy ZKAuthorizer
const ZKAuthorizer = await ethers.getContractFactory('ZKAuthorizer');
const zkAuth = await ZKAuthorizer.deploy(
  verifier.target,
  ADMIN_ADDRESS
);

// 3. Switch authorizer
const tx = await registry.setAuthorizer(zkAuth.target);
await tx.wait();

console.log('Upgraded to ZK mode!');
```

---

## Event Monitoring

### Listen for Petition Events

```javascript
// Listen for signatures
registry.on('PetitionSigned', (petitionId, nullifier, event) => {
  console.log(`Petition ${petitionId} signed by nullifier ${nullifier}`);
  // Update UI signature count
});

// Listen for comments
registry.on('PetitionCommented', (petitionId, nullifier, commentHash, event) => {
  console.log(`Comment ${commentHash} on petition ${petitionId}`);
  // Fetch comment from backend using commentHash
  fetchComment(commentHash).then(displayComment);
});
```

---

## Security Considerations

### M1 (Attestation Mode)
- Backend signer key must be secure (HSM recommended for production)
- Use short expiry times (5-15 minutes) for attestations
- Consider rate limiting attestation requests
- Monitor for suspicious nullifier patterns

### M2 (ZK Mode)
- Membership tree must be maintained securely
- Users need membership witnesses (store locally or fetch from backend)
- Verifier contract deployment is critical (verify via bb --verify-contract)
- Consider gas costs (UltraHonk proofs are ~300k gas)

### Both Modes
- Users must keep memberSecret secure (lost secret = lost identity)
- Consider allowing users to rotate memberSecret (with merkle tree update)
- Nullifiers are permanent - cannot sign/comment twice on same petition

---

## Testing Checklist

- [ ] Deploy contracts on testnet
- [ ] Backend can issue valid attestations
- [ ] Frontend can compute nullifiers correctly
- [ ] Transactions succeed with valid attestations
- [ ] Transactions fail with expired/invalid attestations
- [ ] Nullifiers prevent double-signing
- [ ] Events are emitted correctly
- [ ] Authorizer can be swapped (M1 → M2)
- [ ] ZK proofs verify on-chain (M2)

---

## Next Steps

1. **For M1 Launch:**
   - Implement backend attestation service
   - Build frontend UI with nullifier generation
   - Deploy to Aurora testnet
   - Test end-to-end flow

2. **For M2 Preparation:**
   - Design Noir circuit for membership proofs
   - Set up membership tree infrastructure
   - Test proof generation locally
   - Benchmark gas costs on testnet

