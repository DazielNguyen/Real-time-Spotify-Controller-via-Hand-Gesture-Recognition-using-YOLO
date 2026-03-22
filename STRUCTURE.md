# Project Structure Guide

## Folder Organization

This document explains the project structure and where to find each component.

```
real-time-spotify-controller/
│
├── README.md                    ← Start here! Main project documentation
├── CONTRIBUTING.md              ← How to contribute
├── requirements.txt             ← Python dependencies
├── setup.py                     ← Installation script
├── LICENSE                      ← MIT License
│
├── src/                         ← Source code (executables)
│   ├── hand_tracking.py         ← Main inference script (RUN THIS)
│   ├── generate_report_figures.py       ← Generate training curves
│   └── generate_pipeline_and_realtime_figures.py  ← Generate diagrams
│
├── models/                      ← ML model weights
│   └── weights/
│       ├── yolov8n.pt           ← YOLOv8 Nano pretrained
│       └── yolo26n.pt           ← Alternative checkpoint
│
├── dataset/                     ← Training dataset (YOLO format)
│   ├── images/
│   │   ├── train/               ← 8,487 training images
│   │   └── val/                 ← 2,121 validation images
│   ├── labels/
│   │   ├── train/               ← Bounding box annotations
│   │   └── val/
│   ├── data.yaml                ← Dataset configuration
│   ├── data_runtime.yaml        ← Runtime settings
│   └── classes.txt              ← Class names (fist, one, peace, etc.)
│
├── runs/                        ← Training outputs and logs
│   └── detect/
│       └── gesture_v100_ft/     ← Fine-tuned model results
│           ├── weights/
│           │   ├── best.pt      ← Best epoch checkpoint (mAP50-95: 0.87623)
│           │   └── last.pt      ← Final epoch checkpoint
│           ├── results.csv      ← 100-epoch metrics log
│           └── plots/           ← Training visualizations
│
├── docs/                        ← Documentation
│   ├── report.md                ← Technical research paper (IEEE format)
│   └── figures/                 ← Generated visualizations
│       ├── fig1_pipeline_placeholder.png         ← Architecture diagram
│       ├── fig2_metrics_placeholder.png          ← Accuracy curves
│       ├── fig3_loss_placeholder.png             ← Training loss curves
│       └── fig4_realtime_ui_placeholder.png      ← Inference mockup
│
├── notebooks/                   ← Jupyter notebooks
│   └── YOLOv8.ipynb             ← Training notebook
│
├── configs/                     ← Configuration files (extensible)
│
└── .gitignore                   ← Git ignore patterns
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Hand Detection

```bash
python3 src/hand_tracking.py
```

### 3. Generate Training Figures (Optional)

```bash
# Generate metrics and loss curves
python3 src/generate_report_figures.py

# Generate pipeline diagram and UI mockup
python3 src/generate_pipeline_and_realtime_figures.py
```

## Key Files

| File | Purpose | Size |
|------|---------|------|
| `src/hand_tracking.py` | Main real-time detection script | 320 KB |
| `models/weights/yolov8n.pt` | Model weights | 12.6 MB |
| `runs/detect/.../weights/best.pt` | Fine-tuned model | 12.6 MB |
| `dataset/` | Training data (10,608 images) | ~2.5 GB |
| `docs/report.md` | Technical paper | 45 KB |
| `docs/figures/` | Visualizations | ~3 MB |

## Where to Find What?

| I want to... | Location |
|--------------|----------|
| Run gesture control | `python3 src/hand_tracking.py` |
| Read documentation | `README.md` |
| View technical details | `docs/report.md` |
| Access training data | `dataset/` |
| Check model weights | `models/weights/` or `runs/detect/.../weights/` |
| See results and charts | `runs/detect/gesture_v100_ft/` |
| Modify code | `src/` |
| Review history | `.git/` (git commits) |

## Configuration Paths

When running scripts, paths are relative to project root:

```python
# Models are auto-discovered from:
runs/detect/*/weights/best.pt
runs/detect/*/weights/last.pt

# Training data is read from:
dataset/images/train/
dataset/images/val/
dataset/labels/train/
dataset/labels/val/

# Results are saved to:
runs/detect/gesture_v100_ft/results.csv
docs/figures/*.png
```

## Dataset Structure Breakdown

### Images Directory
```
dataset/images/
├── train/    (8,487 images)
│   ├── 0010984f-71e2-403a-b62c-edf76647b5d5.jpg
│   ├── 001c5ee9-43f0-46b5-9854-36a6faf7c51b.jpg
│   └── ... (8,485 more)
└── val/      (2,121 images)
    ├── 0035c780-f055-4a42-9da9-4c02df40f634.jpg
    └── ... (2,120 more)
```

### Labels Directory (YOLO Format)
```
dataset/labels/
├── train/    (8,487 .txt files, one per image)
│   ├── 0010984f-71e2-403a-b62c-edf76647b5d5.txt
│   └── ...
└── val/      (2,121 .txt files)
    └── ...

# File format (YOLO)
# Each line: class_id center_x center_y width height
# All coordinates normalized to [0, 1]
# Example:
0 0.45 0.52 0.23 0.31
```

## Gesture Class Mapping

```
Class ID  →  Class Name  →  Boxes (Train)  →  Action
0         →  fist        →  1,372          →  Pause
1         →  one         →  1,424          →  Next Track
2         →  peace       →  1,411          →  Previous Track
3         →  three       →  1,406          →  Volume Up
4         →  four        →  1,444          →  Volume Down
5         →  palm        →  1,429          →  Play
6         →  no_gesture  →  1,981          →  (Background/Filter)
```

## Running from Different Locations

### Option 1: From Project Root (Recommended)
```bash
cd /path/to/real-time-spotify-controller/
python3 src/hand_tracking.py
```

### Option 2: From Anywhere (if installed with pip)
```bash
pip install -e .  # First time setup
gesture-control   # Run from anywhere
```

### Option 3: Direct Python
```bash
cd /path/to/real-time-spotify-controller/
python3 -m src.hand_tracking
```

## Troubleshooting Paths

If the script can't find models or data:

1. **Check current directory**
   ```bash
   pwd
   ```

2. **Verify file structure**
   ```bash
   ls -la runs/detect/
   ls -la dataset/
   ls -la models/
   ```

3. **Check relative paths in code**
   - `hand_tracking.py` looks for `runs/detect/*/weights/*.pt`
   - Dataset is in `dataset/images/` and `dataset/labels/`

4. **Run from project root**
   ```bash
   cd real-time-spotify-controller
   python3 src/hand_tracking.py
   ```

## Additional Resources

- **Main README**: [README.md](README.md)
- **Research Paper**: [docs/report.md](docs/report.md)
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Requirements**: [requirements.txt](requirements.txt)

---

**Last Updated**: March 2024

