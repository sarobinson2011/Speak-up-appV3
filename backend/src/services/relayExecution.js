import { ethers } from "ethers";
import {
  TEMPEST_CONTROLLED_FAILURE_ENV,
  TEMPEST_GROUP0_MAX_SLOT,
  TEMPEST_PERMUTATION_INCREMENT,
  TEMPEST_PERMUTATION_MASK,
  TEMPEST_PERMUTATION_MULTIPLIER,
  TEMPEST_RELAY_SLOTS,
  TEMPEST_SLOT_COUNT,
} from "./tempestConfig.js";

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
  const n = TEMPEST_SLOT_COUNT;
  const indices = Array.from({ length: n }, (_, i) => i);

  let state = seedBI;

  for (let i = n - 1; i > 0; i -= 1) {
    state = (state * TEMPEST_PERMUTATION_MULTIPLIER + TEMPEST_PERMUTATION_INCREMENT) & TEMPEST_PERMUTATION_MASK;
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

function createTempestExecutors({ registry, secondaryRegistry }) {
  return {
    group0Executor: registry,
    group1Executor:
      process.env[TEMPEST_CONTROLLED_FAILURE_ENV] === "true"
        ? makeFailingExecutor()
        : secondaryRegistry,
  };
}

function selectExecutorForSlot({
  selectedIndex,
  group0Executor,
  group1Executor,
}) {
  return selectedIndex <= TEMPEST_GROUP0_MAX_SLOT ? group0Executor : group1Executor;
}

async function dispatchRelayExecution({
  registry,
  secondaryRegistry,
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

  const { group0Executor, group1Executor } = createTempestExecutors({ registry, secondaryRegistry });

  let lastError = null;

  for (const selectedIndex of permutation) {
    const relay = {
      ...TEMPEST_RELAY_SLOTS[selectedIndex],
      executor: selectExecutorForSlot({
        selectedIndex,
        group0Executor,
        group1Executor,
      }),
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
  secondaryRegistry,
  submission,
}) {
  Object.freeze(submission);
  Object.freeze(submission.proof);

  return dispatchRelayExecution({
    registry,
    secondaryRegistry,
    submission,
  });
}
