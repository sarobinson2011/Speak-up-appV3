// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

/*
    AdmissionRegistry.sol

    Enrollment Layer V1:
    - Upgradeable
    - Public bonded admission rights
    - Identity-agnostic economic rights keyed by admissionCommitment
    - Sponsored / non-funder activation permitted
    - Accounting-real right consumption
    - Direct AdmissionRegistry -> AnonymousMembershipRegistry interaction

    AdmissionRegistry is an economic rights ledger.
    It is not a participant identity layer.
*/

import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {IPoseidon1} from "./poseidon/IPoseidon1.sol";
import {IAnonymousMembershipRegistry} from "./interfaces/IAnonymousMembershipRegistry.sol";

contract AdmissionRegistry is Initializable, OwnableUpgradeable, ReentrancyGuard {
    // ============================================================
    // Types
    // ============================================================

    enum Status {
        None,
        Funded,
        Consumed,
        Refunded
    }

    struct AdmissionRight {
        uint256 amount;
        uint256 fundedAt;
        uint256 unlockAt;
        uint8 status;
    }

    // ============================================================
    // Errors
    // ============================================================

    error ZeroAddress();
    error InvalidBondAmount();
    error RightAlreadyExists();
    error RightNotFound();
    error RightNotFunded();
    error RightNotConsumed();
    error RefundTooEarly();
    error InvalidRecipient();
    error InvalidCommitment();
    error InvalidLeaf();
    error LeafAlreadyRegistered();
    error AnonymousMembershipRegistryNotSet();
    error AdmissionHasherNotSet();
    error SecretDoesNotMatchCommitment();
    error RefundTransferFailed();
    error UnauthorizedSettlementModule();
    error ConsumedRefundAlreadyPaid();
    error InvalidRefundAmount();
    error NotPetitionRegistry();
    error RightAlreadyActionLinked();
    error InvalidLockPeriod();

    // ============================================================
    // Events
    // ============================================================

    event AnonymousMembershipRegistrySet(address indexed anonymousMembershipRegistry);
    event AdmissionHasherSet(address indexed admissionHasher);
    event AdmissionBondSet(uint256 admissionBond);
    event LockPeriodSet(uint256 lockPeriod);
    event IncentiveSettlementSet(address indexed incentiveSettlement);

    event AdmissionRightFunded(bytes32 indexed admissionCommitment, uint256 amount, uint256 unlockAt);

    event AdmissionRightConsumed(bytes32 indexed admissionCommitment);

    event AdmissionRightRefunded(bytes32 indexed admissionCommitment, address indexed recipient, uint256 amount);

    event ConsumedRightRefundPaid(bytes32 indexed admissionCommitment, address indexed recipient, uint256 amount);

    // ============================================================
    // Storage
    // ============================================================

    uint256 public admissionBond;
    uint256 public lockPeriod;

    address public anonymousMembershipRegistry;
    address public admissionHasher;

    mapping(bytes32 => AdmissionRight) public rights;

    // Appended storage for upgrade compatibility from deployed b6997d5 baseline.
    // Do not insert new state variables above existing storage.
    address public incentiveSettlement;
    mapping(bytes32 => bool) public consumedRefundPaid;
    address public petitionRegistry;
    mapping(bytes32 => bool) private _actionLinked;

    // ============================================================
    // Modifiers
    // ============================================================

    modifier onlyIncentiveSettlement() {
        if (msg.sender != incentiveSettlement) revert UnauthorizedSettlementModule();
        _;
    }

    // ============================================================
    // Initializer
    // ============================================================

    function initialize(
        address initialOwner,
        address anonymousMembershipRegistry_,
        address admissionHasher_,
        uint256 admissionBond_,
        uint256 lockPeriod_
    ) external initializer {
        if (initialOwner == address(0)) revert ZeroAddress();
        if (anonymousMembershipRegistry_ == address(0)) revert ZeroAddress();
        if (admissionHasher_ == address(0)) revert ZeroAddress();

        __Ownable_init(initialOwner);

        anonymousMembershipRegistry = anonymousMembershipRegistry_;
        admissionHasher = admissionHasher_;
        admissionBond = admissionBond_;
        lockPeriod = lockPeriod_;

        emit AnonymousMembershipRegistrySet(anonymousMembershipRegistry_);
        emit AdmissionHasherSet(admissionHasher_);
        emit AdmissionBondSet(admissionBond_);
        emit LockPeriodSet(lockPeriod_);
    }

    // ============================================================
    // Admin
    // ============================================================

    function setAnonymousMembershipRegistry(address newAnonymousMembershipRegistry) external onlyOwner {
        if (newAnonymousMembershipRegistry == address(0)) revert ZeroAddress();

        anonymousMembershipRegistry = newAnonymousMembershipRegistry;
        emit AnonymousMembershipRegistrySet(newAnonymousMembershipRegistry);
    }

    function setAdmissionHasher(address newAdmissionHasher) external onlyOwner {
        if (newAdmissionHasher == address(0)) revert ZeroAddress();

        admissionHasher = newAdmissionHasher;
        emit AdmissionHasherSet(newAdmissionHasher);
    }

    function setAdmissionBond(uint256 newAdmissionBond) external onlyOwner {
        if (newAdmissionBond == 0) revert InvalidBondAmount();
        admissionBond = newAdmissionBond;
        emit AdmissionBondSet(newAdmissionBond);
    }

    function setLockPeriod(uint256 newLockPeriod) external onlyOwner {
        if (newLockPeriod == 0) revert InvalidLockPeriod();
        lockPeriod = newLockPeriod;
        emit LockPeriodSet(newLockPeriod);
    }

    function setIncentiveSettlement(address newIncentiveSettlement) external onlyOwner {
        if (newIncentiveSettlement == address(0)) revert ZeroAddress();

        incentiveSettlement = newIncentiveSettlement;
        emit IncentiveSettlementSet(newIncentiveSettlement);
    }

    function setPetitionRegistry(address petitionRegistry_) external onlyOwner {
        if (petitionRegistry_ == address(0)) revert ZeroAddress();
        petitionRegistry = petitionRegistry_;
    }

    // ============================================================
    // Core lifecycle
    // ============================================================

    function fundAdmissionRight(bytes32 admissionCommitment) external payable {
        if (msg.value != admissionBond) revert InvalidBondAmount();
        if (admissionCommitment == bytes32(0)) revert InvalidCommitment();

        AdmissionRight storage right = rights[admissionCommitment];
        if (Status(right.status) != Status.None) revert RightAlreadyExists();

        uint256 unlockAt = block.timestamp + lockPeriod;

        rights[admissionCommitment] = AdmissionRight({
            amount: msg.value, fundedAt: block.timestamp, unlockAt: unlockAt, status: uint8(Status.Funded)
        });

        emit AdmissionRightFunded(admissionCommitment, msg.value, unlockAt);
    }

    /*
        V1 enrollment semantics:
        - caller supplies commitment
        - caller supplies secret
        - contract verifies secret opens commitment
        - contract consumes the funded admission right
        - contract requests registration of exactly one leaf in AnonymousMembershipRegistry

        AdmissionRegistry accounts for right consumption only.
        It does not publicly narrate participant creation or participant readiness.
    */
    function activateMembership(bytes32 admissionCommitment, bytes32 admissionSecret, bytes32 leaf) external {
        if (anonymousMembershipRegistry == address(0)) revert AnonymousMembershipRegistryNotSet();
        if (admissionHasher == address(0)) revert AdmissionHasherNotSet();
        if (admissionCommitment == bytes32(0)) revert InvalidCommitment();
        if (leaf == bytes32(0)) revert InvalidLeaf();

        bytes32 derivedCommitment = _computeAdmissionCommitment(admissionSecret);
        if (derivedCommitment != admissionCommitment) revert SecretDoesNotMatchCommitment();

        AdmissionRight storage right = rights[admissionCommitment];
        if (Status(right.status) != Status.Funded) revert RightNotFunded();

        if (IAnonymousMembershipRegistry(anonymousMembershipRegistry).knownLeaves(leaf)) {
            revert LeafAlreadyRegistered();
        }

        right.status = uint8(Status.Consumed);

        IAnonymousMembershipRegistry(anonymousMembershipRegistry).registerLeaf(leaf);

        emit AdmissionRightConsumed(admissionCommitment);
    }

    function refundAdmissionRight(bytes32 admissionSecret, address recipient) external nonReentrant {
        if (recipient == address(0)) revert InvalidRecipient();
        if (admissionHasher == address(0)) revert AdmissionHasherNotSet();

        bytes32 admissionCommitment = _computeAdmissionCommitment(admissionSecret);
        AdmissionRight storage right = rights[admissionCommitment];

        if (Status(right.status) != Status.Funded) revert RightNotFunded();
        if (block.timestamp < right.unlockAt) revert RefundTooEarly();

        uint256 amount = right.amount;

        right.status = uint8(Status.Refunded);
        right.amount = 0;

        (bool ok,) = recipient.call{value: amount}("");
        if (!ok) revert RefundTransferFailed();

        emit AdmissionRightRefunded(admissionCommitment, recipient, amount);
    }

    /*
        Narrow payout hook for consumed-right incentive refunds.

        This function performs no incentive interpretation.
        It only executes an authorized payout for a right that is already in
        the Consumed state and has not already received a consumed-right refund.
    */
    function settleConsumedRightRefund(bytes32 admissionCommitment, address recipient, uint256 amount)
        external
        onlyIncentiveSettlement
        nonReentrant
    {
        if (recipient == address(0)) revert InvalidRecipient();

        AdmissionRight storage right = rights[admissionCommitment];

        if (Status(right.status) != Status.Consumed) revert RightNotConsumed();
        if (consumedRefundPaid[admissionCommitment]) revert ConsumedRefundAlreadyPaid();
        if (amount == 0 || amount > right.amount) revert InvalidRefundAmount();

        consumedRefundPaid[admissionCommitment] = true;

        (bool ok,) = recipient.call{value: amount}("");
        if (!ok) revert RefundTransferFailed();

        emit ConsumedRightRefundPaid(admissionCommitment, recipient, amount);
    }

    function recordActionLink(bytes32 admissionCommitment) external {
        if (msg.sender != petitionRegistry) revert NotPetitionRegistry();

        AdmissionRight storage right = rights[admissionCommitment];

        if (right.amount == 0) revert RightNotFound();
        if (Status(right.status) != Status.Consumed) revert RightNotConsumed();
        if (consumedRefundPaid[admissionCommitment]) revert ConsumedRefundAlreadyPaid();
        if (_actionLinked[admissionCommitment]) revert RightAlreadyActionLinked();

        _actionLinked[admissionCommitment] = true;
    }

    // ============================================================
    // Views
    // ============================================================

    function getRight(bytes32 admissionCommitment) external view returns (AdmissionRight memory) {
        return rights[admissionCommitment];
    }

    function getStatus(bytes32 admissionCommitment) external view returns (Status) {
        return Status(rights[admissionCommitment].status);
    }

    // ============================================================
    // Internal helpers
    // ============================================================

    function _computeAdmissionCommitment(bytes32 admissionSecret) internal view returns (bytes32) {
        if (admissionHasher == address(0)) revert AdmissionHasherNotSet();

        uint256[1] memory input = [uint256(admissionSecret)];
        uint256 out = IPoseidon1(admissionHasher).poseidon(input);
        return bytes32(out);
    }

    // ============================================================
    // Storage gap
    // ============================================================

    uint256[40] private __gap;
}
