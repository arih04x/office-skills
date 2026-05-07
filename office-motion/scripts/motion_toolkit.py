#!/usr/bin/env python3
"""Create and inspect promotional GIF/PPT motion assets."""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageSequence


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    return ImageFont.load_default()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise SystemExit(f"Invalid hex color: {value}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def ease(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


def draw_gradient(draw: ImageDraw.ImageDraw, width: int, height: int, c1, c2, offset: float) -> None:
    for x in range(width):
        t = ((x / max(width - 1, 1)) + offset) % 1.0
        wave = 0.5 + 0.5 * math.sin((t * math.pi * 2.0))
        color = tuple(int(lerp(c1[i], c2[i], wave)) for i in range(3))
        draw.line([(x, 0), (x, height)], fill=color)


def text_bbox(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int, int, int]:
    return draw.textbbox((0, 0), text, font=font)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, bold: bool) -> ImageFont.ImageFont:
    size = start_size
    while size > 16:
        font = load_font(size, bold=bold)
        bbox = text_bbox(draw, text, font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return load_font(size, bold=bold)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font,
    fill,
    stroke_fill=None,
    stroke_width: int = 0,
) -> None:
    bbox = text_bbox(draw, text, font)
    x = xy[0] - (bbox[2] - bbox[0]) / 2
    y = xy[1] - (bbox[3] - bbox[1]) / 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def command_promo_gif(args: argparse.Namespace) -> int:
    width = args.width
    height = args.height
    fps = args.fps
    total_frames = max(2, int(args.duration * fps))
    bg1 = hex_to_rgb(args.bg)
    bg2 = hex_to_rgb(args.bg2)
    accent = hex_to_rgb(args.accent)
    cream = (246, 244, 238)
    ink = (18, 24, 38)

    scratch = Image.new("RGB", (width, height))
    scratch_draw = ImageDraw.Draw(scratch)
    title_font = fit_font(scratch_draw, args.title, int(width * 0.78), int(height * 0.115), True)
    subtitle_font = fit_font(scratch_draw, args.subtitle, int(width * 0.72), int(height * 0.045), False)
    cta_font = fit_font(scratch_draw, args.cta, int(width * 0.34), int(height * 0.04), True)
    label_font = load_font(max(13, int(height * 0.022)), bold=True)

    frames: list[Image.Image] = []
    for index in range(total_frames):
        phase = index / total_frames
        img = Image.new("RGB", (width, height), bg1)
        draw = ImageDraw.Draw(img)
        draw_gradient(draw, width, height, bg1, bg2, phase * 0.25)

        # Moving geometric bands.
        sweep = int(lerp(-width * 0.25, width * 0.88, ease((phase * 1.15) % 1.0)))
        draw.polygon([(sweep, 0), (sweep + width * 0.18, 0), (sweep - width * 0.24, height), (sweep - width * 0.42, height)], fill=accent)
        draw.rectangle([0, height - int(height * 0.11), width, height], fill=(10, 14, 24))
        draw.rectangle([0, height - int(height * 0.115), int(width * (0.22 + 0.18 * math.sin(phase * math.tau))), height - int(height * 0.107)], fill=accent)

        # Soft feature cards.
        card_w = int(width * 0.18)
        card_h = int(height * 0.135)
        base_x = int(width * 0.09)
        card_y = int(height * 0.68)
        for i, label in enumerate(args.cards):
            delay = i * 0.08
            t = ease(min(1.0, max(0.0, phase * 1.6 - delay)))
            x = int(base_x + i * (card_w + width * 0.025))
            y = int(card_y + (1 - t) * 22)
            fill = tuple(int(lerp(cream[j], accent[j], 0.10 + i * 0.04)) for j in range(3))
            draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=10, fill=fill, outline=(255, 255, 255), width=2)
            draw.text((x + 16, y + 16), label, font=label_font, fill=ink)
            draw.rectangle([x + 16, y + card_h - 22, x + int(card_w * (0.54 + 0.12 * i)), y + card_h - 16], fill=accent)

        # Stable title/subtitle and CTA.
        title_y = int(height * 0.33 + math.sin(phase * math.tau) * 2)
        draw_centered_text(draw, (width // 2, title_y), args.title, title_font, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2)
        draw_centered_text(draw, (width // 2, int(height * 0.45)), args.subtitle, subtitle_font, fill=(232, 238, 246), stroke_fill=(0, 0, 0), stroke_width=1)
        pulse = 0.5 + 0.5 * math.sin(phase * math.tau * 2)
        cta_w = int(width * (0.245 + pulse * 0.012))
        cta_h = int(height * 0.068)
        cta_x = width // 2 - cta_w // 2
        cta_y = int(height * 0.535)
        draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=cta_h // 2, fill=cream)
        draw_centered_text(draw, (width // 2, cta_y + cta_h // 2 - 1), args.cta, cta_font, fill=ink)

        frames.append(img)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    duration_ms = int(1000 / fps)
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
    )
    if args.still:
        still = Path(args.still)
        still.parent.mkdir(parents=True, exist_ok=True)
        frames[0].save(still)
    print(json.dumps(inspect_gif(out), ensure_ascii=False, indent=2))
    return 0


def inspect_gif(path: Path) -> dict:
    with Image.open(path) as img:
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        durations = [frame.info.get("duration", img.info.get("duration", 0)) for frame in ImageSequence.Iterator(img)]
        total_ms = sum(durations)
        return {
            "status": "ok",
            "input": str(path),
            "width": img.width,
            "height": img.height,
            "frames": len(frames),
            "duration_ms": total_ms,
            "fps": round(len(frames) / (total_ms / 1000), 2) if total_ms else None,
            "loop": img.info.get("loop", None),
            "size_bytes": path.stat().st_size,
        }


def command_inspect(args: argparse.Namespace) -> int:
    print(json.dumps(inspect_gif(Path(args.input)), ensure_ascii=False, indent=2))
    return 0


def command_still(args: argparse.Namespace) -> int:
    source = Path(args.input)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as img:
        img.seek(max(0, args.frame - 1))
        img.convert("RGB").save(out)
    print(json.dumps({"status": "ok", "out": str(out)}, ensure_ascii=False, indent=2))
    return 0


def command_images_to_gif(args: argparse.Namespace) -> int:
    frames = [Image.open(path).convert("RGB").resize((args.width, args.height)) if args.width and args.height else Image.open(path).convert("RGB") for path in args.inputs]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=args.duration, loop=0, optimize=True)
    print(json.dumps(inspect_gif(out), ensure_ascii=False, indent=2))
    return 0


def command_video_to_gif(args: argparse.Namespace) -> int:
    if not shutil.which("ffmpeg"):
        raise SystemExit("Missing ffmpeg. Install with `brew install ffmpeg`, `apt install ffmpeg`, or Windows winget/choco.")
    input_path = Path(args.input)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    palette = out.with_suffix(out.suffix + ".palette.png")
    scale_filter = f"fps={args.fps},scale={args.width}:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-y", "-i", str(input_path), "-vf", f"{scale_filter},palettegen=stats_mode=diff", str(palette)], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(input_path), "-i", str(palette),
        "-lavfi", f"{scale_filter} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        str(out),
    ], check=True)
    palette.unlink(missing_ok=True)
    print(json.dumps(inspect_gif(out), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="office-motion toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    promo = sub.add_parser("promo-gif", help="Create a local promotional GIF")
    promo.add_argument("--title", required=True)
    promo.add_argument("--subtitle", default="")
    promo.add_argument("--cta", default="Learn more")
    promo.add_argument("--out", required=True)
    promo.add_argument("--still")
    promo.add_argument("--width", type=int, default=1280)
    promo.add_argument("--height", type=int, default=720)
    promo.add_argument("--duration", type=float, default=3.2)
    promo.add_argument("--fps", type=int, default=14)
    promo.add_argument("--accent", default="#E8B84A")
    promo.add_argument("--bg", default="#102033")
    promo.add_argument("--bg2", default="#2F445C")
    promo.add_argument("--cards", nargs="*", default=["DOCX", "PDF", "PPTX", "FIGURE"])
    promo.set_defaults(func=command_promo_gif)

    inspect = sub.add_parser("inspect", help="Inspect GIF dimensions, frames, duration, and size")
    inspect.add_argument("--input", required=True)
    inspect.set_defaults(func=command_inspect)

    still = sub.add_parser("still", help="Export one GIF frame as PNG")
    still.add_argument("--input", required=True)
    still.add_argument("--out", required=True)
    still.add_argument("--frame", type=int, default=1)
    still.set_defaults(func=command_still)

    seq = sub.add_parser("images-to-gif", help="Create GIF from image sequence")
    seq.add_argument("--out", required=True)
    seq.add_argument("--duration", type=int, default=100)
    seq.add_argument("--width", type=int)
    seq.add_argument("--height", type=int)
    seq.add_argument("inputs", nargs="+")
    seq.set_defaults(func=command_images_to_gif)

    convert = sub.add_parser("video-to-gif", help="Convert MP4/video to GIF with ffmpeg")
    convert.add_argument("--input", required=True)
    convert.add_argument("--out", required=True)
    convert.add_argument("--fps", type=int, default=15)
    convert.add_argument("--width", type=int, default=720)
    convert.set_defaults(func=command_video_to_gif)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
