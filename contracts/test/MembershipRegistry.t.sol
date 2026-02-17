// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";

import {MembershipRegistry} from "../src/MembershipRegistry.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";

contract MembershipRegistryTest is Test {
    MembershipRegistry reg;
    Poseidon2 hasher;

    address alice = address(0xA11CE);
    address bob = address(0xB0B);

    uint256 constant BOND = 0.01 ether;
    uint64 constant LOCK = 1 hours;

    function setUp() public {
        // Deploy poseidon hasher as you prefer (local deployment per env)
        hasher = new Poseidon2();

        // Deploy registry
        reg = new MembershipRegistry(address(hasher), BOND, LOCK);

        // Fund users
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
    }

    function test_registerLeaf_success_setsState_andEmitsRoot() public {
        uint256 leaf = _fakeLeaf(1);

        vm.prank(alice);
        (uint32 index, bytes32 newRoot) = reg.registerLeaf{value: BOND}(leaf);

        assertEq(index, 0, "first index should be 0");
        assertEq(reg.nextIndex(), 1, "nextIndex should advance");

        assertTrue(reg.isRegistered(alice), "alice should be registered");
        assertEq(reg.leafOf(alice), leaf, "leafOf should store leaf");

        // Root should be known
        assertTrue(reg.isKnownRoot(newRoot), "newRoot should be known");
        // And equal to currentRoot()
        assertEq(newRoot, reg.currentRoot(), "currentRoot mismatch");
    }

    function test_registerLeaf_requiresExactBond() public {
        uint256 leaf = _fakeLeaf(2);

        vm.prank(alice);
        vm.expectRevert(bytes("bad bond"));
        reg.registerLeaf{value: BOND - 1}(leaf);

        vm.prank(alice);
        vm.expectRevert(bytes("bad bond"));
        reg.registerLeaf{value: BOND + 1}(leaf);
    }

    function test_registerLeaf_rejectsSecondRegistrationSameWallet() public {
        uint256 leaf1 = _fakeLeaf(3);
        uint256 leaf2 = _fakeLeaf(4);

        vm.prank(alice);
        reg.registerLeaf{value: BOND}(leaf1);

        vm.prank(alice);
        vm.expectRevert(bytes("already registered"));
        reg.registerLeaf{value: BOND}(leaf2);
    }

    function test_withdrawBond_enforcesTimelock_thenRefunds() public {
        uint256 leaf = _fakeLeaf(5);

        vm.prank(alice);
        reg.registerLeaf{value: BOND}(leaf);

        // Still locked immediately
        vm.prank(alice);
        vm.expectRevert(bytes("still locked"));
        reg.withdrawBond();

        // Jump forward past lock
        vm.warp(block.timestamp + LOCK + 1);

        uint256 balBefore = alice.balance;

        vm.prank(alice);
        reg.withdrawBond();

        assertEq(alice.balance, balBefore + BOND, "refund not received");
        assertEq(reg.bonded(alice), 0, "bonded should reset");
        assertEq(reg.unlockAt(alice), 0, "unlockAt should reset");
    }

    function test_rootHistory_eviction_lastNRoots() public {
        // We want to prove that after enough inserts,
        // an old root is evicted from isKnownRoot.

        bytes32 root0 = reg.currentRoot();
        assertTrue(reg.isKnownRoot(root0), "initial root should be known");

        uint256 N = reg.ROOT_HISTORY_SIZE(); // constant getter exists
        // Insert N leaves (each insert pushes a root). After N inserts,
        // we have stored N+1 roots total; with eviction on each push,
        // the earliest root should be evicted at some point.
        for (uint256 i = 0; i < N; i++) {
            address user = address(uint160(0x1000 + i));
            vm.deal(user, 1 ether);

            vm.prank(user);
            reg.registerLeaf{value: BOND}(_fakeLeaf(100 + i));
        }

        // After enough pushes, root0 should be evicted
        assertFalse(reg.isKnownRoot(root0), "initial root should have been evicted");
        // Current root must still be known
        assertTrue(reg.isKnownRoot(reg.currentRoot()), "current root should be known");
    }

    // ---------- helpers ----------
    function _fakeLeaf(uint256 salt) internal pure returns (uint256) {
        // For contract testing, leaf just needs to be nonzero.
        // In the real system: leaf = Poseidon1(memberSecret).
        return uint256(keccak256(abi.encodePacked("leaf", salt))) | 1;
    }
}
