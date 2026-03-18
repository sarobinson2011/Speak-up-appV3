// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Test} from "forge-std/Test.sol";
import {Poseidon1} from "../src/poseidon/Poseidon1.sol";
import {IPoseidon1} from "../src/poseidon/IPoseidon1.sol";

contract Poseidon1Test is Test {
    Poseidon1 internal poseidon1;

    function setUp() public {
        poseidon1 = new Poseidon1();
    }

    function testPoseidon1_DeterministicForSameInput() public view {
        uint256[1] memory input = [uint256(123)];
        uint256 out1 = IPoseidon1(address(poseidon1)).poseidon(input);
        uint256 out2 = IPoseidon1(address(poseidon1)).poseidon(input);

        assertEq(out1, out2);
    }

    function testPoseidon1_DifferentInputsProduceDifferentOutputs() public view {
        uint256[1] memory input1 = [uint256(123)];
        uint256[1] memory input2 = [uint256(124)];

        uint256 out1 = IPoseidon1(address(poseidon1)).poseidon(input1);
        uint256 out2 = IPoseidon1(address(poseidon1)).poseidon(input2);

        assertTrue(out1 != out2);
    }

    function testPoseidon1_PrintAnchorVector() public {
        uint256[1] memory input = [uint256(111)];
        uint256 out = IPoseidon1(address(poseidon1)).poseidon(input);

        emit log_named_uint("POSEIDON1_INPUT", input[0]);
        emit log_named_uint("POSEIDON1_OUTPUT", out);
    }
}