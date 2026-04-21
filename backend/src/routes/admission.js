import express from "express";
import { getAdmissionRight } from "../db/repositories/admission.js";

export function makeAdmissionRouter() {
  const router = express.Router();

  router.get("/:admissionCommitment", (req, res) => {
    try {
      const { admissionCommitment } = req.params;

      if (
        typeof admissionCommitment !== "string" ||
        !/^0x[a-fA-F0-9]{64}$/.test(admissionCommitment)
      ) {
        return res.status(400).json({ error: "invalid admission commitment" });
      }

      const right = getAdmissionRight(admissionCommitment);

      if (!right) {
        return res.status(404).json({ error: "admission right not found" });
      }

      return res.json({
        ok: true,
        admissionRight: {
          admissionCommitment: right.admission_commitment,
          state: right.state,
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

  return router;
}