// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {PetitionRegistry} from "../src/PetitionRegistry.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract MockAuthorizer {
    function authorizeSign(uint256, bytes32, bytes calldata) external pure returns (bool) {
        return true;
    }

    function authorizeComment(uint256, bytes32, bytes32, bytes calldata) external pure returns (bool) {
        return true;
    }
}

contract MockVerifier {
    bool internal _shouldVerify = true;

    function setShouldVerify(bool shouldVerify_) external {
        _shouldVerify = shouldVerify_;
    }

    function verifyProof(
        uint256[2] calldata,
        uint256[2][2] calldata,
        uint256[2] calldata,
        uint256[3] calldata
    ) external view returns (bool) {
        return _shouldVerify;
    }
}

contract MockAdmissionRegistryActionLink {
    bool public shouldRevert;
    bytes32 public lastAdmissionCommitment;
    uint256 public callCount;

    error MockLinkRevert();

    function setShouldRevert(bool shouldRevert_) external {
        shouldRevert = shouldRevert_;
    }

    function recordActionLink(bytes32 admissionCommitment) external {
        if (shouldRevert) revert MockLinkRevert();
        lastAdmissionCommitment = admissionCommitment;
        callCount++;
    }
}

contract PetitionRegistryZKSigningCorrelationTest is Test {
    PetitionRegistry internal registry;
    MockAuthorizer internal authorizer;
    MockVerifier internal verifier;
    MockAdmissionRegistryActionLink internal admission;

    address internal creator = address(0xBEEF);

    function setUp() public {
        authorizer = new MockAuthorizer();
        verifier = new MockVerifier();
        admission = new MockAdmissionRegistryActionLink();

        PetitionRegistry impl = new PetitionRegistry();

        bytes memory initData =
            abi.encodeCall(PetitionRegistry.initialize, (address(authorizer), address(0x1234)));

        ERC1967Proxy proxy = new ERC1967Proxy(address(impl), initData);
        registry = PetitionRegistry(address(proxy));

        registry.setGroth16Verifier(address(verifier));
        registry.setAdmissionRegistry(address(admission));

        vm.prank(creator);
        registry.createPetition("ipfs://petition-1");
    }

    function _proof()
        internal
        pure
        returns (
            uint256[2] memory pA,
            uint256[2][2] memory pB,
            uint256[2] memory pC
        )
    {
        pA = [uint256(1), uint256(2)];
        pB = [[uint256(3), uint256(4)], [uint256(5), uint256(6)]];
        pC = [uint256(7), uint256(8)];
    }

    function testSignPetitionWithZKProof_SucceedsWithoutEmittingAdmissionCommitment() public {
        bytes32 nullifier = bytes32(uint256(111));
        bytes32 admissionCommitment = bytes32(uint256(222));

        (uint256[2] memory pA, uint256[2][2] memory pB, uint256[2] memory pC) = _proof();
        uint256[3] memory pubSignals = [uint256(nullifier), uint256(1), uint256(999)];

        vm.expectEmit(true, true, false, true);
        emit PetitionRegistry.PetitionSigned(1, nullifier, bytes32(0));

        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment, pA, pB, pC, pubSignals);

        assertEq(admission.callCount(), 0);
        assertEq(admission.lastAdmissionCommitment(), bytes32(0));
        assertTrue(registry.hasSignedPetition(1, nullifier));
    }

    function testSignPetitionWithZKProof_RevertsWithoutRecordingSignatureOnInvalidProof() public {
        bytes32 nullifier = bytes32(uint256(111));
        bytes32 admissionCommitment = bytes32(uint256(222));

        verifier.setShouldVerify(false);

        (uint256[2] memory pA, uint256[2][2] memory pB, uint256[2] memory pC) = _proof();
        uint256[3] memory pubSignals = [uint256(nullifier), uint256(1), uint256(999)];

        vm.expectRevert(PetitionRegistry.InvalidZKProof.selector);
        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment, pA, pB, pC, pubSignals);

        assertEq(admission.callCount(), 0);
        assertFalse(registry.hasSignedPetition(1, nullifier));
    }

    function testSignPetitionWithZKProof_DoesNotCallActionLinkRegistry() public {
        bytes32 nullifier = bytes32(uint256(111));
        bytes32 admissionCommitment = bytes32(uint256(222));

        admission.setShouldRevert(true);

        (uint256[2] memory pA, uint256[2][2] memory pB, uint256[2] memory pC) = _proof();
        uint256[3] memory pubSignals = [uint256(nullifier), uint256(1), uint256(999)];

        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment, pA, pB, pC, pubSignals);

        assertEq(admission.callCount(), 0);
        assertTrue(registry.hasSignedPetition(1, nullifier));
    }

    function testSignPetitionWithZKProof_DoesNotMutateAdmissionRegistry() public {
        bytes32 nullifier = bytes32(uint256(444));
        bytes32 admissionCommitment = bytes32(uint256(555));

        bytes32 lastCommitmentBefore = admission.lastAdmissionCommitment();
        uint256 callCountBefore = admission.callCount();

        (uint256[2] memory pA, uint256[2][2] memory pB, uint256[2] memory pC) = _proof();
        uint256[3] memory pubSignals = [uint256(nullifier), uint256(1), uint256(999)];

        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment, pA, pB, pC, pubSignals);

        assertEq(admission.callCount(), callCountBefore);
        assertEq(admission.lastAdmissionCommitment(), lastCommitmentBefore);
        assertTrue(registry.hasSignedPetition(1, nullifier));
    }

    function testSignPetitionWithZKProof_RevertsOnDuplicateNullifier() public {
        bytes32 nullifier = bytes32(uint256(111));
        bytes32 admissionCommitment1 = bytes32(uint256(222));
        bytes32 admissionCommitment2 = bytes32(uint256(333));

        (uint256[2] memory pA, uint256[2][2] memory pB, uint256[2] memory pC) = _proof();
        uint256[3] memory pubSignals = [uint256(nullifier), uint256(1), uint256(999)];

        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment1, pA, pB, pC, pubSignals);

        vm.expectRevert(PetitionRegistry.NullifierAlreadyUsed.selector);
        registry.signPetitionWithZKProof(1, nullifier, admissionCommitment2, pA, pB, pC, pubSignals);

        assertEq(admission.callCount(), 0);
    }
}