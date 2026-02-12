Next work:
- Remove email verification flow; anchor membership to wallet address.
- Backend: replace verifiedEmails + memberSecrets keyed by email -> by wallet address.
- Frontend: replace JWT/email gating with wallet gating.
- Keep: Merkle tree + memberSecret persistence + M2 signed-state check.
