// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";

interface IAdmissionRegistry {
    function refundAdmissionRight(bytes32 admissionSecret, address recipient) external;

    function getStatus(bytes32 admissionCommitment) external view returns (uint8);

    function getRight(bytes32 admissionCommitment)
        external
        view
        returns (uint256 amount, uint256 fundedAt, uint256 unlockAt, uint8 status);
}

interface IPoseidon1 {
    function poseidon(uint256[1] memory input) external view returns (uint256);
}

contract ClaimAdmissionRefundLive is Script {
    function run() external {
        address admission = vm.envAddress("ADMISSION_PROXY_ADDRESS");
        address poseidon1 = vm.envAddress("POSEIDON1_ADDRESS");
        address recipient = vm.envAddress("OWNER_ADDRESS");

        // Must match the funded refund-path test vector exactly.
        bytes32 admissionSecret = keccak256(
            abi.encodePacked("aurora-live-refund-secret-v1")
        );

        uint256[1] memory input = [uint256(admissionSecret)];
        bytes32 admissionCommitment = bytes32(
            IPoseidon1(poseidon1).poseidon(input)
        );

        console2.log("AdmissionRegistry:", admission);
        console2.log("Poseidon1:", poseidon1);
        console2.log("Recipient:", recipient);
        console2.log("Refund-path admission secret:");
        console2.logBytes32(admissionSecret);
        console2.log("Refund-path admission commitment:");
        console2.logBytes32(admissionCommitment);

        console2.log("Pre-refund status:");
        console2.log(IAdmissionRegistry(admission).getStatus(admissionCommitment));

        (
            uint256 amountBefore,
            uint256 fundedAtBefore,
            uint256 unlockAtBefore,
            uint8 statusBefore
        ) = IAdmissionRegistry(admission).getRight(admissionCommitment);

        console2.log("Pre-refund right.amount:");
        console2.log(amountBefore);
        console2.log("Pre-refund right.fundedAt:");
        console2.log(fundedAtBefore);
        console2.log("Pre-refund right.unlockAt:");
        console2.log(unlockAtBefore);
        console2.log("Pre-refund right.status:");
        console2.log(statusBefore);

        vm.startBroadcast();

        IAdmissionRegistry(admission).refundAdmissionRight(admissionSecret, recipient);

        vm.stopBroadcast();

        console2.log("Post-refund status:");
        console2.log(IAdmissionRegistry(admission).getStatus(admissionCommitment));

        (
            uint256 amountAfter,
            uint256 fundedAtAfter,
            uint256 unlockAtAfter,
            uint8 statusAfter
        ) = IAdmissionRegistry(admission).getRight(admissionCommitment);

        console2.log("Post-refund right.amount:");
        console2.log(amountAfter);
        console2.log("Post-refund right.fundedAt:");
        console2.log(fundedAtAfter);
        console2.log("Post-refund right.unlockAt:");
        console2.log(unlockAtAfter);
        console2.log("Post-refund right.status:");
        console2.log(statusAfter);
    }
}