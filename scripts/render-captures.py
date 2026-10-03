#!/usr/bin/env python3
"""Rasterize captured native OpenTUI cells using a terminal's monospace font."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("capture_dir", type=Path)
parser.add_argument("output_dir", type=Path)
parser.add_argument("--font", type=Path, required=True)
args = parser.parse_args()
font = ImageFont.truetype(str(args.font), 18)
bold_path = args.font.with_name(args.font.name.replace("Regular", "Bold"))
bold = ImageFont.truetype(str(bold_path), 18) if bold_path.exists() else font
cell_width = font.getlength("M")
cell_height = 25
args.output_dir.mkdir(parents=True, exist_ok=True)
for file in sorted(args.capture_dir.glob("*.json")):
    capture = json.loads(file.read_text())
    image = Image.new("RGB", (round(capture["cols"] * cell_width), capture["rows"] * cell_height), "#16181c")
    draw = ImageDraw.Draw(image)
    for y, line in enumerate(capture["lines"]):
        x = 0
        for span in line["spans"]:
            foreground, background = tuple(span["fg"][:3]), tuple(span["bg"][:3])
            if span["attributes"] & 32:
                foreground, background = background, foreground
            draw.rectangle((round(x * cell_width), y * cell_height, round((x + span["width"]) * cell_width) - 1, (y + 1) * cell_height - 1), fill=background)
            draw.text((round(x * cell_width), y * cell_height + 2), span["text"], fill=foreground, font=bold if span["attributes"] & 1 else font)
            x += span["width"]
    target = args.output_dir / f"{file.stem}.png"
    image.save(target, optimize=True)
    print(target)
