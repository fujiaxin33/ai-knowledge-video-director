#!/usr/bin/env python3
"""Validate delivery codec, canvas, fps, bitrate, decode and black frames."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def rate(value):
    if not value or value == "0/0":
        return 0.0
    a, b = value.split("/")
    return float(a) / float(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    ap.add_argument("--fps", type=float, required=True)
    ap.add_argument("--codec", default="h264")
    ap.add_argument("--information-screen", action="store_true")
    ap.add_argument("--min-bitrate", type=int, default=4_000_000)
    ap.add_argument("--decode", action="store_true")
    ap.add_argument("--blackdetect", action="store_true")
    ap.add_argument("--report", type=Path)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--ffprobe", default="ffprobe")
    args = ap.parse_args()
    probe = json.loads(subprocess.check_output([args.ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(args.video)], text=True))
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    errors, warnings = [], []
    actual_fps = rate(video.get("avg_frame_rate"))
    bitrate = int(video.get("bit_rate") or probe["format"].get("bit_rate") or 0)
    if video.get("width") != args.width or video.get("height") != args.height:
        errors.append(f"canvas {video.get('width')}x{video.get('height')} != {args.width}x{args.height}")
    if abs(actual_fps - args.fps) > 0.01:
        errors.append(f"fps {actual_fps:.3f} != {args.fps:.3f}")
    if video.get("codec_name") != args.codec:
        errors.append(f"codec {video.get('codec_name')} != {args.codec}")
    if args.information_screen and bitrate < args.min_bitrate:
        errors.append(f"video bitrate {bitrate} < required {args.min_bitrate}")
    if video.get("pix_fmt") not in ("yuv420p", "yuv420p10le"):
        warnings.append(f"unusual delivery pixel format: {video.get('pix_fmt')}")

    decode_ok = None
    if args.decode:
        null_sink = "NUL" if os.name == "nt" else "/dev/null"
        completed = subprocess.run([args.ffmpeg, "-v", "error", "-i", str(args.video), "-f", "null", null_sink], capture_output=True, text=True)
        decode_ok = completed.returncode == 0
        if not decode_ok:
            errors.append("full decode failed: " + completed.stderr[-500:])

    black_segments = []
    if args.blackdetect:
        completed = subprocess.run([args.ffmpeg, "-hide_banner", "-i", str(args.video), "-vf", "blackdetect=d=0.033:pix_th=0.02", "-an", "-f", "null", "NUL" if os.name == "nt" else "/dev/null"], capture_output=True, text=True)
        for line in completed.stderr.splitlines():
            if "black_start:" in line:
                black_segments.append(line.split("black_start:", 1)[1].strip())
        if black_segments:
            warnings.append(f"blackdetect found {len(black_segments)} candidate segment(s)")

    result = {"pass": not errors, "errors": errors, "warnings": warnings, "video": {"codec": video.get("codec_name"), "width": video.get("width"), "height": video.get("height"), "fps": actual_fps, "pixel_format": video.get("pix_fmt"), "bitrate": bitrate, "duration": float(probe["format"].get("duration", 0))}, "decode_ok": decode_ok, "black_candidates": black_segments}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())

