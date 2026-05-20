# Working Commands Reference - Speak-Up V3

Supporting historical operational command reference only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

This document contains operational commands accumulated across multiple architecture phases.

Current canonical implementation state, development governance, deployed-address interpretation, and architecture authority are defined in `STATE.md`.

M1, attestation, `AttestationAuthorizer`, and older deployment references in this file are retained as historical operational context only unless explicitly reintroduced in `STATE.md`.

---

**All tested and working commands for Aurora Testnet deployment and verification**

## Environment Setup

```bash
# Load repo root environment variables (root/.env) into the prcoess shell
set -a
source ../.env
set +a
```

## Helper Scripts

**Location:** `/contracts/deploy.sh` and `/contracts/verify.sh`

### Deploy Script

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

# One-command deployment
./deploy.sh

# This automatically:
# - Loads .env
# - Deploys all contracts with UUPS proxies
# - Shows deployment summary
```

### Verify Script

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

# Verify any contract
./verify.sh <address> <path:ContractName>

# Examples:
./verify.sh 0x84f20ca0DC16595DE314b779ae3F528708Df0557 src/PetitionRegistry.sol:PetitionRegistry
./verify.sh 0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336 src/AttestationAuthorizer.sol:AttestationAuthorizer

# This automatically:
# - Loads .env (including AURORA_API_KEY)
# - Submits verification
# - Shows explorer link
```

## Contract Compilation

```bash
cd contracts

# Clean build
forge clean
forge build

# Test
forge test

# Gas report
forge test --gas-report
```

## Contract Deployment

### Quick Deploy (Recommended)

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

# One-command deployment
./deploy.sh
```

### Manual Deploy

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

# Deploy to Aurora Testnet
forge script script/Deploy.s.sol:DeployV3 \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --broadcast \
  --legacy

# Save the output addresses to .env!
```

## Contract Verification (WORKING METHOD)

**Reference:** GitHub issue aurora-is-near/aurora-relayer #363 (user: sarobinson2011)

### Quick Verify (Recommended)

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

# Verify using helper script
./verify.sh <address> <path:ContractName>

# Examples:
./verify.sh 0x84f20ca0DC16595DE314b779ae3F528708Df0557 src/PetitionRegistry.sol:PetitionRegistry
./verify.sh 0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336 src/AttestationAuthorizer.sol:AttestationAuthorizer
```

### Manual Verify

**Prerequisites:**
```bash
# Must have AURORA_API_KEY in .env
# Already set to "placeholder" in .env
source ../.env
```

**IMPORTANT:** Use `/api/v1/` with trailing slash (NOT `/api/v1/verify_smart_contract`)

**PetitionRegistry Implementation:**
```bash
forge verify-contract \
  0x84f20ca0DC16595DE314b779ae3F528708Df0557 \
  src/PetitionRegistry.sol:PetitionRegistry \
  --chain-id 1313161555 \
  --verifier blockscout \
  --verifier-url https://explorer.testnet.aurora.dev/api/v1/
```

**AttestationAuthorizer Implementation:**
```bash
forge verify-contract \
  0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336 \
  src/AttestationAuthorizer.sol:AttestationAuthorizer \
  --chain-id 1313161555 \
  --verifier blockscout \
  --verifier-url https://explorer.testnet.aurora.dev/api/v1/
```

### Important Notes on Verification

- ✅ **CRITICAL:** Use `https://explorer.testnet.aurora.dev/api/v1/` (with trailing slash)
- ❌ **DO NOT USE:** `/api` or `/api/v1/verify_smart_contract`
- ✅ **Must have:** `AURORA_API_KEY` in .env (already set to "placeholder")
- ✅ **Helper script:** Use `./verify.sh` for simplicity
- ⚠️ **Proxies auto-verify** - only verify implementations
- 📝 **Reference:** aurora-is-near/aurora-relayer #363 (@sarobinson2011)

## Contract Interaction

### Using Cast

