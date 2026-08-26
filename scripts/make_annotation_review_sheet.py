#!/usr/bin/env python3
"""Create a visual annotation audit sheet: full frame plus target close-up."""

import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def font(size):
    candidates = [Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/arial.ttf")]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    anns = data.get("annotations", [])
    if not anns:
        raise SystemExit("manifest contains no annotations")
    row_h, sheet_w = 480, 1500
    sheet = Image.new("RGB", (sheet_w, row_h * len(anns)), "#171717")
    draw = ImageDraw.Draw(sheet)

    for i, ann in enumerate(anns):
        y0 = i * row_h
        frame_path = Path(ann["frame_path"])
        if not frame_path.is_absolute():
            frame_path = args.manifest.parent / frame_path
        frame = Image.open(frame_path).convert("RGB")
        fw, fh = frame.size
        preview = frame.copy()
        pd = ImageDraw.Draw(preview)
        m = ann["annotation"]
        t = ann["target"]
        pd.rectangle((m["x"], m["y"], m["x"] + m["width"], m["y"] + m["height"]), outline="#ff4b32", width=6)
        pd.rectangle((t["x"], t["y"], t["x"] + t["width"], t["y"] + t["height"]), outline="#ffc14d", width=3)
        preview.thumbnail((780, 390))
        sheet.paste(preview, (20, y0 + 70))

        margin = 40
        left = max(0, t["x"] - margin)
        top = max(0, t["y"] - margin)
        right = min(fw, t["x"] + t["width"] + margin)
        bottom = min(fh, t["y"] + t["height"] + margin)
        crop = frame.crop((left, top, right, bottom))
        crop.thumbnail((470, 300))
        sheet.paste(crop, (820, y0 + 120))

        draw.text((20, y0 + 20), f"{ann['id']}  frames {ann['start_frame']}–{ann['end_frame']}  {ann.get('kind', 'box')}", fill="#f6f0e6", font=font(25))
        draw.text((1310, y0 + 120), "TARGET", fill="#ffc14d", font=font(20))
        lines = [ann.get("semantic_target", ""), ann.get("why_now", "")]
        yy = y0 + 165
        for line in lines:
            for part in [line[j:j+18] for j in range(0, len(line), 18)] or [""]:
                draw.text((1310, yy), part, fill="#d8d2c8", font=font(16))
                yy += 24
        draw.line((0, y0 + row_h - 1, sheet_w, y0 + row_h - 1), fill="#555", width=1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92)
    print(json.dumps({"output": str(args.output), "rows": len(anns), "size": sheet.size}, ensure_ascii=False))


if __name__ == "__main__":
    main()
