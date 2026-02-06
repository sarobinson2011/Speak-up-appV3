// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

interface IAuthorizer {
    function authorizeSign(uint256 petitionId, bytes32 nullifier, bytes calldata authData) external view returns (bool);
    function authorizeComment(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes calldata authData) external view returns (bool);
}

interface IGroth16Verifier {
    function verifyProof(
        uint256[2] calldata _pA,
        uint256[2][2] calldata _pB,
        uint256[2] calldata _pC,
        uint256[3] calldata _pubSignals
    ) external view returns (bool);
}

/**
 * @title PetitionRegistry
 * @notice Core petition platform contract for Speak-Up V3 (UUPS Upgradeable)
 * @dev State model and events are FROZEN - they work identically for both
 *      attestation-based (M1) and ZK-proof-based (M2) authorization.
 */
contract PetitionRegistry is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    /*//////////////////////////////////////////////////////////////
                                ERRORS
    //////////////////////////////////////////////////////////////*/

    error Unauthorized();
    error NullifierAlreadyUsed();
    error PetitionDoesNotExist();
    error InvalidAuthorizer();
    error InvalidVerifier();
    error InvalidZKProof();

    /*//////////////////////////////////////////////////////////////
                                EVENTS
    //////////////////////////////////////////////////////////////*/

    event PetitionCreated(uint256 indexed petitionId, address indexed creator, string metadataURI);
    event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier);
    event PetitionCommented(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 commentHash);
    event AuthorizerUpdated(address indexed oldAuthorizer, address indexed newAuthorizer);
    event Groth16VerifierUpdated(address indexed oldVerifier, address indexed newVerifier);

    /*//////////////////////////////////////////////////////////////
                            STATE VARIABLES
    //////////////////////////////////////////////////////////////*/

    uint256 public petitionCount;
    IAuthorizer public authorizer;
    IGroth16Verifier public groth16Verifier;

    /*//////////////////////////////////////////////////////////////
                        STABLE STATE MODEL
    //////////////////////////////////////////////////////////////*/

    struct Petition {
        address creator;
        uint256 createdAt;
        string metadataURI;
        bool exists;
    }

    mapping(uint256 => Petition) public petitions;
    mapping(uint256 => mapping(bytes32 => bool)) public usedSignNullifier;
    mapping(uint256 => mapping(bytes32 => bool)) public usedCommentNullifier;

    /*//////////////////////////////////////////////////////////////
                            CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /**
     * @notice Initialize the contract (replaces constructor for upgradeable)
     * @param _authorizer Initial authorizer (AttestationAuthorizer for M1)
     */
    function initialize(address _authorizer) public initializer {
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
        
        if (_authorizer == address(0)) revert InvalidAuthorizer();
        authorizer = IAuthorizer(_authorizer);
    }

    /*//////////////////////////////////////////////////////////////
                        PETITION MANAGEMENT
    //////////////////////////////////////////////////////////////*/

    function createPetition(string calldata metadataURI) external returns (uint256 petitionId) {
        petitionId = ++petitionCount;
        
        petitions[petitionId] = Petition({
            creator: msg.sender,
            createdAt: block.timestamp,
            metadataURI: metadataURI,
            exists: true
        });

        emit PetitionCreated(petitionId, msg.sender, metadataURI);
    }

    /*//////////////////////////////////////////////////////////////
                    ANONYMOUS SIGNING & COMMENTING
    //////////////////////////////////////////////////////////////*/

    function signPetition(uint256 petitionId, bytes32 nullifier, bytes calldata authData) external {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeSign(petitionId, nullifier, authData)) revert Unauthorized();

        usedSignNullifier[petitionId][nullifier] = true;
        emit PetitionSigned(petitionId, nullifier);
    }

    /**
     * @notice Sign petition with ZK proof (M2 Strong Privacy)
     * @dev Verifies Groth16 proof that user is a verified member without revealing identity
     * @param petitionId The petition to sign
     * @param nullifier User's unique nullifier for this petition
     * @param pA Groth16 proof component A
     * @param pB Groth16 proof component B
     * @param pC Groth16 proof component C
     * @param pubSignals Public signals [nullifier, petitionId, membershipRoot]
     */
    function signPetitionWithZKProof(
        uint256 petitionId,
        bytes32 nullifier,
        uint256[2] calldata pA,
        uint256[2][2] calldata pB,
        uint256[2] calldata pC,
        uint256[3] calldata pubSignals
    ) external {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        
        // Verify ZK proof
        if (address(groth16Verifier) == address(0)) revert InvalidVerifier();
        if (!groth16Verifier.verifyProof(pA, pB, pC, pubSignals)) revert InvalidZKProof();
        
        // Verify public signals match
        if (uint256(nullifier) != pubSignals[0]) revert InvalidZKProof();
        if (petitionId != pubSignals[1]) revert InvalidZKProof();
        // pubSignals[2] is membershipRoot - verified by circuit
        
        // Mark nullifier as used and emit event
        usedSignNullifier[petitionId][nullifier] = true;
        emit PetitionSigned(petitionId, nullifier);
    }

    function commentOnPetition(
        uint256 petitionId,
        bytes32 nullifier,
        bytes32 commentHash,
        bytes calldata authData
    ) external {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedCommentNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeComment(petitionId, nullifier, commentHash, authData)) revert Unauthorized();

        usedCommentNullifier[petitionId][nullifier] = true;
        emit PetitionCommented(petitionId, nullifier, commentHash);
    }

    /*//////////////////////////////////////////////////////////////
                            GOVERNANCE
    //////////////////////////////////////////////////////////////*/

    function setAuthorizer(address newAuthorizer) external onlyOwner {
        if (newAuthorizer == address(0)) revert InvalidAuthorizer();
        
        address oldAuthorizer = address(authorizer);
        authorizer = IAuthorizer(newAuthorizer);
        
        emit AuthorizerUpdated(oldAuthorizer, newAuthorizer);
    }

    function setGroth16Verifier(address newVerifier) external onlyOwner {
        if (newVerifier == address(0)) revert InvalidVerifier();
        
        address oldVerifier = address(groth16Verifier);
        groth16Verifier = IGroth16Verifier(newVerifier);
        
        emit Groth16VerifierUpdated(oldVerifier, newVerifier);
    }

    /*//////////////////////////////////////////////////////////////
                            VIEW FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    function hasSignedPetition(uint256 petitionId, bytes32 nullifier) external view returns (bool) {
        return usedSignNullifier[petitionId][nullifier];
    }

    function hasCommentedOnPetition(uint256 petitionId, bytes32 nullifier) external view returns (bool) {
        return usedCommentNullifier[petitionId][nullifier];
    }

    function getPetition(uint256 petitionId) external view returns (Petition memory) {
        return petitions[petitionId];
    }

    /*//////////////////////////////////////////////////////////////
                            UUPS UPGRADE
    //////////////////////////////////////////////////////////////*/

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
