import { useState } from 'react';
import { BACKEND_URL } from './config';
import './EmailVerification.css';

export default function EmailVerification({ onVerified }) {
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [step, setStep] = useState('email'); // 'email' or 'code'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function requestCode() {
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/request-verification`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to send verification code');
      }

      // Store email in localStorage
      localStorage.setItem('userEmail', email);

      setStep('code');
      
      // Show debug code in development
      if (data.debugCode) {
        console.log('DEBUG CODE:', data.debugCode);
        alert(`Development mode - Code: ${data.debugCode}`);
      }
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  }

  async function verifyCode() {
    if (!code || code.length !== 6) {
      setError('Please enter the 6-digit code');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/verify-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code })
      });

      const data = await response.json();
      console.log('✅ Verify response data:', data);
      console.log('✅ Token exists?', !!data.token);
      console.log('✅ Token value:', data.token);

      if (!response.ok) {
        throw new Error(data.error || 'Invalid verification code');
      }

      // Store JWT token in localStorage
      if (data.token) {
        console.log('✅ Storing token in localStorage...');
        localStorage.setItem('authToken', data.token);
        console.log('✅ JWT token stored!');
        console.log('✅ Verify stored:', localStorage.getItem('authToken'));
      } else {
        console.log('❌ No token in response!');
      }

      // Store email
      localStorage.setItem('userEmail', email);

      // Email verified! Notify parent component
      onVerified(email);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  }

  return (
    <div className="email-verification">
      <h2>Email Verification</h2>
      <p>Verify your email to sign petitions and post comments.</p>

      {step === 'email' ? (
        <div>
          <input
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && requestCode()}
          />
          <button 
            onClick={requestCode} 
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Sending...' : 'Send Verification Code'}
          </button>
        </div>
      ) : (
        <div>
          <div className="sent-badge">
            ✉️ Code sent to {email}
          </div>
          <input
            type="text"
            placeholder="Enter 6-digit code"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            onKeyPress={(e) => e.key === 'Enter' && verifyCode()}
            className="code-input"
            maxLength={6}
          />
          <button 
            onClick={verifyCode} 
            disabled={loading}
            className="btn-primary"
          >
            {loading ? 'Verifying...' : 'Verify Email'}
          </button>
          <button 
            onClick={() => setStep('email')}
            className="btn-secondary"
          >
            Change Email
          </button>
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}
    </div>
  );
}
