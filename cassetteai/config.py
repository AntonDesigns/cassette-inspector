import os
from pathlib import Path

# This is the only file you need to edit to run this on a new machine.
# Everything else reads from here. Do not hardcode paths or names anywhere else.

# ---------------------------------------------------------------
# Engineers
# I keep the full team list here. When someone new joins, add them.
# The windows_user field needs to match their actual Windows domain
# username exactly. At startup I read os.environ.get("USERNAME") and
# match it against this list to figure out who is sitting at the machine.
# If I cannot find a match, the dashboard shows a dropdown so the
# engineer can pick their name manually. No passwords, no fuss.
# ---------------------------------------------------------------

ENGINEERS = [
    {"name": "Anton Horvat",  "role": "Intern",               "windows_user": "anton.horvat"},
    {"name": "Robin",         "role": "Software Developer",    "windows_user": "robin"},
    {"name": "Linde",         "role": "Software Engineer",     "windows_user": "linde"},
    {"name": "Emiel",         "role": "Lead-System Engineer",  "windows_user": "emiel"},
    {"name": "Johan",         "role": "Software Teamleader",   "windows_user": "johan"},
    {"name": "Paul",          "role": "Software Tester",       "windows_user": "paul"},
]

# ---------------------------------------------------------------
# Server
# I bind to 0.0.0.0 so the app is reachable from other machines
# on the Trymax network. Do not change this to 127.0.0.1 or the
# NEO software will not be able to reach the backend in Level 2.
# ---------------------------------------------------------------

HOST = "0.0.0.0"
PORT = 8000

# ---------------------------------------------------------------
# Slot labeler deep link
# When the main app flags an image for review, I open the slot
# labeler directly on that image using this base URL. The format
# is: http://localhost:5050?crop=<path>&engineer=<name>
# ---------------------------------------------------------------

LABELER_URL = "http://localhost:5050"

# ---------------------------------------------------------------
# Database
# I use SQLite for Level 1. When Level 2 is ready, flip DB_BACKEND
# to "mysql" and that is the only line that needs to change.
# Nothing else in the app knows or cares which one is active.
# ---------------------------------------------------------------

DB_BACKEND = "sqlite"

SQLITE_PATH = Path(__file__).parent / "cassetteai.db"

# I read MySQL credentials from environment variables so they are
# never hardcoded or committed to git.
MYSQL_HOST     = os.environ.get("MYSQL_HOST",     "localhost")
MYSQL_USER     = os.environ.get("MYSQL_USER",     "")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "cassetteai")

# ---------------------------------------------------------------
# Model paths
# I never commit model files to git. Place best.pt and best.onnx
# in the folders below after training.
# ---------------------------------------------------------------

MODELS_DIR          = Path(__file__).parent / "models"
CASSETTE_MODEL_PATH = MODELS_DIR / "cassette_detector" / "best.pt"
SLOT_MODEL_PATH     = MODELS_DIR / "slot_classifier"   / "best.onnx"

# Flip this to 2 when mapper data is integrated and machine type
# detection is working. The labeler and the main app both respect
# this number. No other code changes needed.
SLOT_MODEL_VERSION = 1

# ---------------------------------------------------------------
# Data roots
# I resolve the data folder in this order:
#   1. CASSETTE_DATA_ROOT environment variable, set this on any
#      new machine and nothing else needs touching
#   2. LOCAL_DATA_ROOT, my own laptop path while developing
#   3. COMPANY_DATA_ROOT, the Z: drive share for Level 2
#   4. SIBLING_DATA_ROOT, folder next to the repo as a last resort
# ---------------------------------------------------------------

LOCAL_DATA_ROOT   = Path("C:/Users/anton.horvat/Documents/ImageDetection")
COMPANY_DATA_ROOT = Path("Z:/D&E/Engineering/AI/Cassette-Inspection")
SIBLING_DATA_ROOT = Path(__file__).parent.parent / "ImageDetection"

def get_data_root() -> Path:
    env = os.environ.get("CASSETTE_DATA_ROOT")
    if env:
        return Path(env)
    if LOCAL_DATA_ROOT.exists():
        return LOCAL_DATA_ROOT
    if COMPANY_DATA_ROOT.exists():
        return COMPANY_DATA_ROOT
    return SIBLING_DATA_ROOT

DATA_ROOT = get_data_root()
