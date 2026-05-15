import assert from "assert";

import {
  executeRelaySubmission,
} from "./relayExecution.js";

import {
  assertTempestExecutionTopology,
} from "./tempestDomains.js";

const ZERO =
  "0x0000000000000000000000000000000000000000000000000000000000000000";

function makeSubmission() {
  return {
    petitionId: "1",
    nullifier:
      "0x1111111111111111111111111111111111111111111111111111111111111111",
    proof: {
      pA: [ZERO, ZERO],
      pB: [
        [ZERO, ZERO],
        [ZERO, ZERO],
      ],
      pC: [ZERO, ZERO],
    },
    pubSignals: [
      "0x1111111111111111111111111111111111111111111111111111111111111111",
      "0x01",
      ZERO,
    ],
    admissionCommitment: ZERO,
  };
}

function makeWorkingHandle(label, calls) {
  return {
    async signPetitionWithZKProof() {
      calls.push(label);
      return { hash: `0x${"ab".repeat(32)}` };
    },
  };
}

function makeFailingHandle(label, calls) {
  return {
    async signPetitionWithZKProof() {
      calls.push(label);
      throw new Error("TEMPEST controlled execution failure");
    },
  };
}


function makeErrorHandle(label, calls, error) {
  return {
    async signPetitionWithZKProof() {
      calls.push(label);
      throw error;
    },
  };
}


function makeReconcilingFailureHandle(label, calls, alreadyRecorded) {
  return {
    async signPetitionWithZKProof() {
      calls.push(`${label}:submit`);
      throw Object.assign(new Error("network unavailable"), {
        code: "NETWORK_ERROR",
      });
    },

    async hasSignedPetition() {
      calls.push(`${label}:reconcile`);
      return alreadyRecorded;
    },
  };
}

function makeDomain(handle) {
  return Object.freeze({
    provider: {},
    wallet: {},
    handle,
    health: Object.freeze({ usable: true }),
  });
}

const calls = [];

const result = await executeRelaySubmission({
  executionDomains: Object.freeze([
    makeDomain(makeFailingHandle("a", calls)),
    makeDomain(makeWorkingHandle("b", calls)),
  ]),
  submission: makeSubmission(),
});

assert.strictEqual(result.txHash, `0x${"ab".repeat(32)}`);
assert(calls.length >= 2);

assert.throws(
  () =>
    assertTempestExecutionTopology([
      makeDomain(makeWorkingHandle("a", [])),
      Object.freeze({
        provider: {},
        wallet: {},
        handle: {},
        health: Object.freeze({ usable: false }),
      }),
    ]),
  /Invalid TEMPEST execution topology/,
);

const builtDomain = makeDomain(makeWorkingHandle("frozen", []));
assert(Object.isFrozen(builtDomain));
assert(Object.isFrozen(builtDomain.health));



const transportCalls = [];

const transportResult = await executeRelaySubmission({
  executionDomains: Object.freeze([
    makeDomain(
      makeErrorHandle(
        "transport-a",
        transportCalls,
        Object.assign(new Error("network unavailable"), {
          code: "NETWORK_ERROR",
        }),
      ),
    ),
    makeDomain(makeWorkingHandle("transport-b", transportCalls)),
  ]),
  submission: makeSubmission(),
});

assert.strictEqual(transportResult.txHash, `0x${"ab".repeat(32)}`);
assert(transportCalls.length >= 2);

const revertCalls = [];

await assert.rejects(
  () =>
    executeRelaySubmission({
      executionDomains: Object.freeze([
        makeDomain(
          makeErrorHandle(
            "revert-a",
            revertCalls,
            Object.assign(new Error("execution reverted"), {
              code: "CALL_EXCEPTION",
            }),
          ),
        ),
        makeDomain(makeWorkingHandle("revert-b", revertCalls)),
      ]),
      submission: makeSubmission(),
    }),
  /execution reverted/,
);

assert.deepStrictEqual(revertCalls, ["revert-a"]);

const unclassifiedCalls = [];

await assert.rejects(
  () =>
    executeRelaySubmission({
      executionDomains: Object.freeze([
        makeDomain(
          makeErrorHandle(
            "unknown-a",
            unclassifiedCalls,
            new Error("unexpected execution boundary failure"),
          ),
        ),
        makeDomain(makeWorkingHandle("unknown-b", unclassifiedCalls)),
      ]),
      submission: makeSubmission(),
    }),
  /unexpected execution boundary failure/,
);

assert.deepStrictEqual(unclassifiedCalls, ["unknown-a"]);




const reconciledCalls = [];

const reconciledResult = await executeRelaySubmission({
  executionDomains: Object.freeze([
    makeDomain(makeReconcilingFailureHandle("reconciled-a", reconciledCalls, true)),
    makeDomain(makeWorkingHandle("reconciled-b", reconciledCalls)),
  ]),
  submission: makeSubmission(),
});

assert.deepStrictEqual(reconciledResult, { txHash: null });
assert.deepStrictEqual(reconciledCalls, [
  "reconciled-a:submit",
  "reconciled-a:reconcile",
]);

const unreconciledCalls = [];

const unreconciledResult = await executeRelaySubmission({
  executionDomains: Object.freeze([
    makeDomain(makeReconcilingFailureHandle("unreconciled-a", unreconciledCalls, false)),
    makeDomain(makeWorkingHandle("unreconciled-b", unreconciledCalls)),
  ]),
  submission: makeSubmission(),
});

assert.strictEqual(unreconciledResult.txHash, `0x${"ab".repeat(32)}`);
assert.deepStrictEqual(unreconciledCalls, [
  "unreconciled-a:submit",
  "unreconciled-a:reconcile",
  "unreconciled-b",
]);


console.log("tempest execution validation ok");
