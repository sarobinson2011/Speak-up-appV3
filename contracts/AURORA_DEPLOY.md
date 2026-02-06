# Aurora Testnet Deploy & Verify Reference

**Quick reference for deploying and verifying contracts on Aurora testnet.**

---

## Prerequisites

- Foundry installed
- Keystore set up: `~/.foundry/keystores/dev-deployer`
- `.env` file with: `export AURORA_API_KEY="dummy"` (Blockscout doesn't actually need it)

---

## Deploy Pattern

```bash
cd contracts

forge script script/YourScript.s.sol:YourContract \
    --rpc-url https://testnet.aurora.dev \
    --account dev-deployer \
    --sender 0xf8f8269488f73fab3935555fcddd6035699dee25 \
    --broadcast \
    --legacy \
    --skip-simulation
```

**Key flags:**
- `--account dev-deployer` - Uses keystore (will prompt for password)
- `--sender 0xf8f8...` - Match the address that keystore unlocks
- `--legacy` - Aurora prefers legacy transactions
- `--skip-simulation` - Forces actual deployment (no dry-run)

---

## Verify Pattern

```bash
cd contracts
source ../.env  # Loads AURORA_API_KEY

./verify.sh <CONTRACT_ADDRESS> src/path/Contract.sol:ContractName
```

**verify.sh contents:**
```bash
#!/bin/bash
source ../.env
forge verify-contract \
  "$1" \
  "$2" \
  --chain-id 1313161555 \
  --verifier blockscout \
  --verifier-url https://explorer.testnet.aurora.dev/api/v1/
```

---

## Common Issues

### "No associated wallet for addresses"
**Problem:** Wrong `--sender` address  
**Fix:** Use address that keystore actually unlocks (check keystore password prompt)

### "Address is not a smart-contract"
**Problem:** Contract didn't actually deploy (simulation only)  
**Fix:** Add `--skip-simulation` flag

### "environment variable AURORA_API_KEY not found"
**Problem:** Missing in .env  
**Fix:** Add `export AURORA_API_KEY="dummy"` to .env (Blockscout ignores it anyway)

### "No such file or directory with aurora-testnet"
**Problem:** Using alias instead of URL  
**Fix:** Use full URL `https://testnet.aurora.dev`

---

## Testing Deployed Contracts

```bash
# Read-only call (free)
cast call <CONTRACT> "functionName()" --rpc-url https://testnet.aurora.dev

# State-changing transaction (costs gas)
cast send <CONTRACT> \
  "functionName(args)" \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy
```

---

## Explorer Links

- Testnet Explorer: https://explorer.testnet.aurora.dev
- Transaction: `https://explorer.testnet.aurora.dev/tx/0x...`
- Contract: `https://explorer.testnet.aurora.dev/address/0x...`

---

## V3 Groth16 Example (Successfully Deployed)

```bash
# Deploy
forge script script/DeployGroth16.s.sol:DeployGroth16 \
    --rpc-url https://testnet.aurora.dev \
    --account dev-deployer \
    --sender 0xf8f8269488f73fab3935555fcddd6035699dee25 \
    --broadcast \
    --legacy \
    --skip-simulation

# Verify
./verify.sh 0xE70E2cFA4a4272B39918A45BA1F067676CCf8c11 src/v3/Groth16Verifier.sol:Groth16Verifier
./verify.sh 0x89e7B76fB04aDC4C088FA321aCA3E19A79BaBB8a src/v3/Groth16VerifierTest.sol:Groth16VerifierTest

# Test
cast send 0x89e7B76fB04aDC4C088FA321aCA3E19A79BaBB8a \
  "testGoldenProof(...)" \
  [...calldata...] \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --legacy
```

**Deployed addresses:**
- Groth16Verifier: `0xE70E2cFA4a4272B39918A45BA1F067676CCf8c11`
- Groth16VerifierTest: `0x89e7B76fB04aDC4C088FA321aCA3E19A79BaBB8a`

---

## Pro Tips

1. **Always use `--legacy`** on Aurora
2. **Check keystore address** before setting `--sender`
3. **`source ../.env`** before verify.sh
4. **Verification is optional** - contracts work without it
5. **Keep this file in `contracts/AURORA_DEPLOY.md`** for reference
