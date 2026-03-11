import json
from db.base import BaseDB
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

# Level 2 MySQL implementation.
# This is a drop-in replacement for sqlite.py. The interface is identical.
# To activate it I flip DB_BACKEND to "mysql" in config.py. Nothing else changes.
#
# I read credentials from environment variables set in config.py so they
# are never hardcoded or committed to git.


class MySQLDB(BaseDB):

    def __init__(self):
        self.conn = None

    def connect(self):
        import mysql.connector
        self.conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inspections (
                inspection_id   VARCHAR(64) PRIMARY KEY,
                timestamp_utc   VARCHAR(32) NOT NULL,
                slots           TEXT NOT NULL,
                confidence      TEXT NOT NULL,
                inference_ms    INT,
                final_status    VARCHAR(32) DEFAULT 'pending',
                needs_review    TINYINT(1) DEFAULT 0,
                reviewed_by     VARCHAR(128),
                engineer        VARCHAR(128)
            )
        """)
        self.conn.commit()
        cursor.close()

    def write_inspection(self, data: dict):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO inspections (
                inspection_id, timestamp_utc, slots, confidence,
                inference_ms, final_status, needs_review
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
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
        cursor.close()

    def confirm_inspection(self, data: dict) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE inspections
            SET slots = %s, final_status = %s, reviewed_by = %s
            WHERE inspection_id = %s
        """, (
            json.dumps(data["slots"]),
            data.get("final_status", "reviewed"),
            data.get("engineer"),
            data["inspection_id"],
        ))
        self.conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def get_recent(self, limit: int = 20) -> list:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM inspections
            ORDER BY timestamp_utc DESC
            LIMIT %s
        """, (limit,))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            row["slots"] = json.loads(row["slots"])
            row["confidence"] = json.loads(row["confidence"])
            result.append(row)
        return result

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
