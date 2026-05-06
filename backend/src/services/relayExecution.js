import { ethers } from "ethers";

const TEMPEST_RELAY_SLOTS = [
  { id: 0, type: "primary" },
  { id: 1, type: "primary" },
  { id: 2, type: "primary" },
  { id: 3, type: "primary" },
  { id: 4, type: "primary" },
  { id: 5, type: "primary" },
  { id: 6, type: "primary" },
];

function encodeTempestSeedPreimage(submission) {
  const {
    petitionId,
    nullifier,
    proof,
    pubSignals,
    admissionCommitment,
  } = submission;

  return ethers.AbiCoder.defaultAbiCoder().encode(
    [
      "uint256",
      "bytes32",
      "bytes32",
      "uint256[2]",
      "uint256[2][2]",
      "uint256[2]",
      "uint256[3]",
    ],
    [
      BigInt(petitionId),
      nullifier,
      admissionCommitment,
      proof.pA,
      proof.pB,
      proof.pC,
      pubSignals,
    ]
  );
}

export function deriveTempestSeed(submission) {
  return ethers.keccak256(encodeTempestSeedPreimage(submission));
}

function deriveTempestPermutation(seedBI) {
  const n = 7;
  const indices = Array.from({ length: n }, (_, i) => i);

  let state = seedBI;

  for (let i = n - 1; i > 0; i -= 1) {
    state = (state * 1103515245n + 12345n) & ((1n << 64n) - 1n);
    const j = Number(state % BigInt(i + 1));
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }

  return indices;
}

function makeFailingExecutor() {
  return {
    async signPetitionWithZKProof() {
      throw new Error("TEMPEST controlled executor failure");
    },
  };
}

async function dispatchRelayExecution({
  registry,
  submission,
}) {
  const seed = deriveTempestSeed(submission);
  const seedBI = BigInt(seed);
  const index = Number(seedBI % 7n);
  const permutation = deriveTempestPermutation(seedBI);
  void index;

  const {
    petitionId,
    nullifier,
    proof,
    pubSignals,
    admissionCommitment,
  } = submission;

  const executorA = registry;
  const executorB =
    process.env.TEMPEST_FAIL_EXECUTOR_B === "true"
      ? makeFailingExecutor()
      : registry;

  let lastError = null;

  for (const selectedIndex of permutation) {
    const relay = {
      ...TEMPEST_RELAY_SLOTS[selectedIndex],
      executor: selectedIndex < 4 ? executorA : executorB,
    };

    try {
      const tx = await relay.executor.signPetitionWithZKProof(
        BigInt(petitionId),
        nullifier,
        admissionCommitment,
        proof.pA,
        proof.pB,
        proof.pC,
        pubSignals
      );

      return {
        txHash: tx.hash,
      };
    } catch (e) {
      lastError = e;
    }
  }

  throw lastError || new Error("relay execution failed");
}

export async function executeRelaySubmission({
  registry,
  submission,
}) {
  Object.freeze(submission);
  Object.freeze(submission.proof);

  return dispatchRelayExecution({
    registry,
    submission,
  });
}
