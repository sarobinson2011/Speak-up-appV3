async function dispatchRelayExecution({
  registry,
  submission,
}) {
  const {
    petitionId,
    nullifier,
    proof,
    pubSignals,
    admissionCommitment,
  } = submission;

  const tx = await registry.signPetitionWithZKProof(
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
