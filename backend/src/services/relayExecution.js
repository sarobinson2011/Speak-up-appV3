import { ethers } from "ethers";
import {
  TEMPEST_CONTROLLED_FAILURE_ENV,
  getTempestDomainIndexForSlot,
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

function makeFailingDomainHandle() {
  return {
    async signPetitionWithZKProof() {
      throw new Error("TEMPEST controlled execution failure");
    },
  };
}

function applyControlledDomainFailure(executionDomains) {
  if (process.env[TEMPEST_CONTROLLED_FAILURE_ENV] !== "true") {
    return executionDomains;
  }

  return [
    executionDomains[0],
    {
      handle: makeFailingDomainHandle(),
    },
  ];
}

function selectDomainHandleForSlot({
  selectedIndex,
  executionDomains,
}) {
  const domainIndex = getTempestDomainIndexForSlot(selectedIndex);

  return executionDomains[domainIndex].handle;
}

async function dispatchRelayExecution({
  executionDomains,
  submission,
}) {
  const seed = deriveTempestSeed(submission);
  const seedBI = BigInt(seed);
  const permutation = deriveTempestPermutation(seedBI);

  const {
    petitionId,
    nullifier,
    proof,
    pubSignals,
    admissionCommitment,
  } = submission;

  const activeExecutionDomains = applyControlledDomainFailure(executionDomains);

  let lastError = null;

  for (const selectedIndex of permutation) {
    const relay = {
      ...TEMPEST_RELAY_SLOTS[selectedIndex],
      domainHandle: selectDomainHandleForSlot({
        selectedIndex,
        executionDomains: activeExecutionDomains,
      }),
    };

    try {
      const tx = await relay.domainHandle.signPetitionWithZKProof(
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
  executionDomains,
  submission,
}) {
  Object.freeze(submission);
  Object.freeze(submission.proof);

  return dispatchRelayExecution({
    executionDomains,
    submission,
  });
}
