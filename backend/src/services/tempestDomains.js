import { ethers } from "ethers";

function assertDomainConfig(domainConfig) {
  if (!domainConfig || typeof domainConfig !== "object") {
    throw new Error("Invalid TEMPEST domain configuration");
  }

  if (
    !domainConfig.rpcUrl ||
    !domainConfig.registryAddress ||
    !domainConfig.registryAbi ||
    !domainConfig.relayerPrivateKey
  ) {
    throw new Error("Invalid TEMPEST domain configuration");
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

  return {
    rpcUrl,
    registryAddress,
    provider,
    wallet,
    handle,
  };
}

export function buildTempestExecutionDomains({ domainConfigs }) {
  if (!Array.isArray(domainConfigs) || domainConfigs.length < 2) {
    throw new Error("Invalid TEMPEST domain configuration");
  }

  domainConfigs.forEach(assertDomainConfig);

  return domainConfigs.map((domainConfig) => buildDomain(domainConfig));
}
