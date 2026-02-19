ANTI_SYBIL_POLICY_V2.md
0) Purpose

Define a plug-and-play “Access Policy / Anti-Sybil” module for Speak-up-appV3 that determines whether a user action (sign/comment) is allowed and under what friction:

Refundable bond (baseline, permissionless)

Optional light PoW (adaptive throttle / burst defense)

Optional credentials (fast lane / low friction when available)

The module must be:

deterministic and testable

minimally subjective (no “spam detection” content moderation)

upgradeable without changing the core petition verification logic

1) Scope and non-goals
In scope

Gate decisioning for actions: SIGN, COMMENT

Bond requirements (amount, lock duration, refund conditions)

Optional PoW requirements (difficulty, verification)

Optional credential gates (ZK proof or attestation-based)

Objective “suspicion” scoring for adaptive friction

Events for indexing/auditing

Upgrade path

Non-goals

Content moderation or “truth” evaluation

Identity doxxing or wallet linking

Perfect Sybil resistance (impossible without strong identity primitives)

Off-chain ML/heuristics required for correctness

2) Terms

Actor: an entity attempting an action; may be represented by wallet, relayer identity, or credential subject.

Action: SIGN or COMMENT.

Context: the set of inputs used to compute policy (petitionId, action type, epoch, rate window, etc.).

Nullifier: protocol-level uniqueness primitive; stored separately by core contract to enforce one-per-(petition, actor secret).

Bond: refundable deposit held for a lock duration.

PoW: hashcash-style nonce puzzle.

Credential: a proof/attestation that grants lower friction access.

3) High-level architecture
3.1 Core contract responsibilities (unchanged)

Core petition contract remains responsible for:

verifying Groth16 proof

enforcing nullifier uniqueness

recording the action / emitting domain events

3.2 Policy module responsibilities

Policy module is responsible for:

deciding the required friction for an action attempt:

requiredBond

requiredPowDifficulty (optional)

gateTypeUsed

tracking bond lockups and refunds

tracking objective rate/abuse signals (without content inspection)

3.3 Integration pattern

Core contract calls policy module before finalizing action:

User submits ActionRequest including any bond/PoW/credential payloads.

Core verifies ZK proof & nullifier (or can invert order; see 10.1).

Core calls policy.evaluate(...) and then policy.consume(...).

If allowed, core finalizes action and emits domain events.

Policy emits policy events for analytics and future tuning.

4) Interfaces
   
4.1 Data structures:

enum ActionType { SIGN, COMMENT }

enum GateType {
  BOND_ONLY,          // default baseline
  BOND_PLUS_POW,      // baseline + throttle
  CREDENTIAL,         // low friction if credential satisfied
  CREDENTIAL_PLUS_POW // optional, for attack mode
}

struct ActionContext {
  uint256 petitionId;
  ActionType actionType;
  uint64  epoch;        // policy-defined epoch (e.g., day/week)
  bytes32 root;         // optional: merkle root / public input reference
  bytes32 nullifier;    // the nullifier for this action (public)
}

struct CredentialPayload {
  bytes   proof;        // opaque bytes (ZK proof or signature)
  bytes32 credentialId; // optional identifier (NOT identity); e.g. issuer/type hash
}

struct PowPayload {
  bytes32 challenge;    // computed challenge hash
  uint64  nonce;        // solution nonce
  uint32  difficulty;   // leading-zero bits or target index
}

struct EvaluateResult {
  bool    allowed;
  GateType gate;
  uint256 requiredBond;       // wei
  uint64  bondLockSeconds;    // lockup duration for refund eligibility
  uint32  requiredPowDifficulty;
  uint32  suspicionScore;     // 0..1000 (internal, evented)
  bytes32 reasonCode;         // e.g. "OK", "RATE", "BURST", "ATTACKMODE", etc.
}

struct ConsumeParams {
  uint256 bondPaid;           // msg.value sent or token transfer amount
  PowPayload pow;
  CredentialPayload cred;
}

4.2 Policy module functions

interface IAccessPolicyV2 {
  function evaluate(ActionContext calldata ctx, CredentialPayload calldata cred)
    external view returns (EvaluateResult memory);

  // Called by core once it is ready to commit the action.
  // Must revert if requirements not met (bond, pow, credential validity, etc.)
  function consume(ActionContext calldata ctx, ConsumeParams calldata params)
    external payable;

  // Refund flow for refundable bonds
  function claimRefund(bytes32 bondId) external;

  // Admin / governance tuning
  function setParams(PolicyParams calldata p) external;
  function setAttackMode(bool enabled) external;
}

4.3 Bond accounting primitives
struct BondPosition {
  address payer;
  uint256 amount;
  uint64  unlockAt;       // timestamp when refundable
  bool    claimed;
  bytes32 contextHash;    // hash of (petitionId, actionType, nullifier, epoch)
}


Bond positions are keyed by a deterministic bondId:

