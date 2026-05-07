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

export function buildTempestExecutionDomains({
  rpcUrl,
  registryAddress,
  registryAbi,
  relayerPrivateKey,
}) {
  if (!rpcUrl) {
    throw new Error("buildTempestExecutionDomains requires rpcUrl");
  }

  if (!registryAddress) {
    throw new Error("buildTempestExecutionDomains requires registryAddress");
  }

  if (!registryAbi) {
    throw new Error("buildTempestExecutionDomains requires registryAbi");
  }

  if (!relayerPrivateKey) {
    throw new Error("buildTempestExecutionDomains requires relayerPrivateKey");
  }

  return [
    buildDomain({
      rpcUrl,
      registryAddress,
      registryAbi,
      relayerPrivateKey,
    }),
    buildDomain({
      rpcUrl,
      registryAddress,
      registryAbi,
      relayerPrivateKey,
    }),
  ];
}
