import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from multiprocessing import freeze_support
from ultralytics import YOLO
import torch
from pathlib import Path
import time
import json
from datetime import datetime


class ProgressTracker:
    def __init__(self, total_epochs, save_path="training_progress.json"):
        self.total_epochs = total_epochs
        self.save_path = save_path
        self.history = {
            "epoch": [],
            "train_loss": [],
            "val_loss": [],
            "mAP50": [],
            "mAP50-95": [],
            "precision": [],
            "recall": [],
            "lr": [],
            "time_elapsed": [],
            "gpu_mem_used": []
        }
        self.start_time = time.time()
        self.best_map50 = 0.0
        self.best_epoch = 0
        self.wait = 0

    def on_train_epoch_end(self, trainer):
        epoch = trainer.epoch + 1
        metrics = trainer.metrics

        train_loss = getattr(trainer.loss, 'loss', None)
        val_loss = metrics.get('val_loss', None)
        map50 = metrics.get('metrics/mAP50(B)', None)
        map50_95 = metrics.get('metrics/mAP50-95(B)', None)
        precision = metrics.get('metrics/precision(B)', None)
        recall = metrics.get('metrics/recall(B)', None)
        lr = trainer.optimizer.param_groups[0]['lr']

        gpu_mem = torch.cuda.memory_allocated(0) / (1024**3) if torch.cuda.is_available() else 0
        elapsed = time.time() - self.start_time

        self.history["epoch"].append(epoch)
        self.history["train_loss"].append(float(train_loss) if train_loss else None)
        self.history["val_loss"].append(float(val_loss) if val_loss else None)
        self.history["mAP50"].append(float(map50) if map50 else None)
        self.history["mAP50-95"].append(float(map50_95) if map50_95 else None)
        self.history["precision"].append(float(precision) if precision else None)
        self.history["recall"].append(float(recall) if recall else None)
        self.history["lr"].append(float(lr))
        self.history["time_elapsed"].append(round(elapsed, 1))
        self.history["gpu_mem_used"].append(round(gpu_mem, 2))

        if map50 and map50 > self.best_map50:
            self.best_map50 = map50
            self.best_epoch = epoch
            self.wait = 0
        else:
            self.wait += 1

        self.save_progress()
        return False

    def save_progress(self):
        with open(self.save_path, 'w') as f:
            json.dump(self.history, f, indent=2)


def main():
    print("=" * 60)
    print("YOLOv8 Training on RTX 4060 (8GB) with CUDA")
    print("=" * 60)
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
    if torch.cuda.is_available():
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"GPU Memory: {gpu_mem:.1f} GB")
    print("=" * 60)

    abs_dataset_path = Path("dataset").resolve()
    yaml_path = abs_dataset_path / "data.yaml"

    pretrained_weights = "yolov8n.pt"
    yolo_epochs = 100
    yolo_imgsz = 640
    yolo_batch = 8
    yolo_workers = 0   # đổi 0 trước để tránh lỗi spawn trên Windows
    yolo_amp = True
    device = 0

    box_loss_gain = 7.5
    cls_loss_gain = 0.5
    dfl_loss_gain = 1.5

    freeze_layers = 10
    warmup_epochs = 3
    warmup_bias_lr = 1e-6
    initial_lr = 1e-3
    final_lr = 1e-5
    weight_decay = 5e-4
    momentum = 0.937
    early_stopping_patience = 20

    hsv_h = 0.01
    hsv_s = 0.3
    hsv_v = 0.3
    degrees = 5.0
    translate = 0.1
    scale = 0.3
    shear = 0.0
    perspective = 0.0
    flipud = 0.0
    fliplr = 0.0

    fine_tune_stages = [
        {"epochs": 30, "freeze": 10, "lr": 1e-3, "batch": 8},
        {"epochs": 70, "freeze": 0, "lr": 1e-4, "batch": 8},
    ]
    run_staged_training = True

    print(f"Loading pretrained model: {pretrained_weights}")
    model = YOLO(pretrained_weights)

    tracker = ProgressTracker(yolo_epochs, save_path="training_progress.json")

    if run_staged_training:
        for stage_idx, stage in enumerate(fine_tune_stages):
            tracker = ProgressTracker(
                stage["epochs"],
                save_path=f"training_progress_stage{stage_idx+1}.json"
            )
            model.add_callback("on_train_epoch_end", tracker.on_train_epoch_end)

            results = model.train(
                data=str(yaml_path),
                epochs=stage["epochs"],
                imgsz=yolo_imgsz,
                batch=stage["batch"],
                device=device,
                workers=yolo_workers,
                freeze=stage["freeze"],
                lr0=stage["lr"],
                lrf=final_lr,
                momentum=momentum,
                weight_decay=weight_decay,
                warmup_epochs=warmup_epochs,
                warmup_bias_lr=warmup_bias_lr,
                amp=yolo_amp,
                optimizer="SGD",
                cos_lr=True,
                box=box_loss_gain,
                cls=cls_loss_gain,
                dfl=dfl_loss_gain,
                patience=early_stopping_patience,
                hsv_h=hsv_h, hsv_s=hsv_s, hsv_v=hsv_v,
                degrees=degrees, translate=translate, scale=scale,
                shear=shear, perspective=perspective,
                flipud=flipud, fliplr=fliplr,
                mosaic=1.0, mixup=0.0, copy_paste=0.0,
                close_mosaic=10,
                cache=False,
                project="runs/detect",
                name=f"yolov8_hand_gesture_stage{stage_idx+1}",
                exist_ok=True,
                verbose=False,
            )

            if stage_idx < len(fine_tune_stages) - 1:
                best_weights = f"runs/detect/yolov8_hand_gesture_stage{stage_idx+1}/weights/best.pt"
                if Path(best_weights).exists():
                    model = YOLO(best_weights)

        return   # rất quan trọng: tránh rơi xuống train lần 2

    model.add_callback("on_train_epoch_end", tracker.on_train_epoch_end)
    results = model.train(
        data=str(yaml_path),
        epochs=yolo_epochs,
        imgsz=yolo_imgsz,
        batch=yolo_batch,
        device=device,
        workers=yolo_workers,
        freeze=freeze_layers,
        lr0=initial_lr,
        lrf=final_lr,
        momentum=momentum,
        weight_decay=weight_decay,
        warmup_epochs=warmup_epochs,
        warmup_bias_lr=warmup_bias_lr,
        amp=yolo_amp,
        optimizer="SGD",
        cos_lr=True,
        box=box_loss_gain,
        cls=cls_loss_gain,
        dfl=dfl_loss_gain,
        patience=early_stopping_patience,
        hsv_h=hsv_h,
        hsv_s=hsv_s,
        hsv_v=hsv_v,
        degrees=degrees,
        translate=translate,
        scale=scale,
        shear=shear,
        perspective=perspective,
        flipud=flipud,
        fliplr=fliplr,
        mosaic=1.0,
        mixup=0.0,
        copy_paste=0.0,
        close_mosaic=10,
        cache=False,
        project="runs/detect",
        name="yolov8_hand_gesture_cuda",
        exist_ok=True,
        verbose=False,
    )


if __name__ == "__main__":
    freeze_support()
    main()