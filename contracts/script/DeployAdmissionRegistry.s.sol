// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";

contract DeployAdmissionRegistry is Script {
    function run()
        external
        returns (
            address logicAddr,
            address proxyAddr,
            address proxyAdminAddr
        )
    {
        address owner = vm.envAddress("OWNER_ADDRESS");
        address anonymousMembershipRegistry = vm.envAddress("ANON_MEMBERSHIP_PROXY_ADDRESS");
        address admissionHasher = vm.envAddress("POSEIDON1_ADDRESS");
        uint256 admissionBond = vm.envUint("ADMISSION_BOND_WEI");
        uint256 lockPeriod = vm.envUint("ADMISSION_LOCK_SECONDS");

        vm.startBroadcast();

        AdmissionRegistry logic = new AdmissionRegistry();

        bytes memory initData = abi.encodeCall(
            AdmissionRegistry.initialize,
            (owner, anonymousMembershipRegistry, admissionHasher, admissionBond, lockPeriod)
        );

        TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
            address(logic),
            owner,
            initData
        );

        vm.stopBroadcast();

        logicAddr = address(logic);
        proxyAddr = address(proxy);

        bytes32 adminSlot = bytes32(uint256(keccak256("eip1967.proxy.admin")) - 1);
        proxyAdminAddr = address(uint160(uint256(vm.load(proxyAddr, adminSlot))));

        AdmissionRegistry instance = AdmissionRegistry(proxyAddr);

        console2.log("AdmissionRegistry logic:", logicAddr);
        console2.log("AdmissionRegistry proxy:", proxyAddr);
        console2.log("AdmissionRegistry proxy admin:", proxyAdminAddr);
        console2.log("Owner:", instance.owner());
        console2.log("AnonymousMembershipRegistry:", instance.anonymousMembershipRegistry());
        console2.log("AdmissionHasher:", instance.admissionHasher());
        console2.log("AdmissionBond:", instance.admissionBond());
        console2.log("LockPeriod:", instance.lockPeriod());
    }
}