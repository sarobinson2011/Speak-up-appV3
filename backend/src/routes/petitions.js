import express from "express";
import {
  getPetitionsWithCounts,
  getPetitionByIdWithCount,
  getPetitionSignatureCount,
} from "../db/repositories/petitions.js";
import { decodePetitionMetadata } from "../utils/decodePetitionMetadata.js";

export function makePetitionsRouter() {
  const router = express.Router();

  // ---------------------------
  // List petitions
  // ---------------------------
  router.get("/", (req, res) => {
    try {
      const petitions = getPetitionsWithCounts();

      return res.json({
        ok: true,
        petitions: petitions.map((p) => ({
          petitionId: p.petition_id,
          creator: p.creator,
          metadataURI: p.metadata_uri,
          metadata: decodePetitionMetadata(p.metadata_uri),
          createdAt: p.created_at,
          signatureCount: p.signature_count,
        })),
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e),
      });
    }
  });

  // ---------------------------
  // Petition detail
  // ---------------------------
  router.get("/:id", (req, res) => {
    try {
      const petitionId = Number(req.params.id);

      if (!Number.isInteger(petitionId) || petitionId < 0) {
        return res.status(400).json({ error: "invalid petition id" });
      }

      const petition = getPetitionByIdWithCount(petitionId);

      if (!petition) {
        return res.status(404).json({ error: "petition not found" });
      }

      return res.json({
        ok: true,
        petition: {
          petitionId: petition.petition_id,
          creator: petition.creator,
          metadataURI: petition.metadata_uri,
          metadata: decodePetitionMetadata(petition.metadata_uri),
          createdAt: petition.created_at,
          signatureCount: petition.signature_count,
        },
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e),
      });
    }
  });

  // ---------------------------
  // Petition signature count
  // ---------------------------
  router.get("/:id/signature-count", (req, res) => {
    try {
      const petitionId = Number(req.params.id);

      if (!Number.isInteger(petitionId) || petitionId < 0) {
        return res.status(400).json({ error: "invalid petition id" });
      }

      const countRow = getPetitionSignatureCount(petitionId);

      if (!countRow) {
        return res.status(404).json({ error: "petition not found" });
      }

      return res.json({
        ok: true,
        petitionId: countRow.petition_id,
        signatureCount: countRow.signature_count,
      });
    } catch (e) {
      return res.status(500).json({
        ok: false,
        error: "internal",
        details: e?.message || String(e),
      });
    }
  });

  return router;
}