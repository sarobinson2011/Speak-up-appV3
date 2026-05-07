import { ethers } from "ethers";

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
  if (!Array.isArray(domainConfigs) || domainConfigs.length === 0) {
    throw new Error("buildTempestExecutionDomains requires domainConfigs");
  }

  return domainConfigs.map((domainConfig) => buildDomain(domainConfig));
}
