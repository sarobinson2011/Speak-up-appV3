# Speak-Up V3 🎤

Anonymous petition platform with upgradeable smart contracts and modular authorization.

## Quick Start

```bash
# 1. Setup
cd Speak-up-appV3
cp .env.example .env
# Edit .env with your keys

# 2. Contracts
cd contracts
./install-deps.sh
forge build
forge test

# 3. Backend
cd ../backend
npm install
npm run dev

# 4. Frontend  
cd ../frontend
npm install
npm run dev
```

**Full setup guide:** [SETUP.md](./SETUP.md)

## Architecture

### Smart Contracts (UUPS Upgradeable)

- **PetitionRegistry** - Core contract with frozen state model
- **AttestationAuthorizer** - M1: EIP-712 attestations (~50k gas)
- **ZKAuthorizer** - M2: ZK proofs (~300k gas, future)

### Authorization Flow

```
M1 (Standard Privacy):
User → Backend (verify membership) → Issue attestation → Sign on-chain

M2 (Strong Privacy):
User → Generate ZK proof → Sign on-chain (no backend trust needed)
```

### Upgradeability

All contracts use OpenZeppelin's UUPS pattern:

```
User → Proxy (state) → Implementation (logic)
                           ↓ upgradeable
                     New Implementation
```

Upgrade without losing state or events!

## Project Structure

```
.
├── contracts/      # Foundry smart contracts
│   ├── src/       # Upgradeable contracts
│   ├── script/    # Deploy + upgrade scripts
│   └── test/      # Foundry tests
├── backend/        # Node.js Express API
│   └── src/       # Attestation service
├── frontend/       # React + Vite
│   └── src/       # UI components
├── zk/             # Noir circuits (M2)
└── docs/           # Documentation
```

## Key Features

✅ **UUPS Upgradeable** - All contracts can be upgraded without state migration  
✅ **Modular Auth** - Swap between attestations (M1) and ZK proofs (M2)  
✅ **Frozen State** - Same storage/events across both modes  
✅ **One Sign + One Comment** - Per petition, enforced by nullifiers  
✅ **AI Moderation** - Comments filtered before on-chain anchoring  
✅ **EIP-712 Attestations** - Secure, expiring, replay-protected permits  

## Development

### Contracts
```bash
cd contracts
forge build          # Compile
forge test           # Test
forge test -vvv      # Verbose
forge coverage       # Coverage
```

### Backend
```bash
cd backend
npm run dev          # Development mode
curl localhost:3001/health  # Test
```

### Frontend
```bash
cd frontend
npm run dev          # Start on localhost:3000
```

## Deployment

### Testnet (Aurora)

```bash
cd contracts

# Deploy
forge script script/Deploy.s.sol:DeployV3 \
  --rpc-url https://testnet.aurora.dev \
  --broadcast --verify

# Save proxy addresses to .env
```

### Upgrade Contracts

```bash
# Upgrade PetitionRegistry
forge script script/Deploy.s.sol:UpgradePetitionRegistry \
  --rpc-url https://testnet.aurora.dev \
  --broadcast

# Proxy address stays the same!
```

## Documentation

- [SETUP.md](./SETUP.md) - Complete setup guide
- [Architecture Docs](./docs/) - Design decisions and specifications

## Milestones

### M1: Attestation-Based (Current) ✅
- EIP-712 signed permits
- Backend verification
- Fast, cheap (~50k gas)
- Social anonymity

### M2: ZK Proof-Based (Future) 🔄
- Noir circuits
- UltraHonk verifier
- Cryptographic privacy
- No backend trust needed

**Upgrade path:** `registry.setAuthorizer(zkAuthorizer)` - that's it!

## Tech Stack

- **Contracts:** Solidity 0.8.24, Foundry, OpenZeppelin UUPS
- **Backend:** Node.js, Express, ethers.js
- **Frontend:** React, Vite, ethers.js
- **Network:** Aurora (EVM-compatible L2)

## Security

- UUPS upgradeable pattern (owner-controlled)
- EIP-712 domain separation
- Nullifier-based one-per-petition enforcement
- Expiring attestations
- Comment moderation

## License

MIT

---

**Build anonymous petitions with confidence! 🚀**
