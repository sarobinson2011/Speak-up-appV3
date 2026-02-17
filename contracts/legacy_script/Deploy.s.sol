// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script} from "forge-std/Script.sol";
import {console} from "forge-std/console.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {PetitionRegistry} from "../src/PetitionRegistry.sol";
import {AttestationAuthorizer} from "../src/AttestationAuthorizer.sol";
import {ZKAuthorizer} from "../src/ZKAuthorizer.sol";

contract DeployV3 is Script {
    function run() external {
        address attester = vm.envAddress("ATTESTER_ADDRESS");

        console.log("=== Deploying Speak-Up V3 (UUPS Upgradeable) ===");
        console.log("Deployer:", msg.sender);
        console.log("Attester:", attester);
        console.log("Chain ID:", block.chainid);

        vm.startBroadcast();

        // 1. Deploy AttestationAuthorizer implementation
        console.log("\n--- Deploying AttestationAuthorizer Implementation ---");
        AttestationAuthorizer authorizerImpl = new AttestationAuthorizer();
        console.log("AttestationAuthorizer Implementation:", address(authorizerImpl));

        // 2. Deploy PetitionRegistry implementation
        console.log("\n--- Deploying PetitionRegistry Implementation ---");
        PetitionRegistry registryImpl = new PetitionRegistry();
        console.log("PetitionRegistry Implementation:", address(registryImpl));

        // 3. Deploy PetitionRegistry Proxy (with placeholder authorizer)
        console.log("\n--- Deploying PetitionRegistry Proxy ---");
        bytes memory registryInitData = abi.encodeWithSelector(
            PetitionRegistry.initialize.selector,
            address(1) // Placeholder authorizer
        );
        ERC1967Proxy registryProxy = new ERC1967Proxy(
            address(registryImpl),
            registryInitData
        );
        console.log("PetitionRegistry Proxy:", address(registryProxy));

        // 4. Deploy AttestationAuthorizer Proxy
        console.log("\n--- Deploying AttestationAuthorizer Proxy ---");
        bytes memory authorizerInitData = abi.encodeWithSelector(
            AttestationAuthorizer.initialize.selector,
            attester,
            address(registryProxy) // EIP-712 verifying contract
        );
        ERC1967Proxy authorizerProxy = new ERC1967Proxy(
            address(authorizerImpl),
            authorizerInitData
        );
        console.log("AttestationAuthorizer Proxy:", address(authorizerProxy));

        // 5. Set the authorizer on the registry
        console.log("\n--- Setting Authorizer ---");
        PetitionRegistry registry = PetitionRegistry(address(registryProxy));
        registry.setAuthorizer(address(authorizerProxy));
        console.log("Authorizer set successfully");

        vm.stopBroadcast();

        // Print deployment summary
        console.log("\n=== DEPLOYMENT SUMMARY ===");
        console.log("PetitionRegistry Proxy:", address(registryProxy));
        console.log("PetitionRegistry Implementation:", address(registryImpl));
        console.log("AttestationAuthorizer Proxy:", address(authorizerProxy));
        console.log("AttestationAuthorizer Implementation:", address(authorizerImpl));
        console.log("Owner (Deployer):", msg.sender);
        console.log("Attester:", attester);
        
        console.log("\n=== ADD TO .env ===");
        console.log("REGISTRY_PROXY=", address(registryProxy));
        console.log("REGISTRY_IMPL=", address(registryImpl));
        console.log("AUTHORIZER_PROXY=", address(authorizerProxy));
        console.log("AUTHORIZER_IMPL=", address(authorizerImpl));
    }
}

contract UpgradePetitionRegistry is Script {
    function run() external {
        address proxyAddress = vm.envAddress("REGISTRY_PROXY");

        console.log("=== Upgrading PetitionRegistry ===");
        console.log("Proxy:", proxyAddress);

        vm.startBroadcast();

        PetitionRegistry newImpl = new PetitionRegistry();
        console.log("New Implementation:", address(newImpl));

        PetitionRegistry registry = PetitionRegistry(proxyAddress);
        registry.upgradeToAndCall(address(newImpl), "");
        
        console.log("Upgrade complete!");

        vm.stopBroadcast();
    }
}

contract DeployZKAuthorizer is Script {
    function run() external {
        address verifier = vm.envAddress("VERIFIER_ADDRESS");

        console.log("=== Deploying ZKAuthorizer (UUPS) ===");
        console.log("Verifier:", verifier);

        vm.startBroadcast();

        ZKAuthorizer zkAuthImpl = new ZKAuthorizer();
        console.log("ZKAuthorizer Implementation:", address(zkAuthImpl));

        bytes memory initData = abi.encodeWithSelector(
            ZKAuthorizer.initialize.selector,
            verifier
        );
        ERC1967Proxy zkAuthProxy = new ERC1967Proxy(
            address(zkAuthImpl),
            initData
        );
        console.log("ZKAuthorizer Proxy:", address(zkAuthProxy));

        vm.stopBroadcast();

        console.log("\n=== UPGRADE TO ZK MODE ===");
        console.log("When ready, call:");
        console.log("registry.setAuthorizer(", address(zkAuthProxy), ")");
    }
}