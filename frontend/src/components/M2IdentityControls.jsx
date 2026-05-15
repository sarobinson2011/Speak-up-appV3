export function M2IdentityControls({
  secretImportText,
  setSecretImportText,
  handleCreateSecret,
  handleImportSecret,
  handleExportSecret,
  secretExportText,
  secretActionError,
  showExport = false
}) {
  return (
    <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ fontSize: 13, lineHeight: 1.45, color: '#374151' }}>
        This secret exists only in local browser storage unless you export and save it elsewhere.
        Losing browser storage without a saved secret prevents continuity restoration.
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
                Save this secret securely offline. Anyone with this secret can continue the same anonymous membership.
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