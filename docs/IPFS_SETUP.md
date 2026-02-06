# IPFS Integration Setup Guide

## Overview

Petition metadata is now stored on **IPFS** (InterPlanetary File System) via **Pinata** for:
- ✅ Permanent, censorship-resistant storage
- ✅ Content-addressed integrity (hash proves authenticity)
- ✅ Decentralized Web3 infrastructure
- ✅ No data loss on server restart

## Setup Steps

### 1. Create Pinata Account (FREE)

1. Go to https://www.pinata.cloud/
2. Click "Sign Up" (free tier: 1GB storage, unlimited requests)
3. Verify your email

### 2. Get API Keys

1. Go to https://app.pinata.cloud/developers/api-keys
2. Click "New Key"
3. Enable permissions:
   - ✅ `pinJSONToIPFS`
   - ✅ `pinFileToIPFS`
4. Name it: `Speak-Up-V3`
5. Click "Create Key"
6. **Copy both values:**
   - API Key (starts with letters)
   - API Secret (longer key)

### 3. Add to Backend .env

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/backend

# Edit .env
nano .env

# Add these three lines:
PINATA_API_KEY=your_api_key_here
PINATA_SECRET_KEY=your_secret_key_here
PINATA_GATEWAY=gateway.pinata.cloud
```

Save and exit (Ctrl+X, Y, Enter)

### 4. Restart Backend

```bash
npm run dev
```

You should see:
```
🚀 Speak Up Backend running on port 3001
```

(No warnings about Pinata - it will silently work!)

## Testing

### Test 1: Create Petition with IPFS Upload

```bash
curl -X POST http://localhost:3001/api/petition/create \
  -H "Content-Type: application/json" \
  -d '{
    "petitionId": 999,
    "title": "Test IPFS Petition",
    "description": "This petition metadata is stored on IPFS!",
    "category": "Technology"
  }'
```

Should return:
```json
{
  "success": true,
  "metadata": {...},
  "ipfsHash": "QmXy1234...",
  "metadataURI": "ipfs://QmXy1234...",
  "gatewayUrl": "https://gateway.pinata.cloud/ipfs/QmXy1234..."
}
```

### Test 2: Fetch from IPFS

```bash
curl http://localhost:3001/api/petition/999
```

Should return the same metadata (fetched from IPFS!)

### Test 3: Verify on IPFS Gateway

Copy the `gatewayUrl` from step 1 and paste it into your browser:

```
https://gateway.pinata.cloud/ipfs/QmXy1234...
```

You should see the petition metadata JSON! 🎉

## How It Works

### When Creating a Petition:

1. Frontend calls `POST /api/petition/create` with petition data
2. Backend uploads JSON to Pinata IPFS
3. Pinata returns IPFS hash (e.g., `QmXy1234...`)
4. Backend creates on-chain with `ipfs://QmXy1234...`
5. Metadata is now **permanent** and **decentralized**!

### When Viewing a Petition:

1. Frontend reads `metadataURI` from smart contract
2. Extracts IPFS hash from `ipfs://QmXy1234...`
3. Fetches from IPFS gateway
4. Displays petition details

### Storage Flow:

```
User Creates Petition
    ↓
Backend uploads to Pinata
    ↓
Pinata pins to IPFS network
    ↓
Returns IPFS hash (QmXy...)
    ↓
Smart contract stores ipfs://QmXy...
    ↓
Content is now permanent! ✅
```

## Fallback Behavior

**If Pinata credentials are NOT set:**
- Backend logs warning
- Uses in-memory storage (like before)
- Generates fake IPFS hashes
- Useful for local testing

**If Pinata upload fails:**
- Backend catches error
- Falls back to in-memory storage
- Returns warning in response
- Prevents service disruption

## Cost & Limits

**Pinata Free Tier:**
- 1GB storage
- Unlimited requests
- Unlimited bandwidth
- Perfect for testnet/demo

**If you exceed limits:**
- Upgrade to paid plan (~$20/month for 100GB)
- Or use alternative: Web3.Storage (Filecoin-backed, free)

## IPFS Gateways

Your metadata is accessible via multiple gateways:

- **Pinata:** `https://gateway.pinata.cloud/ipfs/QmXy...`
- **IPFS.io:** `https://ipfs.io/ipfs/QmXy...`
- **Cloudflare:** `https://cloudflare-ipfs.com/ipfs/QmXy...`
- **Your own:** Run IPFS node locally

This redundancy ensures your data is always available!

## Verifying on Pinata Dashboard

1. Go to https://app.pinata.cloud/pinmanager
2. You'll see all your pinned files
3. Each petition appears as `petition-{id}`
4. Click to view details and IPFS hash

## Migration from In-Memory

Old petitions (created before IPFS) still work:
- Stored in backend's in-memory Map
- Will be lost on restart (expected)
- New petitions use IPFS (permanent)

To migrate old petitions:
1. Fetch from in-memory Map
2. Upload to IPFS
3. Update on-chain metadataURI (requires contract upgrade)

## Troubleshooting

### "Pinata credentials not set"
- Check PINATA_API_KEY and PINATA_SECRET_KEY in .env
- No quotes, no spaces
- Restart backend after adding

### "IPFS upload failed"
- Check API keys are correct
- Check internet connection
- Check Pinata status: https://status.pinata.cloud/
- Backend will fallback to in-memory storage

### "IPFS fetch failed"
- Check IPFS hash is valid (starts with Qm)
- Try different gateway
- Check Pinata gateway status

### Can't access via browser
- IPFS gateways can be slow (30s-60s first load)
- Try different gateway (ipfs.io, cloudflare-ipfs.com)
- Content is cached after first access

## Security Notes

- IPFS is **public** by default
- Anyone with the hash can view content
- Don't store sensitive data
- Petition metadata is meant to be public anyway!

## References

- Pinata Docs: https://docs.pinata.cloud/
- IPFS Docs: https://docs.ipfs.tech/
- Get API Keys: https://app.pinata.cloud/developers/api-keys

---

**IPFS integration complete! Your petitions are now permanently stored on the decentralized web.** 🌐✨
