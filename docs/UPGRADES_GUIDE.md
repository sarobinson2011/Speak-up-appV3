# UUPS Upgradeable Pattern - Quick Reference

## What is UUPS?

**Universal Upgradeable Proxy Standard** - A pattern where:
- **Proxy** holds the state (storage)
- **Implementation** holds the logic (functions)
- Upgrade by pointing proxy to new implementation

## Why UUPS over Transparent Proxy?

| Feature | UUPS | Transparent Proxy |
|---------|------|-------------------|
| Upgrade function location | Implementation | Proxy |
| Gas cost | Lower | Higher |
| Deployment cost | Lower | Higher |
| Complexity | Medium | Lower |

**We use UUPS because:** Lower gas, cheaper deployment, works great with owner-controlled upgrades.

## Contract Structure

### Before Upgrade
```
User → Proxy (0xABC...)
         ↓ delegatecall
       Implementation V1 (0x123...)
         - petitionCount: 5
         - usedSignNullifier: {...}
```

### After Upgrade
```
User → Proxy (0xABC...) ← Same address!
         ↓ delegatecall
       Implementation V2 (0x456...) ← New logic
         - petitionCount: 5 ← State preserved!
         - usedSignNullifier: {...}
```

## Key Concepts

### 1. Storage Layout MUST NOT Change

```solidity
// ✅ SAFE: Add new variables at end
contract V1 {
    uint256 public petitionCount;  // Slot 0
}

contract V2 {
    uint256 public petitionCount;  // Slot 0 - SAME
    uint256 public newFeature;     // Slot 1 - NEW
}

// ❌ UNSAFE: Reorder or remove variables
contract V2Bad {
    uint256 public newFeature;     // Slot 0 - WRONG!
    uint256 public petitionCount;  // Slot 1 - CORRUPTED!
}
```

### 2. Initialize, Don't Construct

```solidity
// ❌ WRONG: Constructor won't work
constructor(address _authorizer) {
    authorizer = _authorizer;
}

// ✅ CORRECT: Use initializer
function initialize(address _authorizer) public initializer {
    __Ownable_init(msg.sender);
    __UUPSUpgradeable_init();
    authorizer = IAuthorizer(_authorizer);
}
```

### 3. Disable Initializers in Implementation

```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
    _disableInitializers();  // Prevent initialization of implementation
}
```

## How to Upgrade

### Step 1: Deploy New Implementation

```bash
forge create src/PetitionRegistry.sol:PetitionRegistry \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY

# Note the address: 0x456...
```

### Step 2: Call upgradeToAndCall

```bash
# Option A: Using cast
cast send $PROXY_ADDRESS \
  "upgradeToAndCall(address,bytes)" \
  0x456... \  # New implementation address
  0x \        # No initialization data
  --rpc-url $RPC_URL \
  --private-key $OWNER_PRIVATE_KEY

# Option B: Using script
forge script script/Deploy.s.sol:UpgradePetitionRegistry \
  --rpc-url $RPC_URL \
  --broadcast
```

### Step 3: Verify Upgrade

```bash
# Check implementation address changed
cast call $PROXY_ADDRESS "implementation()" --rpc-url $RPC_URL

# Check state preserved
cast call $PROXY_ADDRESS "petitionCount()" --rpc-url $RPC_URL
# Should show same count as before!
```

## Common Upgrade Scenarios

### Add New Function

```solidity
// V1
contract PetitionRegistry {
    function signPetition(...) { ... }
}

// V2 - Add new function
contract PetitionRegistry {
    function signPetition(...) { ... }  // Existing
    function batchSign(...) { ... }     // NEW - totally safe!
}
```

### Fix Bug in Existing Function

```solidity
// V1
function signPetition(...) {
    // Bug: missing check
    authorizer.authorizeSign(...);
}

// V2 - Fix bug
function signPetition(...) {
    require(petition.exists, "Not found");  // FIX
    authorizer.authorizeSign(...);
}
```

### Add New Storage Variable

