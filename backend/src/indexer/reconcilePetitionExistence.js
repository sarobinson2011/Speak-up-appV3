import "dotenv/config";
import { JsonRpcProvider, Contract } from "ethers";
import {
  getAllPetitionIds,
  setPetitionActive,
} from "../db/repositories/petitions.js";

const RPC_URL = process.env.RPC_URL;
const PETITION_REGISTRY_ADDRESS = process.env.PETITION_REGISTRY_ADDRESS;

if (!RPC_URL) {
  throw new Error("Missing RPC_URL");
}

if (!PETITION_REGISTRY_ADDRESS) {
  throw new Error("Missing PETITION_REGISTRY_ADDRESS");
}

const abi = [
  "function petitions(uint256) view returns (address creator, uint256 createdAt, string metadataURI, bool exists)",
];

async function main() {
  const provider = new JsonRpcProvider(RPC_URL);
  const registry = new Contract(PETITION_REGISTRY_ADDRESS, abi, provider);

  const rows = getAllPetitionIds();

  let active = 0;
  let inactive = 0;

  for (const row of rows) {
    const petitionId = Number(row.petition_id);

    // eslint-disable-next-line no-await-in-loop
    const petition = await registry.petitions(petitionId);
    const exists = Boolean(petition.exists);

    setPetitionActive(petitionId, exists);

    if (exists) active += 1;
    else inactive += 1;

    console.log(
      `[PetitionRegistry reconcile] petition ${petitionId} -> ${
        exists ? "active" : "inactive"
      }`
    );
  }

  console.log(
    `[PetitionRegistry reconcile] complete: active=${active} inactive=${inactive}`
  );
}

main().catch((err) => {
  console.error("[PetitionRegistry reconcile] failed:", err);
  process.exit(1);
});
