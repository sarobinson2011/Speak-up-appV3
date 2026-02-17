// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "forge-std/Test.sol";
import {Poseidon2} from "../src/poseidon/Poseidon2.sol";
import {IPoseidon2} from "../src/poseidon/IPoseidon2.sol";

contract Poseidon2Test is Test {
    function test_poseidon2_call_works() public {
        Poseidon2 h = new Poseidon2();

        uint256[2] memory inp = [uint256(1), uint256(2)];
        uint256 out = IPoseidon2(address(h)).poseidon(inp);

        // Don’t assert nonzero (Poseidon can output 0 for some inputs in principle).
        // The important property is: it returns and is deterministic.
        uint256 out2 = IPoseidon2(address(h)).poseidon(inp);
        assertEq(out, out2, "not deterministic");
    }

    function test_poseidon2_selector_exists() public {
        Poseidon2 h = new Poseidon2();

        uint256[2] memory inp = [uint256(1), uint256(2)];
        (bool ok, bytes memory data) = address(h).staticcall(abi.encodeWithSelector(IPoseidon2.poseidon.selector, inp));

        assertTrue(ok, "staticcall failed");
        assertEq(data.length, 32, "bad return size");
    }
}
