// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

interface IAnonymousMembershipRegistry {
    function registerLeaf(bytes32 leaf) external returns (uint256 leafIndex);
    function knownLeaves(bytes32 leaf) external view returns (bool);
}
