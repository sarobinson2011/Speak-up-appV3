// frontend/src/hooks/useZKProof.js
import { useState } from 'react';
import * as snarkjs from 'snarkjs';
import { poseidon1, poseidon2, poseidon3 } from 'poseidon-lite';

const FIELD =
  21888242871839275222246405745257275088548364400416034343698204186575808495617n;

const EXPECTED_DEPTH = 16;

function assertField(x, label) {
  const v = BigInt(x);
  if (v < 0n || v >= FIELD) throw new Error(`${label} out of field: ${x}`);
}

function isNil(x) {
  return x === undefined || x === null;
}

function normalizeInputs(maybePathObj, petitionId, memberSecretFallback) {
  const obj = maybePathObj || {};

  const memberSecretRaw = !isNil(obj.memberSecret) ? obj.memberSecret : memberSecretFallback;
  if (isNil(memberSecretRaw) || memberSecretRaw === '') {
    throw new Error('Missing memberSecret. Pass generateProof(pathObj, petitionId, memberSecret).');
  }

  const membershipRootRaw = !isNil(obj.membershipRoot) ? obj.membershipRoot : obj.root;
  if (isNil(membershipRootRaw) || membershipRootRaw === '') {
    throw new Error('Missing membership root (expected membershipRoot or root).');
  }

  const leafRaw = obj.leaf; // backend-provided leaf (if available)

  const membershipPathRaw = !isNil(obj.membershipPath) ? obj.membershipPath : obj.siblings;
  const membershipIndicesRaw = !isNil(obj.membershipIndices)
    ? obj.membershipIndices
    : obj.pathBits;

  if (!Array.isArray(membershipPathRaw)) {
    throw new Error('Missing membership path array (expected membershipPath or siblings).');
  }
  if (!Array.isArray(membershipIndicesRaw)) {
    throw new Error('Missing membership indices array (expected membershipIndices or pathBits).');
  }

  if (
    membershipPathRaw.length !== EXPECTED_DEPTH ||
    membershipIndicesRaw.length !== EXPECTED_DEPTH
  ) {
    throw new Error(
      `Membership proof depth mismatch: expected ${EXPECTED_DEPTH}, got siblings=${membershipPathRaw.length}, bits=${membershipIndicesRaw.length}.`
    );
  }

  const memberSecret = BigInt(memberSecretRaw);
  const membershipRoot = BigInt(membershipRootRaw);

  const leafFromBackend = !isNil(leafRaw) && leafRaw !== '' ? BigInt(leafRaw) : null;

  const membershipPath = membershipPathRaw.map((x, i) => {
    if (isNil(x) || x === '') throw new Error(`membershipPath[${i}] is missing`);
    return BigInt(x);
  });

  const membershipIndices = membershipIndicesRaw.map((b, i) => {
    if (isNil(b) || b === '') throw new Error(`membershipIndices[${i}] is missing`);
    const bi = BigInt(b);
    if (bi !== 0n && bi !== 1n) throw new Error(`membershipIndices[${i}] must be 0/1 (got ${b})`);
    return bi;
  });

  const petitionIdBI = BigInt(petitionId);

  return {
    memberSecret,
    membershipRoot,
    leafFromBackend,
    membershipPath,
    membershipIndices,
    petitionIdBI
  };
}

function computeRootFromPath({ leaf, siblings, bits }) {
  let cur = BigInt(leaf);

  for (let i = 0; i < EXPECTED_DEPTH; i++) {
    const sib = BigInt(siblings[i]);
    const b = BigInt(bits[i]);
    cur = b === 0n ? poseidon2([cur, sib]) : poseidon2([sib, cur]);
  }

  return cur;
}

function flipBits(bits) {
  return bits.map((b) => (b === 0n ? 1n : 0n));
}

function reverseArr(arr) {
  return [...arr].reverse();
}