bondId = keccak256(abi.encodePacked(
  "BOND_V2",
  chainid,
  address(policy),
  ctx.petitionId,
  ctx.actionType,
  ctx.nullifier
));

5) Storage

Minimum on-chain storage needed to enforce objective anti-abuse:

5.1 Parameters
struct PolicyParams {
  // baseline economics
  uint256 baseBondSign;
  uint256 baseBondComment;

  // lockup
  uint64  baseLockSecondsSign;
  uint64  baseLockSecondsComment;

  // pow config
  bool    powEnabled;
  uint32  basePowDifficulty;         // e.g., bits
  uint32  maxPowDifficulty;

  // adaptive scaling knobs
  uint32  rateWindowSeconds;         // e.g., 60
  uint32  maxActionsPerWindow;       // e.g., 3 per window (system-wide or per petition)
  uint32  burstWindowSeconds;        // e.g., 10
  uint32  burstThreshold;            // e.g., N actions in 10s triggers attack mode

  // dynamic bond scaling
  uint32  bondMultiplierMin;         // e.g., 1000 = 1.0x (fixed-point)
  uint32  bondMultiplierMax;         // e.g., 5000 = 5.0x
  uint32  scoreToMultiplierK;        // mapping slope constant

  // credential gate
  bool    credentialEnabled;
  uint256 credentialBondDiscountBps; // e.g. 9000 => 90% off
  uint32  credentialPowDiscountBps;  // e.g. 10000 => 100% off
}

5.2 Rate / abuse counters (objective)

Pick one of two designs (start simple):

A) System-wide counters (cheapest, coarser)

mapping(uint64 windowId => uint32 count) public actionsInWindow;
mapping(uint64 burstId  => uint32 count) public actionsInBurst;


B) Per-petition counters (more targeted, more storage)

mapping(uint256 petitionId => mapping(uint64 windowId => uint32)) public actionsInWindowByPetition;
mapping(uint256 petitionId => mapping(uint64 burstId  => uint32)) public actionsInBurstByPetition;


Recommended: start with B for comments, A for sign, or do A first then upgrade.

5.3 Bond positions
mapping(bytes32 bondId => BondPosition) public bonds;

5.4 Attack mode flag
bool public attackMode;

6) Events

Emit enough for indexing, tuning, and transparency.

event PolicyEvaluated(
  uint256 indexed petitionId,
  ActionType indexed actionType,
  GateType gate,
  uint256 requiredBond,
  uint64  bondLockSeconds,
  uint32  requiredPowDifficulty,
  uint32  suspicionScore,
  bytes32 reasonCode
);

event BondPosted(
  bytes32 indexed bondId,
  address indexed payer,
  uint256 amount,
  uint64  unlockAt,
  bytes32 contextHash
);

event BondRefunded(
  bytes32 indexed bondId,
  address indexed payer,
  uint256 amount
);

event PowVerified(
  uint256 indexed petitionId,
  ActionType indexed actionType,
  uint32 difficulty,
  bytes32 challenge
);

event CredentialVerified(
  bytes32 indexed credentialId,
  uint256 indexed petitionId,
  ActionType indexed actionType
);

event ParamsUpdated(bytes32 indexed paramsHash);
event AttackModeChanged(bool enabled);

7) Gate types and behavior
7.1 Default: BOND_ONLY

Requires base bond for action type

No PoW unless attack mode or score threshold requires it

Bond refundable after lock

7.2 BOND_PLUS_POW

Requires bond and PoW

Used when suspicion score exceeds a threshold or attackMode = true

7.3 CREDENTIAL

If credential valid: bond discounted (possibly near-zero)

PoW discounted or removed

Must not reveal identity; only “valid credential” proof

7.4 CREDENTIAL_PLUS_POW

Used during attack mode to keep abuse expensive even with stolen/compromised credentials

8) Dynamic bond sizing
8.1 Motivation

Bond should act as a negative-feedback controller:

low friction under normal conditions

higher cost under spam/burst conditions

still refundable to preserve non-financial nature

8.2 Suspicion score → multiplier

Compute a suspicionScore in [0..1000].

Then:

mult = clamp(
  bondMultiplierMin,
  bondMultiplierMin + (suspicionScore * scoreToMultiplierK),
  bondMultiplierMax
)

requiredBond = baseBond(actionType) * mult / 1000


(Where multipliers are fixed-point with 1000 = 1.0×)

8.3 Lockup scaling (optional)

To penalize throughput without increasing money:

lockSeconds = baseLockSeconds * clamp(1, 1 + suspicionScore/500, 4)


This keeps it “refundable but time-expensive”.

9) Objective “suspicious” scoring (no subjective moderation)

The score must be based on system-measurable signals only.

9.1 Signals (all objective)

Use a weighted sum:

Global load (rate window)

rateCount = actionsInWindow[windowId]

score component increases when rateCount > maxActionsPerWindow

Burst detection

