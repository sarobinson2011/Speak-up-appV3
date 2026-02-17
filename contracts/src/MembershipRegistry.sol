// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {IPoseidon2} from "./poseidon/IPoseidon2.sol";

/**
 * MembershipRegistry
 * - Permissionless leaf registration (one per wallet for baseline)
 * - Incremental Merkle tree (Poseidon(left,right))
 * - Root validity: last N roots (ring buffer) + mapping membership
 * - Minimal refundable bond: lock funds for a time window, then user can withdraw
 */
contract MembershipRegistry {
    // ======== Locked baseline params (per STATE) ========
    uint8 public constant DEPTH = 16; // 2^16 leaves
    uint8 public constant ROOT_HISTORY_SIZE = 16; // last N roots

    // BN254 scalar field (optional guard for sanity; not strictly required)
    // uint256 public constant SNARK_FIELD =
    //   21888242871839275222246405745257275088548364400416034343698204186575808495617;

    // ======== Hasher ========
    address public immutable hasher;

    // ======== Tree state ========
    uint32 public nextIndex; // next leaf index
    uint256 public currentRootU256; // root as uint256 (field element)

    uint256[DEPTH] public zeroes; // zero values per level
    uint256[DEPTH] public filledSubtrees; // incremental insert helpers

    // ======== Root validity (last N) ========
    bytes32[ROOT_HISTORY_SIZE] public rootHistory;
    uint256 public rootHistoryIndex; // ring pointer
    mapping(bytes32 => bool) public isKnownRoot; // membership check

    // ======== Membership mapping (baseline: 1 leaf per wallet) ========
    mapping(address => bool) public isRegistered;
    mapping(address => uint256) public leafOf; // leaf as uint256

    // ======== Minimal refundable bond (baseline) ========
    uint256 public registerBondWei; // exact amount required to register
    uint64 public bondLockSeconds; // lock duration
    mapping(address => uint256) public bonded;
    mapping(address => uint64) public unlockAt;

    // ======== Events ========
    event LeafRegistered(address indexed wallet, uint256 leaf, uint32 index, bytes32 newRoot);
    event RootAdded(bytes32 root);
    event BondWithdrawn(address indexed wallet, uint256 amount);

    constructor(address _hasher, uint256 _registerBondWei, uint64 _bondLockSeconds) {
        require(_hasher != address(0), "hasher=0");
        hasher = _hasher;

        registerBondWei = _registerBondWei;
        bondLockSeconds = _bondLockSeconds;

        _initTree();
        _pushRoot(bytes32(currentRootU256));
    }

    // ---------- External views ----------
    function currentRoot() external view returns (bytes32) {
        return bytes32(currentRootU256);
    }

    function isValidRoot(bytes32 root) external view returns (bool) {
        return isKnownRoot[root];
    }

    // ---------- Admin knobs (optional; can delete if you want ZERO admin) ----------
    // For now keep it simple: anyone can deploy with chosen parameters.
    // If you want adjustable later, add Ownable and setters.

    // ---------- Registration ----------
    function registerLeaf(uint256 leaf) external payable returns (uint32 index, bytes32 newRoot) {
        require(!isRegistered[msg.sender], "already registered");

        // Optional sanity: avoid zero leaf (helps with "unset" detection)
        require(leaf != 0, "leaf=0");

        // Optional field check (uncomment if you want hard guard)
        // require(leaf < SNARK_FIELD, "leaf not in field");

        // Bond
        require(msg.value == registerBondWei, "bad bond");
        bonded[msg.sender] += msg.value;
        uint64 until = uint64(block.timestamp) + bondLockSeconds;
        if (until > unlockAt[msg.sender]) unlockAt[msg.sender] = until;

        // Insert into tree
        index = _insert(leaf);

        isRegistered[msg.sender] = true;
        leafOf[msg.sender] = leaf;

        newRoot = bytes32(currentRootU256);
        emit LeafRegistered(msg.sender, leaf, index, newRoot);
    }

    /// @notice Refund the registration bond after the lock period.
    /// Baseline: user can withdraw while keeping membership (this is “friction”, not a permanent fee).
    function withdrawBond() external {
        uint256 amt = bonded[msg.sender];
        require(amt > 0, "no bond");
        require(block.timestamp >= unlockAt[msg.sender], "still locked");

        bonded[msg.sender] = 0;
        unlockAt[msg.sender] = 0;

        (bool ok,) = msg.sender.call{value: amt}("");
        require(ok, "transfer failed");

        emit BondWithdrawn(msg.sender, amt);
    }

    // ---------- Internal: tree ----------
    function _hashLeftRight(uint256 left, uint256 right) internal view returns (uint256) {
        uint256[2] memory input = [left, right];
        // Hasher is a pure function, but we call it externally (staticcall) via interface.
        return IPoseidon2(hasher).poseidon(input);
    }

    function _initTree() internal {
        // Level 0 zero is usually 0 for Poseidon-based IMTs (matches common Circom patterns).
        zeroes[0] = 0;
        filledSubtrees[0] = 0;

        for (uint8 i = 1; i < DEPTH; i++) {
            zeroes[i] = _hashLeftRight(zeroes[i - 1], zeroes[i - 1]);
            filledSubtrees[i] = zeroes[i];
        }

        // Empty tree root
        currentRootU256 = zeroes[DEPTH - 1];
        nextIndex = 0;
    }

    function _insert(uint256 leaf) internal returns (uint32 index) {
        index = nextIndex;
        require(index < (uint32(1) << DEPTH), "tree full");
        nextIndex = index + 1;

        uint256 cur = leaf;
        uint32 idx = index;

        for (uint8 level = 0; level < DEPTH; level++) {
            if ((idx & 1) == 0) {
                // left node
                filledSubtrees[level] = cur;
                cur = _hashLeftRight(cur, zeroes[level]);
            } else {
                // right node
                cur = _hashLeftRight(filledSubtrees[level], cur);
            }
            idx >>= 1;
        }

        currentRootU256 = cur;
        _pushRoot(bytes32(cur));
    }

    function _pushRoot(bytes32 root) internal {
        // Evict old root at pointer
        bytes32 old = rootHistory[rootHistoryIndex % ROOT_HISTORY_SIZE];
        if (old != bytes32(0)) {
            isKnownRoot[old] = false;
        }

        rootHistory[rootHistoryIndex % ROOT_HISTORY_SIZE] = root;
        rootHistoryIndex++;

        isKnownRoot[root] = true;
        emit RootAdded(root);
    }

    receive() external payable {}
}
