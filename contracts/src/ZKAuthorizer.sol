// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

interface IAuthorizer {
    function authorizeSign(uint256 petitionId, bytes32 nullifier, bytes calldata authData) external view returns (bool);
    function authorizeComment(uint256 petitionId, bytes32 nullifier, bytes32 commentHash, bytes calldata authData) external view returns (bool);
}

/**
 * @notice UltraHonk verifier interface
 */
interface IUltraHonkVerifier {
    function verify(bytes calldata proof, bytes32[] calldata publicInputs) external view returns (bool);
}

/**
 * @title ZKAuthorizer
 * @notice M2 authorizer using zero-knowledge proofs (Noir + bb UltraHonk) - UUPS Upgradeable
 */
contract ZKAuthorizer is Initializable, UUPSUpgradeable, OwnableUpgradeable, IAuthorizer {
    /*//////////////////////////////////////////////////////////////
                                ERRORS
    //////////////////////////////////////////////////////////////*/

    error InvalidProof();
    error InvalidVerifier();
    error InvalidPublicInputs();

    /*//////////////////////////////////////////////////////////////
                                EVENTS
    //////////////////////////////////////////////////////////////*/

    event VerifierUpdated(address indexed oldVerifier, address indexed newVerifier);

    /*//////////////////////////////////////////////////////////////
                            STATE VARIABLES
    //////////////////////////////////////////////////////////////*/

    address public verifier;

    /*//////////////////////////////////////////////////////////////
                            CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /**
     * @notice Initialize the contract
     * @param _verifier UltraHonk verifier contract address
     */
    function initialize(address _verifier) public initializer {
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
        
        if (_verifier == address(0)) revert InvalidVerifier();
        verifier = _verifier;
    }

    /*//////////////////////////////////////////////////////////////
                        AUTHORIZATION LOGIC
    //////////////////////////////////////////////////////////////*/

    function authorizeSign(
        uint256 petitionId,
        bytes32 nullifier,
        bytes calldata authData
    ) external view override returns (bool) {
        (bytes memory proof, bytes32[] memory publicInputs) = abi.decode(authData, (bytes, bytes32[]));

        if (publicInputs.length != 2) revert InvalidPublicInputs();
        if (uint256(publicInputs[0]) != petitionId) revert InvalidPublicInputs();
        if (publicInputs[1] != nullifier) revert InvalidPublicInputs();

        bool valid = IUltraHonkVerifier(verifier).verify(proof, publicInputs);
        if (!valid) revert InvalidProof();

        return true;
    }

    function authorizeComment(
        uint256 petitionId,
        bytes32 nullifier,
        bytes32 commentHash,
        bytes calldata authData
    ) external view override returns (bool) {
        (bytes memory proof, bytes32[] memory publicInputs) = abi.decode(authData, (bytes, bytes32[]));

        if (publicInputs.length != 3) revert InvalidPublicInputs();
        if (uint256(publicInputs[0]) != petitionId) revert InvalidPublicInputs();
        if (publicInputs[1] != nullifier) revert InvalidPublicInputs();
        if (publicInputs[2] != commentHash) revert InvalidPublicInputs();

        bool valid = IUltraHonkVerifier(verifier).verify(proof, publicInputs);
        if (!valid) revert InvalidProof();

        return true;
    }

    /*//////////////////////////////////////////////////////////////
                            GOVERNANCE
    //////////////////////////////////////////////////////////////*/

    function setVerifier(address newVerifier) external onlyOwner {
        if (newVerifier == address(0)) revert InvalidVerifier();
        
        address oldVerifier = verifier;
        verifier = newVerifier;
        
        emit VerifierUpdated(oldVerifier, newVerifier);
    }

    /*//////////////////////////////////////////////////////////////
                            UUPS UPGRADE
    //////////////////////////////////////////////////////////////*/

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}