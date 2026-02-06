// ... (keep everything the same until line 63)

      // Submit to blockchain
      setStatus('submitting');
      console.log('📤 Submitting...');

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      // PREFLIGHT TEST - call verifier directly first
      const VERIFIER_ADDRESS = '0xE70E2cFA4a4272B39918A45BA1F067676CCf8c11';
      const VERIFIER_ABI = [
        'function verifyProof(uint256[2],uint256[2][2],uint256[2],uint256[3]) external view returns (bool)'
      ];
      
      const verifier = new ethers.Contract(VERIFIER_ADDRESS, VERIFIER_ABI, provider);
      
      const preflightOk = await verifier.verifyProof(
        zkProof.proof.pA,
        zkProof.proof.pB,
        zkProof.proof.pC,
        zkProof.proof.publicSignals
      );
      
      console.log('🔍 PREFLIGHT VERIFIER:', preflightOk);
      console.log('Proof:', { pA: zkProof.proof.pA, pB: zkProof.proof.pB, pC: zkProof.proof.pC, input: zkProof.proof.publicSignals });
      
      if (!preflightOk) {
        throw new Error('PREFLIGHT FAILED: Verifier returned false. Proof/verifier mismatch!');
      }
      
      console.log('✅ Preflight passed - proof is valid!');

      // Continue with registry call...
