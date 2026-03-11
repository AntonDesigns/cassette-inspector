# CassetteAI main application config.
# This is the only file a colleague needs to edit to run on a new machine.
from pathlib import Path
import os

# Engineer list — used for Windows username matching and the dropdown fallback.
ENGINEERS = [
    {"name": "Anton Horvat", "role": "Intern",               "windows_user": "anton.horvat"},
    {"name": "Robin",        "role": "Software Developer",   "windows_user": "robin"},
    {"name": "Linde",        "role": "Software Engineer",    "windows_user": "linde"},
    {"name": "Emiel",        "role": "Lead-System Engineer", "windows_user": "emiel"},
    {"name": "Johan",        "role": "Software Teamleader",  "windows_user": "johan"},
    {"name": "Paul",         "role": "Software Tester",      "windows_user": "paul"},
]

# Slot labeler URL — used when opening the deep link from the dashboard.
LABELER_URL = "http://localhost:5050"

# Model paths
MODELS_DIR           = Path(__file__).parent / "models"
CASSETTE_MODEL_PATH  = MODELS_DIR / "cassette_detector" / "best.pt"
SLOT_MODEL_PATH      = MODELS_DIR / "slot_classifier"   / "best.onnx"

# Database (Level 1: SQLite, Level 2: swap to MySQL)
DB_BACKEND  = "sqlite"
SQLITE_PATH = Path(__file__).parent / "cassetteai.db"

# MySQL settings (Level 2 only)
MYSQL_HOST     = os.getenv("MYSQL_HOST",     "localhost")
MYSQL_USER     = os.getenv("MYSQL_USER",     "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "cassetteai")

# Server
HOST = "0.0.0.0"
PORT = 8000

# Slot model version (1 = binary only, 2 = all 7 states)
SLOT_MODEL_VERSION = 1
