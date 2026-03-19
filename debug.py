#!/usr/bin/env python3
"""Debug YOLO labels by drawing reverse-converted boxes on the image."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

import cv2


def yolo_to_xyxy(
    x_center_n: float,
    y_center_n: float,
    width_n: float,
    height_n: float,
    image_w: int,
    image_h: int,
) -> Tuple[int, int, int, int]:
    x_center = x_center_n * image_w
    y_center = y_center_n * image_h
    width = width_n * image_w
    height = height_n * image_h

    xmin = int(round(x_center - width / 2.0))
    ymin = int(round(y_center - height / 2.0))
    xmax = int(round(x_center + width / 2.0))
    ymax = int(round(y_center + height / 2.0))

    xmin = max(0, min(image_w - 1, xmin))
    ymin = max(0, min(image_h - 1, ymin))
    xmax = max(0, min(image_w - 1, xmax))
    ymax = max(0, min(image_h - 1, ymax))
    return xmin, ymin, xmax, ymax


def read_yolo_label(label_path: Path) -> List[Tuple[int, float, float, float, float]]:
    rows: List[Tuple[int, float, float, float, float]] = []
    text = label_path.read_text(encoding="utf-8").strip()
    if not text:
        return rows

    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        class_id = int(parts[0])
        x_c, y_c, w, h = map(float, parts[1:])
        rows.append((class_id, x_c, y_c, w, h))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw YOLO bbox labels on image for visual validation")
    parser.add_argument("--image", type=Path, required=True, help="Path to input image")
    parser.add_argument("--label", type=Path, required=True, help="Path to YOLO .txt label")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("debug_overlay.jpg"),
        help="Path to output image with drawn boxes",
    )
    parser.add_argument("--show", action="store_true", help="Open preview window")
    args = parser.parse_args()

    image = cv2.imread(str(args.image))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {args.image}")
    if not args.label.exists():
        raise FileNotFoundError(f"Label file not found: {args.label}")

    h, w = image.shape[:2]
    rows = read_yolo_label(args.label)

    for class_id, x_c, y_c, bw, bh in rows:
        xmin, ymin, xmax, ymax = yolo_to_xyxy(x_c, y_c, bw, bh, w, h)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"id:{class_id}",
            (xmin, max(12, ymin - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), image)
    print(f"Saved debug image: {args.output}")
    print(f"Boxes drawn: {len(rows)}")

    if args.show:
        cv2.imshow("YOLO Debug", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
