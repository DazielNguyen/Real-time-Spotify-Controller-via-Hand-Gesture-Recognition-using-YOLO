# Quick Start Guide

## Get Started in 3 Minutes

### Step 1: Install Dependencies
```bash
cd real-time-spotify-controller
pip install -r requirements.txt
```

### Step 2: Run Hand Gesture Detection
```bash
python3 src/hand_tracking.py
```

### Step 3: Control Music with Hand Gestures
- Palm → Play
- Fist → Pause
- One → Next Track
- Peace → Previous Track
- Three → Volume Up
- Four → Volume Down

---

## Common Commands

### See Help
```bash
python3 src/hand_tracking.py --help
```

### Custom Confidence (Higher = Stricter)
```bash
python3 src/hand_tracking.py --conf 0.50
```

### Faster Response
```bash
python3 src/hand_tracking.py --conf 0.25 --stable-frames 2
```

### More Reliable (Fewer False Triggers)
```bash
python3 src/hand_tracking.py --conf 0.55 --stable-frames 6 --cooldown 3.0
```

### Different Camera
```bash
python3 src/hand_tracking.py --camera 1
```

---

## Important Files

| File | Purpose |
|------|---------|
| README.md | Full documentation |
| src/hand_tracking.py | Main script |
| models/weights/yolov8n.pt | Model weights |
| dataset/ | Training data |
| docs/report.md | Technical paper |

---

## Troubleshooting Quick Fix

**Camera not detected?**
```bash
python3 src/hand_tracking.py --camera 0  # or --camera 1
```

**No gestures detected?**
```bash
python3 src/hand_tracking.py --conf 0.25
```

**Too many false triggers?**
```bash
python3 src/hand_tracking.py --conf 0.50 --stable-frames 5
```

**Spotify commands not working?**
```bash
osascript -e 'tell application "Spotify" to playpause'
```

---

## Learn More

- Full guide: README.md
- Project structure: STRUCTURE.md
- Contributing: CONTRIBUTING.md
- Research paper: docs/report.md

---

Status: Production Ready
Last Updated: March 2024
