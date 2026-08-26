#!/usr/bin/env python3
"""Flag one/two-frame visual discontinuities for human frame review."""

import argparse
import json
import subprocess
import sys
from pathlib import Path
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--ffprobe", default="ffprobe")
    ap.add_argument("--threshold", type=float, default=20.0)
    args = ap.parse_args()
    probe = json.loads(subprocess.check_output([args.ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate", "-of", "json", str(args.video)], text=True))
    num, den = probe["streams"][0]["avg_frame_rate"].split("/")
    fps = float(num) / float(den)
    w, h = 96, 54
    proc = subprocess.Popen([args.ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(args.video), "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    raw = proc.stdout.read()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg decode failed")
    frame_bytes = w * h
    n = len(raw) // frame_bytes
    frames = np.frombuffer(raw[:n * frame_bytes], dtype=np.uint8).reshape(n, h, w).astype(np.float32)
    candidates = []
    for i in range(1, n - 1):
        d_prev = float(np.mean(np.abs(frames[i] - frames[i - 1])))
        d_next = float(np.mean(np.abs(frames[i] - frames[i + 1])))
        bridge = float(np.mean(np.abs(frames[i - 1] - frames[i + 1])))
        std = float(np.std(frames[i]))
        if d_prev >= args.threshold and d_next >= args.threshold and bridge <= args.threshold * 0.45:
            candidates.append({"frame": i, "time": round(i / fps, 4), "type": "single_frame_discontinuity", "prev": round(d_prev, 2), "next": round(d_next, 2), "bridge": round(bridge, 2)})
        elif std < 1.2 and float(np.mean(frames[i])) < 5:
            candidates.append({"frame": i, "time": round(i / fps, 4), "type": "black_or_solid_dark"})
    result = {"video": str(args.video), "fps": fps, "frame_count": n, "candidate_count": len(candidates), "candidates": candidates, "note": "Candidates require visual confirmation; hard cuts can create false positives."}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

