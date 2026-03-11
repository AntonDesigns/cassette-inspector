import json
from db.base import BaseDB
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

# Level 2 MySQL implementation.
# Nothing outside this file knows it is MySQL.
# This is a drop-in replacement for sqlite.py. The interface is identical.
# To activate it I flip DB_BACKEND to "mysql" in config.py. Nothing else changes.
#
# Column names match inspections.csv exactly, same as sqlite.py.
# The two implementations must always stay in sync with each other.
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
                crop_image_path VARCHAR(512),
                final_status    VARCHAR(32) DEFAULT 'pending',
                needs_review    TINYINT(1) DEFAULT 0,
                reviewed_by     VARCHAR(128),
                machine_type    VARCHAR(16),
                cassette_type   VARCHAR(32),
                ai_slots        TEXT,
                ai_conf         TEXT,
                inference_ms    INT
            )
        """)
        self.conn.commit()
        cursor.close()

    def write_inspection(self, data: dict):
        # ai_slots holds ai_s01..ai_s25 values.
        # ai_conf holds ai_p01..ai_p25 values.
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO inspections (
                inspection_id, timestamp_utc, crop_image_path, final_status,
                needs_review, reviewed_by, machine_type, cassette_type,
                ai_slots, ai_conf, inference_ms
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                final_status = VALUES(final_status),
                ai_slots = VALUES(ai_slots),
                ai_conf = VALUES(ai_conf),
                inference_ms = VALUES(inference_ms)
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
        cursor.close()

    def confirm_inspection(self, data: dict) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE inspections
            SET ai_slots = %s, final_status = %s, reviewed_by = %s
            WHERE inspection_id = %s
        """, (
            json.dumps(data.get("slots", [])),
            data.get("final_status", "reviewed"),
            data.get("engineer"),
            data.get("inspection_id"),
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
            row["ai_slots"] = json.loads(row["ai_slots"] or "[]")
            row["ai_conf"] = json.loads(row["ai_conf"] or "[]")
            result.append(row)
        return result

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
