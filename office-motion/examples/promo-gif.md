# Promo GIF Example

Request:

Create a PowerPoint-ready promotional GIF for an Office automation workflow.

Use:

- `scripts/motion_toolkit.py`
- `references/promo-gif.md`
- `references/ppt-motion.md`
- `references/validation.md`

Run:

```bash
python scripts/motion_toolkit.py promo-gif --title "Office Workflow" --subtitle "DOCX, PDF, PPTX, figures, and motion" --cta "Automate the deck" --out examples/showcase/office-motion-promo.gif
python scripts/motion_toolkit.py still --input examples/showcase/office-motion-promo.gif --out examples/showcase/office-motion-promo.png
python scripts/motion_toolkit.py inspect --input examples/showcase/office-motion-promo.gif
```
