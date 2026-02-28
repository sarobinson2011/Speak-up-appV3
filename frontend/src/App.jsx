// frontend/src/App.jsx (M2-only)
import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { ensureMemberSecret } from './m2Identity';
import Petitions from './Petitions';
import Analytics from './Analytics';
import HomePage from './HomePage';

import './App.css';

function App() {
  const [account, setAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);

  // Keep this so the UI still has the same tabs/layout
  const [currentView, setCurrentView] = useState('petitions');

  async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
      try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        const p = new ethers.BrowserProvider(window.ethereum);
        const s = await p.getSigner();
        const address = await s.getAddress();

        setProvider(p);
        setSigner(s);
        setAccount(address);

        console.log('Connected:', address);
      } catch (error) {
        console.error('Error connecting wallet:', error);
      }
    } else {
      alert('Please install MetaMask!');
    }
  }

  function goToHomepage() {
    setAccount(null);
    setProvider(null);
    setSigner(null);
    // M2-only: no verifiedEmail/JWT to preserve
  }

  useEffect(() => {
    if (!account) return;
    ensureMemberSecret(account);
  }, [account]);

  // Keep account in sync if user changes accounts in MetaMask
  useEffect(() => {
    if (!window.ethereum) return;

    const handleAccountsChanged = async (accounts) => {
      if (!accounts || accounts.length === 0) {
        setAccount(null);
        setProvider(null);
        setSigner(null);
        return;
      }

      try {
        const p = new ethers.BrowserProvider(window.ethereum);
        const s = await p.getSigner();
        const address = await s.getAddress();

        setProvider(p);
        setSigner(s);
        setAccount(address);

        console.log('Account changed:', address);
      } catch (e) {
        console.warn('accountsChanged handler error:', e);
      }
    };

    window.ethereum.on('accountsChanged', handleAccountsChanged);
    return () => {
      window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
    };
  }, []);

  // ===== M2-only Gate =====
  // Only require wallet connect. No email verification.
  if (!account) {
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
                <button onClick={connectWallet} className="connect-wallet-btn">
                  Connect Wallet
                </button>

                <div className="network-badge-header">
                  <span className="built-on-text">Built on</span>
                  <span className="network-name">Aurora</span>
                  <svg
                    className="aurora-logo"
                    width="24"
                    height="24"
                    viewBox="0 0 808 808"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
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

        <HomePage onGetStarted={connectWallet} />
      </div>
    );
  }

  // ===== Dashboard (wallet connected) =====
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
              <svg
                className="aurora-logo"
                width="24"
                height="24"
                viewBox="0 0 808 808"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
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
              Connected: {account.slice(0, 6)}...{account.slice(-4)} | M2-only ✓
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
            <Petitions signer={signer} account={account} />
          )}
          {currentView === 'analytics' && (
            <Analytics />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;