import { Router } from "express";
import { ethers } from "ethers";

function withTimeout(promise, ms, label = "timeout") {
    return Promise.race([
        promise,
        new Promise((_, rej) => setTimeout(() => rej(new Error(label)), ms)),
    ]);
}

export function makeMembershipRouter(indexer) {
    const router = Router();

    // FAST status: never touches RPC
    router.get("/status", (req, res) => {
        res.json({
            ok: true,
            membershipAddress: indexer?.membershipAddress ?? indexer?.address ?? null,
            rpcUrl: indexer?.rpcUrl ?? null,
            depth: indexer?.depth ?? null,
            lastSyncedBlock: indexer?.lastSyncedBlock ?? null,
            synced: Boolean(indexer?.synced),
        });
    });

    // GET /api/membership/pathByIndex?index=123
    router.get("/pathByIndex", async (req, res) => {
        try {
            const index = Number(req.query.index);
            if (!Number.isInteger(index) || index < 0) {
                return res.status(400).json({ error: "bad index" });
            }

            // pick whichever method your indexer actually has
            const fn =
                indexer?.pathByIndex ||
                indexer?.getPathByIndex ||
                indexer?.proofByIndex;

            if (!fn) {
                return res.status(500).json({
                    error: "indexer missing method",
                    details: "Expected pathByIndex/getPathByIndex/proofByIndex",
                });
            }

            const proof = await withTimeout(fn.call(indexer, index), 10_000, "RPC timeout");
            return res.json(proof);
        } catch (e) {
            const msg = String(e?.message || e);
            const code = msg.toLowerCase().includes("timeout") ? "TIMEOUT" : "ERR";
            return res.status(500).json({ error: "internal", code, details: msg });
        }
    });

    // GET /api/membership/path?wallet=0x...
    router.get("/path", async (req, res) => {
        try {
            const walletRaw = String(req.query.wallet || "");
            const wallet = walletRaw.trim().toLowerCase();

            if (!ethers.isAddress(wallet)) {
                return res.status(400).json({ error: "bad wallet" });
            }

            // 1) Verify registered (fast + clear error)
            if (indexer?.contract?.isRegistered) {
                const ok = await withTimeout(indexer.contract.isRegistered(wallet), 7000, "RPC timeout");
                if (!ok) return res.status(404).json({ error: "wallet not registered" });
            }

            // 2) Get index from contract by trying common function names
            const c = indexer?.contract;
            if (!c) {
                return res.status(500).json({ error: "internal", details: "indexer.contract missing" });
            }

            const tryFns = ["indexOf", "indexOfWallet", "walletIndex", "getIndex", "indexByWallet"];
            let idx = null;

            for (const name of tryFns) {
                try {
                    // ethers v6: if function doesn’t exist, calling it throws
                    const v = await withTimeout(c[name](wallet), 7000, "RPC timeout");
                    idx = Number(v);
                    if (Number.isInteger(idx) && idx >= 0) break;
                } catch (_) { }
            }

            if (idx === null) {
                return res.status(500).json({
                    error: "internal",
                    details:
                        "Could not find an index lookup function on contract. Add one (recommended) or tell me the function name.",
                });
            }

            // 3) Use the indexer’s working pathByIndex
            const fn = indexer?.pathByIndex || indexer?.getPathByIndex || indexer?.proofByIndex;
            if (!fn) {
                return res.status(500).json({
                    error: "indexer missing method",
                    details: "Expected pathByIndex/getPathByIndex/proofByIndex",
                });
            }

            const proof = await withTimeout(fn.call(indexer, idx), 10_000, "RPC timeout");
            return res.json(proof);
        } catch (e) {
            const msg = String(e?.message || e);
            const code = msg.toLowerCase().includes("timeout") ? "TIMEOUT" : "ERR";
            return res.status(500).json({ error: "internal", code, details: msg });
        }
    });


    return router;
}
