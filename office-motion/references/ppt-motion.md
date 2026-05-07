# PPT Motion Assets

Use this reference when creating animated assets for PowerPoint.

## Format Choice

| Need | Prefer |
| --- | --- |
| Simple loop, broad compatibility | GIF |
| Smooth gradients or photo motion | MP4 |
| Editable labels | PPT native text/shapes over a motion background |
| Static export fallback | PNG |

## PowerPoint Rules

- Keep important text inside safe margins.
- If text must remain editable, place it in PowerPoint, not inside the GIF.
- For animated backgrounds, deliver both motion asset and still fallback.
- Verify playback in desktop PowerPoint when possible.
- Avoid huge GIFs in decks; use MP4 for longer motion or photo-heavy content.

## PPT-Friendly Dimensions

- 16:9 full slide: `1920x1080` or `1280x720`
- half-width panel: `960x540`
- square sticker/callout: `720x720` or `512x512`

## Insertion Notes

PPTX generation libraries usually insert GIFs as image media; PowerPoint handles
playback. For exact deck QA, open/export with PowerPoint after insertion.
