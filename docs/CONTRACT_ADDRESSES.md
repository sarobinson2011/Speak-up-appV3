# Deployed Contract Addresses

## Aurora Testnet

**Deployment Date:** January 22, 2025  
**Deployer:** 0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38  
**Attester:** 0xF8f8269488f73fab3935555FCDdD6035699deE25

### Core Contracts (UUPS Upgradeable)

| Contract | Type | Address | Explorer |
|----------|------|---------|----------|
| **PetitionRegistry** | Proxy | `0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD` | [View](https://explorer.testnet.aurora.dev/address/0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD) |
| PetitionRegistry | Implementation | `0x84f20ca0DC16595DE314b779ae3F528708Df0557` | [View](https://explorer.testnet.aurora.dev/address/0x84f20ca0DC16595DE314b779ae3F528708Df0557) |
| **AttestationAuthorizer** | Proxy | `0xf4FDc4a107f13b4C4d7C8be7dc0088026D201b37` | [View](https://explorer.testnet.aurora.dev/address/0xf4FDc4a107f13b4C4d7C8be7dc0088026D201b37) |
| AttestationAuthorizer | Implementation | `0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336` | [View](https://explorer.testnet.aurora.dev/address/0x6Bb3d9e2CBE100853db11B997aa0c77f13b6d336) |

### Network Details

- **Chain ID:** 1313161555
- **RPC URL:** https://testnet.aurora.dev
- **Explorer:** https://explorer.testnet.aurora.dev

### Quick Commands

```bash
# Load environment
source .env

# Check petition count
cast call $REGISTRY_PROXY "petitionCount()" --rpc-url $AURORA_TESTNET_RPC

# Check owner
cast call $REGISTRY_PROXY "owner()" --rpc-url $AURORA_TESTNET_RPC

# Check attester
cast call $AUTHORIZER_PROXY "attester()" --rpc-url $AURORA_TESTNET_RPC

# Get petition details
cast call $REGISTRY_PROXY "getPetition(uint256)" 1 --rpc-url $AURORA_TESTNET_RPC
```

### Upgrade Instructions

To upgrade the implementation:

```bash
# Deploy new implementation
forge create src/PetitionRegistry.sol:PetitionRegistry \
  --rpc-url $AURORA_TESTNET_RPC \
  --account dev-deployer \
  --legacy

# Upgrade proxy (replace NEW_IMPL with new address)
cast send $REGISTRY_PROXY \
  "upgradeToAndCall(address,bytes)" \
  NEW_IMPL \
  0x \
  --rpc-url $AURORA_TESTNET_RPC \
  --account dev-deployer \
  --legacy
```

### Contract Interactions

**Create Petition:**
```bash
cast send $REGISTRY_PROXY \
  "createPetition(string)" \
  "ipfs://QmYourMetadata" \
  --rpc-url $AURORA_TESTNET_RPC \
  --account dev-deployer \
  --legacy
```

**Sign Petition:**
1. Request attestation from backend
2. Submit with attestation:
```bash
cast send $REGISTRY_PROXY \
  "signPetition(uint256,bytes32,bytes)" \
  PETITION_ID \
  NULLIFIER \
  AUTH_DATA \
  --rpc-url $AURORA_TESTNET_RPC \
  --account dev-deployer \
  --legacy
```

---

**Status:** ✅ Active on Aurora Testnet  
**Last Updated:** January 22, 2025
