import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL, BACKEND_URL } from './config';

export default function Petitions({ signer, account, verifiedEmail }) {
  const [petitions, setPetitions] = useState([]);
  const [newPetitionTitle, setNewPetitionTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [memberSecret, setMemberSecret] = useState('');

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
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
      
      const count = await registry.petitionCount();
      const petitionList = [];
      
      for (let i = 1; i <= count; i++) {
        const petition = await registry.getPetition(i);
        
        // Get signature count by counting PetitionSigned events
        const filter = registry.filters.PetitionSigned(i);
        const events = await registry.queryFilter(filter);
        const signatureCount = events.length;
        
        // Check if current user signed (using their member secret)
        let userSigned = false;
        if (memberSecret) {
          const nullifier = ethers.keccak256(
            ethers.solidityPacked(
              ['bytes32', 'uint256', 'string'],
              [memberSecret, i, 'SIGN']
            )
          );
          userSigned = await registry.hasSignedPetition(i, nullifier);
        }
        
        petitionList.push({
          id: i,
          creator: petition.creator,
          metadataURI: petition.metadataURI,
          createdAt: new Date(Number(petition.createdAt) * 1000).toLocaleDateString(),
          signatureCount,
          userSigned
        });
      }
      
      setPetitions(petitionList);
    } catch (error) {
      console.error('Error loading petitions:', error);
    }
  }

  async function createPetition() {
    if (!newPetitionTitle.trim()) {
      alert('Please enter a petition title');
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
          description: 'Created via frontend',
          category: 'General'
        })
      });
      
      const metadataResult = await metadataResponse.json();
      
      if (!metadataResult.success) {
        throw new Error('Failed to upload metadata to IPFS');
      }
      
      console.log('IPFS upload successful:', metadataResult.ipfsHash);
      
      // 3. Create petition on-chain with IPFS URI
      const registryWithSigner = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registryWithSigner.createPetition(metadataResult.metadataURI);
      await tx.wait();
      
      alert(`Petition created and stored on IPFS!\nHash: ${metadataResult.ipfsHash}`);
      setNewPetitionTitle('');
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

      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, signer);
      const tx = await registry.signPetition(petitionId, nullifier, authData);
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

  return (
    <div>
      <h2>Petitions</h2>
      
      <div style={{ marginBottom: '2rem', padding: '1rem', background: 'white', borderRadius: '8px' }}>
        <h3>Create New Petition</h3>
        <input
          type="text"
          placeholder="Petition title..."
          value={newPetitionTitle}
          onChange={(e) => setNewPetitionTitle(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
        />
        <button onClick={createPetition} disabled={loading}>
          {loading ? 'Creating...' : 'Create Petition'}
        </button>
      </div>

      <div>
        <h3>All Petitions ({petitions.length})</h3>
        {petitions.map(petition => (
          <div key={petition.id} style={{ 
            background: 'white', 
            padding: '1rem', 
            marginBottom: '1rem', 
            borderRadius: '8px',
            border: petition.userSigned ? '2px solid #4CAF50' : '1px solid #ddd'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h4>Petition #{petition.id}</h4>
              {petition.userSigned && (
                <span style={{ 
                  background: '#4CAF50', 
                  color: 'white', 
                  padding: '0.25rem 0.75rem', 
                  borderRadius: '12px',
                  fontSize: '0.85rem'
                }}>
                  ✓ You signed this
                </span>
              )}
            </div>
            <p><strong>Metadata:</strong> {petition.metadataURI}</p>
            <p><strong>Created:</strong> {petition.createdAt}</p>
            <p><strong>Creator:</strong> {petition.creator.slice(0, 10)}...</p>
            <p style={{ 
              fontSize: '1.2rem', 
              fontWeight: 'bold', 
              color: '#667eea',
              margin: '0.5rem 0'
            }}>
              📝 {petition.signatureCount} {petition.signatureCount === 1 ? 'signature' : 'signatures'}
            </p>
            <button 
              onClick={() => signPetition(petition.id)} 
              disabled={loading || petition.userSigned}
              style={{ opacity: petition.userSigned ? 0.5 : 1 }}
            >
              {petition.userSigned ? 'Already Signed' : 'Sign Anonymously'}
            </button>
          </div>
        ))}
      </div>

      {memberSecret && (
        <div style={{ marginTop: '2rem', fontSize: '0.8rem', color: '#666' }}>
          <strong>Your Member Secret (stored locally):</strong><br />
          {memberSecret.slice(0, 20)}...
        </div>
      )}
    </div>
  );
}
