# Real-time-Spotify-Controller-via-Hand-Gesture-Recognition-using-YOLO

**Nguyen Van Anh Duy, Trần Huỳnh Bảo Minh, Trần Quốc Huân, Trần Hoàng Tuấn Hưng, Phan Quốc Anh**  
Independent Researcher, Vietnam  
Email: duynvse181823@fpt.edu.vn, baominh@gmail.com, quochuan@gmail.com, tuanhung@gmail.com, quocanh@gmail.com

## Abstract
This paper presents a real-time hand-gesture music control system on macOS using YOLOv8 object detection. The system detects seven gesture classes (including a background-style no_gesture class) and maps six control gestures to media commands: play, pause, next track, previous track, volume up, and volume down. The training pipeline is designed around a reproducible runtime YAML generation flow, strict train/validation path checks, and a 100-epoch fine-tuning setup from yolov8n pretrained weights. Experimental results show strong performance with best mAP50-95 of 0.87623 (epoch 85), best precision of 0.99096, and best recall of 0.98995. The final deployed script integrates confidence-based top-gesture selection, temporal stability checks, and action cooldown to reduce false command triggering in practical webcam usage.

## Index Terms
YOLOv8, hand gesture recognition, real-time vision, human-computer interaction, macOS media control, object detection.

## I. Introduction
Human-computer interaction via vision-based gestures is a practical alternative to keyboard or touch input for media control scenarios. In this work, we develop a real-time gesture control framework where a YOLOv8 detector identifies hand gestures from a webcam stream and triggers media commands on macOS. The contribution is twofold: (1) a complete training-to-deployment pipeline with quantitative evaluation, and (2) a robust command trigger strategy that improves safety in real-world operation.

## II. Dataset and Problem Definition

### A. Detection Classes
The model is trained with seven classes defined in the project dataset configuration:
1) fist, 2) one, 3) peace, 4) three, 5) four, 6) palm, 7) no_gesture.

At deployment time, six classes are used for command mapping. The no_gesture class acts as a negative/background intent class and helps reduce accidental actions.

### B. Data Source and Splits
The project uses a curated dataset in the dataset directory, with references to HaGRID-style data resources. The effective split statistics are:

- Train images: 8,487
- Validation images: 2,121
- Total images: 10,608

- Train boxes: 10,467
- Validation boxes: 2,606
- Total boxes: 13,073

### C. Class Distribution
Train boxes per class:
- fist: 1,372
- one: 1,424
- peace: 1,411
- three: 1,406
- four: 1,444
- palm: 1,429
- no_gesture: 1,981

Validation boxes per class:
- fist: 362
- one: 354
- peace: 358
- three: 345
- four: 361
- palm: 341
- no_gesture: 485

The six command classes are relatively balanced. The larger no_gesture share provides useful regularization against false positives during live inference.

## III. Training Methodology

### A. Model and Environment
- Backbone model: YOLOv8n pretrained (yolov8n.pt)
- Framework: Ultralytics YOLOv8
- Intended training hardware: Tesla V100 32GB

### B. Training Configuration
The main hyperparameters are:
- Epochs: 100
- Image size: 640
- Batch size: 64
- Device: GPU index 0
- Workers: 8
- Optimizer: SGD
- Initial learning rate (lr0): 0.01
- Final learning rate factor (lrf): 0.01
- Momentum: 0.937
- Weight decay: 5e-4
- Warmup epochs: 3.0
- Cosine LR schedule: enabled
- Early-stop patience: 20
- AMP: enabled

**Table I**  
**Training Configuration (YOLOv8 Fine-Tuning)**

| Parameter | Value |
|---|---|
| Model initialization | yolov8n.pt |
| Epochs | 100 |
| Image size | 640 |
| Batch size | 64 |
| Optimizer | SGD |
| lr0 | 0.01 |
| lrf | 0.01 |
| Momentum | 0.937 |
| Weight decay | 5e-4 |
| Warmup epochs | 3.0 |
| Cosine LR | Enabled |
| AMP | Enabled |

**Fig. 1.** Pipeline overview placeholder: data preparation, YOLOv8 training, realtime inference, and macOS command execution.

![Fig. 1 - System pipeline placeholder](figures/fig1_pipeline_placeholder.png)

### C. Reproducible Data Runtime Handling
Before training, the notebook regenerates data_runtime.yaml from the dataset structure and validates train/val directory existence. This prevents stale path issues when moving between local and remote environments.

## IV. Experimental Results

### A. Logged Epochs
The run contains 100 logged epochs in runs/detect/gesture_v100_ft/results.csv.

### B. Key Metrics at Important Epochs

