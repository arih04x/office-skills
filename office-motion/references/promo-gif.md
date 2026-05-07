# Promotional GIFs

Use this reference for looping marketing GIFs, animated banners, launch cards,
feature announcements, and lightweight social motion assets.

## Default Specs

| Surface | Size | Duration | FPS |
| --- | --- | --- | --- |
| PPT wide banner | `1280x720` | 3-4 s | 12-18 |
| WeChat/social square | `1080x1080` | 2-4 s | 12-15 |
| Email GIF | `800x450` | 2-3 s | 10-12 |
| Story/reel preview | `720x1280` | 3-5 s | 15 |

## Message Structure

Keep one message per asset:

- title: 3-7 words
- subtitle: one short supporting phrase
- CTA or tag: 1-3 words

Do not animate paragraphs. If the content needs a paragraph, make a PPT slide or
PDF instead.

## Motion Pattern

Reliable local patterns:

- slow background pan
- accent bar sweep
- title fade/slide
- CTA pulse
- small data/feature cards stepping in

Avoid motion that distorts text. Exact words should be rendered locally with a
font, not generated inside a video frame.

## Command

```bash
python scripts/motion_toolkit.py promo-gif \
  --title "AI Office Workflow" \
  --subtitle "DOCX, PDF, PPTX, figures, and motion assets" \
  --cta "Ship faster" \
  --out promo.gif
```
