# Quickstart

## Create a promotional GIF
```bash
python office-motion/scripts/motion_toolkit.py promo-gif \
  --title "Launch Day" --subtitle "Ship it" --out out/promo.gif
```

## Inspect a GIF (frames, duration, dimensions)
```bash
python office-motion/scripts/motion_toolkit.py inspect --input out/promo.gif
```

## Convert a video to GIF
```bash
python office-motion/scripts/motion_toolkit.py video-to-gif \
  --input clip.mp4 --out out/clip.gif --fps 15 --width 720
```

## Create a sticker from image sequence
```bash
python office-motion/scripts/motion_toolkit.py images-to-gif \
  --out out/sticker.gif --duration 80 frame1.png frame2.png frame3.png
```
