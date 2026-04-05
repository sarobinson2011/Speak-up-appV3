// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";

/*
    Test-first file for the new narrow payout hook on AdmissionRegistry.

    This file intentionally locks the proposed AdmissionRegistry delta:

    New external/admin surface expected in AdmissionRegistry:
    - setIncentiveSettlement(address newIncentiveSettlement)

    New payout hook expected in AdmissionRegistry:
    - settleConsumedRightRefund(bytes32 admissionCommitment, address recipient, uint256 amount)

    New accounting getter expected via public mapping:
    - consumedRefundPaid(bytes32 admissionCommitment) -> bool

    New custom errors expected in AdmissionRegistry:
    - UnauthorizedSettlementModule()
    - RightNotConsumed()
    - ConsumedRefundAlreadyPaid()
    - InvalidRefundAmount()
*/

contract MockPoseidon1 {
    function poseidon(uint256[1] memory input) external pure returns (uint256) {
        // Deterministic 1:1 mock for tests.
        return input[0];
    }
}

contract MockAnonymousMembershipRegistry {
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

contract AdmissionRegistryIncentivePayoutTest is Test {
    AdmissionRegistry internal admission;
    MockPoseidon1 internal poseidon1;
    MockAnonymousMembershipRegistry internal anon;

    address internal owner = address(0xA11CE);
    address internal user = address(0xB0B);
    address internal settlementModule = address(0xC0DE);
    address internal recipient = address(0xD00D);

    uint256 internal constant BOND = 1 ether;
    uint256 internal constant LOCK_PERIOD = 7 days;

    function setUp() public {
        poseidon1 = new MockPoseidon1();
        anon = new MockAnonymousMembershipRegistry();

        admission = new AdmissionRegistry();
        admission.initialize(
            owner,
            address(anon),
            address(poseidon1),
            BOND,
            LOCK_PERIOD
        );

        vm.prank(owner);
        admission.setIncentiveSettlement(settlementModule);
    }

    // -------------------------------------------------------------------------
    // Helpers
    // -------------------------------------------------------------------------

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

    // -------------------------------------------------------------------------
    // AR-02 — non-settlement caller rejected
    // -------------------------------------------------------------------------

    function testSettleConsumedRightRefund_RevertsForNonSettlementCaller() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(user);
        vm.expectRevert(AdmissionRegistry.UnauthorizedSettlementModule.selector);
        admission.settleConsumedRightRefund(commitment, recipient, 0.4 ether);
    }

    // -------------------------------------------------------------------------
    // AR-04 — Funded right rejected
    // -------------------------------------------------------------------------

    function testSettleConsumedRightRefund_RevertsIfRightNotConsumed_FundedState() public {
        bytes32 admissionSecret = bytes32(uint256(333));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.RightNotConsumed.selector);
        admission.settleConsumedRightRefund(commitment, recipient, 0.4 ether);
    }

    // -------------------------------------------------------------------------
    // AR-01 — authorized consumed-right payout succeeds
    // -------------------------------------------------------------------------

    function testSettleConsumedRightRefund_SucceedsForAuthorizedSettlementModule() public {
        bytes32 admissionSecret = bytes32(uint256(444));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(555));
        uint256 refundAmount = 0.4 ether;

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        uint256 recipientBefore = recipient.balance;

        vm.prank(settlementModule);
        admission.settleConsumedRightRefund(commitment, recipient, refundAmount);

        assertEq(recipient.balance, recipientBefore + refundAmount, "recipient should receive payout");
        assertTrue(admission.consumedRefundPaid(commitment), "consumed refund should be marked paid");
    }

    // -------------------------------------------------------------------------
    // AR-06 — consumed refund already paid rejected
    // -------------------------------------------------------------------------

    function testSettleConsumedRightRefund_RevertsIfConsumedRefundAlreadyPaid() public {
        bytes32 admissionSecret = bytes32(uint256(666));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(777));
        uint256 refundAmount = 0.4 ether;

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(settlementModule);
        admission.settleConsumedRightRefund(commitment, recipient, refundAmount);

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.ConsumedRefundAlreadyPaid.selector);
        admission.settleConsumedRightRefund(commitment, recipient, refundAmount);
    }

    // -------------------------------------------------------------------------
    // Extra narrow guards worth having in this file
    // -------------------------------------------------------------------------

    function testSettleConsumedRightRefund_RevertsIfRightDoesNotExist() public {
        bytes32 nonexistentCommitment = bytes32(uint256(999));

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.RightNotConsumed.selector);
        admission.settleConsumedRightRefund(nonexistentCommitment, recipient, 0.4 ether);
    }

    function testSettleConsumedRightRefund_RevertsIfRightAlreadyRefunded() public {
        bytes32 admissionSecret = bytes32(uint256(1234));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        vm.warp(block.timestamp + LOCK_PERIOD + 1);

        vm.prank(user);
        admission.refundAdmissionRight(admissionSecret, recipient);

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.RightNotConsumed.selector);
        admission.settleConsumedRightRefund(commitment, recipient, 0.4 ether);
    }

    function testSettleConsumedRightRefund_RevertsForZeroAmount() public {
        bytes32 admissionSecret = bytes32(uint256(888));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(889));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.InvalidRefundAmount.selector);
        admission.settleConsumedRightRefund(commitment, recipient, 0);
    }

    function testSettleConsumedRightRefund_RevertsIfAmountExceedsBond() public {
        bytes32 admissionSecret = bytes32(uint256(990));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(991));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(settlementModule);
        vm.expectRevert(AdmissionRegistry.InvalidRefundAmount.selector);
        admission.settleConsumedRightRefund(commitment, recipient, BOND + 1);
    }
}