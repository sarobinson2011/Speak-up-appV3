import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL, BACKEND_URL } from './config';
import { M2SignButton } from './components/M2SignButton';
import './PetitionDetails.css';

export default function PetitionDetails({ petitionId, signer, verifiedEmail, memberSecret, onBack }) {
  const [petition, setPetition] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [userSigned, setUserSigned] = useState(false);
  const [signatureCount, setSignatureCount] = useState(0);

  useEffect(() => {
    loadPetitionDetails();
  }, [petitionId]);

  async function loadPetitionDetails() {
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
      
      // Load petition data from blockchain
      const petitionData = await registry.getPetition(petitionId);
      setPetition(petitionData);
      
      // Load metadata from backend/IPFS
      try {
        const metadataResponse = await fetch(`${BACKEND_URL}/api/petition/${petitionId}`);
        if (metadataResponse.ok) {
          const metadataData = await metadataResponse.json();
          setMetadata(metadataData);
        } else {
          // Fallback for old petitions without metadata
          console.warn('No metadata found, using fallback');
          setMetadata({
            petitionId: petitionId,
            title: `Petition #${petitionId}`,
            description: 'No description available (petition created before metadata storage was implemented)',
            category: 'Unknown',
            target: 'Unknown',
            goalSignatures: 100,
            createdAt: new Date(Number(petitionData.createdAt) * 1000).toISOString()
          });
        }
      } catch (metadataError) {
        console.error('Error loading metadata:', metadataError);
        // Fallback for old petitions
        setMetadata({
          petitionId: petitionId,
          title: `Petition #${petitionId}`,
          description: 'No description available',
          category: 'Unknown',
          target: 'Unknown',
          goalSignatures: 100,
          createdAt: new Date(Number(petitionData.createdAt) * 1000).toISOString()
        });
      }
      
      // Load signature count
      const filter = registry.filters.PetitionSigned(petitionId);
      const events = await registry.queryFilter(filter);
      setSignatureCount(events.length);
      
      // Check if user signed
      if (memberSecret) {
        const nullifier = ethers.keccak256(
          ethers.solidityPacked(
            ['bytes32', 'uint256', 'string'],
            [memberSecret, petitionId, 'SIGN']
          )
        );
        const signed = await registry.hasSignedPetition(petitionId, nullifier);
        setUserSigned(signed);
      }
      
      // Load comments
      loadComments();
    } catch (error) {
      console.error('Error loading petition details:', error);
    }
  }

  async function loadComments() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/petition/${petitionId}/comments`);
      const data = await response.json();
      setComments(data.comments || []);
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  }

  async function signPetition() {
    setLoading(true);
    try {
      const nullifier = ethers.keccak256(
        ethers.solidityPacked(
          ['bytes32', 'uint256', 'string'],
          [memberSecret, petitionId, 'SIGN']
        )
      );

      const response = await fetch(`${BACKEND_URL}/api/petition/sign-permit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ petitionId, nullifier, email: verifiedEmail })
      });

      const { authData } = await response.json();

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registry.signPetition(petitionId, nullifier, authData, {
        gasLimit: 100000
      });
      await tx.wait();

      alert('Petition signed anonymously!');
      loadPetitionDetails();
    } catch (error) {
      console.error('Error signing petition:', error);
      if (error.message.includes('NullifierAlreadyUsed')) {
        alert('You already signed this petition!');
      } else {
        alert('Failed to sign petition: ' + error.message);
      }
    }
    setLoading(false);
  }

  async function postComment() {
    if (!newComment.trim()) {
      alert('Please enter a comment');
      return;
    }

    setLoading(true);
    try {
      const nullifier = ethers.keccak256(
        ethers.solidityPacked(
          ['bytes32', 'uint256', 'string'],
          [memberSecret, petitionId, 'COMMENT']
        )
      );

      const response = await fetch(`${BACKEND_URL}/api/petition/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          petitionId, 
          nullifier, 
          commentText: newComment,
          email: verifiedEmail 
        })
      });

      const data = await response.json();

      if (!data.approved) {
        alert(`Comment rejected: ${data.reason}`);
        setLoading(false);
        return;
      }

      const { commentHash, authData } = data;

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registry.commentOnPetition(petitionId, nullifier, commentHash, authData, {
        gasLimit: 250000
      });
      await tx.wait();

      alert('Comment posted anonymously!');
      setNewComment('');
      loadComments();
    } catch (error) {
      console.error('Error posting comment:', error);
      if (error.message.includes('NullifierAlreadyUsed')) {
        alert('You already commented on this petition!');
      } else {
        alert('Failed to post comment: ' + error.message);
      }
    }
    setLoading(false);
  }

  if (!petition || !metadata) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div>⏳ Loading petition details...</div>
      </div>
    );
  }

  const progress = metadata.goalSignatures > 0 
    ? Math.min((signatureCount / metadata.goalSignatures) * 100, 100) 
    : 0;

  return (
    <div>
      {/* Back Button */}
      <button 
        onClick={onBack}
        className="back-button"
      >
        ← Back to All Petitions
      </button>

      {/* Petition Header */}
      <div className="petition-detail-header">
        <div className="detail-title-row">
          <h2 className="detail-title">{metadata.title}</h2>
          {userSigned && (
            <span className="signed-badge">
              ✓ You signed this
            </span>
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
            <div className="meta-value">
              {new Date(metadata.createdAt).toLocaleDateString()}
            </div>
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
          <p className="description-text">
            {metadata.description}
          </p>
        </div>

        {/* Progress Bar */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <strong style={{ fontSize: '1.3rem', color: '#667eea' }}>
              {signatureCount.toLocaleString()} signatures
            </strong>
            <span style={{ color: '#666' }}>
              Goal: {metadata.goalSignatures.toLocaleString()}
            </span>
          </div>
          <div style={{ 
            width: '100%', 
            height: '20px', 
            background: '#e0e0e0', 
            borderRadius: '10px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              width: `${progress}%`, 
              height: '100%', 
              background: progress >= 100 ? '#4CAF50' : '#667eea',
              transition: 'width 0.3s ease'
            }} />
          </div>
          <small style={{ color: '#666' }}>
            {progress.toFixed(1)}% of goal reached
          </small>
        </div>

        {/* Sign Buttons - M2 INTEGRATION */}
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          gap: '12px',
          marginTop: '24px' 
        }}>
          {/* Standard Privacy Button */}
          <button
            onClick={signPetition}
            disabled={loading || userSigned}
            style={{
              padding: '16px 32px',
              fontSize: '18px',
              fontWeight: 'bold',
              border: 'none',
              borderRadius: '8px',
              background: userSigned ? '#ccc' : '#667eea',
              color: 'white',
              cursor: userSigned ? 'not-allowed' : 'pointer',
              transition: 'background 0.3s'
            }}
          >
            {userSigned ? '✓ Already Signed' : '📝 Sign This Petition (Standard)'}
          </button>

          {/* M2 Strong Privacy Button */}
          <M2SignButton 
            petitionId={petitionId}
            onSuccess={(result) => {
              console.log('M2 signature successful:', result);
              alert(`Signed anonymously with ZK proof!\nTransaction: ${result.txHash.slice(0, 10)}...`);
              loadPetitionDetails();
            }}
            onError={(error) => {
              alert('M2 signing failed: ' + error.message);
            }}
          />

          {/* Privacy Info */}
          <div style={{
            fontSize: '14px',
            color: '#666',
            marginTop: '8px',
            padding: '12px',
            background: '#f3f4f6',
            borderRadius: '6px'
          }}>
            <strong>🔐 Strong Privacy Mode:</strong> Uses zero-knowledge proofs to sign anonymously.
            Your signature is completely private - even we can't link it to you!
          </div>
        </div>
      </div>

      {/* Comments Section */}
      <div className="comments-card">
        <h3 className="comments-title">
          Comments ({comments.length})
        </h3>

        {/* Comment Input */}
        <div className="comment-input-section">
          <textarea
            placeholder="Share your thoughts on this petition..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="comment-textarea"
          />
          <button 
            onClick={postComment} 
            disabled={loading}
            className="post-comment-button btn-primary"
          >
            {loading ? 'Posting...' : 'Post Comment Anonymously'}
          </button>
        </div>

        {/* Comments List */}
        <div>
          {comments.length > 0 ? (
            comments.map((comment, idx) => (
              <div key={idx} style={{ 
                background: '#f9f9f9', 
                padding: '1.5rem', 
                marginBottom: '1rem',
                borderRadius: '4px',
                borderLeft: '4px solid #667eea'
              }}>
                <p style={{ margin: '0 0 0.75rem 0', lineHeight: '1.6' }}>
                  {comment.text}
                </p>
                <small style={{ color: '#666' }}>
                  Posted {new Date(comment.timestamp).toLocaleString()}
                </small>
              </div>
            ))
          ) : (
            <p style={{ 
              textAlign: 'center', 
              color: '#999', 
              fontStyle: 'italic',
              padding: '2rem'
            }}>
              No comments yet. Be the first to share your thoughts!
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
