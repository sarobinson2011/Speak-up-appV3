export const REGISTRY_ADDRESS = '0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD';
export const AUTHORIZER_ADDRESS = '0xf4FDc4a107f13b4C4d7C8be7dc0088026D201b37';
export const BACKEND_URL = 'http://localhost:3001';
export const RPC_URL = 'https://testnet.aurora.dev';
export const CHAIN_ID = 1313161555;

export const REGISTRY_ABI = [
    'function createPetition(string metadataURI) returns (uint256)',
    'function signPetition(uint256 petitionId, bytes32 nullifier, bytes authData)',
    'function commentOnPetition(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes authData)',
    'function petitionCount() view returns (uint256)',
    'function getPetition(uint256) view returns (tuple(address creator, uint256 createdAt, string metadataURI, bool exists))',
    'function hasSignedPetition(uint256 petitionId, bytes32 nullifier) view returns (bool)',
    'function hasCommentedOnPetition(uint256 petitionId, bytes32 nullifier) view returns (bool)',
    'event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier)',
    'event PetitionCommented(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 commentHash)'
];