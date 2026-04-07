// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";
import {Poseidon1} from "../src/poseidon/Poseidon1.sol";
import {IPoseidon1} from "../src/poseidon/IPoseidon1.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";

contract AdmissionRegistryActionLinkingTest is Test {
    AdmissionRegistry internal admission;
    AnonymousMembershipRegistry internal anon;
    Poseidon1 internal poseidon1;
    Poseidon2 internal poseidon2;

    address internal owner = address(this);
    address internal user = address(0xBEEF);
    address internal petitionRegistry = address(0xABCD);

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
        admission.setPetitionRegistry(petitionRegistry);

        vm.deal(user, 10 ether);
    }

    function _commit(bytes32 secret) internal view returns (bytes32) {
        uint256[1] memory input = [uint256(secret)];
        uint256 out = IPoseidon1(address(poseidon1)).poseidon(input);
        return bytes32(out);
    }

    function _fund(bytes32 commitment) internal {
        vm.prank(user);
        admission.fundAdmissionRight{value: BOND}(commitment);
    }

    function _consume(bytes32 commitment, bytes32 admissionSecret, bytes32 leaf) internal {
        admission.activateMembership(commitment, admissionSecret, leaf);
    }

    function testRecordActionLink_SucceedsForConsumedRight() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(petitionRegistry);
        admission.recordActionLink(commitment);
    }

    function testRecordActionLink_RevertsIfAlreadyLinked() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(petitionRegistry);
        admission.recordActionLink(commitment);

        vm.prank(petitionRegistry);
        vm.expectRevert(AdmissionRegistry.RightAlreadyActionLinked.selector);
        admission.recordActionLink(commitment);
    }

    function testRecordActionLink_RevertsIfNotConsumed() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);

        _fund(commitment);

        vm.prank(petitionRegistry);
        vm.expectRevert(AdmissionRegistry.RightNotConsumed.selector);
        admission.recordActionLink(commitment);
    }

    function testRecordActionLink_RevertsIfRightNotFound() public {
        bytes32 commitment = bytes32(uint256(999));

        vm.prank(petitionRegistry);
        vm.expectRevert(AdmissionRegistry.RightNotFound.selector);
        admission.recordActionLink(commitment);
    }

    function testRecordActionLink_RevertsIfCallerNotPetitionRegistry() public {
        bytes32 admissionSecret = bytes32(uint256(111));
        bytes32 commitment = _commit(admissionSecret);
        bytes32 leaf = bytes32(uint256(222));

        _fund(commitment);
        _consume(commitment, admissionSecret, leaf);

        vm.prank(user);
        vm.expectRevert(AdmissionRegistry.NotPetitionRegistry.selector);
        admission.recordActionLink(commitment);
    }
}
