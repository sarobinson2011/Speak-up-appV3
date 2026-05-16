export function M2IdentityControls({
  secretImportText,
  setSecretImportText,
  handleCreateSecret,
  handleImportSecret,
  encryptedBundleImportText,
  setEncryptedBundleImportText,
  encryptedBundleImportPassword,
  setEncryptedBundleImportPassword,
  handleImportEncryptedBundle,
  handleExportSecret,
  encryptedBundlePassword,
  setEncryptedBundlePassword,
  handleExportEncryptedBundle,
  encryptedBundleText,
  secretExportText,
  secretActionError,
  showExport = false
}) {
  return (
    <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ fontSize: 13, lineHeight: 1.45, color: '#374151' }}>
        This secret exists only in local browser storage unless you export and save it elsewhere.
        Losing browser storage without a saved copy of this secret breaks continuity.
      </div>

      <button
        onClick={handleCreateSecret}
        style={{
          padding: '10px 12px',
          borderRadius: 8,
          border: '1px solid #e5e7eb',
          background: '#111827',
          color: '#ffffff',
          cursor: 'pointer',
          fontWeight: 600
        }}
      >
        Create new secret
      </button>

      <label style={{ fontSize: 14, fontWeight: 600, color: '#111827' }}>
        Import saved secret
      </label>

      <textarea
        value={secretImportText}
        onChange={(e) => setSecretImportText(e.target.value)}
        placeholder="Paste a previously exported secret"
        rows={3}
        style={{
          width: '100%',
          padding: 12,
          borderRadius: 8,
          border: '1px solid #d1d5db',
          fontFamily: 'monospace',
          fontSize: 14,
          lineHeight: 1.5
        }}
      />

      <button
        onClick={handleImportSecret}
        disabled={!secretImportText.trim()}
        style={{
          padding: '10px 12px',
          borderRadius: 8,
          border: '1px solid #e5e7eb',
          background: !secretImportText.trim() ? '#f3f4f6' : '#111827',
          color: !secretImportText.trim() ? '#6b7280' : '#ffffff',
          cursor: !secretImportText.trim() ? 'not-allowed' : 'pointer',
          fontWeight: 600
        }}
      >
        Import secret
      </button>

      <div style={{ marginTop: 10, borderTop: '1px solid #e5e7eb', paddingTop: 10 }}>
        <label style={{ fontSize: 14, fontWeight: 600, color: '#111827' }}>
          Import encrypted continuity bundle
        </label>

        <textarea
          value={encryptedBundleImportText}
          onChange={(e) => setEncryptedBundleImportText(e.target.value)}
          placeholder="Paste an encrypted continuity bundle"
          rows={6}
          style={{
            width: '100%',
            marginTop: 6,
            padding: 12,
            borderRadius: 8,
            border: '1px solid #d1d5db',
            fontFamily: 'monospace',
            fontSize: 13,
            lineHeight: 1.5
          }}
        />

        <input
          type="password"
          value={encryptedBundleImportPassword}
          onChange={(e) => setEncryptedBundleImportPassword(e.target.value)}
          placeholder="Password for this encrypted bundle"
          style={{
            width: '100%',
            marginTop: 8,
            padding: 12,
            borderRadius: 8,
            border: '1px solid #d1d5db',
            fontSize: 14,
            lineHeight: 1.5
          }}
        />

        <button
          onClick={handleImportEncryptedBundle}
          disabled={!encryptedBundleImportText.trim() || !encryptedBundleImportPassword.trim()}
          style={{
            width: '100%',
            marginTop: 8,
            padding: '10px 12px',
            borderRadius: 8,
            border: '1px solid #e5e7eb',
            background:
              !encryptedBundleImportText.trim() || !encryptedBundleImportPassword.trim()
                ? '#f3f4f6'
                : '#111827',
            color:
              !encryptedBundleImportText.trim() || !encryptedBundleImportPassword.trim()
                ? '#6b7280'
                : '#ffffff',
            cursor:
              !encryptedBundleImportText.trim() || !encryptedBundleImportPassword.trim()
                ? 'not-allowed'
                : 'pointer',
            fontWeight: 600
          }}
        >
          Import encrypted continuity bundle
        </button>

        <div style={{ fontSize: 13, lineHeight: 1.45, color: '#374151' }}>
          Importing a bundle sets the active local secret to the decrypted secret. Continuity exists only when this is the same original secret.
        </div>
      </div>

      {showExport ? (
        <>
          <button
            onClick={handleExportSecret}
            style={{
              padding: '10px 12px',
              borderRadius: 8,
              border: '1px solid #e5e7eb',
              background: '#ffffff',
              color: '#111827',
              cursor: 'pointer',
              fontWeight: 600
            }}
          >
            Export current secret
          </button>

          {secretExportText ? (
            <>
              <label style={{ fontSize: 14, fontWeight: 600, color: '#111827' }}>
                Exported secret
              </label>

              <textarea
                readOnly
                value={secretExportText}
                rows={4}
                style={{
                  width: '100%',
                  padding: 12,
                  borderRadius: 8,
                  border: '1px solid #d1d5db',
                  fontFamily: 'monospace',
                  fontSize: 14,
                  lineHeight: 1.5
                }}
              />

              <div style={{ fontSize: 13, lineHeight: 1.45, color: '#374151' }}>
                Save this secret securely offline. Anyone with this exact secret can continue the same anonymous membership.
              </div>

              <div style={{ marginTop: 10, borderTop: '1px solid #e5e7eb', paddingTop: 10 }}>
                <label style={{ fontSize: 14, fontWeight: 600, color: '#111827' }}>
                  Encrypted continuity bundle password
                </label>

                <input
                  type="password"
                  value={encryptedBundlePassword}
                  onChange={(e) => setEncryptedBundlePassword(e.target.value)}
                  placeholder="Enter a password for the encrypted bundle"
                  style={{
                    width: '100%',
                    marginTop: 6,
                    padding: 12,
                    borderRadius: 8,
                    border: '1px solid #d1d5db',
                    fontSize: 14,
                    lineHeight: 1.5
                  }}
                />

                <button
                  onClick={handleExportEncryptedBundle}
                  disabled={!encryptedBundlePassword.trim()}
                  style={{
                    width: '100%',
                    marginTop: 8,
                    padding: '10px 12px',
                    borderRadius: 8,
                    border: '1px solid #e5e7eb',
                    background: !encryptedBundlePassword.trim() ? '#f3f4f6' : '#111827',
                    color: !encryptedBundlePassword.trim() ? '#6b7280' : '#ffffff',
                    cursor: !encryptedBundlePassword.trim() ? 'not-allowed' : 'pointer',
                    fontWeight: 600
                  }}
                >
                  Export encrypted continuity bundle
                </button>

                {encryptedBundleText ? (
                  <>
                    <label style={{ display: 'block', marginTop: 10, fontSize: 14, fontWeight: 600, color: '#111827' }}>
                      Encrypted continuity bundle
                    </label>

                    <textarea
                      readOnly
                      value={encryptedBundleText}
                      rows={8}
                      style={{
                        width: '100%',
                        marginTop: 6,
                        padding: 12,
                        borderRadius: 8,
                        border: '1px solid #d1d5db',
                        fontFamily: 'monospace',
                        fontSize: 13,
                        lineHeight: 1.5
                      }}
                    />

                    <div style={{ fontSize: 13, lineHeight: 1.45, color: '#374151' }}>
                      Save this encrypted bundle securely. It contains only the current secret, encrypted with the password you entered.
                    </div>
                  </>
                ) : null}
              </div>
            </>
          ) : null}
        </>
      ) : null}

      {secretActionError ? (
        <div style={{ color: '#b91c1c' }}>{secretActionError}</div>
      ) : null}
    </div>
  );
}