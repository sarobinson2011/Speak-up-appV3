// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {IncentiveSettlement} from "../src/IncentiveSettlement.sol";

contract IncentiveSettlementAdminTest is Test {
    IncentiveSettlement internal settlement;

    address internal owner = address(0xA11CE);
    address internal nonOwner = address(0xB0B);
    address internal signer = address(0xC0DE);
    address internal signer2 = address(0xC0DF);
    address internal registry = address(0xD00D);
    address internal registry2 = address(0xD00E);

    uint256 internal constant REDUCED = 0.25 ether;
    uint256 internal constant STANDARD = 0.50 ether;
    uint256 internal constant ENHANCED = 0.75 ether;

    function setUp() public {
        settlement = new IncentiveSettlement();
        settlement.initialize(owner);
    }

    // ============================================================
    // policy signer
    // ============================================================

    function testSetPolicySigner_RevertsForNonOwner() public {
        vm.prank(nonOwner);
        vm.expectRevert();
        settlement.setPolicySigner(signer);
    }

    function testSetPolicySigner_RevertsForZeroAddress() public {
        vm.prank(owner);
        vm.expectRevert(IncentiveSettlement.ZeroAddress.selector);
        settlement.setPolicySigner(address(0));
    }

    function testSetPolicySigner_Succeeds() public {
        vm.prank(owner);
        settlement.setPolicySigner(signer);

        assertEq(settlement.policySigner(), signer, "policy signer should be updated");
    }

    function testSetPolicySigner_CanRotate() public {
        vm.startPrank(owner);
        settlement.setPolicySigner(signer);
        settlement.setPolicySigner(signer2);
        vm.stopPrank();

        assertEq(settlement.policySigner(), signer2, "policy signer should rotate");
    }

    // ============================================================
    // admission registry
    // ============================================================

    function testSetAdmissionRegistry_RevertsForNonOwner() public {
        vm.prank(nonOwner);
        vm.expectRevert();
        settlement.setAdmissionRegistry(registry);
    }

    function testSetAdmissionRegistry_RevertsForZeroAddress() public {
        vm.prank(owner);
        vm.expectRevert(IncentiveSettlement.ZeroAddress.selector);
        settlement.setAdmissionRegistry(address(0));
    }

    function testSetAdmissionRegistry_Succeeds() public {
        vm.prank(owner);
        settlement.setAdmissionRegistry(registry);

        assertEq(settlement.admissionRegistry(), registry, "registry should be updated");
    }

    function testSetAdmissionRegistry_CanRotate() public {
        vm.startPrank(owner);
        settlement.setAdmissionRegistry(registry);
        settlement.setAdmissionRegistry(registry2);
        vm.stopPrank();

        assertEq(settlement.admissionRegistry(), registry2, "registry should rotate");
    }

    // ============================================================
    // refund schedule
    // ============================================================

    function testSetRefundSchedule_RevertsForNonOwner() public {
        vm.prank(nonOwner);
        vm.expectRevert();
        settlement.setRefundSchedule(REDUCED, STANDARD, ENHANCED);
    }

    function testSetRefundSchedule_RevertsIfReducedGreaterThanStandard() public {
        vm.prank(owner);
        vm.expectRevert(IncentiveSettlement.InvalidRefundSchedule.selector);
        settlement.setRefundSchedule(0.60 ether, 0.50 ether, 0.75 ether);
    }

    function testSetRefundSchedule_RevertsIfStandardGreaterThanEnhanced() public {
        vm.prank(owner);
        vm.expectRevert(IncentiveSettlement.InvalidRefundSchedule.selector);
        settlement.setRefundSchedule(0.25 ether, 0.80 ether, 0.75 ether);
    }

    function testSetRefundSchedule_RevertsIfEnhancedExceedsMaxRefund() public {
        vm.prank(owner);
        vm.expectRevert(IncentiveSettlement.InvalidRefundSchedule.selector);
        settlement.setRefundSchedule(0.25 ether, 0.50 ether, 1.01 ether);
    }

    function testSetRefundSchedule_Succeeds() public {
        vm.prank(owner);
        settlement.setRefundSchedule(REDUCED, STANDARD, ENHANCED);

        assertEq(settlement.reducedRefundAmount(), REDUCED, "reduced refund mismatch");
        assertEq(settlement.standardRefundAmount(), STANDARD, "standard refund mismatch");
        assertEq(settlement.enhancedRefundAmount(), ENHANCED, "enhanced refund mismatch");
    }

    function testSetRefundSchedule_AllowsEqualityBetweenBands() public {
        vm.prank(owner);
        settlement.setRefundSchedule(0.50 ether, 0.50 ether, 0.50 ether);

        assertEq(settlement.reducedRefundAmount(), 0.50 ether);
        assertEq(settlement.standardRefundAmount(), 0.50 ether);
        assertEq(settlement.enhancedRefundAmount(), 0.50 ether);
    }
}