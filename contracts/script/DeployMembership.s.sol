// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";
import "forge-std/console2.sol";

import {Poseidon2} from "../src/poseidon/Poseidon2.sol";
import {MembershipRegistry} from "../src/MembershipRegistry.sol";

contract DeployMembership is Script {
    function run() external {
        // Pull params from env (so the script is reusable/atomic)
        uint256 bondWei = vm.envUint("MEMBERSHIP_REGISTER_BOND_WEI");
        uint64 lockSeconds = uint64(vm.envUint("MEMBERSHIP_BOND_LOCK_SECONDS"));

        vm.startBroadcast();

        Poseidon2 hasher = new Poseidon2();
        MembershipRegistry reg = new MembershipRegistry(address(hasher), bondWei, lockSeconds);

        vm.stopBroadcast();

        console2.log("Poseidon2:", address(hasher));
        console2.log("MembershipRegistry:", address(reg));
        console2.log("BondWei:", bondWei);
        console2.log("LockSeconds:", lockSeconds);
    }
}

