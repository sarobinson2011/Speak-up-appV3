// backend/src/membership/indexer.js
import { ethers } from "ethers";
import { IncrementalBinaryTree, to0x32 } from "./tree.js";

const MEMBERSHIP_ABI = [
  "event LeafRegistered(address indexed wallet, uint256 leaf, uint32 index, bytes32 newRoot)",
  "function currentRoot() view returns (bytes32)",
  "function isValidRoot(bytes32) view returns (bool)"
];

export class MembershipIndexer {
  constructor({ rpcUrl, membershipAddress, depth = 16 }) {
    if (!rpcUrl) throw new Error("rpcUrl required");
    if (!membershipAddress) throw new Error("membershipAddress required");

    this.rpcUrl = rpcUrl;
    this.membershipAddress = membershipAddress;

    const AURORA_TESTNET = { name: "aurora-testnet", chainId: 1313161555 };

    const req = new ethers.FetchRequest(rpcUrl);
    req.timeout = 30_000;

    this.provider = new ethers.JsonRpcProvider(req, AURORA_TESTNET);

    this.contract = new ethers.Contract(
      membershipAddress,
      MEMBERSHIP_ABI,
      this.provider
    );

    this.depth = depth;

    this.tree = new IncrementalBinaryTree(depth);

    // wallet -> { leaf: bigint, index: number }
    this.byWallet = new Map();

    // leaf (0x32) -> { leaf: bigint, index: number }
    // NOTE: intentionally does NOT store wallet to avoid leaf->wallet correlation.
    this.byLeaf = new Map();

    // wallet -> bigint leaf override (DEV ONLY)
    this.manualOverrides = new Map();

    this.synced = false;
    this.lastBlock = 0;
  }

  // -----------------------------------
  // FULL DETERMINISTIC REBUILD
  // -----------------------------------
  async rebuildFromChainAndOverrides(fromBlock = 0) {
    const latest = await this.provider.getBlockNumber();
    const filter = this.contract.filters.LeafRegistered();
    const logs = await this.contract.queryFilter(filter, fromBlock, latest);

    const newTree = new IncrementalBinaryTree(this.depth);
    const newMap = new Map();

    // 1️⃣ Replay on-chain events
    for (const ev of logs) {
      const wallet = ev.args.wallet.toLowerCase();
      const leaf = BigInt(ev.args.leaf.toString());
      const index = Number(ev.args.index);

      const inserted = newTree.insert(leaf);
      if (inserted !== index) {
        throw new Error(`index mismatch: chain=${index} local=${inserted}`);
      }

      newMap.set(wallet, { leaf, index });
    }

    // 2️⃣ Apply overrides (replace or insert)
    for (const [wallet, overrideLeaf] of this.manualOverrides.entries()) {
      if (newMap.has(wallet)) {
        // Replace leaf at same index
        const entry = newMap.get(wallet);
        entry.leaf = overrideLeaf;
      } else {
        const index = newTree.insert(overrideLeaf);
        newMap.set(wallet, { leaf: overrideLeaf, index });
      }
    }

    // 3️⃣ Rebuild final tree from final leaf set
    const finalTree = new IncrementalBinaryTree(this.depth);
    const finalMap = new Map();
    const finalLeafMap = new Map();

    for (const [wallet, { leaf }] of newMap.entries()) {
      const idx = finalTree.insert(leaf);
      const leafKey = to0x32(leaf);
      finalMap.set(wallet, { leaf, index: idx });
      finalLeafMap.set(leafKey, { leaf, index: idx });
    }

    this.tree = finalTree;
    this.byWallet = finalMap;
    this.byLeaf = finalLeafMap;
    this.lastBlock = latest;
    this.synced = true;
  }

  // -----------------------------------
  // SYNC
  // -----------------------------------
  async sync(fromBlock = 0) {
    await this.rebuildFromChainAndOverrides(fromBlock);
    return { fromBlock, toBlock: this.lastBlock };
  }

  // -----------------------------------
  // MANUAL ENROLL / REPLACE
  // -----------------------------------
  async addManualMember(wallet, leafHex) {
    const key = wallet.toLowerCase();

    if (!leafHex.startsWith("0x") || leafHex.length !== 66) {
      throw new Error("leaf must be 32-byte hex");
    }

    const leaf = BigInt(leafHex);

    this.manualOverrides.set(key, leaf);

    await this.rebuildFromChainAndOverrides(0);
  }

  // -----------------------------------
  // PATH BY WALLET
  // -----------------------------------
  async getPath(wallet) {
    if (!this.synced) throw new Error("INDEXER_NOT_SYNCED");

    const key = wallet.toLowerCase();
    const entry = this.byWallet.get(key);
    if (!entry) return null;

    const { leaf, index } = entry;
    const { siblings, pathIndices } = this.tree.path(index);

    const root = await this.contract.currentRoot();

    return {
      wallet: key,
      leaf: to0x32(leaf),
      index,
      root,
      siblings: siblings.map(to0x32),
      pathBits: pathIndices
    };
  }

  // -----------------------------------
  // PATH BY LEAF
  // -----------------------------------
  async getPathByLeaf(leafHex) {
    if (!this.synced) throw new Error("INDEXER_NOT_SYNCED");

    const leaf = BigInt(leafHex);
    const leafKey = to0x32(leaf);
    const entry = this.byLeaf.get(leafKey);
    if (!entry) return null;

    const { index } = entry;
    const { siblings, pathIndices } = this.tree.path(index);
    const root = await this.contract.currentRoot();

    return {
      wallet: null,
      leaf: leafKey,
      index,
      root,
      siblings: siblings.map(to0x32),
      pathBits: pathIndices
    };
  }

  // -----------------------------------
  // PATH BY INDEX
  // -----------------------------------
  async getPathByIndex(index) {
    if (!this.synced) throw new Error("INDEXER_NOT_SYNCED");

    if (typeof index === "string") index = Number(index);
    if (isNaN(index)) throw new Error("bad index");

    const leaf = this.tree.leaves[index] ?? 0n;
    const { siblings, pathIndices } = this.tree.path(index);
    const root = await this.contract.currentRoot();

    return {
      leaf: to0x32(leaf),
      index,
      root,
      siblings: siblings.map(to0x32),
      pathBits: pathIndices
    };
  }

  // -----------------------------------
  // STATUS
  // -----------------------------------
  async getStatus() {
    if (!this.synced) await this.sync(0);

    const network = await this.provider.getNetwork();
    let chainId;

    try {
      chainId = Number(network.chainId);
      if (Number.isNaN(chainId)) chainId = String(network.chainId);
    } catch {
      chainId = String(network.chainId);
    }

    const currentRoot = String(await this.contract.currentRoot());

    return {
      chainId,
      registryAddress: this.membershipAddress,
      depth: this.depth,
      nextIndex: this.tree.nextIndex,
      currentRoot
    };
  }
}