// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";

contract LinkAdmissionRegistry is Script {
    function run() external {
        address anonymousMembershipProxy = vm.envAddress("ANON_MEMBERSHIP_PROXY_ADDRESS");
        address admissionProxy = vm.envAddress("ADMISSION_PROXY_ADDRESS");

        vm.startBroadcast();

        AnonymousMembershipRegistry anon = AnonymousMembershipRegistry(anonymousMembershipProxy);
        anon.setAdmissionRegistry(admissionProxy);

        vm.stopBroadcast();

        console2.log("AnonymousMembershipRegistry proxy:", anonymousMembershipProxy);
        console2.log("AdmissionRegistry proxy set to:", anon.admissionRegistry());
    }
}