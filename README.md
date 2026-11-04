# Speak Up

Speak Up is a privacy-preserving petition application built around the Privacy Engine’s principle of **private actors, public actions**. The engine is designed to let an eligible member prove that an action is valid while keeping the membership secret private. Speak Up applies that design to petitions. It generates a Groth16 proof in the browser, uses a per-petition nullifier to prevent repeat signing, and relies on on-chain verification. Indexing, proof-path delivery and relaying support that flow.

## Project status

The application has a recorded M2-only Aurora testnet baseline. The Privacy Engine’s parameterized Generation 4 definition is accepted at the reviewed definition scope. The Generation 4 implementation evidence here is source-only and laboratory scoped. Final model binding and readiness remain blocked, and admission remains disabled. The threat model describes the assumptions behind privacy, including secret custody and the limits of relaying and path distribution.

## Try a local example

With Git and Node.js 22 available, clone the repository and run the checked-in REFLECT publication-object fixture from the checkout root.

    git clone https://github.com/sarobinson2011/Speak-up-appV3.git
    cd Speak-up-appV3
    node backend/src/services/reflect/publicationObjects.test.js

Expected output is `reflect publication object validation ok` with exit code 0. The fixture uses Node’s built-ins and local modules, and exercises publication objects and proof-path reconstruction without a service, wallet or database. The command and expected result are derived from the source and retained validation record. This documentation review did not rerun it.

## Explore or contribute

- [STATE.md](STATE.md) is authoritative for architecture, invariants and project status.
- [Privacy Engine design](docs/PRIVACY_ENGINE_DEFINITION.md), [threat model](docs/PRIVACY_THREAT_MODEL.md) and [accepted G4 definition baseline](docs/privacy-engine/generation-004/accepted-definition/engineering-287/README.md).
- [Developer guide](docs/DEVELOPER_GUIDE.md) covers implementation entry points, request shapes, examples, evidence and contributions.
- [Report a problem or discuss a change](https://github.com/sarobinson2011/Speak-up-appV3/issues). Include the commit, environment and a reproducible example.
- [Licensing and third-party terms](docs/LICENSING.md).

Development and scoped verification are human-directed and AI-assisted. Formal-Lab is a separate review role within that workflow. The checkpoint records identify reviewer provenance and the scope of each check.

## Tip jar

I’m building this to help people. If it’s helped you, taught you something, or you just like what I’m doing, then please feel free to chuck a little ETH in the jar.  Many thanks.

Using it, sharing it, or helping improve it is also appreciated. 👍

**Native ETH on Ethereum mainnet, Base mainnet or Arbitrum One.** Use the same receiving address on any of these networks:

`0x8cA41B152eDA1C8c4F9df9AF98E07888EDc17416`
