from abc import ABC, abstractmethod
from config import DB_BACKEND

# This is the only file the rest of the app imports from.
# I define the interface here. The actual implementation lives in
# sqlite.py for Level 1 and mysql.py for Level 2.
#
# When I flip DB_BACKEND in config.py from "sqlite" to "mysql",
# the whole app switches backends without any other code changing.
# That is Liskov Substitution in practice: sqlite and mysql are
# interchangeable because they both satisfy this interface.


class BaseDB(ABC):

    @abstractmethod
    def connect(self):
        # Open the database connection.
        pass

    @abstractmethod
    def write_inspection(self, data: dict):
        # Write a new inspection row. Called by snapshot.py after every scan.
        # data contains inspection_id, timestamp_utc, slots, confidence,
        # inference_ms, final_status, and needs_review.
        pass

    @abstractmethod
    def confirm_inspection(self, data: dict) -> bool:
        # Update an existing row when the engineer confirms or corrects the result.
        # data contains inspection_id, slots, engineer, and final_status.
        # Returns True if the row was found and updated, False if not found.
        pass

    @abstractmethod
    def get_recent(self, limit: int = 20) -> list:
        # Return the most recent inspections for the dashboard history panel.
        # I return them newest first.
        pass

    @abstractmethod
    def close(self):
        # Close the connection cleanly on shutdown.
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