```solidity
// V1
contract PetitionRegistry {
    uint256 public petitionCount;
}

// V2 - Add new variable AT END
contract PetitionRegistry {
    uint256 public petitionCount;     // Slot 0 - SAME
    uint256 public minimumSignatures; // Slot 1 - NEW at end
}
```

## Upgrade Checklist

Before upgrading, verify:

- [ ] Storage layout hasn't changed order
- [ ] New variables added at end only
- [ ] No variables removed
- [ ] New functions don't conflict with old
- [ ] Tested on testnet first
- [ ] Have rollback plan (previous implementation address)

## Emergency Rollback

If upgrade breaks something:

```bash
# Deploy old implementation again OR reuse old address
OLD_IMPL=0x123...

# Downgrade
cast send $PROXY_ADDRESS \
  "upgradeToAndCall(address,bytes)" \
  $OLD_IMPL \
  0x \
  --rpc-url $RPC_URL \
  --private-key $OWNER_PRIVATE_KEY
```

## Testing Upgrades

```solidity
// test/Upgrade.t.sol
function testUpgrade() public {
    // Deploy V1
    PetitionRegistryV1 implV1 = new PetitionRegistryV1();
    ERC1967Proxy proxy = new ERC1967Proxy(
        address(implV1),
        abi.encodeWithSelector(PetitionRegistryV1.initialize.selector, attester)
    );
    PetitionRegistryV1 registry = PetitionRegistryV1(address(proxy));
    
    // Use V1
    registry.createPetition("test");
    assertEq(registry.petitionCount(), 1);
    
    // Upgrade to V2
    PetitionRegistryV2 implV2 = new PetitionRegistryV2();
    registry.upgradeToAndCall(address(implV2), "");
    
    // Cast to V2
    PetitionRegistryV2 registryV2 = PetitionRegistryV2(address(proxy));
    
    // Verify state preserved
    assertEq(registryV2.petitionCount(), 1);  // Still 1!
    
    // Test new function
    registryV2.newFeature();
}
```

## Security Considerations

### 1. Only Owner Can Upgrade

```solidity
function _authorizeUpgrade(address newImplementation) 
    internal 
    override 
    onlyOwner  // ← Only owner can upgrade
{}
```

### 2. Consider Timelock for Production

```solidity
// Add 48-hour delay for upgrades
contract TimelockController {
    function scheduleUpgrade(address newImpl) external onlyOwner {
        executeAfter[newImpl] = block.timestamp + 48 hours;
    }
}
```

### 3. Multi-sig for Owner

Instead of single owner, use Gnosis Safe:

```bash
# Set owner to multi-sig
cast send $PROXY_ADDRESS \
  "transferOwnership(address)" \
  $GNOSIS_SAFE_ADDRESS \
  --private-key $CURRENT_OWNER
```

## UUPS vs Our Design

Our contracts are **doubly upgradeable**:

1. **Implementation upgradeable** (UUPS) - Fix bugs, add features
2. **Authorizer swappable** - Change auth mechanism (M1 → M2)

```
Registry Proxy → Registry Implementation (upgradeable)
                        ↓ calls
                   Authorizer (swappable)
                        ↓
               Attestation OR ZK Authorizer (both upgradeable)
```

This gives maximum flexibility!

## Reference Commands

```bash
# Check current implementation
cast call $PROXY "implementation()" --rpc-url $RPC

# Check owner
cast call $PROXY "owner()" --rpc-url $RPC

# Transfer ownership
cast send $PROXY "transferOwnership(address)" $NEW_OWNER \
  --private-key $OWNER_KEY --rpc-url $RPC

# Upgrade
cast send $PROXY "upgradeToAndCall(address,bytes)" $NEW_IMPL 0x \
  --private-key $OWNER_KEY --rpc-url $RPC
```

## Learn More

- [OpenZeppelin UUPS Docs](https://docs.openzeppelin.com/contracts/4.x/api/proxy#UUPSUpgradeable)
- [EIP-1822](https://eips.ethereum.org/EIPS/eip-1822)
- [Foundry Upgrades](https://book.getfoundry.sh/tutorials/best-practices#upgradeable-contracts)
