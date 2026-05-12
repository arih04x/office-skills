---
name: office-motion
description: "Create promotional GIFs, animated stickers, short motion assets, and PowerPoint-ready animated visuals for Office workflows. Use for marketing GIFs, PPT animated GIF insertion, looping product promos, animated banners, social/WeChat motion assets, GIF optimization, MP4-to-GIF conversion, image-sequence animation, motion storyboards, and presentation-safe animated media."
---

# Office Motion

Use this skill for promotional GIFs, animated assets, PPT motion inserts, or GIF/video conversion.

## Operating Model

- `scripts/motion_toolkit.py` for deterministic GIF creation, conversion, inspection.
- Generated image/video APIs are optional upstream sources, not required.
- Deliver PPT-safe assets: `.gif` for loops, `.mp4` for smooth motion, still PNG fallback.
- Dimensions: 16:9 PPT banners, 1:1 stickers, 9:16 stories/reels.

## Task Selection

| Task | Read | Focus |
| --- | --- | --- |
| Promo GIF / banner | `references/promo-gif.md` | Short loop, stable text, readable CTA, compressed |
| PPT animated visual | `references/ppt-motion.md` | PPT-friendly GIF/MP4, safe margins, fallback frame |
| Sticker / expression GIF | `references/sticker-gif.md` | Consistent actions, short captions, loopable |
| Convert / optimize | `references/conversion.md` | FFmpeg two-pass palette or Pillow fallback |
| Validate | `references/validation.md` | Dimensions, frame count, size, readability, loop |

Read the matching reference, implement, validate with `scripts/motion_toolkit.py inspect`.

## Key Rules

- Loop: 2-5s promo, 1-2s stickers.
- Text must not warp/rotate/shimmer — keep stable in local rendering.
- Still frame fallback for PPT thumbnails.
- Under 8 MB (under 3 MB for chat/email).
- MP4 over GIF for photorealistic or gradient-heavy motion.
