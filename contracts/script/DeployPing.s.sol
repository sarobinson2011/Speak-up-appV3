// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {Ping} from "../src/Ping.sol";

contract DeployPing is Script {
    function run() external returns (address pingAddr) {
        vm.startBroadcast();

        Ping ping = new Ping();

        vm.stopBroadcast();

        pingAddr = address(ping);

        console2.log("Ping:", pingAddr);
    }
}
