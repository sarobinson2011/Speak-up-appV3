# TEMPEST Treasury Continuity V1

## Purpose

Ensure relayers remain operational without manual intervention.

---

## Core Principle

Treasury funds continuity, not participation.

---

## Roles

### Relayers
- submit transactions
- do not request funding from users

### Watcher Bots
- monitor relay health
- detect gas thresholds

### Treasury
- funds relayers

---

## Funding Model

Threshold-based:

- if balance < X → top up to Y

---

## Bot Responsibilities

- poll relay health
- check gas balance
- detect nonce stalls
- trigger refill

---

## Forbidden

- funding based on user activity
- exposing submission volume for funding
- linking treasury behavior to user actions

---

## Privacy Guarantee

Funding decisions must be independent of:

- who used the system
- what action occurred
- which petition was signed