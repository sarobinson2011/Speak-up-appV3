// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";

interface IAdmissionRegistry {
    function fundAdmissionRight(bytes32 admissionCommitment) external payable;

    function getStatus(bytes32 admissionCommitment) external view returns (uint8);

    function getRight(bytes32 admissionCommitment)
        external
        view
        returns (uint256 amount, uint256 fundedAt, uint256 unlockAt, uint8 status);
}

interface IPoseidon1 {
    function poseidon(uint256[1] memory input) external view returns (uint256);
}

contract FundAdmissionRefundLive is Script {
    function run() external {
        address admission = vm.envAddress("ADMISSION_PROXY_ADDRESS");
        address poseidon1 = vm.envAddress("POSEIDON1_ADDRESS");
        uint256 bond = vm.envUint("ADMISSION_BOND_WEI");

        // Fresh deterministic refund-path secret.
        // Do not reuse the activation validation secret.
        bytes32 admissionSecret = keccak256(
            abi.encodePacked("aurora-live-refund-secret-v1")
        );

        uint256[1] memory input = [uint256(admissionSecret)];
        bytes32 admissionCommitment = bytes32(
            IPoseidon1(poseidon1).poseidon(input)
        );

        console2.log("AdmissionRegistry:", admission);
        console2.log("Poseidon1:", poseidon1);
        console2.log("Bond:", bond);
        console2.log("Refund-path admission secret:");
        console2.logBytes32(admissionSecret);
        console2.log("Refund-path admission commitment:");
        console2.logBytes32(admissionCommitment);

        console2.log("Pre-check status:");
        console2.log(
            IAdmissionRegistry(admission).getStatus(admissionCommitment)
        );

        vm.startBroadcast();

        IAdmissionRegistry(admission).fundAdmissionRight{value: bond}(
            admissionCommitment
        );

        vm.stopBroadcast();

        console2.log("Post-fund status:");
        console2.log(
            IAdmissionRegistry(admission).getStatus(admissionCommitment)
        );

        (
            uint256 amount,
            uint256 fundedAt,
            uint256 unlockAt,
            uint8 status
        ) = IAdmissionRegistry(admission).getRight(admissionCommitment);

        console2.log("Post-fund right.amount:");
        console2.log(amount);
        console2.log("Post-fund right.fundedAt:");
        console2.log(fundedAt);
        console2.log("Post-fund right.unlockAt:");
        console2.log(unlockAt);
        console2.log("Post-fund right.status:");
        console2.log(status);
    }
}