pragma circom 2.1.0;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/mux1.circom";

// Merkle tree inclusion proof using MultiMux1 (battle-tested pattern)
template MerkleTreeInclusionProof(nLevels) {
    signal input leaf;
    signal input siblings[nLevels];
    signal input pathIndices[nLevels]; // 0 = left child, 1 = right child
    signal input root;

    // Declare arrays at template scope (NOT inside loop)
    component poseidons[nLevels];
    component mux[nLevels];
    signal hashes[nLevels + 1];
    
    hashes[0] <== leaf;

    for (var i = 0; i < nLevels; i++) {
        // Constrain pathIndices to binary (0 or 1)
        pathIndices[i] * (1 - pathIndices[i]) === 0;

        // Instantiate components
        poseidons[i] = Poseidon(2);
        mux[i] = MultiMux1(2);

        // MultiMux1 selects ordering:
        // c[0] = when selector=0 => [hashes[i], siblings[i]] (leaf is left)
        // c[1] = when selector=1 => [siblings[i], hashes[i]] (leaf is right)
        mux[i].c[0][0] <== hashes[i];
        mux[i].c[0][1] <== siblings[i];
        mux[i].c[1][0] <== siblings[i];
        mux[i].c[1][1] <== hashes[i];
        mux[i].s <== pathIndices[i];

        // Hash the selected ordering
        poseidons[i].inputs[0] <== mux[i].out[0];
        poseidons[i].inputs[1] <== mux[i].out[1];

        hashes[i + 1] <== poseidons[i].out;
    }

    // Verify computed root matches expected root
    hashes[nLevels] === root;
}

template SignPetition(nLevels) {
    // ========== PRIVATE INPUTS ==========
    signal input memberSecret;
    signal input membershipPath[nLevels];      // Sibling hashes
    signal input membershipIndices[nLevels];   // Path indices (0/1)
    
    // ========== PUBLIC INPUTS ==========
    signal input petitionId;
    signal input membershipRoot;
    
    // ========== PUBLIC OUTPUTS ==========
    signal output nullifier;
    
    // ========== CONSTRAINTS ==========
    
    // 1. Compute member leaf from secret
    component memberHasher = Poseidon(1);
    memberHasher.inputs[0] <== memberSecret;
    
    // 2. Verify membership in Merkle tree
    component merkleProof = MerkleTreeInclusionProof(nLevels);
    merkleProof.leaf <== memberHasher.out;
    merkleProof.root <== membershipRoot;
    for (var i = 0; i < nLevels; i++) {
        merkleProof.siblings[i] <== membershipPath[i];
        merkleProof.pathIndices[i] <== membershipIndices[i];
    }
    
    // 3. Compute nullifier (prevents double-signing)
    // nullifier = hash(memberSecret, petitionId, SIGN_DOMAIN)
    component nullifierHasher = Poseidon(3);
    nullifierHasher.inputs[0] <== memberSecret;
    nullifierHasher.inputs[1] <== petitionId;
    nullifierHasher.inputs[2] <== 0x5349474e;  // "SIGN" domain separator
    
    nullifier <== nullifierHasher.out;
}

// Depth 10 for testing (1K members)
// Change to 20 for production (1M members)
component main {public [petitionId, membershipRoot]} = SignPetition(16);
