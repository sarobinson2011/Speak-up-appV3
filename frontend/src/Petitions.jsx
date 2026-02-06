import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL, BACKEND_URL } from './config';
import PetitionDetails from './PetitionDetails';
import './Petitions.css';

export default function Petitions({ signer, account, verifiedEmail }) {
  const [petitions, setPetitions] = useState([]);
  const [newPetitionTitle, setNewPetitionTitle] = useState('');
  const [newPetitionDescription, setNewPetitionDescription] = useState('');
  const [newPetitionCategory, setNewPetitionCategory] = useState('General');
  const [newPetitionTarget, setNewPetitionTarget] = useState('');
  const [newPetitionGoal, setNewPetitionGoal] = useState(100);
  const [loading, setLoading] = useState(false);
  const [loadingPetitions, setLoadingPetitions] = useState(true);
  const [memberSecret, setMemberSecret] = useState('');
  const [selectedPetition, setSelectedPetition] = useState(null);
  const [viewingPetitionId, setViewingPetitionId] = useState(null);
  const [comments, setComments] = useState({});
  const [newComment, setNewComment] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [expandedPetition, setExpandedPetition] = useState(null);

  const CATEGORIES = [
    'General',
    'Environment',
    'Politics',
    'Social Justice',
    'Technology',
    'Education',
    'Healthcare',
    'Economy',
    'Human Rights',
    'Animal Welfare'
  ];

  useEffect(() => {
    loadPetitions();
    
    const stored = localStorage.getItem('memberSecret');
    if (stored) {
      setMemberSecret(stored);
    } else {
      const secret = ethers.hexlify(ethers.randomBytes(32));
      localStorage.setItem('memberSecret', secret);
      setMemberSecret(secret);
    }
  }, []);

  async function loadPetitions() {
    console.log('🔵 Loading petitions...');
    const startTime = performance.now();
    setLoadingPetitions(true);
    
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
      
      // 1. Get petition count
      const count = await registry.petitionCount();
      console.log(`🔵 Found ${count} petitions`);
      
      if (count === 0) {
        setPetitions([]);
        return;
      }
      
      // 2. Batch load all petition data in parallel
      const petitionIds = Array.from({ length: Number(count) }, (_, i) => i + 1);
      
      const [petitionDataArray, eventArrays, userSignedArray] = await Promise.all([
        // Load all petition basic data
        Promise.all(petitionIds.map(id => registry.getPetition(id))),
        
        // Load all signature events
        Promise.all(petitionIds.map(id => {
          const filter = registry.filters.PetitionSigned(id);
          return registry.queryFilter(filter);
        })),
        
        // Check if user signed each petition
        Promise.all(petitionIds.map(id => {
          if (!memberSecret) return false;
          
          const nullifier = ethers.keccak256(
            ethers.solidityPacked(
              ['bytes32', 'uint256', 'string'],
              [memberSecret, id, 'SIGN']
            )
          );
          return registry.hasSignedPetition(id, nullifier);
        }))
      ]);
      
      // 3. Combine all data
      const petitionList = petitionIds
        .map((id, index) => {
          const petition = petitionDataArray[index];
          const events = eventArrays[index];
          const userSigned = userSignedArray[index];

          return {
            petitionId: id,
            creator: petition.creator,
            metadataURI: petition.metadataURI,
            createdAt: new Date(Number(petition.createdAt) * 1000).toLocaleDateString(),
            signatureCount: events.length,
            userSigned,
            exists: Boolean(petition.exists)
          };
        })
        // Only show petitions that actually exist on-chain
        .filter(p => p.exists);

      setPetitions(petitionList);

      const loadTime = performance.now() - startTime;
      console.log(`🔵 Loaded ${petitionList.length} existing petitions in ${(loadTime / 1000).toFixed(2)}s`);} catch (error) {
      console.error('❌ Error loading petitions:', error);
    } finally {
      setLoadingPetitions(false);
    }
  }

  async function createPetition() {
    // Validation
    if (!newPetitionTitle.trim()) {
      alert('Please enter a petition title');
      return;
    }
    
    if (newPetitionTitle.length < 10) {
      alert('Title must be at least 10 characters');
      return;
    }
    
    if (newPetitionTitle.length > 100) {
      alert('Title must be less than 100 characters');
      return;
    }
    
    if (!newPetitionDescription.trim()) {
      alert('Please enter a description');
      return;
    }
    
    if (newPetitionDescription.length < 20) {
      alert('Description must be at least 20 characters');
      return;
    }

    setLoading(true);
    try {
      // 1. Get next petition ID
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
      const currentCount = await registry.petitionCount();
      const nextPetitionId = Number(currentCount) + 1;
      
      // 2. Upload metadata to IPFS via backend
      console.log('Uploading metadata to IPFS...');
      const metadataResponse = await fetch(`${BACKEND_URL}/api/petition/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          petitionId: nextPetitionId,
          title: newPetitionTitle,
          description: newPetitionDescription,
          category: newPetitionCategory,
          target: newPetitionTarget || 'Public',
          goalSignatures: newPetitionGoal
        })
      });
      
      const metadataResult = await metadataResponse.json();
      
      if (!metadataResult.success) {
        throw new Error('Failed to upload metadata to IPFS');
      }
      
      console.log('IPFS upload successful:', metadataResult.ipfsHash);
      
      // 3. Create petition on-chain with IPFS URI
      const registryWithSigner = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registryWithSigner.createPetition(metadataResult.metadataURI, {
        gasLimit: 150000
      });
      await tx.wait();
      
      alert(`Petition created and stored on IPFS!\nHash: ${metadataResult.ipfsHash}`);
      
      // Reset form
      setNewPetitionTitle('');
      setNewPetitionDescription('');
      setNewPetitionCategory('General');
      setNewPetitionTarget('');
      setNewPetitionGoal(100);
      
      loadPetitions();
    } catch (error) {
      console.error('Error creating petition:', error);
      alert('Failed to create petition: ' + error.message);
    }
    setLoading(false);
  }

  async function signPetition(petitionId) {
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

      console.log('🟢 Building transaction...');
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      
      // Use fixed gas limit for Aurora testnet (skip slow estimation)
      // Mainnet should use automatic estimation for safety
      const tx = await registry.signPetition(petitionId, nullifier, authData, {
        gasLimit: 100000 // ~50k actual + buffer
      });
      
      await tx.wait();

      alert('Petition signed anonymously!');
      loadPetitions(); // Reload to update counts
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

  async function loadComments(petitionId) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/petition/${petitionId}/comments`);
      const data = await response.json();
      
      setComments(prev => ({
        ...prev,
        [petitionId]: data.comments || []
      }));
    } catch (error) {
      console.error('Error loading comments:', error);
    }
  }

  async function postComment(petitionId) {
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

      // Request comment attestation from backend
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

      // Submit comment on-chain
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registry.commentOnPetition(petitionId, nullifier, commentHash, authData);
      await tx.wait();

      alert('Comment posted anonymously!');
      setNewComment('');
      loadComments(petitionId); // Reload comments
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

  function togglePetitionView(petitionId) {
    if (selectedPetition === petitionId) {
      setSelectedPetition(null);
    } else {
      setSelectedPetition(petitionId);
      loadComments(petitionId);
    }
  }

  return (
    <div>
      {viewingPetitionId ? (
        <PetitionDetails
          petitionId={viewingPetitionId}
          signer={signer}
          verifiedEmail={verifiedEmail}
          memberSecret={memberSecret}
          onBack={() => setViewingPetitionId(null)}
        />
      ) : (
        <>
      <h2>Petitions</h2>
      
      <div style={{ marginBottom: 'var(--space-xl)' }}>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className={`create-toggle-btn ${showCreateForm ? 'active' : ''}`}
        >
          <span>{showCreateForm ? 'Hide Form' : 'Create New Petition'}</span>
          <span className="create-toggle-icon">{showCreateForm ? '−' : '+'}</span>
        </button>

        {showCreateForm && (
          <div className="create-form">
            <div className="card">
              <h3 style={{ marginTop: 0, marginBottom: 'var(--space-lg)', color: 'var(--text-primary)' }}>Create New Petition</h3>
        
        {/* Title */}
        <div className="form-group">
          <label className="form-label required">
            Title
          </label>
          <input
            type="text"
            placeholder="Enter petition title (10-100 characters)"
            value={newPetitionTitle}
            onChange={(e) => setNewPetitionTitle(e.target.value)}
            maxLength={100}
          />
          <small className="char-count">{newPetitionTitle.length}/100 characters</small>
        </div>

        {/* Description */}
        <div className="form-group">
          <label className="form-label required">
            Description
          </label>
          <textarea
            placeholder="Explain what this petition is about and why people should sign it (minimum 20 characters)"
            value={newPetitionDescription}
            onChange={(e) => setNewPetitionDescription(e.target.value)}
          />
          <small className="char-count">{newPetitionDescription.length} characters</small>
        </div>

        {/* Category and Target - Side by side */}
        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label">
              Category
            </label>
            <select
              value={newPetitionCategory}
              onChange={(e) => setNewPetitionCategory(e.target.value)}
            >
              {CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">
              Target
            </label>
            <input
              type="text"
              placeholder="e.g., City Council, Government"
              value={newPetitionTarget}
              onChange={(e) => setNewPetitionTarget(e.target.value)}
            />
          </div>
        </div>

        {/* Goal Signatures */}
        <div className="form-group">
          <label className="form-label">
            Signature Goal
          </label>
          <input
            type="number"
            min="1"
            max="1000000"
            value={newPetitionGoal}
            onChange={(e) => setNewPetitionGoal(parseInt(e.target.value) || 100)}
            style={{ 
              width: '200px', 
              padding: '0.75rem',
              fontSize: '1rem',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          />
          <small style={{ display: 'block', color: '#666', marginTop: '0.25rem' }}>
            How many signatures are you aiming for?
          </small>
        </div>

        {/* Submit Button */}
        <button 
          onClick={createPetition} 
          disabled={loading}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.1rem',
            background: loading ? '#ccc' : '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontWeight: 'bold'
          }}
        >
          {loading ? 'Creating Petition...' : 'Create Petition'}
        </button>
            </div>
          </div>
        )}
      </div>

      <div>
        <h3>All Petitions ({petitions.length})</h3>
        
        {loadingPetitions ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '3rem', 
            color: '#667eea',
            fontSize: '1.2rem'
          }}>
            <div>⏳ Loading petitions...</div>
            <div style={{ fontSize: '0.9rem', color: '#999', marginTop: '0.5rem' }}>
              Fetching data from blockchain
            </div>
          </div>
        ) : petitions.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#999', padding: '2rem' }}>
            No petitions yet. Create the first one!
          </p>
        ) : (
          petitions.map(petition => {
            const isExpanded = expandedPetition === petition.petitionId;
            return (
          <div 
            key={petition.petitionId} 
            className={`petition-card ${petition.userSigned ? 'signed' : ''} ${isExpanded ? 'expanded' : ''}`}
          >
            {/* Compact Preview - Always Visible */}
            <div 
              className="petition-preview"
              onClick={() => setExpandedPetition(isExpanded ? null : petition.petitionId)}
            >
              <div className="petition-preview-left">
                <h4 className="petition-compact-title">
                  Petition #{petition.petitionId}
                  {petition.userSigned && <span style={{ marginLeft: '0.5rem', color: 'var(--accent-success)' }}>✓</span>}
                </h4>
                <div className="petition-compact-meta">
                  Created {petition.createdAt} · {petition.creator.slice(0, 10)}...
                </div>
              </div>
              <div className="petition-preview-right">
                <div className="petition-compact-signatures">
                  {petition.signatureCount} 📝
                </div>
                <div className="expand-icon">
                  {isExpanded ? '▲' : '▼'}
                </div>
              </div>
            </div>

            {/* Expanded Content - Only when clicked */}
            {isExpanded && (
              <div className="petition-expanded-content">
                <p className="petition-meta"><strong>Metadata:</strong> {petition.metadataURI}</p>
                <p className="petition-meta"><strong>Creator:</strong> {petition.creator}</p>
                
                <div className="petition-actions">
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      setViewingPetitionId(petition.petitionId);
                    }}
                    className="btn-outline"
                  >
                    View Full Details
                  </button>
                  
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      signPetition(petition.petitionId);
                    }}
                    disabled={loading || petition.userSigned}
                    className={petition.userSigned ? 'btn-outline' : 'btn-primary'}
                  >
                    {petition.userSigned ? 'Already Signed' : 'Sign Anonymously'}
                  </button>
                  
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      togglePetitionView(petition.petitionId);
                    }}
                    className="btn-outline"
                  >
                    {selectedPetition === petition.petitionId ? 'Hide Comments' : 'View Comments'}
                  </button>
                </div>

            {/* Comments Section */}
            {selectedPetition === petition.petitionId && (
              <div className="comments-section">
                <h4 className="comments-header">Comments</h4>
                
                {/* Comment Input */}
                <div style={{ marginBottom: '1rem' }}>
                  <textarea
                    placeholder="Write your comment..."
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    style={{ 
                      width: '100%', 
                      padding: '0.75rem', 
                      minHeight: '80px',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      marginBottom: '0.5rem'
                    }}
                  />
                  <button 
                    onClick={() => postComment(petition.petitionId)} 
                    disabled={loading}
                    style={{ width: '100%' }}
                  >
                    {loading ? 'Posting...' : 'Post Comment Anonymously'}
                  </button>
                </div>

                {/* Comments List */}
                <div>
                  {comments[petition.petitionId] && comments[petition.petitionId].length > 0 ? (
                    comments[petition.petitionId].map((comment, idx) => (
                      <div key={idx} style={{ 
                        background: '#f9f9f9', 
                        padding: '1rem', 
                        marginBottom: '0.5rem',
                        borderRadius: '4px',
                        borderLeft: '3px solid #667eea'
                      }}>
                        <p style={{ margin: '0 0 0.5rem 0' }}>{comment.text}</p>
                        <small style={{ color: '#666' }}>
                          {new Date(comment.timestamp).toLocaleString()}
                        </small>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: '#999', fontStyle: 'italic' }}>No comments yet. Be the first!</p>
                  )}
                </div>
              </div>
            )}
              </div>
            )}
          </div>
            );
          })
        )}
      </div>

      {memberSecret && (
        <div 
          className="member-secret-display" 
          title={`Full secret: ${memberSecret}`}
          style={{ 
            marginTop: 'var(--space-lg)', 
            padding: 'var(--space-sm) var(--space-md)',
            fontSize: '0.8rem', 
            color: 'var(--text-muted)',
            background: 'var(--bg-secondary)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--border-radius)',
            fontFamily: 'var(--font-mono)',
            cursor: 'help'
          }}
        >
          <strong style={{ color: 'var(--text-secondary)' }}>Your Member Secret (stored locally):</strong><br />
          {memberSecret.slice(0, 20)}...{memberSecret.slice(-10)} <small style={{ color: 'var(--text-muted)' }}>(hover for full)</small>
        </div>
      )}
        </>
      )}
    </div>
  );
}