```bash
# Load environment
source .env

# Check petition count
cast call $REGISTRY_PROXY "petitionCount()" --rpc-url https://testnet.aurora.dev

# Get petition details
cast call $REGISTRY_PROXY "getPetition(uint256)" 1 --rpc-url https://testnet.aurora.dev

# Create petition
cast send $REGISTRY_PROXY \
  "createPetition(string)" \
  "ipfs://QmYourMetadata" \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy

# Check if signed
cast call $REGISTRY_PROXY \
  "hasSignedPetition(uint256,bytes32)" \
  PETITION_ID \
  NULLIFIER \
  --rpc-url https://testnet.aurora.dev

# Check owner
cast call $REGISTRY_PROXY "owner()" --rpc-url https://testnet.aurora.dev

# Check attester
cast call $AUTHORIZER_PROXY "attester()" --rpc-url https://testnet.aurora.dev
```

### Update Attester Address

```bash
source .env

cast send $AUTHORIZER_PROXY \
  "setAttester(address)" \
  NEW_ATTESTER_ADDRESS \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy
```

## Backend Operations

### Start Backend

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/backend

# Install dependencies (first time)
npm install

# Start development server
npm run dev

# Should output:
# 🚀 Speak Up Backend running on port 3001
# Attester address: 0x...
```

### Test Backend

```bash
# Health check
curl http://localhost:3001/health

# Request sign attestation
curl -X POST http://localhost:3001/api/petition/sign-permit \
  -H "Content-Type: application/json" \
  -d '{"petitionId": 1, "nullifier": "0x..."}'

# Request comment attestation
curl -X POST http://localhost:3001/api/petition/comment \
  -H "Content-Type: application/json" \
  -d '{"petitionId": 1, "nullifier": "0x...", "commentText": "Great petition!"}'
```

## Frontend Operations

### Start Frontend

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/frontend

# Install dependencies (first time)
npm install

# Start development server
npm run dev

# Opens on http://localhost:3000
```

### Build for Production

```bash
cd frontend
npm run build

# Preview production build
npm run preview
```

## Keystore Management

### Import Keys

```bash
# Import deployer key
cast wallet import dev-deployer --interactive
# Enter private key
# Enter password

# List all keystores
cast wallet list

# Get address from keystore
cast wallet address dev-deployer

# Export private key (CAREFUL - shows key!)
cast wallet private-key dev-deployer
# Enter password
```

## Nullifier Generation

### For Signing

```bash
# Using cast
cast keccak "YOUR-SECRET-HEREpetitionIDSIGN"

# Example:
cast keccak "test-secret-123petition1SIGN"
# Output: 0x1f80d9a92671093c55023d5dd6964b7ca213c371a4d4a8859c4190564bad9970
```

### For Commenting

```bash
cast keccak "YOUR-SECRET-HEREpetitionIDCOMMENT"

# Example:
cast keccak "test-secret-123petition1COMMENT"
# Output: 0x6687e50cdfce49a192d06652efb448d65bb97ad715527e6afe1198127b758a38
```

## Contract Upgrades

### Upgrade PetitionRegistry

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/contracts

source ../.env

# Deploy new implementation
forge create src/PetitionRegistry.sol:PetitionRegistry \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy

# Note the new implementation address, then:
cast send $REGISTRY_PROXY \
  "upgradeToAndCall(address,bytes)" \
  NEW_IMPLEMENTATION_ADDRESS \
  0x \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy
```

### Upgrade AttestationAuthorizer

```bash
# Deploy new implementation
forge create src/AttestationAuthorizer.sol:AttestationAuthorizer \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy

# Upgrade
cast send $AUTHORIZER_PROXY \
  "upgradeToAndCall(address,bytes)" \
  NEW_IMPLEMENTATION_ADDRESS \
  0x \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy
```

## Useful One-Liners

```bash
# Check all deployed contracts have code
cast code $REGISTRY_PROXY --rpc-url https://testnet.aurora.dev | head -c 20
cast code $REGISTRY_IMPL --rpc-url https://testnet.aurora.dev | head -c 20
cast code $AUTHORIZER_PROXY --rpc-url https://testnet.aurora.dev | head -c 20
cast code $AUTHORIZER_IMPL --rpc-url https://testnet.aurora.dev | head -c 20

# View on explorer
echo "Registry: https://explorer.testnet.aurora.dev/address/$REGISTRY_PROXY"
echo "Authorizer: https://explorer.testnet.aurora.dev/address/$AUTHORIZER_PROXY"

# Get current gas price
cast gas-price --rpc-url https://testnet.aurora.dev

