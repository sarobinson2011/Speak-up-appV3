// backend/src/membership/indexer.js
import { ethers } from "ethers";
import { IncrementalBinaryTree, to0x32, toDecString } from "./tree.js";

// Minimal ABI: LeafRegistered + currentRoot + isValidRoot (optional)
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

        // Force static network (prevents ethers trying to detect network on flaky RPC)
        const AURORA_TESTNET = { name: "aurora-testnet", chainId: 1313161555 };

        // Ethers v6: use FetchRequest if you want timeouts
        const req = new ethers.FetchRequest(rpcUrl);
        req.timeout = 30_000; // ms

        this.provider = new ethers.JsonRpcProvider(req, AURORA_TESTNET);

        this.contract = new ethers.Contract(
            membershipAddress,
            MEMBERSHIP_ABI,
            this.provider
        );

        this.depth = depth;
        this.tree = new IncrementalBinaryTree(depth);

        // wallet(lowercase) -> { leaf: bigint, index: number }
        this.byWallet = new Map();

        this.synced = false;
        this.lastBlock = 0;
    }

    async sync(fromBlock = 0) {
        // naive full sync to start
        const latest = await this.provider.getBlockNumber();

        const filter = this.contract.filters.LeafRegistered();
        const logs = await this.contract.queryFilter(filter, fromBlock, latest);

        // reset
        this.tree = new IncrementalBinaryTree(this.depth);
        this.byWallet.clear();

        for (const ev of logs) {
            const wallet = ev.args.wallet.toLowerCase();
            const leaf = BigInt(ev.args.leaf.toString());
            const index = Number(ev.args.index);

            // Insert in order of index. Events should already be sequential, but don't assume:
            // We can just insert; for correctness the contract index must match our insert idx.
            const inserted = this.tree.insert(leaf);
            if (inserted !== index) {
                // If this happens, either logs are out-of-order or your on-chain tree logic differs.
                throw new Error(`index mismatch: chain=${index} local=${inserted}`);
            }

            this.byWallet.set(wallet, { leaf, index });
        }

        this.lastBlock = latest;
        this.synced = true;
        return { fromBlock, toBlock: latest, count: logs.length };
    }

    async getPath(wallet) {
        if (!this.synced) throw new Error('INDEXER_NOT_SYNCED');

        const key = wallet.toLowerCase();
        const entry = this.byWallet.get(key);
        if (!entry) return null;

        const { leaf, index } = entry;
        const { siblings, pathIndices } = this.tree.path(index);

        const root = await this.contract.currentRoot();

        // Optional: sanity check (not strictly needed, but helps catch weirdness)
        // const ok = await this.contract.isValidRoot(root);

        return {
            wallet: key,
            leaf: to0x32(leaf),
            index,
            root,
            siblings: siblings.map(to0x32),
            pathBits: pathIndices
        };
    }

    async getPathByIndex(index) {
        if (!this.synced) throw new Error('INDEXER_NOT_SYNCED');

        if (typeof index === 'string') index = Number(index);
        if (isNaN(index)) throw new Error('bad index');

        if (index < 0 || index >= (1 << this.depth)) return null;

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

    async getStatus() {
        if (!this.synced) await this.sync(0);

        const network = await this.provider.getNetwork();
        // normalize chainId to a JSON-serializable number/string
        let chainId;
        try {
            chainId = Number(network.chainId);
            if (Number.isNaN(chainId)) chainId = String(network.chainId);
        } catch (e) {
            chainId = String(network.chainId);
        }
        const registryAddress = this.membershipAddress;
        const depth = this.depth;
        const nextIndex = this.tree.nextIndex;
        const currentRoot = String(await this.contract.currentRoot());

        return { chainId, registryAddress, depth, nextIndex, currentRoot };
    }
}
