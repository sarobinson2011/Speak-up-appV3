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

// Required qualified current-state verifier port; no production implementation supplied.
interface ILiveComparison {
    function compare(bytes32 decisionHash, bytes32 liveCut, bytes calldata evidence)
        external view returns (bool prerequisitesValid, bool eq, bool mc);
}

/**
 * @title PetitionRegistry
 * @notice Core petition platform contract for Speak-Up V3 (UUPS Upgradeable)
 * @dev State model remains action-centered.
 *      M2 signing uniqueness is enforced per petition by nullifier.
 */
contract PetitionRegistryPilot is Initializable, UUPSUpgradeable, OwnableUpgradeable {
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

    // Appended storage for upgrade compatibility.
    // Do not insert new state variables above existing storage.
    IPoseidon2 public poseidon2;
    address public admissionRegistry;

    // New candidate-only storage; historical file and deployment are unchanged.
    address public pilotExecutor;
    ILiveComparison public liveComparison;
    bytes32 public comparisonCodeHash;
    bytes32 public governingBinding;
    uint256 public configEpoch;
    uint256 public stateRevision;
    bool private entered;
    mapping(bytes32 => bool) public consumedU;
    mapping(bytes32 => bool) public consumedEvidence;
    struct Decision {
        bytes32 u;
        bytes32 operationHash;
        bytes32 actorBinding;
        bytes32 governing;
        bytes32 prerequisiteBinding;
        bytes32 expectedCut;
        bytes32 evidenceHash;
        uint256 epoch;
        uint256 revision;
        uint256 deadline;
    }
    error PilotBlocked();
    modifier serial() {
        if (entered) revert PilotBlocked();
        entered = true;
        _;
        entered = false;
    }
    modifier executorOnly() {
        if (pilotExecutor == address(0) || msg.sender != pilotExecutor) revert PilotBlocked();
        _;
    }
    function configurePilot(address executor_, address comparison_, bytes32 governing_)
        external onlyOwner serial
    {
        if (executor_ == address(0) || comparison_.code.length == 0 || governing_ == bytes32(0)) revert PilotBlocked();
        pilotExecutor = executor_;
        liveComparison = ILiveComparison(comparison_);
        comparisonCodeHash = comparison_.codehash;
        governingBinding = governing_;
        ++configEpoch;
    }
    function configurationHash() public view returns (bytes32) {
        return keccak256(abi.encode(block.chainid, address(this), _getImplementationPilot(),
            address(authorizer), address(groth16Verifier), address(poseidon2), admissionRegistry,
            pilotExecutor, address(liveComparison), comparisonCodeHash, governingBinding, configEpoch));
    }
    // EIP-1967 implementation slot, read in the owning proxy context.
    function _getImplementationPilot() internal view returns (address a) {
        bytes32 slot = bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
        assembly { a := sload(slot) }
    }
    function currentCut(uint256 p, bytes32 n) public view returns (bytes32) {
        return keccak256(abi.encode(configurationHash(), stateRevision, p, n,
            petitions[p].creator, petitions[p].createdAt, keccak256(bytes(petitions[p].metadataURI)),
            petitions[p].exists, usedSignNullifier[p][n]));
    }
    function _compareAndSign(uint256 p, bytes32 n, bytes32 op, Decision calldata d, bytes calldata evidence) internal {
        if (!petitions[p].exists || usedSignNullifier[p][n]) revert PilotBlocked();
        if (d.u == bytes32(0) || consumedU[d.u] || consumedEvidence[d.evidenceHash]
            || d.operationHash != op || d.governing != governingBinding
            || d.actorBinding == bytes32(0) || d.prerequisiteBinding == bytes32(0)
            || d.epoch != configEpoch || d.revision != stateRevision || block.timestamp > d.deadline
            || d.evidenceHash != keccak256(evidence) || evidence.length == 0
            || address(liveComparison).codehash != comparisonCodeHash) revert PilotBlocked();
        bytes32 cut = currentCut(p, n);
        if (d.expectedCut != cut) revert PilotBlocked();
        // STATICCALL: no state mutation/reentry effects. Must verify full accepted comparison.
        (bool valid, bool eq, bool mc) = liveComparison.compare(keccak256(abi.encode(d)), cut, evidence);
        if (!valid || !eq || mc) revert PilotBlocked();
        // No external call between accepted live comparison and effect.
        consumedU[d.u] = true;
        consumedEvidence[d.evidenceHash] = true;
        usedSignNullifier[p][n] = true;
        ++stateRevision;
        emit PetitionSigned(p, n, bytes32(0));
    }
    function transferOwnership(address next) public override onlyOwner serial {
        super.transferOwnership(next); ++configEpoch;
    }
    function renounceOwnership() public override onlyOwner serial {
        super.renounceOwnership(); ++configEpoch;
    }

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

    function createPetition(string calldata metadataURI) external serial returns (uint256 petitionId) {
        petitionId = ++petitionCount;
        ++stateRevision;

        petitions[petitionId] =
            Petition({creator: msg.sender, createdAt: block.timestamp, metadataURI: metadataURI, exists: true});

        emit PetitionCreated(petitionId, msg.sender, metadataURI);
    }

    // ============================================================
    // ANONYMOUS SIGNING & COMMENTING
    // ============================================================

    function signPetition(uint256 petitionId, bytes32 nullifier, bytes calldata authData, Decision calldata d, bytes calldata evidence) external executorOnly serial {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeSign(petitionId, nullifier, authData)) revert Unauthorized();

        if (keccak256(msg.data) != keccak256(abi.encodeWithSelector(msg.sig, petitionId, nullifier, authData, d, evidence))) revert PilotBlocked();
        bytes32 op = keccak256(abi.encode(bytes4(keccak256("signPetition(uint256,bytes32,bytes)")), petitionId, nullifier, authData));
        _compareAndSign(petitionId, nullifier, op, d, evidence);
    }

    /**
     * @notice Sign petition with ZK proof (M2 Strong Privacy)
     * @dev Verifies Groth16 proof that user is a member without revealing identity.
     *      The admissionCommitment parameter is retained for ABI compatibility only.
     *      It must not be used as a public cross-petition correlation tag.
     * @param petitionId The petition to sign
     * @param nullifier User's unique nullifier for this petition
     * @param admissionCommitment Deprecated/ignored. Retained for ABI compatibility.
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
        uint256[3] calldata pubSignals,
        Decision calldata d, bytes calldata evidence
    ) external executorOnly serial {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedSignNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();

        if (address(groth16Verifier) == address(0)) revert InvalidVerifier();
        if (!groth16Verifier.verifyProof(pA, pB, pC, pubSignals)) revert InvalidZKProof();

        if (uint256(nullifier) != pubSignals[0]) revert InvalidZKProof();
        if (petitionId != pubSignals[1]) revert InvalidZKProof();
        // pubSignals[2] is membershipRoot - verified by circuit

        if (keccak256(msg.data) != keccak256(abi.encodeWithSelector(msg.sig, petitionId, nullifier, admissionCommitment, pA, pB, pC, pubSignals, d, evidence))) revert PilotBlocked();
        bytes32 op = keccak256(abi.encode(bytes4(keccak256("signPetitionWithZKProof(uint256,bytes32,bytes32,uint256[2],uint256[2][2],uint256[2],uint256[3])")), petitionId, nullifier, admissionCommitment, pA, pB, pC, pubSignals));
        _compareAndSign(petitionId, nullifier, op, d, evidence);
    }

    function commentOnPetition(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes calldata authData)
        external serial
    {
        if (!petitions[petitionId].exists) revert PetitionDoesNotExist();
        if (usedCommentNullifier[petitionId][nullifier]) revert NullifierAlreadyUsed();
        if (!authorizer.authorizeComment(petitionId, nullifier, commentHash, authData)) revert Unauthorized();

        usedCommentNullifier[petitionId][nullifier] = true;
        ++stateRevision;
        emit PetitionCommented(petitionId, nullifier, commentHash);
    }

    // ============================================================
    // GOVERNANCE
    // ============================================================

    function setAuthorizer(address newAuthorizer) external onlyOwner serial {
        if (newAuthorizer == address(0)) revert InvalidAuthorizer();

        address oldAuthorizer = address(authorizer);
        authorizer = IAuthorizer(newAuthorizer);
        ++configEpoch;

        emit AuthorizerUpdated(oldAuthorizer, newAuthorizer);
    }

    function setGroth16Verifier(address newVerifier) external onlyOwner serial {
        if (newVerifier == address(0)) revert InvalidVerifier();

        address oldVerifier = address(groth16Verifier);
        groth16Verifier = IGroth16Verifier(newVerifier);
        ++configEpoch;

        emit Groth16VerifierUpdated(oldVerifier, newVerifier);
    }

    function setPoseidon2(address newPoseidon2) external onlyOwner serial {
        if (newPoseidon2 == address(0)) revert InvalidAuthorizer(); // retained existing reuse pattern

        address oldPoseidon2 = address(poseidon2);
        poseidon2 = IPoseidon2(newPoseidon2);
        ++configEpoch;

        emit Poseidon2Updated(oldPoseidon2, newPoseidon2);
    }

    function setAdmissionRegistry(address newAdmissionRegistry) external onlyOwner serial {
        if (newAdmissionRegistry == address(0)) revert InvalidAdmissionRegistry();

        address oldAdmissionRegistry = admissionRegistry;
        admissionRegistry = newAdmissionRegistry;
        ++configEpoch;

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

    function _authorizeUpgrade(address) internal override onlyOwner { revert PilotBlocked(); } // Pilot implementation frozen; no gate-removing upgrade.
}