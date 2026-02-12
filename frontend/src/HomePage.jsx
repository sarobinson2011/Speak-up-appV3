import './HomePage.css';

export default function HomePage({ onGetStarted }) {
  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Speak Up</h1>
          <p className="hero-tagline">Your Voice. Your Privacy. Your Power.</p>
          <p className="hero-subtitle">
            Anonymous petitions for <span className="highlight">EVERYONE</span>
          </p>
          <button className="cta-button" onClick={onGetStarted}>
            Get Started →
          </button>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="mission">
        <div className="container">
          <h2>Free Speech Without Fear</h2>
          <p className="lead">
            In a world where speaking truth can cost you everything - your job, your safety,
            your freedom - we believe <strong>every human deserves to be heard</strong>.
          </p>
          <p>
            Speak Up combines <strong>zero-knowledge cryptography</strong> with <strong>blockchain
              technology</strong> to create a truly anonymous petition platform.
            No government can silence you. No corporation can censor you. No one can trace you.
          </p>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <div className="container">
          <h2>How It Works</h2>
          <div className="features-grid">
            <div className="feature">
              <div className="feature-icon">🔐</div>
              <h3>Zero-Knowledge Proofs</h3>
              <p>
                Sign petitions <strong>completely anonymously</strong>. Our ZK technology
                proves you're a verified human without revealing who you are... not even to us.
              </p>
            </div>

            <div className="feature">
              <div className="feature-icon">⛓️</div>
              <h3>Blockchain Permanence</h3>
              <p>
                Every signature is recorded on <strong>Aurora blockchain</strong>. Once published,
                your voice cannot be deleted, altered, or censored by any authority.
              </p>
            </div>

            <div className="feature">
              <div className="feature-icon">🌍</div>
              <h3>Globally Accessible</h3>
              <p>
                No ID required. No location restrictions. If you can access the internet,
                you can make your voice heard in safety.
              </p>
            </div>

            <div className="feature">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Moderation</h3>
              <p>
                Advanced content filtering keeps spam out while protecting legitimate speech.
                We remove bots and abuse, not dissent.
              </p>
            </div>

            <div className="feature">
              <div className="feature-icon">✉️</div>
              <h3>Verified Humans Only</h3>
              <p>
                Email verification ensures one person = one signature, preventing manipulation
                while maintaining complete anonymity.
              </p>
            </div>

            <div className="feature">
              <div className="feature-icon">🔓</div>
              <h3>Open Source</h3>
              <p>
                Our code is public and auditable. Trust is built through transparency,
                not promises. Verify everything yourself.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Why It Matters */}
      <section className="why-matters">
        <div className="container">
          <h2>Why This Matters</h2>
          <div className="stats-grid">
            <div className="stat">
              <div className="stat-number">3.5B</div>
              <div className="stat-label">People live under authoritarian regimes</div>
            </div>
            <div className="stat">
              <div className="stat-number">180+</div>
              <div className="stat-label">Countries restrict freedom of speech</div>
            </div>
            <div className="stat">
              <div className="stat-number">∞</div>
              <div className="stat-label">Voices that deserve to be heard</div>
            </div>
          </div>

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

      {/* Technical Innovation */}
      <section className="technical">
        <div className="container">
          <h2>The Technology Behind Freedom</h2>
          <div className="tech-explainer">
            <div className="tech-item">
              <h3>🔬 Zero-Knowledge Proofs (Groth16)</h3>
              <p>
                When you sign a petition, our ZK circuit generates a cryptographic proof that
                you're a verified user - <strong>without revealing your identity, email, or wallet
                  address</strong>. Even the blockchain can't see who you are.
              </p>
            </div>

            <div className="tech-item">
              <h3>⛓️ Aurora Blockchain </h3>
              <p>
                Signatures are stored on Aurora, an ultra-fast Layer 2 built on NEAR Protocol.
                <strong> 1-2 second finality</strong>, <strong>virtually-zero gas fees</strong>, and
                <strong> MEV protection</strong> built-in. Your petition cannot be frontrun or censored.
              </p>
            </div>

            <div className="tech-item">
              <h3>📦 IPFS Decentralized Storage</h3>
              <p>
                Petition content lives on IPFS - a <strong>peer-to-peer network</strong> that
                can't be taken down by any single authority. If one node goes offline, thousands
                of others keep your voice alive.
              </p>
            </div>

            <div className="tech-item">
              <h3>🧠 GPT-4 Content Moderation</h3>
              <p>
                AI analyzes petition content to filter spam, abuse, and illegal content - while
                <strong> protecting legitimate dissent</strong>. Controversial no longer means prohibited.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="use-cases">
        <div className="container">
          <h2>Who Uses Speak Up?</h2>
          <div className="use-case-grid">
            <div className="use-case">
              <h3>🗳️ Activists</h3>
              <p>Organize movements without exposing supporters to retaliation</p>
            </div>
            <div className="use-case">
              <h3>💼 Whistleblowers</h3>
              <p>Expose corruption while protecting your career and safety</p>
            </div>
            <div className="use-case">
              <h3>🏛️ Dissidents</h3>
              <p>Challenge oppressive governments without risking imprisonment</p>
            </div>
            <div className="use-case">
              <h3>👥 Communities</h3>
              <p>Rally support for local causes without fear of harassment</p>
            </div>
            <div className="use-case">
              <h3>🌐 Global Citizens</h3>
              <p>Sign international petitions regardless of your location</p>
            </div>
            <div className="use-case">
              <h3>🔬 Researchers</h3>
              <p>Study public opinion with privacy-preserving cryptography</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="final-cta">
        <div className="container">
          <h2>Your Voice Matters</h2>
          <p>
            Join thousands using cryptography to protect their right to speak freely.
          </p>
          <button className="cta-button large" onClick={onGetStarted}>
            Start Speaking Up →
          </button>
          <p className="footnote">
            Built on Aurora • Powered by Zero-Knowledge • Free Forever
          </p>
        </div>
      </section>
    </div>
  );
}
