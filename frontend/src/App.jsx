import { useState, useEffect } from 'react'
import { ethers } from 'ethers'
import Petitions from './Petitions'
import EmailVerification from './EmailVerification'
import Analytics from './Analytics'
import HomePage from './HomePage'
import { BACKEND_URL } from './config'
import './App.css'

function App() {
  const [account, setAccount] = useState(null)
  const [provider, setProvider] = useState(null)
  const [signer, setSigner] = useState(null)
  const [verifiedEmail, setVerifiedEmail] = useState(null)
  const [currentView, setCurrentView] = useState('petitions')
  const [checkingToken, setCheckingToken] = useState(true)

  useEffect(() => {
    // Verify JWT token on mount
    async function verifyToken() {
      const token = localStorage.getItem('authToken');
      const email = localStorage.getItem('userEmail');
      
      if (!token || !email) {
        setCheckingToken(false);
        return;
      }

      try {
        const response = await fetch(`${BACKEND_URL}/api/auth/verify-token`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          if (data.valid && data.user.email === email) {
            setVerifiedEmail(email);
            console.log('JWT verified - session restored');
          } else {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
          }
        } else {
          console.log('Token expired or invalid');
          localStorage.removeItem('authToken');
          localStorage.removeItem('userEmail');
        }
      } catch (error) {
        console.error('Error verifying token:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
      }

      setCheckingToken(false);
    }

    verifyToken();
  }, []);

  async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
      try {
        await window.ethereum.request({ method: 'eth_requestAccounts' })
        const provider = new ethers.BrowserProvider(window.ethereum)
        const signer = await provider.getSigner()
        const address = await signer.getAddress()
        
        setProvider(provider)
        setSigner(signer)
        setAccount(address)
        
        console.log('Connected:', address)
      } catch (error) {
        console.error('Error connecting wallet:', error)
      }
    } else {
      alert('Please install MetaMask!')
    }
  }

  function handleEmailVerified(email) {
    setVerifiedEmail(email);
  }

  function goToHomepage() {
    setAccount(null);
    setProvider(null);
    setSigner(null);
    // Keep verifiedEmail and JWT token - user stays logged in
  }

  // Show loading while checking token
  if (checkingToken) {
    return (
      <div className="App">
        <header className="landing-header">
          <div className="container header-flex">
            <div className="header-left">
              <h1 onClick={goToHomepage} className="clickable-logo">Speak Up</h1>
              <p>Anonymous Petitions Platform</p>
            </div>
            <div className="header-right">
              <div className="network-badge-header">
                <span className="built-on-text">Built on</span>
                <span className="network-name">Aurora</span>
                <svg className="aurora-logo" width="24" height="24" viewBox="0 0 808 808" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path 
                    d="M402.91,204.91c18.68,0,35.48,10.38,43.84,27.09l137.85,275.71c7.65,15.31,6.85,33.13-2.14,47.69-9,14.56-24.58,23.25-41.7,23.25H265.06c-17.11,0-32.7-8.69-41.69-23.25-9-14.56-9.8-32.38-2.14-47.69L359.07,232c8.36-16.71,25.16-27.09,43.84-27.09m0-33.7c-31.33,0-59.97,17.7-73.98,45.72L191.08,492.64c-12.82,25.64-11.45,56.09,3.62,80.47,15.07,24.38,41.69,39.23,70.36,39.23h275.71c28.67,0,55.29-14.84,70.36-39.23,15.07-24.38,16.44-54.83,3.62-80.47L476.89,216.93c-14.01-28.02-42.65-45.72-73.98-45.72h0Z" 
                    fill="#5DEB5A"
                  />
                </svg>
              </div>
            </div>
          </div>
        </header>
        <main>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Verifying session...
          </div>
        </main>
      </div>
    );
  }

  // Show landing page if not connected OR not verified
  if (!account || !verifiedEmail) {
    return (
      <div className="App">
        <header className="landing-header">
          <div className="container header-flex">
            <div className="header-left">
              <h1 onClick={goToHomepage} className="clickable-logo">Speak Up</h1>
              <p>Anonymous Petitions Platform</p>
            </div>
            <div className="header-right">
              <div className="header-actions">
                {!account ? (
                  <button onClick={connectWallet} className="connect-wallet-btn">
                    Connect Wallet
                  </button>
                ) : (
                  <div className="wallet-status">
                    <span className="wallet-address">
                      {account.slice(0, 6)}...{account.slice(-4)}
                    </span>
                  </div>
                )}
                <div className="network-badge-header">
                  <span className="built-on-text">Built on</span>
                  <span className="network-name">Aurora</span>
                  <svg className="aurora-logo" width="24" height="24" viewBox="0 0 808 808" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path 
                      d="M402.91,204.91c18.68,0,35.48,10.38,43.84,27.09l137.85,275.71c7.65,15.31,6.85,33.13-2.14,47.69-9,14.56-24.58,23.25-41.7,23.25H265.06c-17.11,0-32.7-8.69-41.69-23.25-9-14.56-9.8-32.38-2.14-47.69L359.07,232c8.36-16.71,25.16-27.09,43.84-27.09m0-33.7c-31.33,0-59.97,17.7-73.98,45.72L191.08,492.64c-12.82,25.64-11.45,56.09,3.62,80.47,15.07,24.38,41.69,39.23,70.36,39.23h275.71c28.67,0,55.29-14.84,70.36-39.23,15.07-24.38,16.44-54.83,3.62-80.47L476.89,216.93c-14.01-28.02-42.65-45.72-73.98-45.72h0Z" 
                      fill="#5DEB5A"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </header>

        {!account ? (
          <HomePage onGetStarted={connectWallet} />
        ) : (
          <main>
            <div style={{ padding: '2rem' }}>
              <EmailVerification onVerified={handleEmailVerified} />
            </div>
          </main>
        )}
      </div>
    );
  }

  // Show dashboard for connected + verified users
  return (
    <div className="App">
      <header>
        <div className="container header-flex">
          <div className="header-left">
            <h1 onClick={goToHomepage} className="clickable-logo">Speak Up</h1>
            <p>Anonymous Petitions Platform</p>
          </div>
          <div className="header-right">
            <div className="network-badge-header">
              <span className="built-on-text">Built on</span>
              <span className="network-name">Aurora</span>
              <svg className="aurora-logo" width="24" height="24" viewBox="0 0 808 808" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path 
                  d="M402.91,204.91c18.68,0,35.48,10.38,43.84,27.09l137.85,275.71c7.65,15.31,6.85,33.13-2.14,47.69-9,14.56-24.58,23.25-41.7,23.25H265.06c-17.11,0-32.7-8.69-41.69-23.25-9-14.56-9.8-32.38-2.14-47.69L359.07,232c8.36-16.71,25.16-27.09,43.84-27.09m0-33.7c-31.33,0-59.97,17.7-73.98,45.72L191.08,492.64c-12.82,25.64-11.45,56.09,3.62,80.47,15.07,24.38,41.69,39.23,70.36,39.23h275.71c28.67,0,55.29-14.84,70.36-39.23,15.07-24.38,16.44-54.83,3.62-80.47L476.89,216.93c-14.01-28.02-42.65-45.72-73.98-45.72h0Z" 
                  fill="#5DEB5A"
                />
              </svg>
            </div>
          </div>
        </div>
      </header>

      <main>
        <div className="dashboard">
          <div className="dashboard-header">
            <p className="account-info" title={`Full address: ${account}`}>
              Connected: {account.slice(0, 6)}...{account.slice(-4)} | 
              Email: {verifiedEmail} ✓
            </p>
            
            <div className="nav-tabs">
              <button 
                className={`nav-tab ${currentView === 'petitions' ? 'active' : ''}`}
                onClick={() => setCurrentView('petitions')}
              >
                📝 Petitions
              </button>
              <button 
                className={`nav-tab ${currentView === 'analytics' ? 'active' : ''}`}
                onClick={() => setCurrentView('analytics')}
              >
                📊 Analytics
              </button>
            </div>
          </div>

          {currentView === 'petitions' && (
            <Petitions signer={signer} account={account} verifiedEmail={verifiedEmail} />
          )}
          {currentView === 'analytics' && (
            <Analytics />
          )}
        </div>
      </main>
    </div>
  )
}

export default App
