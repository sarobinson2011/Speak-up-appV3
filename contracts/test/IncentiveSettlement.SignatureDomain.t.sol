// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {IncentiveSettlement} from "../src/IncentiveSettlement.sol";

contract MockPoseidon1_SIG {
    function poseidon(uint256[1] memory input) external pure returns (uint256) {
        return input[0];
    }
}

contract MockAnonymousMembershipRegistry_SIG {
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

contract IncentiveSettlementSignatureDomainTest is Test {
    AdmissionRegistry internal admission;
    IncentiveSettlement internal settlement;
    MockPoseidon1_SIG internal poseidon1;
    MockAnonymousMembershipRegistry_SIG internal anon;

    uint256 internal signerPk = 0xA11CE;
    uint256 internal signer2Pk = 0xB11CE;

    address internal signer;
    address internal signer2;
    address internal owner = address(0xB0B);
    address internal user = address(0xC0DE);

    uint256 internal constant BOND = 1 ether;
    uint256 internal constant LOCK_PERIOD = 7 days;

    function setUp() public {
        signer = vm.addr(signerPk);
        signer2 = vm.addr(signer2Pk);

        poseidon1 = new MockPoseidon1_SIG();
        anon = new MockAnonymousMembershipRegistry_SIG();

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

    function _signBandWithPk(
        uint256 pk,
        bytes32 admissionCommitment,
        IncentiveSettlement.RefundBand band
    ) internal view returns (bytes memory) {
        bytes32 digest = settlement.bandAssignmentDigest(admissionCommitment, band);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(pk, digest);
        return abi.encodePacked(r, s, v);
    }

    function testSignatureDomain_SignatureValidOnlyForExactCommitmentAndBand() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBandWithPk(
            signerPk,
            commitment,
            IncentiveSettlement.RefundBand.Enhanced
        );

        // Same consumed commitment, wrong band => signature mismatch
        vm.expectRevert(IncentiveSettlement.InvalidSignature.selector);
        settlement.submitRefundBand(
            commitment,
            IncentiveSettlement.RefundBand.Standard,
            sig
        );

        // Different consumed commitment, signature from first commitment => signature mismatch
        bytes32 admissionSecret2 = bytes32(uint256(333));
        bytes32 commitment2 = _commit(admissionSecret2);
        bytes32 leaf2 = bytes32(uint256(444));

        _fund(commitment2);
        _consume(commitment2, admissionSecret2, leaf2);

        vm.expectRevert(IncentiveSettlement.InvalidSignature.selector);
        settlement.submitRefundBand(
            commitment2,
            IncentiveSettlement.RefundBand.Enhanced,
            sig
        );
    }

    function testSignatureDomain_ReplayRejectedAfterBandAssignment() public {
        bytes32 admissionSecret = bytes32(uint256(333));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(444));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        bytes memory sig = _signBandWithPk(
            signerPk,
            commitment,
            IncentiveSettlement.RefundBand.Enhanced
        );

        settlement.submitRefundBand(
            commitment,
            IncentiveSettlement.RefundBand.Enhanced,
            sig
        );

        vm.expectRevert(IncentiveSettlement.BandAlreadyAssigned.selector);
        settlement.submitRefundBand(
            commitment,
            IncentiveSettlement.RefundBand.Enhanced,
            sig
        );
    }

    function testSignatureDomain_OldSignerRejectedAfterRotation() public {
        bytes32 admissionSecret = bytes32(uint256(555));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(666));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(owner);
        settlement.setPolicySigner(signer2);

        bytes memory oldSig = _signBandWithPk(
            signerPk,
            commitment,
            IncentiveSettlement.RefundBand.Standard
        );

        vm.expectRevert(IncentiveSettlement.InvalidSignature.selector);
        settlement.submitRefundBand(
            commitment,
            IncentiveSettlement.RefundBand.Standard,
            oldSig
        );
    }

    function testSignatureDomain_NewSignerAcceptedAfterRotation() public {
        bytes32 admissionSecret = bytes32(uint256(777));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(888));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(owner);
        settlement.setPolicySigner(signer2);

        bytes memory newSig = _signBandWithPk(
            signer2Pk,
            commitment,
            IncentiveSettlement.RefundBand.Standard
        );

        settlement.submitRefundBand(
            commitment,
            IncentiveSettlement.RefundBand.Standard,
            newSig
        );

        assertEq(
            uint8(settlement.refundBandOf(commitment)),
            uint8(IncentiveSettlement.RefundBand.Standard)
        );
        assertTrue(settlement.isBandAssigned(commitment));
    }
}