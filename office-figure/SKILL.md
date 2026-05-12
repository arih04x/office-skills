---
name: office-figure
description: "Create editable research figures, diagrams, charts, and hybrid visual assets for Word, PowerPoint, and LaTeX. Use for method figures, architecture diagrams, pipelines, flowcharts, data charts, scientific illustrations, visual abstracts, figure redesign, style-guided image generation, TikZ/PGFPlots, draw.io, SVG/PNG export, and Word/PPT/LaTeX insertion-ready figures."
---

# Office Figure

Use this skill for figures, diagrams, charts, or insertion-ready visual assets. Main deliverable must be editable.

## Operating Model

- Editable sources: `.drawio` for Office, TikZ/PGFPlots for LaTeX, SVG for vector.
- Generated images only for non-exact material (background, texture, illustration).
- Style references in `assets/styles/` (built-in: `onij.png`).
- Env config from `config/office-skills.local.env`, `OFFICE_SKILLS_ENV`, or `--env`.

## Output Selection

| Target | Editable source | Delivery |
| --- | --- | --- |
| Word/PPT | `.drawio` or `.svg` | `.svg`/`.png` + source |
| LaTeX | `.tex` (TikZ/PGFPlots) | `.pdf`/`.svg` + source |
| Data chart | scripted source | `.pdf`/`.svg`/`.png` |
| Style-heavy | editable overlay + generated layer | source + image |

## Task Selection

| Task | Read | Focus |
| --- | --- | --- |
| Academic/research figure | `references/figure-quality.zh.md` (zh) | Success criteria, layout, editability |
| Chinese roadmap/thesis route | `references/soft-roadmap-style.zh.md` (zh) | draw.io templates, editable labels |
| Diagram/pipeline/flowchart | `references/drawio-figures.md` | Editable `.drawio`; export SVG/PNG |
| LaTeX figure/chart | `references/latex-tikz.md` | TikZ/PGFPlots `.tex`; compile if TeX available |
| Local TikZ rendering | `references/local-rendering-env.zh.md` (zh) | Tectonic + PDF-to-PNG |
| Publication consistency | `references/publication-consistency.zh.md` (zh) | Match typography/colors with manuscript |
| TikZ pattern search | `references/tikz-pattern-library.zh.md` (zh) | Reuse patterns without adding deps |
| Data chart | `references/data-charts.md` | Preserve source data, editable chart |
| GPT visual material | `references/image-generation.md` | Style image + local env; labels editable |
| Word/PPT insertion | `references/office-integration.md` | Source + SVG/PNG asset |
| Quality review | `references/validation.md` | Render, legibility, alignment, completeness |

Common combos: `figure-quality.zh.md` + `drawio-figures.md` + `office-integration.md` for Word-ready diagrams.

Read the matching reference(s), implement, validate with `scripts/check-figure.py`.

## Key Rules

- All precise text must be editable (not rasterized).
- Keep raw data beside rendered charts.
- Prefer `.drawio` for Office; TikZ for LaTeX; SVG for vector insertion.
- Deliver both source and rendered asset unless user requests only one.
