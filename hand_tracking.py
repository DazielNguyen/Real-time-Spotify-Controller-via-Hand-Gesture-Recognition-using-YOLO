#!/usr/bin/env python3
"""Realtime hand tracking with YOLOv8 using native OpenCV window on macOS.

Run:
	python3 hand_tracking.py

Optional:
	python3 hand_tracking.py --weights runs/detect/gesture_v100_ft/weights/best.pt
	python3 hand_tracking.py --camera 0 --conf 0.4 --imgsz 640
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import time
from pathlib import Path

import cv2
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="YOLOv8 realtime webcam detection")
	parser.add_argument(
		"--weights",
		type=str,
		default="",
		help="Path to YOLO weights (.pt). If omitted, auto-find best.pt/last.pt in runs/detect.",
	)
	parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
	parser.add_argument("--conf", type=float, default=0.40, help="Confidence threshold")
	parser.add_argument("--imgsz", type=int, default=640, help="Inference image size")
	parser.add_argument(
		"--cooldown",
		type=float,
		default=1.0,
		help="Seconds to wait before accepting the next gesture action",
	)
	parser.add_argument(
		"--stable-frames",
		type=int,
		default=4,
		help="Require the same top gesture for N consecutive frames before triggering",
	)
	parser.add_argument(
		"--volume-step",
		type=int,
		default=,
		help="Volume delta (0-100 scale) for three/four gestures",
	)
	return parser.parse_args()


def run_osascript(lines: list[str]) -> None:
	cmd = ["osascript"]
	for line in lines:
		cmd.extend(["-e", line])
	subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def control_media(action: str) -> str:
	if action == "play":
		spotify_cmd = "play"
		music_cmd = "play"
	elif action == "pause":
		spotify_cmd = "pause"
		music_cmd = "pause"
	elif action == "next":
		spotify_cmd = "next track"
		music_cmd = "next track"
	elif action == "previous":
		spotify_cmd = "previous track"
		music_cmd = "previous track"
	else:
		raise ValueError(f"Unsupported media action: {action}")

	try:
		run_osascript(
			[
				'tell application "Spotify"',
				f"  {spotify_cmd}",
				"end tell",
			]
		)
		return f"spotify:{action}"
	except Exception:
		# Fallback to Apple Music if Spotify command fails.
		run_osascript(
			[
				'tell application "Music"',
				f"  {music_cmd}",
				"end tell",
			]
		)
		return f"music:{action}"


def change_system_volume(delta: int) -> str:
	run_osascript(
		[
			"set currentVolume to output volume of (get volume settings)",
			f"set newVolume to currentVolume + ({delta})",
			"if newVolume > 100 then set newVolume to 100",
			"if newVolume < 0 then set newVolume to 0",
			"set volume output volume newVolume",
		]
	)
	return f"system_volume:{'+' if delta >= 0 else ''}{delta}"


def execute_gesture_action(gesture: str, volume_step: int) -> str | None:
	if gesture == "fist":
		return control_media("pause")
	if gesture == "palm":
		return control_media("play")
	if gesture == "one":
		return control_media("next")
	if gesture == "peace":
		return control_media("previous")
	if gesture == "three":
		return change_system_volume(volume_step)
	if gesture == "four":
		return change_system_volume(-volume_step)
	return None


def find_weights(project_root: Path, preferred: str) -> Path:
	if preferred:
		p = Path(preferred).expanduser()
		if not p.is_absolute():
			p = (project_root / p).resolve()
		if p.exists():
			return p
		raise FileNotFoundError(f"Weights not found: {p}")

	detect_root = project_root / "runs" / "detect"
	if not detect_root.exists():
		raise FileNotFoundError(f"Cannot find runs/detect at: {detect_root}")

	best_candidates = sorted(
		detect_root.glob("*/weights/best.pt"),
		key=lambda x: x.stat().st_mtime,
		reverse=True,
	)
	last_candidates = sorted(
		detect_root.glob("*/weights/last.pt"),
		key=lambda x: x.stat().st_mtime,
		reverse=True,
	)

	for p in best_candidates + last_candidates:
		if p.exists():
			return p

	raise FileNotFoundError(
		"No trained weights found. Expected something like runs/detect/<run_name>/weights/best.pt"
	)


def ensure_opencv_gui() -> None:
	build_info = cv2.getBuildInformation().lower()
	if "headless" in build_info or "gui:                           none" in build_info:
		raise RuntimeError(
			"OpenCV appears to be headless, so cv2.imshow cannot open a window. "
			"Please install GUI build: pip uninstall -y opencv-python-headless && pip install opencv-python"
		)


def open_camera(index: int) -> cv2.VideoCapture:
	# On macOS, AVFoundation is usually the most reliable backend.
	cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
	if cap.isOpened():
		return cap

	cap = cv2.VideoCapture(index)
	if cap.isOpened():
		return cap

	raise RuntimeError(
		f"Cannot open camera index={index}. Try --camera 0/1/2 and check macOS camera permissions."
	)


def main() -> int:
	args = parse_args()
	project_root = Path(__file__).resolve().parent

	if platform.system() != "Darwin":
		print(f"[WARN] This script is optimized for macOS. Current OS: {platform.system()}")

	ensure_opencv_gui()
	weights_path = find_weights(project_root, args.weights)
	model = YOLO(str(weights_path))

	names = model.names
	class_names = [names[i] for i in sorted(names)] if isinstance(names, dict) else list(names)

	print(f"[INFO] Using weights: {weights_path}")
	print(f"[INFO] Classes ({len(class_names)}): {class_names}")

	cap = open_camera(args.camera)
	window_name = "YOLOv8 Hand Tracking (macOS)"
	cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_name, 1200, 760)

	prev_t = time.time()
	last_action_t = 0.0
	last_action_label = "None"
	stable_name = None
	stable_count = 0
	print("[INFO] Webcam started. Press 'q' or ESC to quit.")
	print("[INFO] Gesture map: fist=pause, palm=play, one=next, peace=previous, three=vol+, four=vol-")
	print(f"[INFO] Debounce: cooldown={args.cooldown}s, stable_frames={args.stable_frames}")

	try:
		while True:
			ret, frame = cap.read()
			if not ret or frame is None:
				print("[WARN] Cannot read frame from webcam. Stopping.")
				break

			results = model.predict(source=frame, conf=args.conf, imgsz=args.imgsz, verbose=False)
			r0 = results[0]
			annotated = r0.plot()

			detected_names = []
			top_gesture = None
			if r0.boxes is not None and len(r0.boxes) > 0:
				cls_ids = r0.boxes.cls.detach().cpu().numpy().astype(int).tolist()
				conf_scores = r0.boxes.conf.detach().cpu().numpy().tolist()
				detected_names = [
					class_names[c] if 0 <= c < len(class_names) else str(c) for c in cls_ids
				]
				if conf_scores:
					best_idx = max(range(len(conf_scores)), key=lambda i: conf_scores[i])
					top_gesture = detected_names[best_idx]

			if top_gesture is None:
				stable_name = None
				stable_count = 0
			elif top_gesture == stable_name:
				stable_count += 1
			else:
				stable_name = top_gesture
				stable_count = 1

			now = time.time()
			cooldown_left = max(0.0, args.cooldown - (now - last_action_t))
			if (
				stable_name is not None
				and stable_count >= max(1, args.stable_frames)
				and cooldown_left <= 0
			):
				action_result = execute_gesture_action(stable_name, args.volume_step)
				if action_result is not None:
					last_action_t = now
					last_action_label = f"{stable_name} -> {action_result}"
					print(f"[ACTION] {last_action_label}")

			fps = 1.0 / max(now - prev_t, 1e-6)
			prev_t = now
			cooldown_left = max(0.0, args.cooldown - (now - last_action_t))

			text_detect = (
				"Detected: " + ", ".join(sorted(set(detected_names)))
				if detected_names
				else "Detected: None"
			)
			text_top = f"Top: {top_gesture if top_gesture else 'None'} | Stable: {stable_count}"
			text_cooldown = f"Cooldown: {cooldown_left:.1f}s | Last action: {last_action_label}"
			cv2.putText(
				annotated,
				f"FPS: {fps:.1f}",
				(10, 28),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.8,
				(20, 220, 20),
				2,
				cv2.LINE_AA,
			)
			cv2.putText(
				annotated,
				text_detect,
				(10, 58),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.65,
				(0, 255, 255),
				2,
				cv2.LINE_AA,
			)
			cv2.putText(
				annotated,
				text_top,
				(10, 88),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.65,
				(255, 200, 0),
				2,
				cv2.LINE_AA,
			)
			cv2.putText(
				annotated,
				text_cooldown,
				(10, 118),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.62,
				(0, 165, 255),
				2,
				cv2.LINE_AA,
			)

			cv2.imshow(window_name, annotated)
			key = cv2.waitKey(1) & 0xFF
			if key in (ord("q"), 27):
				break

	finally:
		cap.release()
		cv2.destroyAllWindows()
		print("[INFO] Webcam closed.")

	return 0


if __name__ == "__main__":
	try:
		raise SystemExit(main())
	except Exception as exc:
		print(f"[ERROR] {exc}")
		raise

