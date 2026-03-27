// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";
import {IPoseidon1} from "../src/poseidon/IPoseidon1.sol";

contract SmokeAdmissionFlow is Script {
    function _commit(address poseidon1, bytes32 secret) internal pure returns (bytes32) {
        uint256[1] memory input = [uint256(secret)];
        return bytes32(IPoseidon1(poseidon1).poseidon(input));
    }

    function _logBytes32(string memory label, bytes32 value) internal pure {
        console2.log(label);
        console2.logBytes32(value);
    }

    function run() external {
        address admissionProxy = vm.envAddress("ADMISSION_PROXY_ADDRESS");
        address anonProxy = vm.envAddress("ANON_MEMBERSHIP_PROXY_ADDRESS");
        address poseidon1 = vm.envAddress("POSEIDON1_ADDRESS");
        uint256 bond = vm.envUint("ADMISSION_BOND_WEI");
        uint256 lockSeconds = vm.envUint("ADMISSION_LOCK_SECONDS");

        AdmissionRegistry admission = AdmissionRegistry(admissionProxy);
        AnonymousMembershipRegistry anon = AnonymousMembershipRegistry(anonProxy);

        bytes32 admissionSecret1 = bytes32(uint256(111));
        bytes32 admissionSecret2 = bytes32(uint256(222));
        bytes32 leaf = bytes32(uint256(444));

        bytes32 commitment1 = _commit(poseidon1, admissionSecret1);
        bytes32 commitment2 = _commit(poseidon1, admissionSecret2);

        console2.log("Admission proxy:", admissionProxy);
        console2.log("Anonymous proxy:", anonProxy);
        _logBytes32("Commitment1:", commitment1);
        _logBytes32("Commitment2:", commitment2);
        _logBytes32("Leaf:", leaf);

        vm.startBroadcast();
        admission.fundAdmissionRight{value: bond}(commitment1);
        admission.activateMembership(commitment1, admissionSecret1, leaf);
        vm.stopBroadcast();

        console2.log("Leaf count after activation:", anon.leafCount());
        _logBytes32("Current root after activation:", anon.currentRoot());

        try admission.refundAdmissionRight(admissionSecret1, msg.sender) {
            revert("expected refund-after-activation to revert");
        } catch {
            console2.log("Refund after activation correctly reverted");
        }

        vm.startBroadcast();
        admission.fundAdmissionRight{value: bond}(commitment2);
        vm.stopBroadcast();

        vm.warp(block.timestamp + lockSeconds);

        uint256 beforeBal = msg.sender.balance;

        vm.startBroadcast();
        admission.refundAdmissionRight(admissionSecret2, msg.sender);
        vm.stopBroadcast();

        uint256 afterBal = msg.sender.balance;

        console2.log("Refund path executed for unused right");
        console2.log("Balance increased:", afterBal > beforeBal);
    }
}