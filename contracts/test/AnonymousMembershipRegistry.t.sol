// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";

contract AnonymousMembershipRegistryTest is Test {
    AnonymousMembershipRegistry internal registry;
    Poseidon2 internal poseidon2;

    address internal owner = address(this);
    address internal admission = address(0xA11CE);
    address internal outsider = address(0xBEEF);

    function setUp() public {
        poseidon2 = new Poseidon2();

        registry = new AnonymousMembershipRegistry();
        registry.initialize(owner, address(poseidon2));
        registry.setAdmissionRegistry(admission);
    }

    function testRegisterLeaf_Succeeds() public {
        bytes32 leaf = bytes32(uint256(123));

        vm.prank(admission);
        uint256 leafIndex = registry.registerLeaf(leaf);

        assertEq(leafIndex, 0);
        assertEq(registry.leafCount(), 1);
        assertTrue(registry.knownLeaves(leaf));
        assertEq(registry.leaves(0), leaf);
        assertTrue(registry.currentRoot() != bytes32(0));
    }

    function testRegisterLeaf_RevertsIfNotAdmissionRegistry() public {
        bytes32 leaf = bytes32(uint256(123));

        vm.prank(outsider);
        vm.expectRevert(AnonymousMembershipRegistry.NotAdmissionRegistry.selector);
        registry.registerLeaf(leaf);
    }

    function testRegisterLeaf_RevertsOnZeroLeaf() public {
        vm.prank(admission);
        vm.expectRevert(AnonymousMembershipRegistry.InvalidLeaf.selector);
        registry.registerLeaf(bytes32(0));
    }

    function testRegisterLeaf_RevertsOnDuplicateLeaf() public {
        bytes32 leaf = bytes32(uint256(123));

        vm.startPrank(admission);
        registry.registerLeaf(leaf);

        vm.expectRevert(AnonymousMembershipRegistry.LeafAlreadyRegistered.selector);
        registry.registerLeaf(leaf);
        vm.stopPrank();
    }

    function testRegisterLeaf_IncrementsLeafCount() public {
        bytes32 leaf1 = bytes32(uint256(123));
        bytes32 leaf2 = bytes32(uint256(456));

        vm.startPrank(admission);
        registry.registerLeaf(leaf1);
        registry.registerLeaf(leaf2);
        vm.stopPrank();

        assertEq(registry.leafCount(), 2);
        assertEq(registry.leaves(0), leaf1);
        assertEq(registry.leaves(1), leaf2);
    }

    function testSetAdmissionRegistry_RevertsForNonOwner() public {
        vm.prank(outsider);
        vm.expectRevert();
        registry.setAdmissionRegistry(address(0x9999));
    }

    function testSetAdmissionRegistry_RevertsOnZeroAddress() public {
        vm.expectRevert(AnonymousMembershipRegistry.ZeroAddress.selector);
        registry.setAdmissionRegistry(address(0));
    }

    function testSetAdmissionRegistry_Succeeds() public {
        address newAdmission = address(0x9999);

        registry.setAdmissionRegistry(newAdmission);

        assertEq(registry.admissionRegistry(), newAdmission);
    }
}