from abc import ABC, abstractmethod
from config import DB_BACKEND

# This is the only file the rest of the app imports from.
# I define the interface here. The actual implementation lives in
# sqlite.py for Level 1 and mysql.py for Level 2.
# When I flip DB_BACKEND in config.py from "sqlite" to "mysql",
# the whole app switches backends without any other code changing.


class BaseDB(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def write_inspection(self, data: dict):
        pass

    @abstractmethod
    def confirm_inspection(self, data: dict) -> bool:
        pass

    @abstractmethod
    def get_recent(self, limit: int = 20) -> list:
        pass

    @abstractmethod
    def close(self):
        pass


def get_db() -> BaseDB:
    # The single place where I decide which backend to use.
    # Everything else calls get_db() and gets back a BaseDB.
    # Nothing outside this file knows whether it is SQLite or MySQL.
    if DB_BACKEND == "mysql":
        from db.mysql import MySQLDB
        db = MySQLDB()
    else:
        from db.sqlite import SQLiteDB
        db = SQLiteDB()

    db.connect()
    return db
