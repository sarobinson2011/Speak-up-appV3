// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../v3/Groth16Verifier.sol";

/**
 * @title Groth16VerifierTest
 * @notice Simple test contract to verify the golden proof on-chain
 * @dev This contract just wraps the verifier for easy testing
 */
contract Groth16VerifierTest {
    Groth16Verifier public verifier;
    
    // Track successful verifications
    uint256 public successfulVerifications;
    
    event ProofVerified(
        address indexed caller,
        uint256[3] publicSignals,
        bool result
    );
    
    constructor(address _verifier) {
        verifier = Groth16Verifier(_verifier);
    }
    
    /**
     * @notice Test the golden proof from Phase 1
     * @dev Uses the exact calldata from golden-proof.json
     */
    function testGoldenProof(
        uint[2] calldata _pA,
        uint[2][2] calldata _pB,
        uint[2] calldata _pC,
        uint[3] calldata _pubSignals
    ) external returns (bool) {
        bool result = verifier.verifyProof(_pA, _pB, _pC, _pubSignals);
        
        if (result) {
            successfulVerifications++;
        }
        
        emit ProofVerified(msg.sender, _pubSignals, result);
        
        require(result, "Proof verification failed");
        
        return result;
    }
    
    /**
     * @notice Direct passthrough to verifier (view function)
     * @dev For read-only testing without state changes
     */
    function verifyProof(
        uint[2] calldata _pA,
        uint[2][2] calldata _pB,
        uint[2] calldata _pC,
        uint[3] calldata _pubSignals
    ) external view returns (bool) {
        return verifier.verifyProof(_pA, _pB, _pC, _pubSignals);
    }
    
    /**
     * @notice Get the verifier address
     */
    function getVerifier() external view returns (address) {
        return address(verifier);
    }
}
