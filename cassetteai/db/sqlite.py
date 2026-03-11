import sqlite3
import json
from db.base import BaseDB
from config import SQLITE_PATH

# Level 1 SQLite implementation.


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
                slots           TEXT NOT NULL,
                confidence      TEXT NOT NULL,
                inference_ms    INTEGER,
                final_status    TEXT DEFAULT 'pending',
                needs_review    INTEGER DEFAULT 0,
                reviewed_by     TEXT,
                engineer        TEXT
            )
        """)
        self.conn.commit()

    def write_inspection(self, data: dict):
        # I serialize slots and confidence as JSON strings so SQLite
        # can store them without needing a separate table.
        self.conn.execute("""
            INSERT INTO inspections (
                inspection_id, timestamp_utc, slots, confidence,
                inference_ms, final_status, needs_review
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["inspection_id"],
            data["timestamp_utc"],
            json.dumps(data["slots"]),
            json.dumps(data["confidence"]),
            data.get("inference_ms"),
            data.get("final_status", "pending"),
            int(data.get("needs_review", False)),
        ))
        self.conn.commit()

    def confirm_inspection(self, data: dict) -> bool:
        cursor = self.conn.execute("""
            UPDATE inspections
            SET slots = ?, final_status = ?, reviewed_by = ?
            WHERE inspection_id = ?
        """, (
            json.dumps(data["slots"]),
            data.get("final_status", "reviewed"),
            data.get("engineer"),
            data["inspection_id"],
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
            entry["slots"] = json.loads(entry["slots"])
            entry["confidence"] = json.loads(entry["confidence"])
            result.append(entry)
        return result

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
