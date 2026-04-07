// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {IPoseidon2} from "./poseidon/IPoseidon2.sol";

interface IAuthorizer {
    function authorizeSign(uint256 petitionId, bytes32 nullifier, bytes calldata authData) external view returns (bool);

    function authorizeComment(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes calldata authData)
        external
        view
        returns (bool);
}

interface IGroth16Verifier {
    function verifyProof(
        uint256[2] calldata _pA,
        uint256[2][2] calldata _pB,
        uint256[2] calldata _pC,
        uint256[3] calldata _pubSignals
    ) external view returns (bool);
}

interface IAdmissionRegistryActionLink {
    function recordActionLink(bytes32 admissionCommitment) external;
}

/**
 * @title PetitionRegistry
 * @notice Core petition platform contract for Speak-Up V3 (UUPS Upgradeable)
 * @dev State model remains action-centered.
 *      The anonymous public action event surface is extended only to carry a
 *      routing-only settlement reference for the ZK signing path.
 */
contract PetitionRegistry is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    // ============================================================
    // ERRORS
    // ============================================================

    error Unauthorized();
    error NullifierAlreadyUsed();
    error PetitionDoesNotExist();
    error InvalidAuthorizer();
    error InvalidVerifier();
    error InvalidZKProof();
    error InvalidAdmissionRegistry();

    // ============================================================
    // EVENTS
    // ============================================================

    event PetitionCreated(uint256 indexed petitionId, address indexed creator, string metadataURI);
    event PetitionSigned(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 admissionCommitment);
    event PetitionCommented(uint256 indexed petitionId, bytes32 indexed nullifier, bytes32 commentHash);
    event AuthorizerUpdated(address indexed oldAuthorizer, address indexed newAuthorizer);
    event Groth16VerifierUpdated(address indexed oldVerifier, address indexed newVerifier);
    event Poseidon2Updated(address indexed oldPoseidon2, address indexed newPoseidon2);
    event AdmissionRegistryUpdated(address indexed oldAdmissionRegistry, address indexed newAdmissionRegistry);

    // ============================================================
    // STATE VARIABLES
    // ============================================================

    uint256 public petitionCount;
    IAuthorizer public authorizer;
    IGroth16Verifier public groth16Verifier;
    IPoseidon2 public poseidon2;
    address public admissionRegistry;

    // ============================================================
    // STABLE STATE MODEL
    // ============================================================

    struct Petition {
        address creator;
        uint256 createdAt;
        string metadataURI;
        bool exists;
    }

    mapping(uint256 => Petition) public petitions;
    mapping(uint256 => mapping(bytes32 => bool)) public usedSignNullifier;
    mapping(uint256 => mapping(bytes32 => bool)) public usedCommentNullifier;

    // ============================================================
    // CONSTRUCTOR
    // ============================================================

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    // ============================================================
    // INITIALIZER
    // ============================================================

    /**
     * @notice Initialize the contract (replaces constructor for upgradeable)
     * @param _authorizer Initial authorizer
     * @param _poseidon2 Initial Poseidon2 hasher address
     */
    function initialize(address _authorizer, address _poseidon2) public initializer {
        __Ownable_init(msg.sender);

        if (_authorizer == address(0)) revert InvalidAuthorizer();
        if (_poseidon2 == address(0)) revert InvalidAuthorizer(); // retained existing reuse pattern

        authorizer = IAuthorizer(_authorizer);
        poseidon2 = IPoseidon2(_poseidon2);
    }

    // ============================================================
    // PETITION MANAGEMENT
    // ============================================================

    function createPetition(string calldata metadataURI) external returns (uint256 petitionId) {
        petitionId = ++petitionCount;

        petitions[petitionId] =
            Petition({creator: msg.sender, createdAt: block.timestamp, metadataURI: metadataURI, exists: true});

        emit PetitionCreated(petitionId, msg.sender, metadataURI);
    }

    // ============================================================
    // ANONYMOUS SIGNING & COMMENTING
    // ============================================================

    function signPetition(uint256 petitionId, bytes32 nullifier, bytes calldata authData) external {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeSign(petitionId, nullifier, authData)) revert Unauthorized();

        usedSignNullifier[petitionId][nullifier] = true;
        emit PetitionSigned(petitionId, nullifier, bytes32(0));
    }

    /**
     * @notice Sign petition with ZK proof (M2 Strong Privacy)
     * @dev Verifies Groth16 proof that user is a verified member without revealing identity.
     *      The admissionCommitment field is a routing-only settlement reference.
     * @param petitionId The petition to sign
     * @param nullifier User's unique nullifier for this petition
     * @param admissionCommitment Routing-only settlement reference
     * @param pA Groth16 proof component A
     * @param pB Groth16 proof component B
     * @param pC Groth16 proof component C
     * @param pubSignals Public signals [nullifier, petitionId, membershipRoot]
     */
    function signPetitionWithZKProof(
        uint256 petitionId,
        bytes32 nullifier,
        bytes32 admissionCommitment,
        uint256[2] calldata pA,
        uint256[2][2] calldata pB,
        uint256[2] calldata pC,
        uint256[3] calldata pubSignals
    ) external {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();

        if (address(groth16Verifier) == address(0)) revert InvalidVerifier();
        if (!groth16Verifier.verifyProof(pA, pB, pC, pubSignals)) revert InvalidZKProof();

        if (uint256(nullifier) != pubSignals[0]) revert InvalidZKProof();
        if (petitionId != pubSignals[1]) revert InvalidZKProof();
        // pubSignals[2] is membershipRoot - verified by circuit

        if (admissionRegistry == address(0)) revert InvalidAdmissionRegistry();
        IAdmissionRegistryActionLink(admissionRegistry).recordActionLink(admissionCommitment);

        usedSignNullifier[petitionId][nullifier] = true;
        emit PetitionSigned(petitionId, nullifier, admissionCommitment);
    }

    function commentOnPetition(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes calldata authData)
        external
    {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedCommentNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeComment(petitionId, nullifier, commentHash, authData)) revert Unauthorized();

        usedCommentNullifier[petitionId][nullifier] = true;
        emit PetitionCommented(petitionId, nullifier, commentHash);
    }

    // ============================================================
    // GOVERNANCE
    // ============================================================

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

    function setPoseidon2(address newPoseidon2) external onlyOwner {
        if (newPoseidon2 == address(0)) revert InvalidAuthorizer(); // retained existing reuse pattern

        address oldPoseidon2 = address(poseidon2);
        poseidon2 = IPoseidon2(newPoseidon2);

        emit Poseidon2Updated(oldPoseidon2, newPoseidon2);
    }

    function setAdmissionRegistry(address newAdmissionRegistry) external onlyOwner {
        if (newAdmissionRegistry == address(0)) revert InvalidAdmissionRegistry();

        address oldAdmissionRegistry = admissionRegistry;
        admissionRegistry = newAdmissionRegistry;

        emit AdmissionRegistryUpdated(oldAdmissionRegistry, newAdmissionRegistry);
    }

    // ============================================================
    // VIEW FUNCTIONS
    // ============================================================

    function hasSignedPetition(uint256 petitionId, bytes32 nullifier) external view returns (bool) {
        return usedSignNullifier[petitionId][nullifier];
    }

    function hasCommentedOnPetition(uint256 petitionId, bytes32 nullifier) external view returns (bool) {
        return usedCommentNullifier[petitionId][nullifier];
    }

    function getPetition(uint256 petitionId) external view returns (Petition memory) {
        return petitions[petitionId];
    }

    // ============================================================
    // UUPS UPGRADE
    // ============================================================

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}