Epoch 1:
- Precision: 0.80324
- Recall: 0.77744
- mAP50: 0.86187
- mAP50-95: 0.68412
- Train box loss: 1.00798
- Train cls loss: 2.92407
- Val box loss: 0.79121
- Val cls loss: 1.30772

Best epoch by mAP50-95 (epoch 85):
- Precision: 0.99096
- Recall: 0.98995
- mAP50: 0.99344
- mAP50-95: 0.87623
- Train box loss: 0.58483
- Train cls loss: 0.33895
- Val box loss: 0.59018
- Val cls loss: 0.24748

Final epoch (epoch 100):
- Precision: 0.99494
- Recall: 0.98155
- mAP50: 0.99342
- mAP50-95: 0.87348
- Train box loss: 0.51878
- Train cls loss: 0.23398
- Val box loss: 0.59487
- Val cls loss: 0.24928

**Table II**  
**Main Detection Metrics by Epoch Milestone**

| Epoch milestone | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Epoch 1 | 0.80324 | 0.77744 | 0.86187 | 0.68412 |
| Best epoch (85) | 0.99096 | 0.98995 | 0.99344 | 0.87623 |
| Final epoch (100) | 0.99494 | 0.98155 | 0.99342 | 0.87348 |

**Table III**  
**Loss Comparison by Epoch Milestone**

| Epoch milestone | Train box loss | Train cls loss | Val box loss | Val cls loss |
|---|---:|---:|---:|---:|
| Epoch 1 | 1.00798 | 2.92407 | 0.79121 | 1.30772 |
| Best epoch (85) | 0.58483 | 0.33895 | 0.59018 | 0.24748 |
| Final epoch (100) | 0.51878 | 0.23398 | 0.59487 | 0.24928 |

**Fig. 2.** Training curves placeholder: precision, recall, mAP50, and mAP50-95 across epochs.

![Fig. 2 - Metrics curves placeholder](figures/fig2_metrics_placeholder.png)

**Fig. 3.** Loss curves placeholder: train/val box loss and train/val classification loss.

![Fig. 3 - Loss curves placeholder](figures/fig3_loss_placeholder.png)

### C. Quantitative Improvement
From epoch 1 to the best epoch:
- Absolute mAP50-95 gain: 0.19211
- Relative mAP50-95 gain: approximately 28.08%

The detector converges to high precision and high recall while maintaining low validation loss, indicating strong detection quality for real-time use.

## V. Deployment on macOS

### A. Real-Time Inference Pipeline
The deployment script captures webcam frames using OpenCV with macOS-friendly backend fallback, performs YOLO inference, and renders annotated frames in a native cv2.imshow window.

**Fig. 4.** Deployment interface placeholder: webcam frame with detection boxes, labels, FPS, and action status.

![Fig. 4 - Realtime UI placeholder](figures/fig4_realtime_ui_placeholder.png)

### B. Gesture-to-Command Mapping
- fist -> pause
- palm -> play
- one -> next track
- peace -> previous track
- three -> volume up
- four -> volume down

### C. False-Trigger Mitigation
To reduce accidental commands when multiple gestures are detected:
1) Only the top-confidence gesture is considered per frame.
2) The same gesture must persist for multiple consecutive frames.
3) A cooldown is enforced between two command triggers.

This temporal and confidence gating is essential for stable user experience in live settings.

## VI. Discussion
The training results show that YOLOv8n can deliver near-saturated mAP50 with strong mAP50-95 in this gesture-control task. The no_gesture class, balanced control classes, and robust deployment logic collectively improve reliability. Remaining limitations include the absence of per-class AP reporting in this draft and no formal latency benchmark across different hardware profiles.

## VII. Conclusion and Future Work
This work demonstrates a complete and practical pipeline for gesture-based media control on macOS using YOLOv8, from data preparation and training to real-time deployment. The model achieves high detection performance and can be safely integrated with operating-system control logic using temporal trigger filtering.

Future work includes per-class error analysis (AP by class and confusion matrix), end-to-end latency profiling, and expanded data collection under challenging illumination and occlusion conditions.

## References
[1] G. Kapusta et al., “HaGRID - HAnd Gesture Recognition Image Dataset,” arXiv, 2023.

[2] G. Jocher et al., “Ultralytics YOLOv8,” 2023. [Online]. Available: https://github.com/ultralytics/ultralytics

[3] J. Redmon et al., “You Only Look Once: Unified, Real-Time Object Detection,” in Proc. CVPR, 2016.

[4] Apple Inc., “AppleScript Language Guide,” [Online]. Available: https://developer.apple.com/library/archive/documentation/AppleScript
