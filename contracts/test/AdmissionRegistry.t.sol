// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";
import {Poseidon1} from "../src/poseidon/Poseidon1.sol";
import {IPoseidon1} from "../src/poseidon/IPoseidon1.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";

contract AdmissionRegistryTest is Test {
    AdmissionRegistry internal admission;
    AnonymousMembershipRegistry internal anon;
    Poseidon1 internal poseidon1;
    Poseidon2 internal poseidon2;

    address internal owner = address(this);
    address internal user = address(0xBEEF);
    address internal recipient = address(0xCAFE);

    uint256 internal constant BOND = 1 ether;
    uint256 internal constant LOCK_PERIOD = 7 days;

    function setUp() public {
        poseidon1 = new Poseidon1();
        poseidon2 = new Poseidon2();

        anon = new AnonymousMembershipRegistry();
        anon.initialize(owner, address(poseidon2));

        admission = new AdmissionRegistry();
        admission.initialize(owner, address(anon), address(poseidon1), BOND, LOCK_PERIOD);

        anon.setAdmissionRegistry(address(admission));

        vm.deal(user, 10 ether);
    }

    function _commit(bytes32 secret) internal view returns (bytes32) {
        uint256[1] memory input = [uint256(secret)];
        uint256 out = IPoseidon1(address(poseidon1)).poseidon(input);
        return bytes32(out);
    }

    function testFundAdmissionRight_Succeeds() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        (
            uint256 amount,
            uint256 fundedAt,
            uint256 unlockAt,
            uint8 status
        ) = admission.rights(commitment);

        assertEq(amount, BOND);
        assertGt(fundedAt, 0);
        assertEq(unlockAt, fundedAt + LOCK_PERIOD);
        assertEq(status, uint8(AdmissionRegistry.Status.Funded));
    }

    function testFundAdmissionRight_RevertsWrongBond() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);

        vm.prank(user);
        vm.expectRevert(AdmissionRegistry.InvalidBondAmount.selector);
        admission.fundAdmissionRight{value: 0.5 ether}(commitment);
    }

    function testFundAdmissionRight_RevertsDuplicate() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);

        vm.startPrank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        vm.expectRevert(AdmissionRegistry.RightAlreadyExists.selector);
        admission.fundAdmissionRight{value: BOND}(commitment);
        vm.stopPrank();
    }

    function testActivateMembership_Succeeds() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        admission.activateMembership(commitment, admissionSecret, leaf);

        (, , , uint8 status) = admission.rights(commitment);
        assertEq(status, uint8(AdmissionRegistry.Status.Consumed));
        assertTrue(anon.knownLeaves(leaf));
        assertEq(anon.leafCount(), 1);
    }

    function testActivateMembership_RevertsWrongSecret() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 wrongSecret = bytes32(uint256(999));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        vm.expectRevert(AdmissionRegistry.SecretDoesNotMatchCommitment.selector);
        admission.activateMembership(commitment, wrongSecret, leaf);
    }

    function testActivateMembership_RevertsDuplicateLeaf() public {
        bytes32 secret1 = bytes32(uint256(111));
        bytes32 secret2 = bytes32(uint256(112));
        bytes32 commitment1 = _commit(secret1);
        bytes32 commitment2 = _commit(secret2);
        bytes32 leaf = bytes32(uint256(222));

        vm.startPrank(user);
        admission.fundAdmissionRight{value: BOND}(commitment1);
        admission.fundAdmissionRight{value: BOND}(commitment2);
        vm.stopPrank();

        admission.activateMembership(commitment1, secret1, leaf);

        vm.expectRevert(AdmissionRegistry.LeafAlreadyRegistered.selector);
        admission.activateMembership(commitment2, secret2, leaf);
    }

    function testRefundAdmissionRight_SucceedsAfterUnlock() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        uint256 beforeBal = recipient.balance;

        vm.warp(block.timestamp + LOCK_PERIOD);

        admission.refundAdmissionRight(secret, recipient);

        (, , , uint8 status) = admission.rights(commitment);

        assertEq(status, uint8(AdmissionRegistry.Status.Refunded));
        assertEq(recipient.balance, beforeBal + BOND);
    }

    function testRefundAdmissionRight_RevertsTooEarly() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        vm.expectRevert(AdmissionRegistry.RefundTooEarly.selector);
        admission.refundAdmissionRight(secret, recipient);
    }

    function testRefundAdmissionRight_RevertsAfterActivation() public {
        bytes32 secret = bytes32(uint256(111));
        bytes32 commitment = _commit(secret);
        bytes32 leaf = bytes32(uint256(222));

        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);

        admission.activateMembership(commitment, secret, leaf);

        vm.warp(block.timestamp + LOCK_PERIOD);

        vm.expectRevert(AdmissionRegistry.RightNotFunded.selector);
        admission.refundAdmissionRight(secret, recipient);
    }