function normalizeMerkleToMatchRoot({
  leafCircuit,
  membershipRoot,
  membershipPath,
  membershipIndices
}) {
  const candidates = [
    { name: 'as-is', siblings: membershipPath, bits: membershipIndices },
    { name: 'flip-bits', siblings: membershipPath, bits: flipBits(membershipIndices) },
    { name: 'reverse', siblings: reverseArr(membershipPath), bits: reverseArr(membershipIndices) },
    {
      name: 'reverse+flip',
      siblings: reverseArr(membershipPath),
      bits: flipBits(reverseArr(membershipIndices))
    }
  ];

  const computed = [];
  for (const c of candidates) {
    const root = computeRootFromPath({ leaf: leafCircuit, siblings: c.siblings, bits: c.bits });
    computed.push({ name: c.name, root });
    if (root === membershipRoot) {
      return { siblings: c.siblings, bits: c.bits, mode: c.name };
    }
  }

  const diag = computed.map((x) => `${x.name}: ${x.root.toString()}`).join('\n');
  throw new Error(
    `Merkle preflight failed: membershipPath/bits do not reproduce membershipRoot (even with 4 conventions).\n` +
      `membershipRoot: ${membershipRoot.toString()}\n` +
      `computed roots:\n${diag}\n` +
      `This indicates backend is serving a root/proof set from a different tree, or siblings/bits are not consistent with the root.`
  );
}

export function useZKProof() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function generateProof(membershipPathObj, petitionId, memberSecretFallback) {
    setLoading(true);
    setError(null);

    try {
      console.log('🔐 Generating ZK proof...');

      const {
        memberSecret,
        membershipRoot,
        leafFromBackend,
        membershipPath,
        membershipIndices,
        petitionIdBI
      } = normalizeInputs(membershipPathObj, petitionId, memberSecretFallback);

      // Circuit leaf definition is fixed:
      // leafCircuit = Poseidon(1)(memberSecret)
      const leafCircuit = poseidon1([memberSecret]);

      // If backend provides a leaf, it MUST equal the circuit leaf or the circuit can never pass.
      if (leafFromBackend !== null && leafFromBackend !== leafCircuit) {
        throw new Error(
          `Member secret mismatch: backend leaf != Poseidon1(memberSecret).\n` +
            `backend leaf: ${leafFromBackend.toString()}\n` +
            `poseidon1(secret): ${leafCircuit.toString()}\n` +
            `Fix: restore the original memberSecret for this wallet (localStorage) OR re-enroll membership using the currently stored memberSecret so the tree contains Poseidon1(secret).`
        );
      }

      // Normalize siblings/bits convention (4 deterministic attempts)
      const norm = normalizeMerkleToMatchRoot({
        leafCircuit,
        membershipRoot,
        membershipPath,
        membershipIndices
      });

      console.log(`✅ Merkle preflight matched root (mode=${norm.mode})`);

      // Nullifier per circuit: Poseidon(3)(memberSecret, petitionId, "SIGN")
      const SIGN_DOMAIN = 0x5349474en; // "SIGN"
      const nullifierBI = poseidon3([memberSecret, petitionIdBI, SIGN_DOMAIN]);
      const nullifierHex = '0x' + nullifierBI.toString(16).padStart(64, '0');

      console.log('Nullifier computed:', nullifierBI.toString());

      const input = {
        memberSecret: memberSecret.toString(),
        membershipPath: norm.siblings.map((x) => x.toString()),
        membershipIndices: norm.bits.map((x) => x.toString()),
        petitionId: petitionIdBI.toString(),
        membershipRoot: membershipRoot.toString()
      };

      const wasmPath = '/zk/sign_petition.wasm';
      const zkeyPath = '/zk/sign_petition_final.zkey';

      const { proof, publicSignals } = await snarkjs.groth16.fullProve(input, wasmPath, zkeyPath);

      console.log('✅ Proof generated successfully!');
      console.log('Public signals:', publicSignals);

      const vkeyResponse = await fetch('/zk/verification_key.json');
      const vkey = await vkeyResponse.json();

      const verified = await snarkjs.groth16.verify(vkey, publicSignals, proof);
      if (!verified) throw new Error('Local proof verification failed');

      console.log('✅ Local verification passed');

      const calldataStr = await snarkjs.groth16.exportSolidityCallData(proof, publicSignals);
      const argv = JSON.parse('[' + calldataStr.replace(/\b(\d+)\b/g, '"$1"') + ']');
      const [pA, pB, pC, pubSigs] = argv;

      [...pA, ...pB[0], ...pB[1], ...pC, ...pubSigs].forEach((x, idx) =>
        assertField(x, `arg[${idx}]`)
      );

      setLoading(false);

      return {
        proof: { pA, pB, pC, publicSignals: pubSigs },
        nullifier: nullifierHex,
        publicSignals: pubSigs
      };
    } catch (err) {
      console.error('ZK proof generation error:', err);
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }

  return { generateProof, loading, error };
}