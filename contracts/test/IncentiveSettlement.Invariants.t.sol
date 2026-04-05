// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {IncentiveSettlement} from "../src/IncentiveSettlement.sol";

contract MockPoseidon1_INV {
    function poseidon(uint256[1] memory input) external pure returns (uint256) {
        return input[0];
    }
}

contract MockAnonymousMembershipRegistry_INV {
    mapping(bytes32 => bool) internal _knownLeaves;
    uint256 public leafCount;

    error LeafAlreadyRegistered();

    function knownLeaves(bytes32 leaf) external view returns (bool) {
        return _knownLeaves[leaf];
    }

    function registerLeaf(bytes32 leaf) external returns (uint256 leafIndex) {
        if (_knownLeaves[leaf]) revert LeafAlreadyRegistered();
        _knownLeaves[leaf] = true;
        leafIndex = leafCount;
        leafCount++;
    }
}

contract IncentiveSettlementInvariantsTest is Test {
    AdmissionRegistry internal admission;
    IncentiveSettlement internal settlement;
    MockPoseidon1_INV internal poseidon1;
    MockAnonymousMembershipRegistry_INV internal anon;

    uint256 internal signerPk = 0xA11CE;
    address internal signer;
    address internal owner = address(0xB0B);
    address internal user = address(0xC0DE);
    address internal recipient = address(0xD00D);

    uint256 internal constant BOND = 1 ether;
    uint256 internal constant LOCK_PERIOD = 7 days;
    uint256 internal constant REDUCED = 0.25 ether;
    uint256 internal constant STANDARD = 0.50 ether;
    uint256 internal constant ENHANCED = 0.75 ether;

    function setUp() public {
        signer = vm.addr(signerPk);

        poseidon1 = new MockPoseidon1_INV();
        anon = new MockAnonymousMembershipRegistry_INV();

        admission = new AdmissionRegistry();
        admission.initialize(
            owner,
            address(anon),
            address(poseidon1),
            BOND,
            LOCK_PERIOD
        );

        settlement = new IncentiveSettlement();
        settlement.initialize(owner);

        vm.startPrank(owner);
        admission.setIncentiveSettlement(address(settlement));
        settlement.setAdmissionRegistry(address(admission));
        settlement.setPolicySigner(signer);
        settlement.setRefundSchedule(REDUCED, STANDARD, ENHANCED);
        vm.stopPrank();
    }

    // ============================================================
    // Helpers
    // ============================================================

    function _commit(bytes32 admissionSecret) internal view returns (bytes32) {
        uint256[1] memory input = [uint256(admissionSecret)];
        return bytes32(poseidon1.poseidon(input));
    }

    function _fund(bytes32 commitment) internal {
        vm.deal(user, 10 ether);
        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);
    }

    function _consume(bytes32 commitment, bytes32 admissionSecret, bytes32 leaf) internal {
        vm.prank(user);
        admission.activateMembership(commitment, admissionSecret, leaf);
    }

    function _signBand(
        bytes32 admissionCommitment,
        IncentiveSettlement.RefundBand band
    ) internal view returns (bytes memory) {
        bytes32 digest = settlement.bandAssignmentDigest(admissionCommitment, band);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerPk, digest);
        return abi.encodePacked(r, s, v);
    }

    function _assignBand(
        bytes32 commitment,
        IncentiveSettlement.RefundBand band
    ) internal {
        bytes memory sig = _signBand(commitment, band);
        settlement.submitRefundBand(commitment, band, sig);
    }

    // ============================================================
    // INV-01 — unused-refunded right cannot receive band
    // ============================================================

    function testInvariant_UnusedRefundedRightCannotReceiveBand() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        vm.warp(block.timestamp + LOCK_PERIOD + 1);

        vm.prank(user);
        admission.refundAdmissionRight(admissionSecret, recipient);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        vm.expectRevert(IncentiveSettlement.RightNotConsumed.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);
    }

    // ============================================================
    // INV-04 — consumed right cannot take unused refund path
    // ============================================================

    function testInvariant_ConsumedRightCannotTakeUnusedRefundPath() public {
        bytes32 admissionSecret = bytes32(uint256(221));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.warp(block.timestamp + LOCK_PERIOD + 1);

        vm.prank(user);
        vm.expectRevert(AdmissionRegistry.RightNotFunded.selector);
        admission.refundAdmissionRight(admissionSecret, recipient);
    }

    // ============================================================
    // INV-03 — consumed-right refund path blocks unused refund path
    // ============================================================

    function testInvariant_ConsumedRightRefundPathBlocksUnusedRefundPath() public {
        bytes32 admissionSecret = bytes32(uint256(331));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(332));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);
        _assignBand(commitment, IncentiveSettlement.RefundBand.Standard);

        settlement.claimConsumedRightRefund(commitment, recipient);

        vm.warp(block.timestamp + LOCK_PERIOD + 1);

        vm.prank(user);
        vm.expectRevert(AdmissionRegistry.RightNotFunded.selector);
        admission.refundAdmissionRight(admissionSecret, recipient);
    }

    // ============================================================
    // INV-05 — one consumed right gets at most one band
    // ============================================================

    function testInvariant_OneConsumedRightGetsAtMostOneBand() public {
        bytes32 admissionSecret = bytes32(uint256(441));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(442));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        _assignBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        bytes memory sig2 = _signBand(commitment, IncentiveSettlement.RefundBand.Reduced);

        vm.expectRevert(IncentiveSettlement.BandAlreadyAssigned.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Reduced, sig2);
    }

    // ============================================================
    // INV-06 — one assigned band gets at most one claim
    // ============================================================

    function testInvariant_OneAssignedBandGetsAtMostOneClaim() public {
        bytes32 admissionSecret = bytes32(uint256(551));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(552));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);
        _assignBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        settlement.claimConsumedRightRefund(commitment, recipient);

        vm.expectRevert(IncentiveSettlement.RefundAlreadyClaimed.selector);
        settlement.claimConsumedRightRefund(commitment, recipient);
    }

    // ============================================================
    // INV-07 — registry blocks second consumed-right payout
    // ============================================================

    function testInvariant_RegistryBlocksSecondConsumedRightPayout() public {
        bytes32 admissionSecret = bytes32(uint256(661));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(662));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(owner);
        admission.setIncentiveSettlement(address(this));

        admission.settleConsumedRightRefund(commitment, recipient, STANDARD);

        vm.expectRevert(AdmissionRegistry.ConsumedRefundAlreadyPaid.selector);
        admission.settleConsumedRightRefund(commitment, recipient, STANDARD);
    }

    // ============================================================
    // INV-12 — total terminal payout never exceeds committed value
    // ============================================================

    function testInvariant_ConsumedRefundPayoutNeverExceedsCommittedValue() public {
        bytes32 admissionSecret = bytes32(uint256(771));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(772));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);
        _assignBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        uint256 beforeBal = recipient.balance;
        settlement.claimConsumedRightRefund(commitment, recipient);
        uint256 paid = recipient.balance - beforeBal;

        assertLe(paid, BOND, "terminal payout must never exceed committed value");
    }

    // ============================================================
    // Extra useful invariant — used path and unused path are exclusive in practice
    // ============================================================

    function testInvariant_UnusedRefundThenConsumedRefundImpossible() public {
        bytes32 admissionSecret = bytes32(uint256(881));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        vm.warp(block.timestamp + LOCK_PERIOD + 1);

        vm.prank(user);
        admission.refundAdmissionRight(admissionSecret, recipient);

        vm.expectRevert(IncentiveSettlement.BandNotAssigned.selector);
        settlement.claimConsumedRightRefund(commitment, recipient);
    }
}