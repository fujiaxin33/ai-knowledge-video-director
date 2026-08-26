#!/usr/bin/env python3
"""Extract representative frames with FFmpeg and tile a timeline contact sheet."""

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def get_duration(ffprobe, video):
    cmd = [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(video)]
    return float(subprocess.check_output(cmd, text=True).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--interval", type=float, default=5.0)
    ap.add_argument("--times", help="comma-separated seconds")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--ffprobe", default="ffprobe")
    args = ap.parse_args()
    duration = get_duration(args.ffprobe, args.video)
    times = [float(x) for x in args.times.split(",")] if args.times else [i * args.interval for i in range(max(1, math.ceil(duration / args.interval)))]
    times = [min(max(0, t), max(0, duration - 0.001)) for t in times]

    with tempfile.TemporaryDirectory() as td:
        paths = []
        for i, t in enumerate(times):
            out = Path(td) / f"f{i:03}.jpg"
            subprocess.run([args.ffmpeg, "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(args.video), "-frames:v", "1", "-vf", "scale=480:-2", "-y", str(out)], check=True)
            paths.append(out)
        cols, cell_w, cell_h = min(4, len(paths)), 500, 320
        rows = math.ceil(len(paths) / cols)
        sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "#111")
        d = ImageDraw.Draw(sheet)
        font_path = Path("C:/Windows/Fonts/arial.ttf")
        fnt = ImageFont.truetype(str(font_path), 22) if font_path.exists() else ImageFont.load_default()
        for i, (p, t) in enumerate(zip(paths, times)):
            x, y = (i % cols) * cell_w, (i // cols) * cell_h
            im = Image.open(p).convert("RGB")
            sheet.paste(im, (x + 10, y + 38))
            d.text((x + 10, y + 8), f"{t:07.3f}s", fill="white", font=fnt)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(args.output, quality=90)
    print(json.dumps({"output": str(args.output), "frames": len(times), "duration": duration}, ensure_ascii=False))


if __name__ == "__main__":
    main()

