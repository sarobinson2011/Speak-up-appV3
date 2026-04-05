// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {IncentiveSettlement} from "../src/IncentiveSettlement.sol";

contract MockPoseidon1_BA {
    function poseidon(uint256[1] memory input) external pure returns (uint256) {
        return input[0];
    }
}

contract MockAnonymousMembershipRegistry_BA {
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

contract IncentiveSettlementBandAssignmentTest is Test {
    AdmissionRegistry internal admission;
    IncentiveSettlement internal settlement;
    MockPoseidon1_BA internal poseidon1;
    MockAnonymousMembershipRegistry_BA internal anon;

    uint256 internal signerPk = 0xA11CE;
    address internal signer;
    address internal owner = address(0xB0B);
    address internal user = address(0xC0DE);

    uint256 internal constant BOND = 1 ether;
    uint256 internal constant LOCK_PERIOD = 7 days;

    function setUp() public {
        signer = vm.addr(signerPk);

        poseidon1 = new MockPoseidon1_BA();
        anon = new MockAnonymousMembershipRegistry_BA();

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
        settlement.setRefundSchedule(0.25 ether, 0.50 ether, 0.75 ether);
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

    // ============================================================
    // Reverts
    // ============================================================

    function testSubmitRefundBand_RevertsForUnsetBand() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Unset);

        vm.expectRevert(IncentiveSettlement.InvalidBand.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Unset, sig);
    }

    function testSubmitRefundBand_RevertsIfRightNotConsumed_FundedState() public {
        bytes32 admissionSecret = bytes32(uint256(333));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        vm.expectRevert(IncentiveSettlement.RightNotConsumed.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);
    }

    function testSubmitRefundBand_RevertsForInvalidSignature() public {
        bytes32 admissionSecret = bytes32(uint256(444));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(555));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes32 digest = settlement.bandAssignmentDigest(commitment, IncentiveSettlement.RefundBand.Enhanced);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0xBAD, digest);
        bytes memory sig = abi.encodePacked(r, s, v);

        vm.expectRevert(IncentiveSettlement.InvalidSignature.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);
    }

    function testSubmitRefundBand_RevertsIfAlreadyAssigned() public {
        bytes32 admissionSecret = bytes32(uint256(666));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(777));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);

        vm.expectRevert(IncentiveSettlement.BandAlreadyAssigned.selector);
        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);
    }

    function testSubmitRefundBand_RevertsIfRegistryNotConfigured() public {
        IncentiveSettlement other = new IncentiveSettlement();
        other.initialize(owner);

        vm.prank(owner);
        other.setPolicySigner(signer);

        bytes32 commitment = bytes32(uint256(999));
        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        vm.expectRevert(IncentiveSettlement.AdmissionRegistryNotSet.selector);
        other.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);
    }

    // ============================================================
    // Success
    // ============================================================

    function testSubmitRefundBand_AssignsReducedBand() public {
        bytes32 admissionSecret = bytes32(uint256(1001));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(1002));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Reduced);

        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Reduced, sig);

        assertEq(uint8(settlement.refundBandOf(commitment)), uint8(IncentiveSettlement.RefundBand.Reduced));
        assertTrue(settlement.isBandAssigned(commitment));
    }

    function testSubmitRefundBand_AssignsStandardBand() public {
        bytes32 admissionSecret = bytes32(uint256(1003));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(1004));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Standard);

        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Standard, sig);

        assertEq(uint8(settlement.refundBandOf(commitment)), uint8(IncentiveSettlement.RefundBand.Standard));
        assertTrue(settlement.isBandAssigned(commitment));
    }

    function testSubmitRefundBand_AssignsEnhancedBand() public {
        bytes32 admissionSecret = bytes32(uint256(1005));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(1006));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBand(commitment, IncentiveSettlement.RefundBand.Enhanced);

        settlement.submitRefundBand(commitment, IncentiveSettlement.RefundBand.Enhanced, sig);

        assertEq(uint8(settlement.refundBandOf(commitment)), uint8(IncentiveSettlement.RefundBand.Enhanced));
        assertTrue(settlement.isBandAssigned(commitment));
    }
}