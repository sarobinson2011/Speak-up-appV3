import path from "path";
import Database from "better-sqlite3";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DB_PATH = path.resolve(__dirname, "../../data/indexer.db");

const db = new Database(DB_PATH);

// Reasonable SQLite defaults for a local backend DB.
db.pragma("foreign_keys = ON");
db.pragma("journal_mode = WAL");

export default db;