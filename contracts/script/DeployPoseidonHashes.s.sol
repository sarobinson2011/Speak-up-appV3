// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console2} from "forge-std/Script.sol";
import {Poseidon1} from "../src/poseidon/Poseidon1.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";

contract DeployPoseidonHashes is Script {
    function run() external returns (address poseidon1Addr, address poseidon2Addr) {
        vm.startBroadcast();

        Poseidon1 poseidon1 = new Poseidon1();
        Poseidon2 poseidon2 = new Poseidon2();

        vm.stopBroadcast();

        poseidon1Addr = address(poseidon1);
        poseidon2Addr = address(poseidon2);

        console2.log("Poseidon1:", poseidon1Addr);
        console2.log("Poseidon2:", poseidon2Addr);
    }
}