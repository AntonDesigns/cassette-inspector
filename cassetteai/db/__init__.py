# Database package.
# The rest of the app imports only from db/base.py.
# Nothing outside this folder ever imports sqlite.py or mysql.py directly.

from db.base import get_db
