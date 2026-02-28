import './HomePage.css';

export default function HomePage({ onGetStarted }) {
  return (
    <div className="homepage">
      {/* Hero */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Speak Up</h1>
          <p className="hero-tagline">Anonymous petitions with on-chain verification.</p>
          <p className="hero-subtitle">
            Strong privacy by default, enforced by <span className="highlight">zero-knowledge proofs</span>.
          </p>
          <button className="cta-button" onClick={onGetStarted}>
            Get Started →
          </button>
        </div>
      </section>

      {/* Mission */}
      <section className="mission">
        <div className="container">
          <h2>Free Speech Without Fear</h2>
          <p className="lead">
            Speak Up is a petition platform designed for situations where attaching your identity to your speech
            creates real risk.
          </p>
          <p>
            Signatures are generated with <strong>client-side zero-knowledge proofs</strong> and verified
            <strong> on-chain</strong>. The chain enforces <strong>one signature per member per petition</strong>
            using a <strong>nullifier</strong>, not a wallet address.
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="how-it-works">
        <div className="container">
          <h2>How It Works</h2>

          <div className="features-grid">
            <div className="feature">
              <h3>Strong Privacy Signatures</h3>
              <p>
                You generate a ZK proof locally in the browser. The proof shows you are an eligible member,
                without revealing which member you are.
              </p>
            </div>

            <div className="feature">
              <h3>On-Chain Enforcement</h3>
              <p>
                The smart contract verifies the proof and enforces uniqueness using a nullifier.
                Once signed, you cannot sign the same petition again.
              </p>
            </div>

            <div className="feature">
              <h3>Permissionless Enrollment</h3>
              <p>
                Membership enrollment is on-chain and requires a small <strong>refundable bond</strong>.
                This is the MVP anti-sybil baseline and will evolve in later versions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Quote (kept) */}
      <section className="why-matters">
        <div className="container">
          <h2>On Liberty</h2>
          <div className="quote">
            <p>
              "The peculiar evil of silencing the expression of an opinion is that it robs
              the human race... If the opinion is right, they are deprived of the opportunity
              of exchanging error for truth; if wrong, they lose what is almost as great a
              benefit: the clearer perception of truth, produced by its collision with error."
            </p>
            <cite>- John Stuart Mill, On Liberty (1859)</cite>
          </div>
        </div>
      </section>

      {/* Tech stack */}
      <section className="technical">
        <div className="container">
          <h2>Technology</h2>
          <div className="tech-explainer">
            <div className="tech-item">
              <h3>Zero-Knowledge (Groth16)</h3>
              <p>
                Proofs are generated in the browser and verified on-chain. No email, no JWT, no attesters.
                Membership is proven without revealing identity.
              </p>
            </div>

            <div className="tech-item">
              <h3>Poseidon + Merkle Membership</h3>
              <p>
                Membership uses Poseidon hashing and a Merkle tree. The backend serves Merkle paths as a
                convenience indexer; it is not authoritative.
              </p>
            </div>

            <div className="tech-item">
              <h3>Aurora Testnet</h3>
              <p>
                Smart contracts run on Aurora testnet for the MVP. Proof verification and signature uniqueness
                are enforced by the chain.
              </p>
            </div>

            <div className="tech-item">
              <h3>Metadata</h3>
              <p>
                Petitions reference a metadata URI (e.g., IPFS). In the MVP baseline, the UI displays the URI
                directly (no heavy metadata pipeline yet).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="final-cta">
        <div className="container">
          <h2>Start a Petition. Sign with Strong Privacy.</h2>
          <p>Connect a wallet, enroll once, and sign with a ZK proof.</p>
          <button className="cta-button large" onClick={onGetStarted}>
            Open the App →
          </button>
          <p className="footnote">M2-only MVP • Groth16 • Poseidon • Aurora</p>
        </div>
      </section>
    </div>
  );
}