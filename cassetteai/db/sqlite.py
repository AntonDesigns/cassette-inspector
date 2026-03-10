# SQLite implementation of the Database interface (Level 1).
# Swap this for mysql.py when moving to Level 2.
# Nothing outside this file knows it is SQLite.
import sqlite3
from db.base import Database

class SQLiteDB(Database):

    def __init__(self, path: str):
        self.path = path
        self._conn = None

    def connect(self):
        self._conn = sqlite3.connect(self.path, check_same_thread=False)

    def write_inspection(self, data: dict):
        # TODO: insert inspection row
        pass

    def get_recent(self, limit: int) -> list:
        # TODO: query recent inspections
        return []

    def close(self):
        if self._conn:
            self._conn.close()
