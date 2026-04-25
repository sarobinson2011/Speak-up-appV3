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

      <textarea
        value={secretImportText}
        onChange={(e) => setSecretImportText(e.target.value)}
        placeholder="Paste existing secret to import"
        rows={3}
        style={{
          width: '100%',
          padding: 10,
          borderRadius: 8,
          border: '1px solid #d1d5db',
          fontFamily: 'monospace'
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
            <textarea
              readOnly
              value={secretExportText}
              rows={3}
              style={{
                width: '100%',
                padding: 10,
                borderRadius: 8,
                border: '1px solid #d1d5db',
                fontFamily: 'monospace'
              }}
            />
          ) : null}
        </>
      ) : null}

      {secretActionError ? (
        <div style={{ color: '#b91c1c' }}>{secretActionError}</div>
      ) : null}
    </div>
  );
}