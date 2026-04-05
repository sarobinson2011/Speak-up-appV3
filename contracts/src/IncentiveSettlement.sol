// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

/*
    IncentiveSettlement.sol

    V1 coarse consequence settlement module.

    This module:
    - stores the policy signer
    - stores the linked AdmissionRegistry
    - stores the three coarse refund amounts
    - accepts signed coarse refund bands
    - triggers authorized payout through AdmissionRegistry

    It does not:
    - compute the hidden evaluation function on-chain
    - store cross-layer traces
    - store scores, thresholds, or explanation metadata
    - hold the primary bond pool
*/

import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

interface IAdmissionRegistrySettlementView {
    enum Status {
        None,
        Funded,
        Consumed,
        Refunded
    }

    function getStatus(bytes32 admissionCommitment) external view returns (Status);
    function settleConsumedRightRefund(
        bytes32 admissionCommitment,
        address recipient,
        uint256 amount
    ) external;
}

contract IncentiveSettlement is Initializable, OwnableUpgradeable {
    // ============================================================
    // Types
    // ============================================================

    enum RefundBand {
        Unset,
        Reduced,
        Standard,
        Enhanced
    }

    // ============================================================
    // Errors
    // ============================================================

    error ZeroAddress();
    error InvalidRefundSchedule();
    error InvalidBand();
    error InvalidSignature();
    error BandAlreadyAssigned();
    error BandNotAssigned();
    error RefundAlreadyClaimed();
    error AdmissionRegistryNotSet();
    error RightNotConsumed();
    error InvalidRecipient();

    // ============================================================
    // Events
    // ============================================================

    event PolicySignerSet(address indexed newSigner);
    event AdmissionRegistrySet(address indexed newRegistry);
    event RefundScheduleSet(
        uint256 reducedAmount,
        uint256 standardAmount,
        uint256 enhancedAmount
    );
    event RefundBandAssigned(bytes32 indexed admissionCommitment, RefundBand band);
    event ConsumedRefundClaimed(
        bytes32 indexed admissionCommitment,
        address indexed recipient,
        uint256 amount
    );

    // ============================================================
    // Storage
    // ============================================================

    address public policySigner;
    address public admissionRegistry;

    uint256 public reducedRefundAmount;
    uint256 public standardRefundAmount;
    uint256 public enhancedRefundAmount;

    mapping(bytes32 => RefundBand) internal _refundBand;
    mapping(bytes32 => bool) internal _bandAssigned;
    mapping(bytes32 => bool) internal _refundClaimed;

    // ============================================================
    // Initializer
    // ============================================================

    function initialize(address initialOwner) external initializer {
        if (initialOwner == address(0)) revert ZeroAddress();
        __Ownable_init(initialOwner);
    }

    // ============================================================
    // Views
    // ============================================================

    function refundBandOf(bytes32 admissionCommitment) external view returns (RefundBand) {
        return _refundBand[admissionCommitment];
    }

    function isBandAssigned(bytes32 admissionCommitment) external view returns (bool) {
        return _bandAssigned[admissionCommitment];
    }

    function isRefundClaimed(bytes32 admissionCommitment) external view returns (bool) {
        return _refundClaimed[admissionCommitment];
    }

    function bandAssignmentDigest(
        bytes32 admissionCommitment,
        RefundBand band
    ) public pure returns (bytes32) {
        return keccak256(abi.encode(admissionCommitment, band));
    }

    // ============================================================
    // Admin / config
    // ============================================================

    function setPolicySigner(address newSigner) external onlyOwner {
        if (newSigner == address(0)) revert ZeroAddress();

        policySigner = newSigner;
        emit PolicySignerSet(newSigner);
    }

    function setAdmissionRegistry(address newRegistry) external onlyOwner {
        if (newRegistry == address(0)) revert ZeroAddress();

        admissionRegistry = newRegistry;
        emit AdmissionRegistrySet(newRegistry);
    }

    function setRefundSchedule(
        uint256 reducedAmount,
        uint256 standardAmount,
        uint256 enhancedAmount
    ) external onlyOwner {
        if (reducedAmount > standardAmount) revert InvalidRefundSchedule();
        if (standardAmount > enhancedAmount) revert InvalidRefundSchedule();
        if (enhancedAmount > 1 ether) revert InvalidRefundSchedule();

        reducedRefundAmount = reducedAmount;
        standardRefundAmount = standardAmount;
        enhancedRefundAmount = enhancedAmount;

        emit RefundScheduleSet(reducedAmount, standardAmount, enhancedAmount);
    }

    // ============================================================
    // Policy / settlement
    // ============================================================

    function submitRefundBand(
        bytes32 admissionCommitment,
        RefundBand band,
        bytes calldata signature
    ) external {
        if (admissionRegistry == address(0)) revert AdmissionRegistryNotSet();
        if (band == RefundBand.Unset) revert InvalidBand();
        if (_bandAssigned[admissionCommitment]) revert BandAlreadyAssigned();

        IAdmissionRegistrySettlementView.Status status =
            IAdmissionRegistrySettlementView(admissionRegistry).getStatus(admissionCommitment);

        if (status != IAdmissionRegistrySettlementView.Status.Consumed) {
            revert RightNotConsumed();
        }

        bytes32 digest = bandAssignmentDigest(admissionCommitment, band);
        address recovered = ECDSA.recover(digest, signature);
        if (recovered != policySigner) revert InvalidSignature();

        _refundBand[admissionCommitment] = band;
        _bandAssigned[admissionCommitment] = true;

        emit RefundBandAssigned(admissionCommitment, band);
    }

    function claimConsumedRightRefund(
        bytes32 admissionCommitment,
        address recipient
    ) external {
        if (admissionRegistry == address(0)) revert AdmissionRegistryNotSet();
        if (!_bandAssigned[admissionCommitment]) revert BandNotAssigned();
        if (_refundClaimed[admissionCommitment]) revert RefundAlreadyClaimed();
        if (recipient == address(0)) revert InvalidRecipient();

        IAdmissionRegistrySettlementView.Status status =
            IAdmissionRegistrySettlementView(admissionRegistry).getStatus(admissionCommitment);

        if (status != IAdmissionRegistrySettlementView.Status.Consumed) {
            revert RightNotConsumed();
        }

        RefundBand band = _refundBand[admissionCommitment];
        uint256 amount = _refundAmountForBand(band);

        _refundClaimed[admissionCommitment] = true;

        IAdmissionRegistrySettlementView(admissionRegistry).settleConsumedRightRefund(
            admissionCommitment,
            recipient,
            amount
        );

        emit ConsumedRefundClaimed(admissionCommitment, recipient, amount);
    }

    // ============================================================
    // Internal helpers
    // ============================================================

    function _refundAmountForBand(RefundBand band) internal view returns (uint256) {
        if (band == RefundBand.Reduced) return reducedRefundAmount;
        if (band == RefundBand.Standard) return standardRefundAmount;
        if (band == RefundBand.Enhanced) return enhancedRefundAmount;
        revert InvalidBand();
    }

    // ============================================================
    // Storage gap
    // ============================================================

    uint256[44] private __gap;
}