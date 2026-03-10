# Cassette Inspector

An AI-powered cassette inspection system for semiconductor wafer handling. It processes a live camera feed through a two-stage computer vision pipeline and exposes the results through a FastAPI backend with Grad-CAM explanations.

Built to integrate with Trymax UV and NEO 2000 series wafer handling robots. In real time, it detects the cassette, classifies each of the 25 slots across 7 states, compares predictions against the robot mapper, and generates visual heatmaps so engineers can clearly see why a decision was made.

![Demo screenshot](docs/screenshots/dashboard.png)

## What it does

- Detects cassettes in a live camera feed using a custom-trained YOLO-based detector
- Classifies all 25 slots per cassette across 7 SlotOccupationStates using a custom-trained model based on YOLO26n-CLS
- Compares AI predictions against the Trymax NEO mapper result and highlights mismatches
- Generates Grad-CAM heatmaps for transparent, debuggable predictions
- Flags low-confidence results for engineer review via deep-link to the slot labeler tool
- Exposes a REST API for direct integration with Trymax NEO software
- Runs in the browser (frontend served by FastAPI)

## Architecture

Two-stage pipeline. The cassette detector first locates and crops the cassette from the full frame. The slot classifier then runs only on that cropped region, reducing background noise and improving reliability.

```
Camera
  -> Cassette detector        (custom-trained, YOLO-based, best.pt)
  -> Slot classifier          (custom-trained, based on YOLO26n-CLS, best.onnx)
  -> Grad-CAM explainer
  -> FastAPI backend
  -> REST API + Browser dashboard
```

## Project structure

```
cassetteai/
├── api/
│   ├── main.py               FastAPI entry point, registers routers only
│   ├── schemas.py            all Pydantic request/response models
│   └── routes/
│       ├── predict.py        POST /api/predict
│       ├── explain.py        POST /api/explain
│       ├── snapshot.py       POST /api/snapshot
│       ├── confirm.py        POST /api/confirm
│       ├── status.py         GET  /api/status
│       └── inspect.py        POST /api/inspect  (Level 2, NEO integration)
├── core/
│   ├── camera.py             OpenCV camera handling
│   ├── inference.py          model loading and prediction
│   ├── gradcam.py            Grad-CAM heatmap generation
│   ├── mapper.py             NEO 2000 raw value translation
│   └── engineer.py           Windows username resolution
├── db/
│   ├── base.py               abstract database interface
│   ├── sqlite.py             Level 1 implementation
│   └── mysql.py              Level 2 implementation (drop-in replacement)
├── dashboard/
│   ├── templates/index.html
│   └── static/
│       ├── css/style.css
│       └── js/               SOLID frontend, one responsibility per module
├── bridge/
│   └── inspect.php           Level 2 PHP bridge for NEO software
├── models/
│   ├── cassette_detector/    best.pt  (not committed)
│   └── slot_classifier/      best.onnx  (not committed)
├── config.py                 only file a colleague needs to edit
├── cli.py
└── pyproject.toml
```

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/predict | Run inference on an image |
| POST | /api/explain | Generate Grad-CAM heatmap |
| POST | /api/snapshot | Capture frame and run inference |
| GET | /api/status | Model and camera status |
| POST | /api/confirm | Engineer confirms or corrects a prediction |
| POST | /api/inspect | NEO integration endpoint (Level 2) |

Example response from `/api/predict`:

```json
{
  "slots": [1, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  "confidence": [0.97, 0.95, 0.98, 0.96, 0.94, 0.95, 0.97, 0.98, 0.96, 0.95,
                 0.97, 0.96, 0.95, 0.98, 0.94, 0.97, 0.96, 0.95, 0.98, 0.97,
                 0.96, 0.95, 0.97, 0.96, 0.98],
  "inference_ms": 380
}
```

Slot values follow the `SlotOccupationState` enum (0-6). See the handoff document for the full state definitions and NEO mapper translation table.

## Getting started

### Requirements

- Python 3.10 or higher
- CUDA-capable GPU recommended (CPU works but slower)
- Webcam or USB industrial camera

### Install

```bash
git clone https://github.com/AntonDesigns/cassette-inspector.git
cd cassette-inspector
pip install -e .
```

### Add model weights

Place your trained model weights in the `models/` folder:

```
models/
├── cassette_detector/
│   └── best.pt
└── slot_classifier/
    └── best.onnx
```

Model weights are not included in this repository.

### Run

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open `http://localhost:8000` in your browser.

The slot labeler tool runs separately on port 5050. Low-confidence results open it automatically via deep-link.

## Training pipeline

Training notebooks and labeled data live in a separate private repository. This repository is the runtime application layer only.

The system uses a continuous improvement cycle:

1. The main app captures inspections and writes results to `inspections.csv`
2. Low-confidence results are flagged and corrected in the slot labeler tool
3. Corrected labels feed back into `inspections.csv`
4. When enough new labeled data exists, retraining notebooks produce an improved model
5. The new model is dropped into `models/` and the app picks it up on next start

## Tech stack

| Component | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Frontend | HTML / CSS / JavaScript |
| Cassette detector | Custom-trained YOLO-based model |
| Slot classifier | Custom-trained model based on YOLO26n-CLS |
| Explainability | Grad-CAM |
| Camera | OpenCV |
| Database (Level 1) | SQLite |
| Database (Level 2) | MySQL (drop-in swap, no code changes) |
| NEO integration | PHP bridge (Level 2) |

## Project context

Developed during a 20-week internship at Trymax Semiconductor Equipment B.V. The objective was to replace manual cassette inspection with a real-time AI system that integrates directly with existing robot software.

The project was delivered in stages:

- **Stage 1:** Cassette detection
- **Stage 2:** Slot classification with 7-state SlotOccupationState model and engineer review workflow
- **Stage 3:** NEO software integration via REST API and PHP bridge

## License

MIT
