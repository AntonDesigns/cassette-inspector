import sqlite3
import json
from db.base import BaseDB
from config import SQLITE_PATH

# Level 1 SQLite implementation.
# Nothing outside this file knows it is SQLite.
# If I ever need to swap this out, only this file changes.
#
# I store the database at SQLITE_PATH from config.py.
# No setup needed, SQLite creates the file automatically on first run.
# This is fine for single-engineer use on a laptop.
#
# Column names match inspections.csv exactly:
#   ai_slots stores ai_s01..ai_s25 as a JSON array
#   ai_conf  stores ai_p01..ai_p25 as a JSON array


class SQLiteDB(BaseDB):

    def __init__(self):
        self.conn = None

    def connect(self):
        # Create the database file and the inspections table if they
        # do not exist yet. Safe to call multiple times.
        self.conn = sqlite3.connect(str(SQLITE_PATH))
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS inspections (
                inspection_id   TEXT PRIMARY KEY,
                timestamp_utc   TEXT NOT NULL,
                crop_image_path TEXT,
                final_status    TEXT DEFAULT 'pending',
                needs_review    INTEGER DEFAULT 0,
                reviewed_by     TEXT,
                machine_type    TEXT,
                cassette_type   TEXT,
                ai_slots        TEXT,
                ai_conf         TEXT,
                inference_ms    INTEGER
            )
        """)
        self.conn.commit()

    def write_inspection(self, data: dict):
        # I serialize the slot arrays as JSON strings so SQLite can store
        # them without needing separate tables.
        # ai_slots holds ai_s01..ai_s25 values.
        # ai_conf holds ai_p01..ai_p25 values.
        self.conn.execute("""
            INSERT INTO inspections (
                inspection_id, timestamp_utc, crop_image_path, final_status,
                needs_review, reviewed_by, machine_type, cassette_type,
                ai_slots, ai_conf, inference_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("inspection_id"),
            data.get("timestamp_utc"),
            data.get("crop_image_path"),
            data.get("final_status", "pending"),
            int(data.get("needs_review", False)),
            data.get("reviewed_by"),
            data.get("machine_type"),
            data.get("cassette_type"),
            json.dumps(data.get("slots", [])),
            json.dumps(data.get("confidence", [])),
            data.get("inference_ms"),
        ))
        self.conn.commit()

    def confirm_inspection(self, data: dict) -> bool:
        cursor = self.conn.execute("""
            UPDATE inspections
            SET ai_slots = ?, final_status = ?, reviewed_by = ?
            WHERE inspection_id = ?
        """, (
            json.dumps(data.get("slots", [])),
            data.get("final_status", "reviewed"),
            data.get("engineer"),
            data.get("inspection_id"),
        ))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_recent(self, limit: int = 20) -> list:
        cursor = self.conn.execute("""
            SELECT * FROM inspections
            ORDER BY timestamp_utc DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            entry = dict(row)
            entry["ai_slots"] = json.loads(entry["ai_slots"] or "[]")
            entry["ai_conf"] = json.loads(entry["ai_conf"] or "[]")
            result.append(entry)
        return result

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
