# Abstract database interface.
# Both SQLite (Level 1) and MySQL (Level 2) implement this.
# The rest of the application only ever imports from here, never from
# sqlite.py or mysql.py directly. That is the Dependency Inversion principle.
from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def write_inspection(self, data: dict): pass

    @abstractmethod
    def get_recent(self, limit: int) -> list: pass

    @abstractmethod
    def close(self): pass
