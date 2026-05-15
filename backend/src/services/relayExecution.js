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

function classifyRelayExecutionFailure(error) {
  const message = error?.message || String(error || "");

  if (message.includes("TEMPEST controlled execution failure")) {
    return "execution_controlled_failure";
  }

  if (
    error?.code === "CALL_EXCEPTION" ||
    message.includes("execution reverted") ||
    message.includes("missing revert data")
  ) {
    return "execution_reverted";
  }

  if (
    error?.code === "NETWORK_ERROR" ||
    error?.code === "SERVER_ERROR" ||
    error?.code === "TIMEOUT" ||
    message.includes("ECONNREFUSED") ||
    message.includes("ETIMEDOUT") ||
    message.includes("network")
  ) {
    return "execution_transport_failure";
  }

  return "execution_unclassified_failure";
}

function normalizeRelayExecutionFailure(error) {
  return Object.freeze({
    classification: classifyRelayExecutionFailure(error),
    error,
  });
}

function shouldContinueRelayExecution(normalizedFailure) {
  return (
    normalizedFailure?.classification === "execution_controlled_failure" ||
    normalizedFailure?.classification === "execution_transport_failure"
  );
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
      ...executionDomains[1],
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

async function reconcileRelayExecutionState({
  domainHandle,
  petitionId,
  nullifier,
}) {
  if (typeof domainHandle?.hasSignedPetition !== "function") {
    return null;
  }

  const alreadyRecorded = await domainHandle.hasSignedPetition(
    BigInt(petitionId),
    nullifier,
  );

  if (alreadyRecorded) {
    return Object.freeze({
      txHash: null,
    });
  }

  return null;
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
      lastError = normalizeRelayExecutionFailure(e);

      if (!shouldContinueRelayExecution(lastError)) {
        throw lastError.error;
      }

      const reconciled = await reconcileRelayExecutionState({
        domainHandle: relay.domainHandle,
        petitionId,
        nullifier,
      });

      if (reconciled) {
        return reconciled;
      }
    }
  }

  if (lastError?.error) {
    throw lastError.error;
  }

  throw new Error("relay execution failed");
}

function freezeRelaySubmission(submission) {
  Object.freeze(submission.proof.pA);
  Object.freeze(submission.proof.pB[0]);
  Object.freeze(submission.proof.pB[1]);
  Object.freeze(submission.proof.pB);
  Object.freeze(submission.proof.pC);
  Object.freeze(submission.proof);
  Object.freeze(submission.pubSignals);
  Object.freeze(submission);

  return submission;
}

export async function executeRelaySubmission({
  executionDomains,
  submission,
}) {
  freezeRelaySubmission(submission);
  Object.freeze(executionDomains);

  return dispatchRelayExecution({
    executionDomains,
    submission,
  });
}
