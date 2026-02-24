export const REGISTRY_ADDRESS = '0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD';
/**
 * Legacy (M1) address — kept only to avoid breaking old imports during the M2-only transition.
 * Safe to remove once no frontend code imports it.
 */
export const AUTHORIZER_ADDRESS = '0xf4FDc4a107f13b4C4d7C8be7dc0088026D201b37';

export const BACKEND_URL = 'http://localhost:3001';
export const RPC_URL = 'https://testnet.aurora.dev';
export const CHAIN_ID = 1313161555;

// Minimal ABI for M2-only UI (read-only + petition creation + signed-state checks)
export const REGISTRY_ABI = [
  'function createPetition(string metadataURI) returns (uint256)',
  'function petitionCount() view returns (uint256)',
  'function getPetition(uint256) view returns (tuple(address creator, uint256 createdAt, string metadataURI, bool exists))',
  'function hasSignedPetition(uint256 petitionId, bytes32 nullifier) view returns (bool)',
  'event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier)'
];