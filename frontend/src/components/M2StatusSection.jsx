import { ethers } from 'ethers';

import { REGISTRY_ADDRESS, REGISTRY_ABI, RPC_URL } from '../config';
import { M2SignButton } from './M2SignButton';
import { M2IdentityControls } from './M2IdentityControls';

export function M2StatusSection({
  petitionId,
  membershipPath,
  membershipExists,
  memberSecretBI,
  currentAdmissionCommitment,
  resolvedHasSignedM2,
  m2CheckLoading,
  membershipPathLoading,
  secretPresent,
  leafMatches,
  admissionBondEth,
  bondSafetyError,
  enrolling,
  enrollError,
  secretImportText,
  setSecretImportText,
  handleCreateSecret,
  handleImportSecret,
  handleExportSecret,
  secretExportText,
  secretActionError,
  enrollMembershipOnce,
  logM2Preflight,
  refreshM2SignedState,
  fetchMembershipPathByLeaf,
  uiLeafHex,
  setSignatureCount,
  onSigned,
  m2Nullifier,
}) {
  return (
    <div className="petition-detail-header">
      <div className="m2-status-stack">
        <div className="m2-status-panel">
          <strong className="m2-status-title">Strong Privacy (M2) status:</strong>
          <div className="m2-status-body">
            {resolvedHasSignedM2 ? (
              <div>Already signed.</div>
            ) : m2CheckLoading ? (
              <div>Checking signed state…</div>
            ) : membershipPathLoading ? (
              <div>Loading membership path…</div>
            ) : !secretPresent ? (
              <>
                <div>No local secret present in this browser.</div>

                <M2IdentityControls
                  secretImportText={secretImportText}
                  setSecretImportText={setSecretImportText}
                  handleCreateSecret={handleCreateSecret}
                  handleImportSecret={handleImportSecret}
                  handleExportSecret={handleExportSecret}
                  secretExportText={secretExportText}
                  secretActionError={secretActionError}
                  showExport={false}
                />
              </>
            ) : membershipExists === false ? (
              <>
                <div>Local secret present, not enrolled.</div>
                <div style={{ marginTop: 6 }}>
                  Enrolling this local secret creates a new anonymous membership for this secret only.
                </div>
                <div style={{ marginTop: 6 }}>
                  Enrollment is one-time and requires a refundable on-chain bond.
                </div>
                <div style={{ marginTop: 6 }}>
                  Creating a new secret replaces the active local secret on this device.
                </div>

                {admissionBondEth ? (
                  <div style={{ marginTop: 6 }}>
                    Live bond from contract: <strong>{admissionBondEth} ETH</strong>
                  </div>
                ) : null}

                {bondSafetyError ? (
                  <div style={{ marginTop: 6, color: '#b91c1c' }}>{bondSafetyError}</div>
                ) : null}

                <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <M2IdentityControls
                    secretImportText={secretImportText}
                    setSecretImportText={setSecretImportText}
                    handleCreateSecret={handleCreateSecret}
                    handleImportSecret={handleImportSecret}
                    handleExportSecret={handleExportSecret}
                    secretExportText={secretExportText}
                    secretActionError={secretActionError}
                    showExport={true}
                  />

                  <button
                    onClick={enrollMembershipOnce}
                    disabled={
                      enrolling ||
                      !secretPresent ||
                      resolvedHasSignedM2 ||
                      Boolean(bondSafetyError)
                    }
                    style={{
                      padding: '10px 12px',
                      borderRadius: 8,
                      border: '1px solid #e5e7eb',
                      background: enrolling || bondSafetyError ? '#f3f4f6' : '#111827',
                      color: enrolling || bondSafetyError ? '#6b7280' : '#ffffff',
                      cursor: enrolling || bondSafetyError ? 'not-allowed' : 'pointer',
                      fontWeight: 600
                    }}
                  >
                    {enrolling ? 'Enrolling…' : 'Enroll current secret'}
                  </button>

                  {enrollError ? (
                    <div style={{ color: '#b91c1c' }}>Enroll failed: {enrollError}</div>
                  ) : null}
                </div>
              </>
            ) : !leafMatches ? (
              <>
                <div>Active local secret does not match the loaded membership path. Import the correct saved secret.</div>

                <M2IdentityControls
                  secretImportText={secretImportText}
                  setSecretImportText={setSecretImportText}
                  handleCreateSecret={handleCreateSecret}
                  handleImportSecret={handleImportSecret}
                  handleExportSecret={handleExportSecret}
                  secretExportText={secretExportText}
                  secretActionError={secretActionError}
                  showExport={true}
                />
              </>
            ) : (
              <>
                <div>Local secret enrolled and usable.</div>

                <div style={{ marginTop: 6 }}>
                  Creating a new secret replaces the active local secret on this device.
                </div>

                <M2IdentityControls
                  secretImportText={secretImportText}
                  setSecretImportText={setSecretImportText}
                  handleCreateSecret={handleCreateSecret}
                  handleImportSecret={handleImportSecret}
                  handleExportSecret={handleExportSecret}
                  secretExportText={secretExportText}
                  secretActionError={secretActionError}
                  showExport={true}
                />
              </>
            )}
          </div>
        </div>

        {secretPresent && !membershipPath && !resolvedHasSignedM2 ? (
          <div className="m2-status-note">
            Signing is unavailable until this local secret is enrolled.
          </div>
        ) : null}

        {secretPresent && membershipPath && !leafMatches && !resolvedHasSignedM2 ? (
          <div className="m2-status-note">
            Signing is unavailable until you import the correct enrolled secret.
          </div>
        ) : null}

        <M2SignButton
          petitionId={petitionId}
          membershipPath={membershipPath}
          memberSecret={memberSecretBI ? memberSecretBI.toString() : ''}
          alreadySigned={resolvedHasSignedM2}
          disabled={
            resolvedHasSignedM2 ||
            m2CheckLoading ||
            membershipPathLoading ||
            !secretPresent ||
            !membershipPath ||
            !leafMatches ||
            enrolling
          }
          onPreflight={() => logM2Preflight('M2_CLICK_PREFLIGHT')}
          onSuccess={async ({ txHash }) => {
            console.log('M2 signature successful:', { txHash });
            alert(`Signed anonymously with ZK proof!\nTransaction: ${txHash.slice(0, 10)}...`);

            try {
              const provider = new ethers.JsonRpcProvider(RPC_URL);
              const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);

              await refreshM2SignedState(registry, petitionId);
              await fetchMembershipPathByLeaf(uiLeafHex);

              const filter = registry.filters.PetitionSigned(petitionId);
              const events = await registry.queryFilter(filter);
              const newCount = events.length;

              setSignatureCount(newCount);
              onSigned?.(petitionId, newCount);
            } catch (e) {
              console.warn('Failed to refresh M2 state:', e);
            }
          }}
          onError={(error) => {
            alert('M2 signing failed: ' + (error?.message || String(error)));
          }}
        />

        {m2Nullifier ? (
          <div
            style={{
              fontSize: '12px',
              color: '#666',
              marginTop: '8px',
              padding: '10px',
              background: '#f3f4f6',
              borderRadius: '6px',
              fontFamily: 'monospace'
            }}
          >
            nullifier: {m2Nullifier.slice(0, 10)}...{m2Nullifier.slice(-8)}
          </div>
        ) : null}
      </div>
    </div>
  );
}