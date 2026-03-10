# MySQL implementation of the Database interface (Level 2).
# Drop-in replacement for sqlite.py. Same interface, different backend.
# Nothing outside this file knows it is MySQL.
from db.base import Database

class MySQLDB(Database):

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host     = host
        self.user     = user
        self.password = password
        self.database = database
        self._conn    = None

    def connect(self):
        # TODO: import mysql.connector and connect
        pass

    def write_inspection(self, data: dict):
        # TODO: insert inspection row
        pass

    def get_recent(self, limit: int) -> list:
        # TODO: query recent inspections
        return []

    def close(self):
        if self._conn:
            self._conn.close()
