# TODO - Future Improvements

## High Priority

### 1. Switch to IPFS for Petition Metadata ⭐
**Current:** In-memory Map() in backend (lost on restart)  
**Target:** IPFS (Pinata or Web3.Storage)

**Why:**
- More credible (decentralized, censorship-resistant)
- Permanent storage
- Aligns with Web3 values
- Content-addressed (hash proves integrity)

**Implementation:**
```javascript
// Instead of:
const metadataURI = `ipfs://Qm${fakeHash}`;

// Use:
const ipfsHash = await pinata.pinJSONToIPFS(metadata);
const metadataURI = `ipfs://${ipfsHash}`;
```

**Services to consider:**
- Pinata (easiest, generous free tier)
- Web3.Storage (Filecoin-backed, free)
- NFT.Storage (free, IPFS + Filecoin)

**Files to update:**
- `backend/src/server.js` - Replace Map with IPFS upload
- `frontend/src/Petitions.jsx` - Fetch from IPFS gateway

**Effort:** ~2 hours  
**Reference:** https://docs.pinata.cloud/

---

### 2. Add AI Comment Moderation
**Current:** All comments auto-approved  
**Target:** OpenAI GPT-4 moderation

**Implementation:**
- Check for spam, hate speech, off-topic
- Rate toxicity (0-1 scale)
- Reject if score > threshold

**Effort:** ~1 hour

---

### 3. Persistent Database
**Current:** In-memory Map (lost on restart)  
**Target:** PostgreSQL or MongoDB

**Why:** Retain petition metadata across restarts

**Effort:** ~3 hours

---

## Medium Priority

### 4. Real Membership Verification
**Current:** Backend issues attestations to anyone  
**Target:** SSO (Google/GitHub) or email verification

---

### 5. Petition Details Page
**Current:** Just list view  
**Target:** Full page with description, comments, signatures

---

### 6. Deploy to Mainnet
**Prerequisites:** IPFS metadata, audited contracts

---

## Low Priority

### 7. M2 - ZK Proofs
**When:** Product proven, strong privacy needed  
**Effort:** ~2-4 weeks (circuit + testing)

---

## Completed ✅
- ✅ Docs cleanup (Jan 23, 2025)
- ✅ UUPS upgradeable contracts
- ✅ Aurora testnet deployment
- ✅ Contract verification
- ✅ Helper scripts (deploy-all.sh, verify.sh)
- ✅ In-memory metadata storage (temporary solution)

---

**Last Updated:** January 23, 2025
