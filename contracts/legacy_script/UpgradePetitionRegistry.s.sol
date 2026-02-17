// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";
import "../src/PetitionRegistry.sol";
import "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract UpgradePetitionRegistry is Script {
    address constant PROXY = 0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD;

    function run() external {
        vm.startBroadcast();

        // Deploy new implementation
        PetitionRegistry newImpl = new PetitionRegistry();
        
        console.log("New Implementation:", address(newImpl));

        // Upgrade proxy to new implementation
        PetitionRegistry proxy = PetitionRegistry(PROXY);
        proxy.upgradeToAndCall(address(newImpl), "");

        console.log("Proxy upgraded successfully!");

        vm.stopBroadcast();
    }
}
