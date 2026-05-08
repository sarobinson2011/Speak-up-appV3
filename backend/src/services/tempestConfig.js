export const TEMPEST_SLOT_COUNT = 7;

export const TEMPEST_RELAY_SLOTS = Object.freeze([
  Object.freeze({ id: 0, type: "primary" }),
  Object.freeze({ id: 1, type: "primary" }),
  Object.freeze({ id: 2, type: "primary" }),
  Object.freeze({ id: 3, type: "primary" }),
  Object.freeze({ id: 4, type: "primary" }),
  Object.freeze({ id: 5, type: "primary" }),
  Object.freeze({ id: 6, type: "primary" }),
]);

export const TEMPEST_PRIMARY_DOMAIN_MAX_SLOT = 3;

export function getTempestDomainIndexForSlot(slotIndex) {
  return slotIndex <= TEMPEST_PRIMARY_DOMAIN_MAX_SLOT ? 0 : 1;
}

// Keep existing env name for compatibility.
// Do not expose this terminology outside internal simulation config.
export const TEMPEST_CONTROLLED_FAILURE_ENV = "TEMPEST_FAIL_EXECUTOR_B";

export const TEMPEST_PERMUTATION_MULTIPLIER = 1103515245n;
export const TEMPEST_PERMUTATION_INCREMENT = 12345n;
export const TEMPEST_PERMUTATION_MASK = (1n << 64n) - 1n;
