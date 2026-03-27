// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {AnonymousMembershipRegistry} from "../src/AnonymousMembershipRegistry.sol";

contract DeployAnonymousMembershipRegistry is Script {
    function run()
        external
        returns (
            address logicAddr,
            address proxyAddr,
            address proxyAdminAddr
        )
    {
        address owner = vm.envAddress("OWNER_ADDRESS");
        address poseidon2 = vm.envAddress("POSEIDON2_ADDRESS");

        vm.startBroadcast();

        AnonymousMembershipRegistry logic = new AnonymousMembershipRegistry();

        bytes memory initData = abi.encodeCall(
            AnonymousMembershipRegistry.initialize,
            (owner, poseidon2)
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

        AnonymousMembershipRegistry instance = AnonymousMembershipRegistry(proxyAddr);

        console2.log("AnonymousMembershipRegistry logic:", logicAddr);
        console2.log("AnonymousMembershipRegistry proxy:", proxyAddr);
        console2.log("AnonymousMembershipRegistry proxy admin:", proxyAdminAddr);
        console2.log("Owner:", instance.owner());
        console2.log("Hasher:", instance.hasher());
        console2.log("AdmissionRegistry:", instance.admissionRegistry());
    }
}