# Engineering[18] Operational Baseline Check

Purpose: verify the current stable live baseline after the admission bond correction.

This is an operator checklist. It does not change contracts, ZK circuits, relay logic, or membership semantics.

## Canonical live addresses

AdmissionRegistry proxy:

`0x36c22227098B24E5aCE48dEa3988327256481F0e`

PetitionRegistry proxy:

`0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD`

Aurora testnet RPC:

`https://testnet.aurora.dev`

## Expected live configuration

Admission bond:

`10000000000000000 wei`

Equivalent:

`0.01 ETH`

Lock period:

`604800 seconds`

Equivalent:

`7 days`

## Read-only live checks

```bash
cast call 0x36c22227098B24E5aCE48dEa3988327256481F0e \
  "admissionBond()(uint256)" \
  --rpc-url https://testnet.aurora.dev

cast call 0x36c22227098B24E5aCE48dEa3988327256481F0e \
  "lockPeriod()(uint256)" \
  --rpc-url https://testnet.aurora.dev

cast call 0x36c22227098B24E5aCE48dEa3988327256481F0e \
  "petitionRegistry()(address)" \
  --rpc-url https://testnet.aurora.dev

cast call 0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD \
  "admissionRegistry()(address)" \
  --rpc-url https://testnet.aurora.dev