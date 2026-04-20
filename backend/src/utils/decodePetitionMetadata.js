export function decodePetitionMetadata(metadataURI) {
  if (!metadataURI || typeof metadataURI !== "string") {
    return null;
  }

  try {
    let jsonString = null;

    // Case 1: data URI
    if (metadataURI.startsWith("data:")) {
      const commaIndex = metadataURI.indexOf(",");
      if (commaIndex === -1) return null;

      const header = metadataURI.slice(0, commaIndex);
      const payload = metadataURI.slice(commaIndex + 1);

      if (header.includes(";base64")) {
        jsonString = Buffer.from(payload, "base64").toString("utf-8");
      } else {
        jsonString = decodeURIComponent(payload);
      }
    }
    // Case 2: looks like raw JSON
    else if (metadataURI.trim().startsWith("{")) {
      jsonString = metadataURI;
    }
    // Case 3: plain base64 JSON
    else if (/^[A-Za-z0-9+/=]+$/.test(metadataURI)) {
      jsonString = Buffer.from(metadataURI, "base64").toString("utf-8");
    }

    if (!jsonString) {
      return null;
    }

    const parsed = JSON.parse(jsonString);
    const out = {};

    if (typeof parsed.title === "string") out.title = parsed.title;
    if (typeof parsed.summary === "string") out.summary = parsed.summary;
    if (typeof parsed.description === "string") out.description = parsed.description;

    return Object.keys(out).length > 0 ? out : null;
  } catch {
    return null;
  }
}