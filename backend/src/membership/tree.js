// backend/src/membership/tree.js
import { poseidon2 } from "poseidon-lite";

// Poseidon2(left,right) -> field element bigint
function H(left, right) {
    return poseidon2([BigInt(left), BigInt(right)]);
}

export class IncrementalBinaryTree {
    constructor(depth = 16) {
        this.depth = depth;

        // zeroes[i] = hash of empty subtree at level i
        this.zeroes = new Array(depth);
        this.filledSubtrees = new Array(depth);

        this.zeroes[0] = 0n;
        this.filledSubtrees[0] = 0n;

        for (let i = 1; i < depth; i++) {
            this.zeroes[i] = H(this.zeroes[i - 1], this.zeroes[i - 1]);
            this.filledSubtrees[i] = this.zeroes[i];
        }

        this.nextIndex = 0;
        this.leaves = [];              // store leaf values by index (needed for paths)
        this.nodesByLevel = [];        // optional, we’ll build levels on demand for paths
        this.root = this.zeroes[depth - 1];
    }

    insert(leaf) {
        const idx = this.nextIndex;
        if (idx >= (1 << this.depth)) throw new Error("tree full");

        const leafBI = BigInt(leaf);
        this.leaves[idx] = leafBI;

        let cur = leafBI;
        let index = idx;

        for (let level = 0; level < this.depth; level++) {
            if ((index & 1) === 0) {
                // cur is left
                this.filledSubtrees[level] = cur;
                cur = H(cur, this.zeroes[level]);
            } else {
                // cur is right
                cur = H(this.filledSubtrees[level], cur);
            }
            index >>= 1;
        }

        this.root = cur;
        this.nextIndex++;
        // invalidate cached nodes; we’ll rebuild lazily when someone asks for a path
        this.nodesByLevel = [];
        return idx;
    }

    // Build full level arrays (cost: O(n)) — fine for v1, depth=16, <=65k leaves
    _buildLevels() {
        if (this.nodesByLevel.length) return;

        const depth = this.depth;
        const leafCount = 1 << depth;

        // level 0: leaves padded with zeros
        const level0 = new Array(leafCount);
        for (let i = 0; i < leafCount; i++) {
            level0[i] = this.leaves[i] ?? 0n;
        }

        this.nodesByLevel[0] = level0;

        for (let level = 1; level < depth; level++) {
            const prev = this.nodesByLevel[level - 1];
            const size = 1 << (depth - level);
            const cur = new Array(size);
            for (let i = 0; i < size; i++) {
                cur[i] = H(prev[i * 2], prev[i * 2 + 1]);
            }
            this.nodesByLevel[level] = cur;
        }
    }

    // Returns siblings + indices for a given leaf index
    path(index) {
        if (index < 0 || index >= (1 << this.depth)) throw new Error("bad index");
        this._buildLevels();

        const siblings = [];
        const pathIndices = [];

        let idx = index;

        for (let level = 0; level < this.depth; level++) {
            const levelNodes = this.nodesByLevel[level];
            const siblingIndex = idx ^ 1;            // flip last bit
            siblings.push(levelNodes[siblingIndex]);
            pathIndices.push(idx & 1);               // 0 => left, 1 => right
            idx >>= 1;
        }

        return { siblings, pathIndices };
    }
}

// helpers for JSON
export function to0x32(x) {
    // x is bigint
    let hex = x.toString(16);
    if (hex.length > 64) throw new Error("too large for bytes32");
    hex = hex.padStart(64, "0");
    return "0x" + hex;
}

export function toDecString(x) {
    return x.toString(10);
}
