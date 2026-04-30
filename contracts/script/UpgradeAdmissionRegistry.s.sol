// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {ProxyAdmin} from "@openzeppelin/contracts/proxy/transparent/ProxyAdmin.sol";
import {ITransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {AdmissionRegistry} from "../src/AdmissionRegistry.sol";

contract UpgradeAdmissionRegistry is Script {
    address constant ADMISSION_PROXY = 0x36c22227098B24E5aCE48dEa3988327256481F0e;
    address constant ADMISSION_PROXY_ADMIN = 0xBc2c8Fbb871530936C56E2Abcbc27F3B2da73BD8;

    function run() external returns (address logicAddr) {
        vm.startBroadcast();

        AdmissionRegistry logic = new AdmissionRegistry();
        logicAddr = address(logic);

        ProxyAdmin(ADMISSION_PROXY_ADMIN).upgradeAndCall(
            ITransparentUpgradeableProxy(payable(ADMISSION_PROXY)),
            logicAddr,
            bytes("")
        );

        vm.stopBroadcast();

        console2.log("AdmissionRegistry new logic:", logicAddr);
        console2.log("AdmissionRegistry proxy upgraded:", ADMISSION_PROXY);
    }
}
