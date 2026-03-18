// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

/*
    AnonymousMembershipRegistry.sol

    V0 merged version:
    - Upgradeable
    - AdmissionRegistry is the only authorized leaf registrar
    - Uses real Poseidon-based incremental Merkle tree internals
    - Keeps root history ring buffer for root validity checks
*/

import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import {IPoseidon2} from "./poseidon/IPoseidon2.sol";

contract AnonymousMembershipRegistry is Initializable, OwnableUpgradeable {
    // ============================================================
    // Locked tree params
    // ============================================================

    uint8 public constant DEPTH = 16; // 2^16 leaves
    uint8 public constant ROOT_HISTORY_SIZE = 16; // last N roots

    // ============================================================
    // Errors
    // ============================================================

    error ZeroAddress();
    error NotAdmissionRegistry();
    error LeafAlreadyRegistered();
    error InvalidLeaf();
    error TreeFull();

    // ============================================================
    // Events
    // ============================================================

    event AdmissionRegistrySet(address indexed admissionRegistry);
    event LeafRegistered(bytes32 indexed leaf, uint256 leafIndex, bytes32 newRoot);
    event RootAdded(bytes32 root);

    // ============================================================
    // Storage
    // ============================================================

    address public admissionRegistry;
    address public hasher;

    uint32 public nextIndex; // next leaf index
    uint256 public currentRootU256; // root as uint256 field element

    uint256[DEPTH] public zeroes;
    uint256[DEPTH] public filledSubtrees;

    bytes32[ROOT_HISTORY_SIZE] public rootHistory;
    uint256 public rootHistoryIndex;
    mapping(bytes32 => bool) public isKnownRoot;

    mapping(bytes32 => bool) public knownLeaves;

    // Optional helper/debug mapping; not required for tree mechanics,
    // but useful for testing and observability.
    mapping(uint256 => bytes32) public leaves;

    // ============================================================
    // Modifiers
    // ============================================================

    modifier onlyAdmissionRegistry() {
        if (msg.sender != admissionRegistry) revert NotAdmissionRegistry();
        _;
    }

    // ============================================================
    // Initializer
    // ============================================================

    function initialize(address initialOwner, address hasher_) external initializer {
        if (initialOwner == address(0)) revert ZeroAddress();
        if (hasher_ == address(0)) revert ZeroAddress();

        __Ownable_init(initialOwner);

        hasher = hasher_;

        _initTree();
        _pushRoot(bytes32(currentRootU256));
    }

    // ============================================================
    // Admin
    // ============================================================

    function setAdmissionRegistry(address newAdmissionRegistry) external onlyOwner {
        if (newAdmissionRegistry == address(0)) revert ZeroAddress();

        admissionRegistry = newAdmissionRegistry;
        emit AdmissionRegistrySet(newAdmissionRegistry);
    }

    // ============================================================
    // External write surface
    // ============================================================

    function registerLeaf(bytes32 leaf) external onlyAdmissionRegistry returns (uint256 leafIndex) {
        if (leaf == bytes32(0)) revert InvalidLeaf();
        if (knownLeaves[leaf]) revert LeafAlreadyRegistered();

        uint256 leafU256 = uint256(leaf);

        knownLeaves[leaf] = true;
        leafIndex = _insert(leafU256);
        leaves[leafIndex] = leaf;

        emit LeafRegistered(leaf, leafIndex, bytes32(currentRootU256));
    }

    // ============================================================
    // External views
    // ============================================================

    function currentRoot() external view returns (bytes32) {
        return bytes32(currentRootU256);
    }

    function isValidRoot(bytes32 root) external view returns (bool) {
        return isKnownRoot[root];
    }

    function leafCount() external view returns (uint256) {
        return uint256(nextIndex);
    }

    function isKnownLeaf(bytes32 leaf) external view returns (bool) {
        return knownLeaves[leaf];
    }

    // ============================================================
    // Internal tree logic
    // ============================================================

    function _hashLeftRight(uint256 left, uint256 right) internal view returns (uint256) {
        uint256[2] memory input = [left, right];
        return IPoseidon2(hasher).poseidon(input);
    }

    function _initTree() internal {
        zeroes[0] = 0;
        filledSubtrees[0] = 0;

        for (uint8 i = 1; i < DEPTH; i++) {
            zeroes[i] = _hashLeftRight(zeroes[i - 1], zeroes[i - 1]);
            filledSubtrees[i] = zeroes[i];
        }

        currentRootU256 = zeroes[DEPTH - 1];
        nextIndex = 0;
    }

    function _insert(uint256 leaf) internal returns (uint32 index) {
        index = nextIndex;
        if (index >= (uint32(1) << DEPTH)) revert TreeFull();

        nextIndex = index + 1;

        uint256 cur = leaf;
        uint32 idx = index;

        for (uint8 level = 0; level < DEPTH; level++) {
            if ((idx & 1) == 0) {
                filledSubtrees[level] = cur;
                cur = _hashLeftRight(cur, zeroes[level]);
            } else {
                cur = _hashLeftRight(filledSubtrees[level], cur);
            }
            idx >>= 1;
        }

        currentRootU256 = cur;
        _pushRoot(bytes32(cur));
    }

    function _pushRoot(bytes32 root) internal {
        bytes32 old = rootHistory[rootHistoryIndex % ROOT_HISTORY_SIZE];
        if (old != bytes32(0)) {
            isKnownRoot[old] = false;
        }

        rootHistory[rootHistoryIndex % ROOT_HISTORY_SIZE] = root;
        rootHistoryIndex++;

        isKnownRoot[root] = true;
        emit RootAdded(root);
    }

    // ============================================================
    // Storage gap
    // ============================================================

    uint256[20] private __gap;
}