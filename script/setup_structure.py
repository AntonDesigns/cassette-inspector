import os

# Base directory — run this script from the repo root
BASE = "cassetteai"

files = {

    # API layer
    "api/main.py": '''\
# CassetteAI - FastAPI entry point
# Registers all routers. No business logic lives here.
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CassetteAI", version="1.0.0")

# TODO: import and register routers from api/routes/
''',

    "api/schemas.py": '''\
# Pydantic request and response models.
# Every endpoint input and output is typed here.
from pydantic import BaseModel
from typing import List, Optional

class PredictResponse(BaseModel):
    slots: List[int]
    confidence: List[float]
    inference_ms: int

class InspectRequest(BaseModel):
    image_b64: str
    machine_type: Optional[str] = None
    engineer: Optional[str] = None
''',

    "api/routes/predict.py": '''\
# POST /api/predict
# Accepts a cassette image, returns 25-slot predictions.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/predict")
async def predict():
    # TODO: call core.inference
    pass
''',

    "api/routes/explain.py": '''\
# POST /api/explain
# Accepts a cassette image, returns Grad-CAM heatmap as base64.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/explain")
async def explain():
    # TODO: call core.gradcam
    pass
''',

    "api/routes/snapshot.py": '''\
# POST /api/snapshot
# Captures current camera frame, runs prediction, writes to DB.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/snapshot")
async def snapshot():
    # TODO: call core.camera + core.inference + db
    pass
''',

    "api/routes/confirm.py": '''\
# POST /api/confirm
# Engineer confirms or corrects AI predictions. Writes ground truth to DB.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/confirm")
async def confirm():
    # TODO: write confirmed labels to db
    pass
''',

    "api/routes/status.py": '''\
# GET /api/status
# Returns model status, last inference time, camera connection state.
from fastapi import APIRouter
router = APIRouter()

@router.get("/api/status")
async def status():
    # TODO: return live status from core modules
    pass
''',

    "api/routes/inspect.py": '''\
# POST /api/inspect  (Level 2)
# Called by Trymax NEO software via the PHP bridge.
# Accepts a cassette image, returns SlotOccupationState[] JSON.
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/inspect")
async def inspect():
    # TODO: call core.inference + core.mapper
    pass
''',

    "api/routes/__init__.py": "",

    # Core modules — each does exactly one thing
    "core/camera.py": '''\
# Camera module — OpenCV only.
# Handles frame capture from webcam or industrial camera.
# Does not know about inference, the database, or the API.
import cv2

class Camera:
    def __init__(self, source=0):
        self.source = source
        self._cap = None

    def open(self):
        self._cap = cv2.VideoCapture(self.source)

    def capture_frame(self):
        if not self._cap:
            raise RuntimeError("Camera not open")
        ok, frame = self._cap.read()
        return frame if ok else None

    def release(self):
        if self._cap:
            self._cap.release()
''',

    "core/inference.py": '''\
# Inference module — model loading and prediction only.
# Does not know about the camera, the database, or the API.
# Swap PyTorch for ONNX here without touching anything else.

class SlotInference:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def load(self):
        # TODO: load PyTorch or ONNX model from self.model_path
        pass

    def predict(self, image):
        # Returns {"slots": [...], "confidence": [...], "inference_ms": int}
        # TODO: run inference
        pass
''',

    "core/gradcam.py": '''\
# Grad-CAM module — heatmap generation only.
# Does not know about the camera, the database, or the API.

class GradCAM:
    def __init__(self, model):
        self.model = model

    def generate(self, image):
        # Returns base64 heatmap overlay image
        # TODO: implement pytorch-grad-cam
        pass
''',

    "core/mapper.py": '''\
# Mapper module — NEO raw value translation only.
# Translates NEO 2000 series raw integers (0-9) to SlotOccupationState (0-6).
# NEO UV series already outputs SlotOccupationState directly, no translation needed.

NEO_2000_MAP = {
    0: 1,  # not exist  -> Empty
    1: 3,  # exists     -> CorrectlyOccupied
    2: 2,  # thick      -> NotEmpty
    3: 5,  # cross      -> CrossSlotted
    4: 5,  # bow/lift   -> CrossSlotted
    7: 4,  # multiple   -> DoubleSlotted
    8: 2,  # thin       -> NotEmpty
    9: 0,  # failure    -> Undefined
}

def translate_neo_2000(raw_values: list) -> list:
    return [NEO_2000_MAP.get(v, 0) for v in raw_values]
''',

    "core/engineer.py": '''\
# Engineer identity module — Windows username resolution + dropdown fallback.
# Reads the logged-in Windows username and matches it against the ENGINEERS list.
# Does not know about the API, the database, or the camera.
import os

def resolve_engineer(engineers: list) -> str | None:
    windows_user = os.environ.get("USERNAME", "").lower().strip()
    for eng in engineers:
        if eng.get("windows_user", "").lower() == windows_user:
            return eng["name"]
    return None
''',

    "core/__init__.py": "",

    # Database layer — abstract interface + two implementations
    "db/base.py": '''\
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
''',

    "db/sqlite.py": '''\
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
''',

    "db/mysql.py": '''\
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
''',

    "db/__init__.py": "",

    # Dashboard — frontend following the same SOLID JS pattern as the labeler
    "dashboard/templates/index.html": '''\
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CassetteAI | Trymax</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
  <header></header>
  <main id="mainGrid"></main>
  <div class="toast" id="toast"></div>

  <script src="/static/js/config.js"></script>
  <script src="/static/js/state.js"></script>
  <script src="/static/js/api.js"></script>
  <script src="/static/js/ui/toast.js"></script>
  <script src="/static/js/ui/camera.js"></script>
  <script src="/static/js/ui/overlay.js"></script>
  <script src="/static/js/ui/gradcam.js"></script>
  <script src="/static/js/ui/comparison.js"></script>
  <script src="/static/js/ui/history.js"></script>
  <script src="/static/js/ui/theme.js"></script>
  <script src="/static/js/actions/inspectActions.js"></script>
  <script src="/static/js/actions/reviewActions.js"></script>
  <script src="/static/js/main.js"></script>
</body>
</html>
''',

    "dashboard/static/css/style.css": '''\
/* CassetteAI dashboard styles */
/* TODO: build out from the slot labeler style.css as base */
''',

    "dashboard/static/js/config.js": '''\
// Single source of truth for slot states and app constants.
// Same pattern as the slot labeler config.js.

var SLOT_STATES = {
  0: { name: "Undefined",         cls: "s-undef",    icon: "?" },
  1: { name: "Empty",             cls: "s-empty",    icon: "○" },
  2: { name: "NotEmpty",          cls: "s-notempty", icon: "◐" },
  3: { name: "CorrectlyOccupied", cls: "s-occupied", icon: "●" },
  4: { name: "DoubleSlotted",     cls: "s-double",   icon: "◉" },
  5: { name: "CrossSlotted",      cls: "s-cross",    icon: "✕" },
  6: { name: "Reserved",          cls: "s-reserved", icon: "-" },
};

var APP_CONFIG = {
  SLOT_COUNT:     25,
  TOAST_DURATION: 1600,
  LABELER_URL:    "http://localhost:5050",
};
''',

    "dashboard/static/js/state.js": '''\
// Single shared State object for all runtime data.
// Every module reads from here. Nobody creates their own copy.

var State = {
  engineer:     null,
  cameraActive: false,
  lastResult:   null,
  history:      [],
};
''',

    "dashboard/static/js/api.js": '''\
// Every fetch() call lives here and nowhere else.
// When a route changes in main.py, this is the only JS file that needs updating.

var API = {

  predict: async function (imageB64) {
    var res = await fetch("/api/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ image_b64: imageB64 }),
    });
    return res.json();
  },

  explain: async function (imageB64) {
    var res = await fetch("/api/explain", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ image_b64: imageB64 }),
    });
    return res.json();
  },

  snapshot: async function () {
    var res = await fetch("/api/snapshot", { method: "POST" });
    return res.json();
  },

  confirm: async function (data) {
    var res = await fetch("/api/confirm", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(data),
    });
    return res.json();
  },

  status: async function () {
    var res = await fetch("/api/status");
    return res.json();
  },

};
''',

    "dashboard/static/js/main.js": '''\
// Boot file — the only file that knows about all other modules.
// Wires event listeners and starts the app. No business logic here.

(async function boot() {
  // TODO: init UI modules, fetch status, start camera feed
}());
''',

    "dashboard/static/js/ui/toast.js":      '// Toast.show(msg, colour) — timed notification. Same as slot labeler.\nvar Toast = { show: function(msg, col) {} };\n',
    "dashboard/static/js/ui/camera.js":     '// Camera.init() — renders the live webcam feed into the camera panel.\nvar Camera = { init: function() {} };\n',
    "dashboard/static/js/ui/overlay.js":    '// Overlay.render(slots, confidence) — draws the 25-slot prediction overlay on the camera feed.\nvar Overlay = { render: function(slots, confidence) {} };\n',
    "dashboard/static/js/ui/gradcam.js":    '// GradCAM.show(heatmapB64) — toggles the Grad-CAM heatmap over the camera feed.\nvar GradCAM = { show: function(heatmapB64) {} };\n',
    "dashboard/static/js/ui/comparison.js": '// Comparison.render(aiSlots, mapperSlots) — side by side AI vs mapper panel.\nvar Comparison = { render: function(aiSlots, mapperSlots) {} };\n',
    "dashboard/static/js/ui/history.js":    '// History.render(items) — session history list of recent inspections.\nvar History = { render: function(items) {} };\n',
    "dashboard/static/js/ui/theme.js":      '// Theme.init() — dark/light toggle. Same pattern as slot labeler.\nvar Theme = { init: function() {} };\n',

    "dashboard/static/js/actions/inspectActions.js": '''\
// Inspect-level actions: trigger snapshot, accept result, flag for review.
// Calls API and updates State. No DOM manipulation here.
var InspectActions = {
  snapshot:     async function() {},
  flagForReview: function(cropPath) {
    // Opens the slot labeler deep link with the flagged crop and engineer name.
    var params = "crop=" + encodeURIComponent(cropPath) + "&engineer=" + encodeURIComponent(State.engineer || "");
    window.open(APP_CONFIG.LABELER_URL + "?" + params);
  },
};
''',

    "dashboard/static/js/actions/reviewActions.js": '''\
// Review-level actions: confirm AI predictions, correct slots, submit ground truth.
var ReviewActions = {
  confirm: async function(slots) {},
  correct: function(slotIndex, value) {},
};
''',

    "dashboard/static/img/.gitkeep": "",

    # PHP bridge (Level 2)
    "bridge/inspect.php": '''\
<?php
// Level 2 PHP bridge — forwards NEO software requests to the FastAPI backend.
// The NEO machine calls this endpoint. This file calls FastAPI and returns the result.
// Nothing in the Python codebase knows this file exists.

$fastapi_url = "http://localhost:8000/api/inspect";

$image_data = file_get_contents("php://input");

$ch = curl_init($fastapi_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $image_data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
curl_close($ch);

header("Content-Type: application/json");
echo $response;
?>
''',

    # Models folder
    "models/cassette_detector/.gitkeep": "",
    "models/slot_classifier/.gitkeep":   "",

    # Docs
    "docs/screenshots/.gitkeep": "",

    # Root config
    "config.py": '''\
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
''',

}

# Gitignore — replaces the current one
GITIGNORE = """\
# Model weights — never commit these
models/**/*.pt
models/**/*.pth
models/**/*.onnx

# Python
__pycache__/
*.py[cod]
*.pyd
*.pyo
.Python
*.egg
*.egg-info/
dist/
build/
.eggs/
.installed.cfg

# Virtual environments
.venv/
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Logs and runtime data
*.log
*.db
data/

# Environment variables
.env
.env.local

# Screenshots — keep folder, ignore images except the demo
docs/screenshots/*
!docs/screenshots/.gitkeep
!docs/screenshots/dashboard.png
cassetteai/docs/screenshots/*
!cassetteai/docs/screenshots/.gitkeep
!cassetteai/docs/screenshots/dashboard.png
"""

def create_structure():
    for rel_path, content in files.items():
        full_path = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  created  {full_path}")
        else:
            print(f"  exists   {full_path} (skipped)")

    # Write .gitignore at repo root
    gitignore_path = ".gitignore"
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(GITIGNORE)
    print(f"  updated  {gitignore_path}")

    print("\nDone. All files created.")

if __name__ == "__main__":
    create_structure()
