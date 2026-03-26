// backend/src/membership/indexer.js
import { ethers, AbiCoder, keccak256, toUtf8Bytes } from "ethers";
import { IncrementalBinaryTree, to0x32 } from "./tree.js";

const MEMBERSHIP_ABI = [
  "event LeafRegistered(bytes32 indexed leaf, uint256 leafIndex, bytes32 newRoot)",
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

    // Leaf-indexed only; no wallet-based correlation is stored.
    this.byLeaf = new Map();

    this.synced = false;
    this.lastBlock = 0;
  }

  // -----------------------------------
  // FULL DETERMINISTIC REBUILD
  // -----------------------------------
  async rebuildFromChainAndOverrides(fromBlock = 0) {
    const latest = await this.provider.getBlockNumber();

    const leafRegisteredTopic = keccak256(
      toUtf8Bytes("LeafRegistered(bytes32,uint256,bytes32)")
    );

    const logs = await this.provider.getLogs({
      address: this.membershipAddress,
      fromBlock,
      toBlock: latest,
      topics: [leafRegisteredTopic]
    });

    const coder = AbiCoder.defaultAbiCoder();

    const finalTree = new IncrementalBinaryTree(this.depth);
    const finalLeafMap = new Map();

    for (const log of logs) {
      if (!log.topics || log.topics.length < 2) {
        throw new Error("LeafRegistered log missing indexed leaf topic");
      }

      const leafHex = log.topics[1];
      const leaf = BigInt(leafHex);

      const [leafIndex, _newRoot] = coder.decode(
        ["uint256", "bytes32"],
        log.data
      );

      const index = Number(leafIndex);

      const inserted = finalTree.insert(leaf);
      if (inserted !== index) {
        throw new Error(`index mismatch: chain=${index} local=${inserted}`);
      }

      const leafKey = to0x32(leaf);
      finalLeafMap.set(leafKey, { leaf, index });
    }

    this.tree = finalTree;
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