#!/usr/bin/env python3
"""Convert HaGRID JSON annotations to YOLO detection labels.

HaGRID bbox format (already normalized):
    [top_left_x, top_left_y, width, height]

YOLO format:
    <class_id> <center_x> <center_y> <width> <height>
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


GESTURE_TO_ID: Dict[str, int] = {
    "call": 0,
    "dislike": 1,
    "fist": 2,
    "four": 3,
    "like": 4,
    "mute": 5,
    "ok": 6,
    "one": 7,
    "palm": 8,
    "peace": 9,
    "peace_inverted": 10,
    "rock": 11,
    "stop": 12,
    "stop_inverted": 13,
    "three": 14,
    "three2": 15,
    "two_up": 16,
    "two_up_inverted": 17,
}


def hagrid_bbox_to_yolo(bbox: List[float]) -> Tuple[float, float, float, float]:
    """Convert [x_tl, y_tl, w, h] to [x_center, y_center, w, h]."""
    x_tl, y_tl, w, h = bbox
    x_center = x_tl + (w / 2.0)
    y_center = y_tl + (h / 2.0)
    return x_center, y_center, w, h


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def convert_json_file(
    json_path: Path,
    image_root: Path,
    output_root: Path,
    dry_run: bool = False,
) -> Tuple[int, int, int]:
    """Convert one gesture JSON and return stats.

    Returns:
        (num_images_written, num_boxes_written, num_boxes_skipped)
    """
    gesture_name = json_path.stem
    image_dir = image_root / f"train_val_{gesture_name}"
    output_dir = output_root / f"train_val_{gesture_name}"

    if not image_dir.exists():
        raise FileNotFoundError(f"Image folder not found for {json_path.name}: {image_dir}")

    with json_path.open("r", encoding="utf-8") as f:
        annotations = json.load(f)

    images_written = 0
    boxes_written = 0
    boxes_skipped = 0

    for image_id, item in annotations.items():
        bboxes = item.get("bboxes", [])
        labels = item.get("labels", [])

        if len(bboxes) != len(labels):
            boxes_skipped += max(len(bboxes), len(labels))
            continue

        yolo_lines: List[str] = []
        for bbox, label in zip(bboxes, labels):
            class_id = GESTURE_TO_ID.get(label)
            if class_id is None:
                # Skip unknown classes (e.g. no_gesture)
                boxes_skipped += 1
                continue

            x_c, y_c, w, h = hagrid_bbox_to_yolo(bbox)
            x_c = clamp01(x_c)
            y_c = clamp01(y_c)
            w = clamp01(w)
            h = clamp01(h)
            yolo_lines.append(f"{class_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")

        # Write empty file if no target gesture boxes exist to keep one-to-one mapping.
        label_path = output_dir / f"{image_id}.txt"
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            label_path.write_text("\n".join(yolo_lines), encoding="utf-8")

        images_written += 1
        boxes_written += len(yolo_lines)

    return images_written, boxes_written, boxes_skipped


def iter_json_files(ann_dir: Path) -> Iterable[Path]:
    for json_path in sorted(ann_dir.glob("*.json")):
        if json_path.stem in GESTURE_TO_ID:
            yield json_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert HaGRID annotations to YOLO txt labels")
    parser.add_argument(
        "--ann-dir",
        type=Path,
        default=Path("hagrid-sample-30k-384p/ann_train_val"),
        help="Folder containing HaGRID JSON annotation files",
    )
    parser.add_argument(
        "--image-root",
        type=Path,
        default=Path("hagrid-sample-30k-384p/hagrid_30k"),
        help="Root image folder containing train_val_<gesture> subfolders",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("hagrid-sample-30k-384p/yolo_labels"),
        help="Output root for YOLO txt labels",
    )
    parser.add_argument("--dry-run", action="store_true", help="Count only, do not write labels")
    args = parser.parse_args()

    ann_dir = args.ann_dir.resolve()
    image_root = args.image_root.resolve()
    output_root = args.output_root.resolve()

    if not ann_dir.exists():
        raise FileNotFoundError(f"Annotation directory not found: {ann_dir}")
    if not image_root.exists():
        raise FileNotFoundError(f"Image root not found: {image_root}")

    total_images = 0
    total_boxes = 0
    total_skipped = 0

    json_files = list(iter_json_files(ann_dir))
    if not json_files:
        raise RuntimeError(f"No gesture JSON files found in: {ann_dir}")

    for json_path in json_files:
        images_written, boxes_written, boxes_skipped = convert_json_file(
            json_path=json_path,
            image_root=image_root,
            output_root=output_root,
            dry_run=args.dry_run,
        )
        total_images += images_written
        total_boxes += boxes_written
        total_skipped += boxes_skipped
        print(
            f"[{json_path.name}] images={images_written} boxes={boxes_written} "
            f"skipped={boxes_skipped}"
        )

    print("=" * 72)
    print(f"DONE | images={total_images} boxes={total_boxes} skipped={total_skipped}")
    print(f"Output root: {output_root}")


if __name__ == "__main__":
    main()