burstCount = actionsInBurst[burstId]

sharp score increase past burstThreshold

Petition-local concentration (if using per-petition counters)

high action density for one petition in short time window

Repeated invalid attempts (optional, objective)

if a caller repeatedly submits failing PoW / underpays bond, increment a per-address “failed attempts” counter with decay

note: this can be gamed with many addresses, so keep weight small

9.2 Example scoring formula

(Concrete and implementable)

score = 0

// rate window penalty
if rateCount > maxActionsPerWindow:
  score += min(400, 20 * (rateCount - maxActionsPerWindow))

// burst penalty
if burstCount > burstThreshold:
  score += min(600, 60 * (burstCount - burstThreshold))

// petition-local (optional)
if petitionRateCount > petitionMax:
  score += min(400, 25 * (petitionRateCount - petitionMax))

// clamp
score = min(score, 1000)

9.3 Mapping score to gate selection

If attackMode = true → require PoW (at least basePowDifficulty)

Else if score >= POW_THRESHOLD_SCORE → require PoW

Else bond only

Recommended thresholds:

POW_THRESHOLD_SCORE = 300 (tunable)

PoW difficulty can scale with score:

requiredPowDifficulty = clamp(
  basePowDifficulty,
  basePowDifficulty + (score / 50),
  maxPowDifficulty
)

10) PoW design (lightweight, verifiable)
10.1 Challenge definition

Bind PoW to context so it can’t be replayed elsewhere:

challenge = keccak256(abi.encodePacked(
  "POW_V2",
  chainid,
  address(policy),
  ctx.petitionId,
  ctx.actionType,
  ctx.nullifier,
  ctx.epoch
));

10.2 Verification rule

Check hash of (challenge || nonce) meets difficulty target:

Leading-zero bits ≥ difficulty, OR

uint256(hash) < target(difficulty)

Simple leading-zero bits is easiest.

10.3 When PoW is required

only in BOND_PLUS_POW or CREDENTIAL_PLUS_POW

default off unless score/attack mode triggers it

11) Credential gate (optional fast lane)
11.1 Credential requirements

A credential must prove membership/uniqueness without identity disclosure, e.g.:

university-issued anon credential

privacy-preserving proof-of-personhood primitive

The policy module only needs a boolean: credentialValid.

11.2 Pluggable verifier

Credential validity can be provided by:

a ZK verifier contract (e.g., Groth16)

an ECDSA signature verifier against an issuer public key

an attestation registry contract

Keep it modular:

interface ICredentialVerifier {
  function verify(CredentialPayload calldata cred, ActionContext calldata ctx)
    external view returns (bool ok, bytes32 credentialId);
}


Policy holds an address credentialVerifier (upgradeable).

12) Upgrade path
12.1 Versioning

Policy module deployed behind proxy (TransparentUpgradeableProxy).

Core contract depends on interface IAccessPolicyV2 (stable).

12.2 Safe upgrades

Add new gate types without changing existing ones.

Add new scoring signals carefully (avoid breaking UX).

Maintain event compatibility; add new events if needed.

12.3 Migration considerations

If moving from system-wide to per-petition counters, keep old mappings but stop writing them; new logic reads new mappings.

Bond positions must remain claimable across upgrades (don’t change bondId derivation).

13) Testing checklist (must pass)

Baseline path: normal load → bond only, no PoW.

Refund path: post bond → after unlockAt → refund succeeds; before unlockAt → refund reverts.

PoW path: under attack mode/score threshold → PoW required; invalid nonce fails.

Dynamic bond: higher rateCount/burstCount increases bond multiplier deterministically.

Replay resistance: PoW challenge cannot be reused across petition/action/epoch.

Credential discount: valid credential reduces bond and/or PoW as configured.

No subjectivity: scoring uses only counters + deterministic rules.

14) Recommended initial V2 parameters (starting point)

baseBondSign: small (enough to matter, not punitive)

baseBondComment: 2–5× sign (comments are higher abuse surface)

baseLockSecondsSign: 1–24 hours (choose based on UX)

baseLockSecondsComment: 1–7 days (discourage comment spam)

powEnabled: true but conditional only

basePowDifficulty: tuned to ~0.5–2s on typical laptop

attackMode: off by default; can be toggled on if needed

rateWindowSeconds: 60, maxActionsPerWindow: set per expected traffic

burstWindowSeconds: 10, burstThreshold: low-ish to detect floods

(Exact numbers should be calibrated once you have traffic assumptions.)

15) Notes on ordering (evaluate vs verify proof)

Two valid sequences:

Option A (cost-saving): Policy gating first

if user can’t satisfy bond/PoW, reject before expensive ZK verify (if ZK verify is on-chain and expensive)

Option B (integrity-first): ZK verify first

avoids policy being probed cheaply with junk requests

useful if policy actions depend on nullifier/root that come from a verified proof

Either is acceptable; pick based on gas/attack surface.