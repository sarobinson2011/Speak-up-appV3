import fs from "fs";
import path from "path";
import Database from "better-sqlite3";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DB_PATH = path.resolve(__dirname, "../../data/indexer.db");
const MIGRATIONS_DIR = path.resolve(__dirname, "../../migrations");

function ensureMigrationsTable(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      filename TEXT PRIMARY KEY,
      applied_at TEXT NOT NULL
    );
  `);
}

function hasMigrationBeenApplied(db, filename) {
  const stmt = db.prepare(`
    SELECT 1
    FROM schema_migrations
    WHERE filename = ?
    LIMIT 1
  `);

  return Boolean(stmt.get(filename));
}

function recordAppliedMigration(db, filename) {
  const stmt = db.prepare(`
    INSERT INTO schema_migrations (filename, applied_at)
    VALUES (?, ?)
  `);

  stmt.run(filename, new Date().toISOString());
}

function main() {
  if (!fs.existsSync(MIGRATIONS_DIR)) {
    throw new Error(`Migrations directory not found: ${MIGRATIONS_DIR}`);
  }

  const db = new Database(DB_PATH);

  try {
    ensureMigrationsTable(db);

    const files = fs
      .readdirSync(MIGRATIONS_DIR)
      .filter((name) => name.endsWith(".sql"))
      .sort();

    if (files.length === 0) {
      console.log("No migration files found.");
      return;
    }

    for (const file of files) {
      if (hasMigrationBeenApplied(db, file)) {
        console.log(`Skipping already applied migration: ${file}`);
        continue;
      }

      const fullPath = path.join(MIGRATIONS_DIR, file);
      const sql = fs.readFileSync(fullPath, "utf8");

      console.log(`Applying migration: ${file}`);

      const tx = db.transaction(() => {
        db.exec(sql);
        recordAppliedMigration(db, file);
      });

      tx();
    }

    console.log("All migrations applied successfully.");
  } finally {
    db.close();
  }
}

main();