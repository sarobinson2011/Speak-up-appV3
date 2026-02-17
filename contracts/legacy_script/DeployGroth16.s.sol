// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script} from "forge-std/Script.sol";
import {console} from "forge-std/console.sol";
import {Groth16Verifier} from "../src/v3/Groth16Verifier.sol";
import {Groth16VerifierTest} from "../src/v3/Groth16VerifierTest.sol";

contract DeployGroth16 is Script {
    function run() external {
        console.log("=== Deploying V3 Groth16 Verifier ===");
        console.log("Deployer:", msg.sender);
        console.log("Chain ID:", block.chainid);
        
        vm.startBroadcast();
        
        // 1. Deploy Groth16Verifier
        console.log("\n--- Deploying Groth16Verifier ---");
        Groth16Verifier verifier = new Groth16Verifier();
        console.log("Groth16Verifier:", address(verifier));
        
        // 2. Deploy test contract
        console.log("\n--- Deploying Groth16VerifierTest ---");
        Groth16VerifierTest testContract = new Groth16VerifierTest(address(verifier));
        console.log("Groth16VerifierTest:", address(testContract));
        
        vm.stopBroadcast();
        
        console.log("\n=== Deployment Complete ===");
        console.log("Verifier:     ", address(verifier));
        console.log("Test Contract:", address(testContract));
    }
}
