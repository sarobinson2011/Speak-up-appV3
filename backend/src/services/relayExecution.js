export async function executeRelaySubmission({
  registry,
  petitionId,
  nullifier,
  admissionCommitment,
  pA,
  pB,
  pC,
  pubSignals,
}) {
  const tx = await registry.signPetitionWithZKProof(
    BigInt(petitionId),
    nullifier,
    admissionCommitment,
    pA,
    pB,
    pC,
    pubSignals
  );

  return {
    txHash: tx.hash,
  };
}
