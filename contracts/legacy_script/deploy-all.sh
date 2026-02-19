#!/bin/bash
# Deploy ALL Speak-Up V3 contracts to Aurora Testnet
# Deploys: PetitionRegistry + AttestationAuthorizer (implementations + proxies)
# Usage: ./deploy-all.sh

# Load environment variables
source ../.env

echo "=== Deploying ALL Speak-Up V3 Contracts to Aurora Testnet ==="
echo ""

# Get deployer address
DEPLOYER=$(cast wallet address dev-deployer)
echo "Deployer: $DEPLOYER"
echo ""

# Deploy everything
forge script script/Deploy.s.sol:DeployV3 \
  --rpc-url https://testnet.aurora.dev \
  --account dev-deployer \
  --broadcast \
  --legacy

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Remember to:"
echo "1. Copy the proxy addresses to your .env file"
echo "2. Update the attester if needed"
echo "3. Verify the implementation contracts with ./verify.sh"
