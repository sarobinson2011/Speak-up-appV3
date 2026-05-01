// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";
import "../src/PetitionRegistry.sol";

interface IUUPSUpgradeable {
    function upgradeToAndCall(address newImplementation, bytes memory data) external payable;
}

contract UpgradePetitionRegistry is Script {
    function run() external {
        address petitionProxy = vm.envAddress("PETITION_REGISTRY_ADDRESS");

        vm.startBroadcast();

        PetitionRegistry newImplementation = new PetitionRegistry();

        IUUPSUpgradeable(petitionProxy).upgradeToAndCall(
            address(newImplementation),
            bytes("")
        );

        vm.stopBroadcast();

        console2.log("PetitionRegistry proxy upgraded:", petitionProxy);
        console2.log("New PetitionRegistry implementation:", address(newImplementation));
    }
}
