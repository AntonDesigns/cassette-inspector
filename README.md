# Cassette Inspector

I built **Cassette Inspector** as an AI-powered cassette inspection
system for semiconductor wafer handling. It processes a live camera feed
through a two-stage computer vision pipeline and exposes the results
through a FastAPI backend with Grad-CAM explanations.

The system is designed to integrate with Trymax UV and 2000 series wafer
handling robots. In real time, it detects the cassette, classifies each
of the 25 slots as occupied or empty, and flags mismatches against the
robot mapper with visual heatmaps so engineers can clearly see why a
decision was made.

![Demo screenshot](docs/screenshots/dashboard.png)

## What it does

-   Detects cassettes in a live camera feed using a based off, YOLO26n-cls, improved throughout training (uses new data, rather the build off yolo26)
-   Classifies all 25 slots per cassette (occupied / empty)\
-   Compares AI predictions against the Trymax mapper result and
    highlights mismatches\
-   Generates Grad-CAM heatmaps for transparent, debuggable predictions\
-   Exposes a REST API for direct integration with Trymax NEO\
-   Runs in the browser (frontend served by FastAPI)

## Architecture

Camera → FastAPI backend → Cassette detector (YOLO26m)\
→ Slot classifier (based off, YOLO26n-cls, improved throughout training (uses new data, rather the build off yolo26))\
→ Grad-CAM explainer\
→ REST API (/api/predict, /api/explain, /api/snapshot, /api/status,
/api/confirm)\
→ Frontend (HTML/CSS/JS served by FastAPI)

I use a two-stage pipeline intentionally. The cassette detector first
locates and crops the cassette from the full frame. The slot classifier
then runs only on that cropped region, which significantly reduces
background noise and improves classification reliability.

## Getting started

### Requirements

-   Python 3.10 or higher\
-   CUDA-capable GPU recommended (CPU works but slower)\
-   Webcam or IP camera

### Install

``` bash
git clone https://github.com/AntonDesigns/cassette-inspector.git
cd cassette-inspector
pip install -e .
```

### Add model weights

Place your trained weights in the `models/` folder:

models/\
cassette_detector/\
best.pt\
slot_classifier/\
best.pt

Model weights are not included in this repository.

### Run

``` bash
cassetteai serve
```

Then open:

http://localhost:8000

## API

  Method   Endpoint        Description
  -------- --------------- ---------------------------------------------
  POST     /api/predict    Run full inference on an image
  POST     /api/explain    Generate Grad-CAM heatmap
  POST     /api/snapshot   Capture and return a camera frame
  GET      /api/status     Model and camera status
  POST     /api/confirm    Engineer confirms or overrides a prediction

Example response from `/api/predict`:

``` json
{
  "slots": [1, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
  "confidence": [0.97, 0.95, 0.98, 0.96, 0.94, 0.95, 0.97, 0.98, 0.96, 0.95,
                 0.97, 0.96, 0.95, 0.98, 0.94, 0.97, 0.96, 0.95, 0.98, 0.97,
                 0.96, 0.95, 0.97, 0.96, 0.98],
  "inference_ms": 380
}
```

## Training

The training notebooks and data pipeline live in a separate private
repository. This repository contains the runtime application layer.

If you want to train your own models:

1.  Collect and label cassette images (YOLO format for detection, slot
    labels for classification)\
2.  Fine-tune the cassette detector (YOLO26m)\
3.  Train the slot classifier (YOLO26n-cls or MobileNet-based approach)\
4.  Place the resulting `best.pt` files in the correct `models/`
    subfolders

## Project context

I developed this during a 20-week internship at Trymax Semiconductor
Equipment B.V. The objective was to replace manual cassette inspection
with a real-time AI system that integrates directly with existing robot
software.

The project evolved in three stages:

-   Stage 1: Cassette detection\
-   Stage 2: Slot classification\
-   Stage 3: Anomaly detection (double-slotting, cross-sided inserts,
    tilted wafers)

## Tech stack

-   PyTorch + Ultralytics YOLO26\
-   YOLO26n-CLS\
-   Grad-CAM\
-   FastAPI + Uvicorn\
-   OpenCV\
-   HTML/CSS/JavaScript\
-   SQLite

## License

MIT
