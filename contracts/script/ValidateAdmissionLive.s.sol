// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Script.sol";

interface IAdmissionRegistry {
    function fundAdmissionRight(bytes32 admissionCommitment) external payable;

    function activateMembership(
        bytes32 admissionCommitment,
        bytes32 admissionSecret,
        bytes32 leaf
    ) external;

    function getStatus(bytes32 admissionCommitment) external view returns (uint8);

    function getRight(bytes32 admissionCommitment)
        external
        view
        returns (uint256 amount, uint256 fundedAt, uint256 unlockAt, uint8 status);
}

interface IAnonymousMembershipRegistry {
    function leafCount() external view returns (uint256);
    function isKnownLeaf(bytes32 leaf) external view returns (bool);
    function currentRoot() external view returns (bytes32);
}

interface IPoseidon1 {
    function poseidon(uint256[1] memory input) external view returns (uint256);
}

contract ValidateAdmissionLive is Script {
    function run() external {
        address admission = vm.envAddress("ADMISSION_PROXY_ADDRESS");
        address membership = vm.envAddress("ANON_MEMBERSHIP_PROXY_ADDRESS");
        address poseidon1 = vm.envAddress("POSEIDON1_ADDRESS");
        uint256 bond = vm.envUint("ADMISSION_BOND_WEI");

        // Deterministic test values for this live validation run.
        // Keep these fixed for reproducibility unless you intentionally want a new run.
        bytes32 admissionSecret = keccak256(
            abi.encodePacked("aurora-live-admission-secret-v1")
        );
        bytes32 memberSecret = keccak256(
            abi.encodePacked("aurora-live-member-secret-v1")
        );

        // Locked model:
        // admissionCommitment = Poseidon1(admissionSecret)
        // leaf                = Poseidon1(memberSecret)
        uint256[1] memory admissionInput = [uint256(admissionSecret)];
        bytes32 admissionCommitment = bytes32(
            IPoseidon1(poseidon1).poseidon(admissionInput)
        );

        uint256[1] memory memberInput = [uint256(memberSecret)];
        bytes32 leaf = bytes32(IPoseidon1(poseidon1).poseidon(memberInput));

        console2.log("AdmissionRegistry:", admission);
        console2.log("MembershipRegistry:", membership);
        console2.log("Poseidon1:", poseidon1);
        console2.log("Bond:", bond);
        console2.log("Admission secret:");
        console2.logBytes32(admissionSecret);
        console2.log("Member secret:");
        console2.logBytes32(memberSecret);
        console2.log("Admission commitment:");
        console2.logBytes32(admissionCommitment);
        console2.log("Leaf:");
        console2.logBytes32(leaf);

        console2.log("Pre-check leafCount:");
        console2.log(IAnonymousMembershipRegistry(membership).leafCount());

        console2.log("Pre-check isKnownLeaf:");
        console2.log(IAnonymousMembershipRegistry(membership).isKnownLeaf(leaf));

        console2.log("Pre-check status:");
        console2.log(IAdmissionRegistry(admission).getStatus(admissionCommitment));

        // Uses the configured Foundry signer path (keystore/account) from the CLI.
        vm.startBroadcast();

        IAdmissionRegistry(admission).fundAdmissionRight{value: bond}(admissionCommitment);

        IAdmissionRegistry(admission).activateMembership(
            admissionCommitment,
            admissionSecret,
            leaf
        );

        vm.stopBroadcast();

        console2.log("Post-check leafCount:");
        console2.log(IAnonymousMembershipRegistry(membership).leafCount());

        console2.log("Post-check isKnownLeaf:");
        console2.log(IAnonymousMembershipRegistry(membership).isKnownLeaf(leaf));

        console2.log("Post-check status:");
        console2.log(IAdmissionRegistry(admission).getStatus(admissionCommitment));

        console2.log("Post-check root:");
        console2.logBytes32(IAnonymousMembershipRegistry(membership).currentRoot());

        (
            uint256 amount,
            uint256 fundedAt,
            uint256 unlockAt,
            uint8 status
        ) = IAdmissionRegistry(admission).getRight(admissionCommitment);

        console2.log("Post-check right.amount:");
        console2.log(amount);
        console2.log("Post-check right.fundedAt:");
        console2.log(fundedAt);
        console2.log("Post-check right.unlockAt:");
        console2.log(unlockAt);
        console2.log("Post-check right.status:");
        console2.log(status);
    }
}