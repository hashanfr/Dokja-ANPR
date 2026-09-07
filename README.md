# DOK-ANPR

## AI-Powered Automatic Number Plate Recognition
### Vehicle Detection and Monitoring System

DOK-ANPR is a local AI-powered Automatic Number Plate Recognition
and vehicle detection system built using Python, Flask, OpenCV,
YOLO and OCR.

The system processes recorded traffic videos and attempts to:

- Detect vehicles
- Identify vehicle types
- Detect number plates
- Read plates using OCR
- Validate plate numbers
- Suppress duplicate detections
- Store detections in SQLite
- Display results through a web dashboard

---

## Architecture

CAPTURE
→ DETECT
→ READ
→ VERIFY
→ STORE
→ DISPLAY

---

## Technology Stack

- Python
- Flask
- OpenCV
- Ultralytics YOLO
- EasyOCR
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript
- Bootstrap
- Chart.js

---

## Project Structure

```text
dok-anpr/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   ├── vehicle/
│   │   └── vehicle_model.pt
│   │
│   └── plate/
│       └── plate_model.pt
│
├── services/
│   ├── vehicle_detector.py
│   ├── plate_detector.py
│   ├── ocr_engine.py
│   ├── video_processor.py
│   └── detection_manager.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── routes/
│   ├── dashboard.py
│   ├── video.py
│   ├── detections.py
│   └── analytics.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── analysis.html
│   ├── detections.html
│   ├── vehicle_details.html
│   ├── analytics.html
│   └── settings.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   └── snapshots/
│
├── uploads/
│
└── data/
    └── anpr.db