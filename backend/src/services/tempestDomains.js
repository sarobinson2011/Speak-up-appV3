import { ethers } from "ethers";

export function buildTempestExecutionDomains({
  registryAddress,
  registryAbi,
  wallet,
}) {
  if (!registryAddress) {
    throw new Error("buildTempestExecutionDomains requires registryAddress");
  }

  if (!registryAbi) {
    throw new Error("buildTempestExecutionDomains requires registryAbi");
  }

  if (!wallet) {
    throw new Error("buildTempestExecutionDomains requires wallet");
  }

  const primaryDomainHandle = new ethers.Contract(
    registryAddress,
    registryAbi,
    wallet
  );

  const secondaryDomainHandle = new ethers.Contract(
    registryAddress,
    registryAbi,
    wallet
  );

  return [
    {
      handle: primaryDomainHandle,
    },
    {
      handle: secondaryDomainHandle,
    },
  ];
}
