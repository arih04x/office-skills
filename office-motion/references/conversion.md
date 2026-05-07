# Conversion and Optimization

Use this reference for MP4-to-GIF, image-sequence GIFs, and optimization.

## MP4 to GIF

When FFmpeg is available, use a two-pass palette conversion:

```bash
python scripts/motion_toolkit.py video-to-gif --input input.mp4 --out output.gif --fps 15 --width 720
```

Lower `--fps` and `--width` to reduce size.

## Image Sequence to GIF

```bash
python scripts/motion_toolkit.py images-to-gif --out loop.gif frame1.png frame2.png frame3.png
```

## Still Frame

```bash
python scripts/motion_toolkit.py still --input promo.gif --out promo-still.png
```

Use a still frame as PPT thumbnail, PDF fallback, or preview image.

## Size Guidance

- Chat/email: target under 3 MB.
- PPT deck asset: under 8 MB when possible.
- Web/social: follow platform limits.

If the GIF is too large, reduce dimensions before reducing FPS too far.
