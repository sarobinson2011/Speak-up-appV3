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

console.log("tempest execution validation ok");