function testSetAdmissionBond_RevertsForNonOwner() public {
    vm.prank(user);
    vm.expectRevert();
    admission.setAdmissionBond(2 ether);
}

function testSetAdmissionBond_RevertsForZero() public {
    vm.expectRevert(AdmissionRegistry.InvalidBondAmount.selector);
    admission.setAdmissionBond(0);
}

function testSetAdmissionBond_Succeeds() public {
    uint256 newBond = 2 ether;

    admission.setAdmissionBond(newBond);

    assertEq(admission.admissionBond(), newBond);
}

function testSetAdmissionBond_AffectsOnlyFutureRights() public {
    bytes32 secret1 = bytes32(uint256(111));
    bytes32 secret2 = bytes32(uint256(222));
    bytes32 commitment1 = _commit(secret1);
    bytes32 commitment2 = _commit(secret2);

    uint256 oldBond = BOND;
    uint256 newBond = 2 ether;

    vm.prank(user);
    admission.fundAdmissionRight{value: oldBond}(commitment1);

    admission.setAdmissionBond(newBond);

    vm.prank(user);
    admission.fundAdmissionRight{value: newBond}(commitment2);

    (uint256 amount1,,,) = admission.rights(commitment1);
    (uint256 amount2,,,) = admission.rights(commitment2);

    assertEq(amount1, oldBond);
    assertEq(amount2, newBond);
}

function testSetLockPeriod_RevertsForNonOwner() public {
    vm.prank(user);
    vm.expectRevert();
    admission.setLockPeriod(1 days);
}

function testSetLockPeriod_RevertsForZero() public {
    vm.expectRevert(AdmissionRegistry.InvalidLockPeriod.selector);
    admission.setLockPeriod(0);
}

function testSetLockPeriod_Succeeds() public {
    uint256 newLockPeriod = 3 days;

    admission.setLockPeriod(newLockPeriod);

    assertEq(admission.lockPeriod(), newLockPeriod);
}

function testSetLockPeriod_AffectsOnlyFutureRights() public {
    bytes32 secret1 = bytes32(uint256(111));
    bytes32 secret2 = bytes32(uint256(222));
    bytes32 commitment1 = _commit(secret1);
    bytes32 commitment2 = _commit(secret2);

    uint256 oldLockPeriod = LOCK_PERIOD;
    uint256 newLockPeriod = 3 days;

    vm.prank(user);
    admission.fundAdmissionRight{value: BOND}(commitment1);

    (, uint256 fundedAt1, uint256 unlockAt1,) = admission.rights(commitment1);
    assertEq(unlockAt1, fundedAt1 + oldLockPeriod);

    admission.setLockPeriod(newLockPeriod);

    vm.prank(user);
    admission.fundAdmissionRight{value: BOND}(commitment2);

    (, uint256 fundedAt2, uint256 unlockAt2,) = admission.rights(commitment2);
    assertEq(unlockAt2, fundedAt2 + newLockPeriod);

    (, , uint256 unlockAt1After,) = admission.rights(commitment1);
    assertEq(unlockAt1After, unlockAt1);
}

}