# Check balance
cast balance $(cast wallet address dev-deployer) --rpc-url https://testnet.aurora.dev
```

## Full End-to-End Test Flow

```bash
# 1. Create petition
cast send $REGISTRY_PROXY \
  "createPetition(string)" \
  "ipfs://QmTestPetition" \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy

# 2. Generate nullifier
NULLIFIER=$(cast keccak "test-secret-456petition1SIGN")
echo "Nullifier: $NULLIFIER"

# 3. Request attestation
curl -X POST http://localhost:3001/api/petition/sign-permit \
  -H "Content-Type: application/json" \
  -d "{\"petitionId\": 1, \"nullifier\": \"$NULLIFIER\"}" \
  > attestation.json

# 4. Extract authData
AUTH_DATA=$(jq -r '.authData' attestation.json)

# 5. Sign petition
cast send $REGISTRY_PROXY \
  "signPetition(uint256,bytes32,bytes)" \
  1 \
  $NULLIFIER \
  $AUTH_DATA \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy

# 6. Verify signature
cast call $REGISTRY_PROXY \
  "hasSignedPetition(uint256,bytes32)" \
  1 \
  $NULLIFIER \
  --rpc-url https://testnet.aurora.dev
# Should return: 0x0000...0001 (true)
```

## Troubleshooting

### "Failed to estimate gas"
- Check you're on Aurora Testnet in MetaMask (Chain ID: 1313161555)
- Add `--legacy` flag for Aurora
- Verify attester address matches backend

### "InvalidSignature" error
- Backend attester doesn't match contract attester
- Update with: `cast send $AUTHORIZER_PROXY "setAttester(address)" ...`

### "NullifierAlreadyUsed"
- You already signed/commented on this petition
- This is expected behavior (one per petition)

### Verification fails
- Must use EXACT URL: `https://explorer.testnet.aurora.dev/api/v1/` (with trailing slash!)
- Must have `AURORA_API_KEY` env var set (any value works, e.g., "placeholder")
- Compiler version must match: 0.8.22
- EVM version: paris
- Optimization: Yes, 200 runs
- Reference: aurora-is-near/aurora-relayer #363

### Backend won't start
- Check `ATTESTER_PRIVATE_KEY` in backend/.env
- Check `REGISTRY_PROXY` address is set
- Port 3001 not in use

## Environment Variables Quick Reference

### Root .env
```bash
ATTESTER_ADDRESS=0x...
AURORA_TESTNET_RPC=https://testnet.aurora.dev
REGISTRY_PROXY=0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD
REGISTRY_IMPL=0x84f20ca0DC16595DE314b779ae3F528708Df0557
AUTHORIZER_PROXY=0xf4FDc4a107f13b4C4d7C8be7dc0088026D201b37
AUTHORIZER_IMPL=0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336
AURORA_API_KEY=placeholder
```

### Backend .env
```bash
PORT=3001
CHAIN_ID=1313161555
RPC_URL=https://testnet.aurora.dev
REGISTRY_PROXY=0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD
ATTESTER_PRIVATE_KEY=0x...
```

---

**Last Updated:** January 22, 2025  
**All commands tested and working on Aurora Testnet**


## Membership (Aurora testnet) — deploy/verify

Prereqs:
- .env exists at repo root OR contracts/.env (ops.sh auto-detects)
- Foundry account: dev-deployer (keystore)
- RPC: https://testnet.aurora.dev
- ChainId: 1313161555



### Deploy - added 18/02-26
cd /home/oem/Documents/Coding/Speak-up-appV3
./contracts/ops.sh membership:deploy

### Verify (paste addresses from deploy output)
./contracts/ops.sh membership:verify <POSEIDON2_ADDR> <MEMBERSHIP_REGISTRY_ADDR>

### One-off manual verify (if needed)
cd contracts
forge verify-contract <ADDR> src/poseidon/Poseidon2.sol:Poseidon2 --chain-id 1313161555 --verifier blockscout --verifier-url https://explorer.testnet.aurora.dev/api/v1/
forge verify-contract <ADDR> src/MembershipRegistry.sol:MembershipRegistry --chain-id 1313161555 --verifier blockscout --verifier-url https://explorer.testnet.aurora.dev/api/v1/
