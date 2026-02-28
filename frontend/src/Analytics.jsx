import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL } from './config';
import './Analytics.css';

export default function Analytics() {
  const [stats, setStats] = useState({
    totalPetitions: 0,
    totalSignatures: 0,
    totalComments: 0,
    avgSignaturesPerPetition: 0,
    mostSignedPetition: null,
    recentActivity: []
  });
  const [loading, setLoading] = useState(true);
  const [petitionData, setPetitionData] = useState([]);

  async function loadAnalytics() {
    setLoading(true);
    try {
      const provider = new ethers.JsonRpcProvider(RPC_URL);
      const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
      
      // Get total petitions
      const count = await registry.petitionCount();
      const totalPetitions = Number(count);
      
      if (totalPetitions === 0) {
        setLoading(false);
        return;
      }
      
      // Load all petition data in parallel
      const petitionIds = Array.from({ length: totalPetitions }, (_, i) => i + 1);
      
      const [petitionDataArray, signatureEvents, commentEvents] = await Promise.all([
        Promise.all(petitionIds.map(id => registry.getPetition(id))),
        Promise.all(petitionIds.map(id => {
          const filter = registry.filters.PetitionSigned(id);
          return registry.queryFilter(filter);
        })),
        Promise.all(petitionIds.map(id => {
          const filter = registry.filters.PetitionCommented(id);
          return registry.queryFilter(filter);
        }))
      ]);
      
      // Process data
      let totalSignatures = 0;
      let totalComments = 0;
      let mostSigned = { id: 0, count: 0 };
      const petitions = [];
      
      petitionIds.forEach((id, index) => {
        const petition = petitionDataArray[index];
        const signatures = signatureEvents[index];
        const comments = commentEvents[index];
        
        const sigCount = signatures.length;
        const commentCount = comments.length;
        
        totalSignatures += sigCount;
        totalComments += commentCount;
        
        if (sigCount > mostSigned.count) {
          mostSigned = { id, count: sigCount };
        }
        
        petitions.push({
          id,
          creator: petition.creator,
          metadataURI: petition.metadataURI,
          createdAt: Number(petition.createdAt),
          signatures: sigCount,
          comments: commentCount
        });
      });
      
      // Get recent activity (last 10 signatures across all petitions)
      const allSignatures = signatureEvents.flat();
      const recentActivity = allSignatures
        .sort((a, b) => b.blockNumber - a.blockNumber)
        .slice(0, 10)
        .map(event => ({
          type: 'signature',
          petitionId: Number(event.args.petitionId),
          blockNumber: event.blockNumber
        }));
      
      setStats({
        totalPetitions,
        totalSignatures,
        totalComments,
        avgSignaturesPerPetition: totalPetitions > 0 ? (totalSignatures / totalPetitions).toFixed(1) : 0,
        mostSignedPetition: mostSigned,
        recentActivity
      });
      
      setPetitionData(petitions);
      
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
    setLoading(false);
  }

  useEffect(() => {
  // eslint-disable-next-line react-hooks/set-state-in-effect
  loadAnalytics();
  }, []);

  function exportToCSV() {
    if (petitionData.length === 0) {
      alert('No data to export');
      return;
    }
    
    // CSV Headers
    const headers = ['Petition ID', 'Creator Address', 'Metadata URI', 'Created Date', 'Signatures', 'Comments'];
    
    // CSV Rows
    const rows = petitionData.map(p => [
      p.id,
      p.creator,
      p.metadataURI,
      new Date(p.createdAt * 1000).toISOString(),
      p.signatures,
      p.comments
    ]);
    
    // Combine
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');
    
    // Download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `speak-up-analytics-${Date.now()}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('📊 Exported petition data to CSV');
  }

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Loading analytics...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h2>Analytics Dashboard</h2>
        <button onClick={exportToCSV} className="btn-primary export-btn">
          📊 Export CSV
        </button>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Petitions</div>
          <div className="stat-value">{stats.totalPetitions}</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-label">Total Signatures</div>
          <div className="stat-value">{stats.totalSignatures}</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-label">Total Comments</div>
          <div className="stat-value">{stats.totalComments}</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-label">Avg Signatures/Petition</div>
          <div className="stat-value">{stats.avgSignaturesPerPetition}</div>
        </div>
      </div>

      {/* Most Popular */}
      {stats.mostSignedPetition && stats.mostSignedPetition.count > 0 && (
        <div className="popular-section">
          <h3>Most Signed Petition</h3>
          <div className="popular-card">
            <div className="popular-id">Petition #{stats.mostSignedPetition.id}</div>
            <div className="popular-count">{stats.mostSignedPetition.count} signatures</div>
          </div>
        </div>
      )}

      {/* Petition Table */}
      <div className="table-section">
        <h3>All Petitions</h3>
        <div className="table-container">
          <table className="analytics-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Creator</th>
                <th>Created</th>
                <th>Signatures</th>
                <th>Comments</th>
              </tr>
            </thead>
            <tbody>
              {petitionData.map(p => (
                <tr key={p.id}>
                  <td>#{p.id}</td>
                  <td className="mono">{p.creator.slice(0, 10)}...</td>
                  <td>{new Date(p.createdAt * 1000).toLocaleDateString()}</td>
                  <td className="signature-cell">{p.signatures} 📝</td>
                  <td className="comment-cell">{p.comments} 💬</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Activity */}
      {stats.recentActivity.length > 0 && (
        <div className="activity-section">
          <h3>Recent Activity</h3>
          <div className="activity-list">
            {stats.recentActivity.map((activity, idx) => (
              <div key={idx} className="activity-item">
                <span className="activity-icon">📝</span>
                <span className="activity-text">
                  New signature on Petition #{activity.petitionId}
                </span>
                <span className="activity-block">Block {activity.blockNumber}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
