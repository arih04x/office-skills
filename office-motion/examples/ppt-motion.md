# PPT Motion Example

Request:

Create a 16:9 animated GIF that can be inserted into a presentation as a
feature-announcement panel, plus a PNG fallback.

Use:

- `references/ppt-motion.md`
- `scripts/motion_toolkit.py`

Run:

```bash
python scripts/motion_toolkit.py promo-gif --width 1280 --height 720 --title "Quarterly Launch" --subtitle "Three updates ready for the board deck" --cta "Preview now" --out launch-panel.gif
python scripts/motion_toolkit.py still --input launch-panel.gif --out launch-panel.png
```
