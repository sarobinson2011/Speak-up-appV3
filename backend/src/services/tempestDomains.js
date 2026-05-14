import { ethers } from "ethers";
import { TEMPEST_SLOT_COUNT, getTempestDomainIndexForSlot } from "./tempestConfig.js";

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isPrivateKey(value) {
  return typeof value === "string" && /^0x[0-9a-fA-F]{64}$/.test(value);
}

function assertDomainConfig(domainConfig) {
  if (!domainConfig || typeof domainConfig !== "object") {
    throw new Error("Invalid TEMPEST execution configuration");
  }

  const {
    rpcUrl,
    registryAddress,
    registryAbi,
    relayerPrivateKey,
  } = domainConfig;

  if (!isNonEmptyString(rpcUrl)) {
    throw new Error("Invalid TEMPEST execution RPC configuration");
  }

  if (!ethers.isAddress(registryAddress)) {
    throw new Error("Invalid TEMPEST execution registry configuration");
  }

  if (!Array.isArray(registryAbi) || registryAbi.length === 0) {
    throw new Error("Invalid TEMPEST execution ABI configuration");
  }

  if (!isPrivateKey(relayerPrivateKey)) {
    throw new Error("Invalid TEMPEST execution signer configuration");
  }
}

function buildDomain({
  rpcUrl,
  registryAddress,
  registryAbi,
  relayerPrivateKey,
}) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(relayerPrivateKey, provider);

  const handle = new ethers.Contract(
    registryAddress,
    registryAbi,
    wallet
  );

  return Object.freeze({
    rpcUrl,
    registryAddress,
    provider,
    wallet,
    handle,
    health: Object.freeze({
      usable: true,
    }),
  });
}

function isUsableExecutionDomain(domain) {
  return Boolean(
    domain &&
    domain.provider &&
    domain.wallet &&
    domain.handle &&
    typeof domain.handle.signPetitionWithZKProof === "function"
  );
}

export function getTempestExecutionReadiness(executionDomains) {
  if (!Array.isArray(executionDomains) || executionDomains.length < 2) {
    return {
      usable: false,
      usableCount: 0,
    };
  }

  const usableCount = executionDomains.filter(isUsableExecutionDomain).length;

  return {
    usable: usableCount >= 1,
    usableCount,
  };
}

export function assertTempestExecutionTopology(executionDomains) {
  if (!Array.isArray(executionDomains) || executionDomains.length < 2) {
    throw new Error("Invalid TEMPEST execution topology");
  }

  for (let slotIndex = 0; slotIndex < TEMPEST_SLOT_COUNT; slotIndex += 1) {
    const domainIndex = getTempestDomainIndexForSlot(slotIndex);

    if (
      !Number.isInteger(domainIndex) ||
      domainIndex < 0 ||
      domainIndex >= executionDomains.length ||
      !isUsableExecutionDomain(executionDomains[domainIndex])
    ) {
      throw new Error("Invalid TEMPEST execution topology");
    }
  }
}

export function buildTempestExecutionDomains({ domainConfigs }) {
  if (!Array.isArray(domainConfigs) || domainConfigs.length < 2) {
    throw new Error("Invalid TEMPEST execution configuration");
  }

  domainConfigs.forEach(assertDomainConfig);

  const registryAddress = domainConfigs[0].registryAddress.toLowerCase();

  for (const domainConfig of domainConfigs) {
    if (domainConfig.registryAddress.toLowerCase() !== registryAddress) {
      throw new Error("Invalid TEMPEST execution registry equivalence");
    }
  }

  const executionDomains = domainConfigs.map((domainConfig) => buildDomain(domainConfig));

  assertTempestExecutionTopology(executionDomains);

  return Object.freeze(executionDomains);
}
