export function PetitionDisplaySection({
  metadata,
  petition,
  signatureCount,
  resolvedHasSignedM2,
  indexerLagBlocks = null
}) {
  const progress =
    metadata.goalSignatures > 0
      ? Math.min((signatureCount / metadata.goalSignatures) * 100, 100)
      : 0;

  return (
    <div className="petition-detail-header">
      <div className="detail-title-row">
        <h2 className="detail-title">{metadata.title}</h2>
        {resolvedHasSignedM2 && (
          <span className="signed-badge">✓ You signed this (strong privacy)</span>
        )}
      </div>

      <div className="meta-grid">
        <div className="meta-item">
          <small className="meta-label">Category</small>
          <div className="meta-value">{metadata.category}</div>
        </div>
        <div className="meta-item">
          <small className="meta-label">Target</small>
          <div className="meta-value">{metadata.target || 'Public'}</div>
        </div>
        <div className="meta-item">
          <small className="meta-label">Created</small>
          <div className="meta-value">{new Date(metadata.createdAt).toLocaleDateString()}</div>
        </div>
        <div className="meta-item">
          <small className="meta-label">Creator</small>
          <div className="meta-value" style={{ fontSize: '0.85rem' }}>
            {petition.creator.slice(0, 10)}...
          </div>
        </div>
      </div>

      <div className="description-section">
        <h3>Description</h3>
        <p className="description-text">{metadata.description}</p>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <div>
            <strong style={{ fontSize: '1.3rem', color: '#667eea' }}>
              {signatureCount.toLocaleString()} signatures
            </strong>
            {indexerLagBlocks > 0 && (
              <div style={{ fontSize: '0.85rem', color: '#999', marginTop: '0.2rem' }}>
                Updating read model… {indexerLagBlocks} block{indexerLagBlocks === 1 ? '' : 's'} behind
              </div>
            )}
          </div>
          <span style={{ color: '#666' }}>Goal: {metadata.goalSignatures.toLocaleString()}</span>
        </div>

        <div
          style={{
            width: '100%',
            height: '20px',
            background: '#e0e0e0',
            borderRadius: '10px',
            overflow: 'hidden'
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              background: progress >= 100 ? '#4CAF50' : '#667eea',
              transition: 'width 0.3s ease'
            }}
          />
        </div>

        <small style={{ color: '#666' }}>{progress.toFixed(1)}% of goal reached</small>
      </div>
    </div>
  );
}