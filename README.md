# Real-time Spotify Controller via Hand Gesture Recognition using YOLO

A sophisticated real-time hand gesture recognition system powered by YOLOv8 object detection. Control Spotify and system media playback on macOS using intuitive hand gestures with minimal latency and high accuracy.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Latest-brightgreen.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Performance Metrics](#performance-metrics)
- [Gesture Mapping](#gesture-mapping)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Research Paper](#research-paper)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Real-time Detection**: Process 30+ FPS with minimal latency on standard hardware
- **7-Class Recognition**: Detect fist, one, peace, three, four, palm, and background gestures
- **Smart Trigger System**: 
  - Confidence-based filtering to eliminate false positives
  - Temporal stability checks (requires 4+ consistent frames)
  - Action cooldown mechanism (2+ seconds between commands)
- **macOS Integration**: Direct AppleScript integration with Spotify and system media controls
- **Optimized Inference**: Pretrained yolov8n weights, fine-tuned for hand gesture recognition
- **Production-Ready**: Tested on real-world webcam streams with robust error handling

---

## System Architecture

```
┌─────────────────────┐
│  Webcam Stream      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Frame Capture      │
│  (OpenCV/AVF)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  YOLOv8 Inference   │
│  (Gesture Detection)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Gesture Decision   │
│  (Confidence Filter)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Temporal Stability │
│  (4-Frame Buffer)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Action Cooldown    │
│  (2+ Second Safety) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  macOS Control      │
│  (AppleScript/API)  │
└─────────────────────┘
```

---

## Project Structure

```
real-time-spotify-controller/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── LICENSE                            # MIT License
│
├── src/                               # Source code
│   ├── hand_tracking.py               # Main inference script
│   ├── generate_report_figures.py      # Metrics visualization
│   └── generate_pipeline_and_realtime_figures.py  # Diagram generation
│
├── models/                            # Model weights
│   └── weights/
│       ├── yolov8n.pt                 # YOLOv8 Nano pretrained
│       └── yolo26n.pt                 # Alternative checkpoint
│
├── dataset/                           # Training dataset
│   ├── images/
│   │   ├── train/                     # 8,487 training images
│   │   └── val/                       # 2,121 validation images
│   ├── labels/                        # YOLO format annotations
│   │   ├── train/                     # Training labels
│   │   └── val/                       # Validation labels
│   ├── data.yaml                      # Dataset configuration
│   ├── data_runtime.yaml              # Runtime configuration
│   └── classes.txt                    # Class definitions
│
├── runs/                              # Training outputs
│   └── detect/
│       └── gesture_v100_ft/           # Fine-tuned model results
│           ├── weights/
│           │   ├── best.pt            # Best epoch checkpoint
│           │   └── last.pt            # Final epoch checkpoint
│           └── results.csv            # Training metrics (100 epochs)
│
├── docs/                              # Documentation
│   ├── report.md                      # Technical research paper (IEEE format)
│   └── figures/                       # Generated visualizations
│       ├── fig1_pipeline_placeholder.png     # Architecture flowchart
│       ├── fig2_metrics_placeholder.png      # Performance curves
│       ├── fig3_loss_placeholder.png         # Training loss curves
│       └── fig4_realtime_ui_placeholder.png  # Inference UI mockup
│
├── notebooks/                         # Jupyter notebooks
│   └── YOLOv8.ipynb                   # Training notebook
│
├── configs/                           # Configuration files
│   └── (Extensible for deployment configs)
│
├── dataset.zip                        # Compressed dataset archive
├── hagrid-sample-30k-384p/            # Original HaGRID dataset reference
└── .gitignore                         # Git ignore rules

```

---

## Installation

### Prerequisites
- **macOS** 10.14 or later
- **Python** 3.8+
- **pip** or **conda** package manager
- Webcam with reasonable lighting

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/real-time-spotify-controller.git
cd real-time-spotify-controller
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate

# OR using conda
conda create --name gesture-control python=3.10
conda activate gesture-control
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python3 -c "import cv2, torch, ultralytics; print('✓ All dependencies installed')"
```

---

## Usage

### Basic Usage

Run the real-time gesture controller:

```bash
python3 src/hand_tracking.py
```

### Advanced Options

```bash
python3 src/hand_tracking.py \
  --weights runs/detect/gesture_v100_ft/weights/best.pt \
  --camera 0 \
  --conf 0.35 \
  --imgsz 640 \
  --cooldown 2.0 \
  --stable-frames 4 \
  --volume-step 5
```

#### Command-line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--weights` | Auto-detect | Path to YOLO model weights |
| `--camera` | 0 | Camera device index |
| `--conf` | 0.35 | Confidence threshold (0-1) |
| `--imgsz` | 640 | Inference image size |
| `--cooldown` | 2.0 | Seconds between actions |
| `--stable-frames` | 4 | Frames for temporal stability |
| `--volume-step` | 5 | Volume increment percentage |

### Example: Custom Confidence Threshold

```bash
# Stricter detection (fewer false positives)
python3 src/hand_tracking.py --conf 0.50 --stable-frames 5

# Faster response (lower latency)
python3 src/hand_tracking.py --conf 0.25 --stable-frames 2
```

---

## Performance Metrics

### Model Evaluation Results (100 Epochs)

| Metric | Epoch 1 | Best (Epoch 85) | Epoch 100 |
|--------|---------|-----------------|-----------|
| **Precision** | 0.60814 | **0.99096** ✓ | 0.98989 |
| **Recall** | 0.52587 | **0.98995** ✓ | 0.97880 |
| **mAP50** | 0.54093 | **0.99395** ✓ | 0.98896 |
| **mAP50-95** | 0.36789 | **0.87623** ✓ | 0.86341 |

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Hardware | NVIDIA Tesla V100 (32GB) |
| Optimizer | SGD |
| Learning Rate | 0.01 |
| Momentum | 0.937 |
| Weight Decay | 5e-4 |
| Batch Size | 64 |
| Image Size | 640 |
| Epochs | 100 |
| Warmup Epochs | 3 |
| Patience | 20 |

### Dataset Statistics

| Metric | Count |
|--------|-------|
| Total Images | 10,608 |
| Training Images | 8,487 |
| Validation Images | 2,121 |
| Total Bounding Boxes | 13,073 |
| Gesture Classes | 7 |

### Per-Class Distribution (Training)

| Gesture | Boxes | % |
|---------|-------|---|
| fist | 1,372 | 13.1% |
| one | 1,424 | 13.6% |
| peace | 1,411 | 13.5% |
| three | 1,406 | 13.4% |
| four | 1,444 | 13.8% |
| palm | 1,429 | 13.6% |
| no_gesture | 1,981 | 18.9% |

---

## Gesture Mapping

The following hand gestures map to media control commands:

| Gesture | Command | Action |
|---------|---------|--------|
| 🤜 **Fist** | Play/Pause | Pause playback |
| ☝️ **One** | Next Track | Skip to next song |
| ✌️ **Peace** | Previous Track | Return to previous song |
| 🖌️ **Three** | Volume Up | Increase system volume by 5% |
| ✋ **Four** | Volume Down | Decrease system volume by 5% |
| 🖐️ **Palm** | Play | Resume playback |

**no_gesture**: Acts as a background class to reduce false positives.

---

## Configuration

### Model Selection

The project includes multiple model checkpoints:

```bash
# Use best performing model (recommended)
python3 src/hand_tracking.py --weights runs/detect/gesture_v100_ft/weights/best.pt

# Use latest checkpoint
python3 src/hand_tracking.py --weights runs/detect/gesture_v100_ft/weights/last.pt
```

### Tuning for Your Environment

#### Low-Light Conditions
```bash
python3 src/hand_tracking.py --conf 0.40 --stable-frames 5
```

#### High-Speed Response
```bash
python3 src/hand_tracking.py --conf 0.30 --stable-frames 2 --cooldown 1.5
```

#### Preventing Accidental Triggers
```bash
python3 src/hand_tracking.py --conf 0.55 --stable-frames 6 --cooldown 3.0
```

### macOS Preferences

To ensure Spotify integration works correctly:

1. Grant microphone/camera permissions to Terminal:
   ```bash
   # System Preferences → Security & Privacy → Microphone/Camera
   ```

2. Allow AppleScript access to Spotify:
   ```bash
   # System Preferences → Security & Privacy → Automation
   ```

---

## Troubleshooting

### Issue: Camera Not Detected

**Symptoms**: `Camera initialization failed` error

**Solution**:
```bash
# Check available cameras
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Try different camera indices
python3 src/hand_tracking.py --camera 1
python3 src/hand_tracking.py --camera 2
```

### Issue: No Gesture Detected

**Symptoms**: Shows "No detection" continuously

**Solutions**:
1. **Improve lighting** - Ensure adequate ambient light
2. **Lower confidence threshold**:
   ```bash
   python3 src/hand_tracking.py --conf 0.25
   ```
3. **Verify model path**:
   ```bash
   ls -la runs/detect/gesture_v100_ft/weights/
   ```

### Issue: False Positive Triggers

**Symptoms**: Unexpected playback commands

**Solutions**:
1. **Increase stability frames**:
   ```bash
   python3 src/hand_tracking.py --stable-frames 6
   ```
2. **Raise confidence threshold**:
   ```bash
   python3 src/hand_tracking.py --conf 0.50
   ```
3. **Increase cooldown period**:
   ```bash
   python3 src/hand_tracking.py --cooldown 3.0
   ```

### Issue: Spotify Commands Not Working

**Symptoms**: Gestures detected but no audio response

**Solution**:
```bash
# Verify AppleScript permissions
osascript -e 'tell application "Spotify" to playpause'

# Manually test media control
osascript -e 'tell application "Music" to playpause'
```

### Issue: Poor Performance / High Latency

**Symptoms**: Slow inference, choppy video

**Solutions**:
1. **Reduce image size**:
   ```bash
   python3 src/hand_tracking.py --imgsz 416
   ```
2. **Close background applications** consuming GPU/CPU
3. **Check GPU availability**:
   ```bash
   python3 -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
   ```

---

## Research Paper

A comprehensive technical paper documenting this project is available in [docs/report.md](docs/report.md).

### Paper Contents

- **Methodology**: Complete training pipeline and architecture design
- **Results**: Quantitative evaluation across 100 training epochs
- **Deployment**: Real-world inference considerations for macOS
- **Discussion**: Performance analysis and limitations
- **Visualizations**: 4 publication-ready figures:
  - Fig. 1: Pipeline flowchart
  - Fig. 2: Performance metrics curves
  - Fig. 3: Training loss curves
  - Fig. 4: Real-time inference mockup

**Recommended Citation Format**:
```
Nguyen, V. A. D., et al. "Real-time Spotify Controller via Hand Gesture Recognition 
using YOLOv8." Project Documentation, 2024.
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution

- [ ] Support for additional media players (YouTube Music, Apple Music)
- [ ] Cross-platform support (Windows, Linux)
- [ ] Additional gesture classes
- [ ] Improved gesture stability algorithms
- [ ] Mobile deployment (iOS/Android)
- [ ] Hand tracking optimization for edge devices

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Authors

**Nguyen Van Anh Duy**  
Independent Researcher, Vietnam  
📧 Email: duynvse181823@fpt.edu.vn

### Contributors

- Trần Huỳnh Bảo Minh
- Trần Quốc Huân
- Trần Hoàng Tuấn Hưng
- Phan Quốc Anh

---

## Acknowledgments

- **YOLOv8** by Ultralytics for the excellent object detection framework
- **HaGRID** dataset creators for hand gesture data
- **macOS** AppleScript community for media control examples
- OpenCV and PyTorch communities for foundational tools

---

## Support

For issues, questions, or suggestions:
1. **Check** existing [GitHub Issues](https://github.com/yourusername/real-time-spotify-controller/issues)
2. **Create** a new issue with detailed information
3. **Include** error messages, system info, and steps to reproduce

---

## Roadmap

- [ ] **v2.0**: Multi-hand detection support
- [ ] **v2.1**: Gesture combination recognition (two hands)
- [ ] **v2.2**: Custom gesture training interface
- [ ] **v3.0**: Web-based dashboard for analytics
- [ ] **v3.1**: Mobile companion app
- [ ] **v4.0**: Lightweight edge device deployment

---

**Last Updated**: March 2024  
**Status**: ✅ Production Ready

