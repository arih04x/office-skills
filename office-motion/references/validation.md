# Motion Validation

Use this before delivering a GIF/MP4/PPT motion asset.

## Inspect

```bash
python scripts/motion_toolkit.py inspect --input asset.gif
```

Check:

- dimensions
- frame count
- duration
- FPS
- file size
- loop setting

## Visual Review

Inspect the animation for:

- readable text on every frame
- no text warping or flicker
- safe margins for PPT
- smooth loop
- no blank first frame
- no final-frame jump
- no excessive file size

## PPT Review

For PowerPoint assets:

- insert into a test slide
- play slideshow mode
- export a still or PNG preview if needed
- confirm the asset does not obscure editable PPT text

## Reporting

State:

- final asset path
- dimensions
- duration/FPS
- file size
- still fallback path if generated
- PowerPoint review status if applicable
