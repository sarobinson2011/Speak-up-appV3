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
 * @title AttestationAuthorizer
 * @notice M1 authorizer using ECDSA attestations (EIP-712) - UUPS Upgradeable
 */
contract AttestationAuthorizer is Initializable, UUPSUpgradeable, OwnableUpgradeable, IAuthorizer {
    /*//////////////////////////////////////////////////////////////
                                ERRORS
    //////////////////////////////////////////////////////////////*/

    error InvalidSignature();
    error ExpiredAttestation();
    error InvalidAttester();

    /*//////////////////////////////////////////////////////////////
                                EVENTS
    //////////////////////////////////////////////////////////////*/

    event AttesterUpdated(address indexed oldAttester, address indexed newAttester);

    /*//////////////////////////////////////////////////////////////
                            STATE VARIABLES
    //////////////////////////////////////////////////////////////*/

    address public attester;
    bytes32 private DOMAIN_SEPARATOR;

    /*//////////////////////////////////////////////////////////////
                            EIP-712 CONSTANTS
    //////////////////////////////////////////////////////////////*/

    bytes32 private constant SIGN_ACTION = keccak256("SIGN");
    bytes32 private constant COMMENT_ACTION = keccak256("COMMENT");

    bytes32 private constant SIGN_PERMIT_TYPEHASH = keccak256(
        "SignPermit(bytes32 action,uint256 petitionId,bytes32 nullifier,uint256 expiry)"
    );

    bytes32 private constant COMMENT_PERMIT_TYPEHASH = keccak256(
        "CommentPermit(bytes32 action,uint256 petitionId,bytes32 nullifier,bytes32 commentHash,uint256 expiry)"
    );

    /*//////////////////////////////////////////////////////////////
                            CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /**
     * @notice Initialize the contract
     * @param _attester Initial attester address (backend signer)
     * @param _verifyingContract The PetitionRegistry contract address (for EIP-712 domain)
     */
    function initialize(address _attester, address _verifyingContract) public initializer {
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
        
        if (_attester == address(0)) revert InvalidAttester();
        attester = _attester;

        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                keccak256("SpeakUpV3"),
                keccak256("1"),
                block.chainid,
                _verifyingContract
            )
        );
    }

    /*//////////////////////////////////////////////////////////////
                        AUTHORIZATION LOGIC
    //////////////////////////////////////////////////////////////*/

    function authorizeSign(
        uint256 petitionId,
        bytes32 nullifier,
        bytes calldata authData
    ) external view override returns (bool) {
        (uint256 expiry, uint8 v, bytes32 r, bytes32 s) = abi.decode(authData, (uint256, uint8, bytes32, bytes32));

        if (block.timestamp > expiry) revert ExpiredAttestation();

        bytes32 structHash = keccak256(
            abi.encode(SIGN_PERMIT_TYPEHASH, SIGN_ACTION, petitionId, nullifier, expiry)
        );

        bytes32 digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));

        address recovered = ecrecover(digest, v, r, s);
        if (recovered != attester || recovered == address(0)) revert InvalidSignature();

        return true;
    }

    function authorizeComment(
        uint256 petitionId,
        bytes32 nullifier,
        bytes32 commentHash,
        bytes calldata authData
    ) external view override returns (bool) {
        (uint256 expiry, uint8 v, bytes32 r, bytes32 s) = abi.decode(authData, (uint256, uint8, bytes32, bytes32));

        if (block.timestamp > expiry) revert ExpiredAttestation();

        bytes32 structHash = keccak256(
            abi.encode(COMMENT_PERMIT_TYPEHASH, COMMENT_ACTION, petitionId, nullifier, commentHash, expiry)
        );

        bytes32 digest = keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));

        address recovered = ecrecover(digest, v, r, s);
        if (recovered != attester || recovered == address(0)) revert InvalidSignature();

        return true;
    }

    /*//////////////////////////////////////////////////////////////
                            GOVERNANCE
    //////////////////////////////////////////////////////////////*/

    function setAttester(address newAttester) external onlyOwner {
        if (newAttester == address(0)) revert InvalidAttester();
        
        address oldAttester = attester;
        attester = newAttester;
        
        emit AttesterUpdated(oldAttester, newAttester);
    }

    /*//////////////////////////////////////////////////////////////
                            VIEW FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    function getDomainSeparator() external view returns (bytes32) {
        return DOMAIN_SEPARATOR;
    }

    function computeSignDigest(uint256 petitionId, bytes32 nullifier, uint256 expiry) 
        external view returns (bytes32) 
    {
        bytes32 structHash = keccak256(
            abi.encode(SIGN_PERMIT_TYPEHASH, SIGN_ACTION, petitionId, nullifier, expiry)
        );
        return keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));
    }

    function computeCommentDigest(
        uint256 petitionId,
        bytes32 nullifier,
        bytes32 commentHash,
        uint256 expiry
    ) external view returns (bytes32) {
        bytes32 structHash = keccak256(
            abi.encode(COMMENT_PERMIT_TYPEHASH, COMMENT_ACTION, petitionId, nullifier, commentHash, expiry)
        );
        return keccak256(abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash));
    }

    /*//////////////////////////////////////////////////////////////
                            UUPS UPGRADE
    //////////////////////////////////////////////////////////////*/

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
