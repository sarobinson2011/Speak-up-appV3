import { getAllMembershipLeavesOrdered } from "../db/repositories/membership.js";
import { IncrementalBinaryTree, to0x32 } from "./tree.js";

export class MembershipIndexer {
  constructor({ depth = 16 }) {
    this.depth = depth;
    this.tree = new IncrementalBinaryTree(depth);

    // leafHex -> { leaf, index }
    this.byLeaf = new Map();

    this.synced = false;
    this.lastLeafIndex = -1;
  }

  // -----------------------------------
  // FULL DETERMINISTIC REBUILD FROM DB
  // -----------------------------------
  rebuildFromIndexedLeaves() {
    const rows = getAllMembershipLeavesOrdered();

    const finalTree = new IncrementalBinaryTree(this.depth);
    const finalLeafMap = new Map();

    for (let expectedIndex = 0; expectedIndex < rows.length; expectedIndex++) {
      const row = rows[expectedIndex];

      if (row.leaf_index !== expectedIndex) {
        throw new Error(
          `membership leaf index gap/mismatch: expected=${expectedIndex} actual=${row.leaf_index}`
        );
      }

      const leaf = BigInt(row.leaf);
      const inserted = finalTree.insert(leaf);

      if (inserted !== row.leaf_index) {
        throw new Error(
          `local tree insert mismatch: db=${row.leaf_index} local=${inserted}`
        );
      }

      const leafKey = to0x32(leaf);
      finalLeafMap.set(leafKey, {
        leaf,
        index: row.leaf_index,
      });
    }

    this.tree = finalTree;
    this.byLeaf = finalLeafMap;
    this.lastLeafIndex = rows.length - 1;
    this.synced = true;

    return {
      leafCount: rows.length,
      currentRoot: to0x32(this.tree.root),
    };
  }

  // -----------------------------------
  // SYNC
  // -----------------------------------
  async sync() {
    return this.rebuildFromIndexedLeaves();
  }

  // -----------------------------------
  // PATH BY LEAF
  // -----------------------------------
  async getPathByLeaf(leafHex) {
    if (!this.synced) {
      throw new Error("INDEXER_NOT_SYNCED");
    }

    const leaf = BigInt(leafHex);
    const leafKey = to0x32(leaf);
    const entry = this.byLeaf.get(leafKey);

    if (!entry) return null;

    const { index } = entry;
    const { siblings, pathIndices } = this.tree.path(index);

    return {
      leaf: leafKey,
      index,
      root: to0x32(this.tree.root),
      siblings: siblings.map(to0x32),
      pathBits: pathIndices,
    };
  }

  // -----------------------------------
  // PATH BY INDEX
  // -----------------------------------
  async getPathByIndex(index) {
    if (!this.synced) {
      throw new Error("INDEXER_NOT_SYNCED");
    }

    if (typeof index === "string") index = Number(index);
    if (!Number.isInteger(index) || index < 0) {
      throw new Error("bad index");
    }

    const leaf = this.tree.leaves[index];
    if (leaf === undefined) return null;

    const { siblings, pathIndices } = this.tree.path(index);

    return {
      leaf: to0x32(leaf),
      index,
      root: to0x32(this.tree.root),
      siblings: siblings.map(to0x32),
      pathBits: pathIndices,
    };
  }

  // -----------------------------------
  // STATUS
  // -----------------------------------
  async getStatus() {
    if (!this.synced) {
      await this.sync();
    }

    return {
      depth: this.depth,
      nextIndex: this.tree.nextIndex,
      currentRoot: to0x32(this.tree.root),
    };
  }
}