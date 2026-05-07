---
name: office-figure
description: "Create editable research figures, diagrams, charts, and hybrid visual assets for Word, PowerPoint, and LaTeX. Use for method figures, architecture diagrams, pipelines, flowcharts, data charts, scientific illustrations, visual abstracts, figure redesign, style-guided image generation, TikZ/PGFPlots, draw.io, SVG/PNG export, and Word/PPT/LaTeX insertion-ready figures."
---

# Office Figure

Use this skill when the user asks for a figure, diagram, chart, research visual,
scientific illustration, or insertion-ready asset for Word, PowerPoint, or
LaTeX.

The main deliverable should be editable. Use generated images as supporting
visual material: background, texture, illustration, icons, or reference panels.
Keep labels, arrows, data marks, legends, formulas, and captions editable in
draw.io, TikZ, PGFPlots, Word drawing shapes, or PowerPoint shapes.

## Output Selection

| Target | Primary editable source | Delivery asset |
| --- | --- | --- |
| Word report or manuscript | `.drawio`, `.svg`, or Word-native drawing shapes | `.svg` or `.png` plus source |
| PowerPoint slide | `.drawio`, `.svg`, or PPT native shapes | `.svg` or `.png` plus source |
| LaTeX paper | `.tex` with TikZ or PGFPlots | `.pdf` or `.svg` plus source |
| Data chart | `.tex` PGFPlots or scripted chart source | `.pdf`, `.svg`, or `.png` |
| Visual abstract or style-heavy figure | editable overlay plus generated image layer | source plus generated image |

## Task Selection

| Task | Read | Implementation focus |
| --- | --- | --- |
| Any academic or research figure | `references/figure-quality.zh.md` | Define success criteria, plan layout, preserve editability, and review rendered output |
| Soft Chinese research roadmap, thesis route, project route, or task breakdown | `references/soft-roadmap-style.zh.md` | Use the stored draw.io roadmap templates and keep all labels editable |
| Research diagram, pipeline, architecture, flowchart | `references/drawio-figures.md` | Build editable `.drawio`; export SVG/PNG if possible |
| LaTeX-native figure or chart | `references/latex-tikz.md` | Build TikZ/PGFPlots `.tex`; compile when TeX is available |
| Render local TikZ/PDF previews or configure lightweight rendering tools | `references/local-rendering-env.zh.md` | Use local Tectonic and Python PDF-to-PNG tooling when available |
| Publication consistency, fonts, colors, vector export, Overleaf, Keynote, or matplotlib styling | `references/publication-consistency.zh.md` | Match figure typography and colors with the manuscript or slide body |
| Neural-network, ML architecture, or scientific TikZ pattern search | `references/tikz-pattern-library.zh.md` | Reuse local pattern knowledge from public diagram libraries without adding repo dependencies |
| Data chart | `references/data-charts.md` | Preserve source data and create editable chart source |
| GPT-generated visual material | `references/image-generation.md` | Use style image and shared local env; keep exact labels editable |
| Figure intended for Word/PPT | `references/office-integration.md` | Deliver source plus SVG/PNG insertion asset |
| Quality review | `references/validation.md` | Check render, text legibility, alignment, and asset completeness |

## Implementation Steps

1. Identify the target context: Word, PowerPoint, LaTeX, or standalone figure.
2. Choose the editable source format from the output table.
3. Decide whether generated images are useful. Use them for visual material, not
   for exact labels or data.
4. If style guidance is requested, resolve a style file in `assets/styles/`.
   The built-in style is `assets/styles/onij.png`.
5. Use `config/office-skills.local.env` at the repository root, `OFFICE_SKILLS_ENV`,
   or a task-specific `--env` path when calling the OpenAI-compatible image API.
   Do not print secret values.
6. Create a task folder beside the requested output.
7. Produce source files, rendered assets, and a short validation note.

## Editing Rules

- Keep all precise text editable.
- Keep raw data or chart source beside rendered chart files.
- Use generated bitmap images only for material that does not need exact
  editing: background, illustration, texture, scene, or style layer.
- Prefer `.drawio` for Office-friendly diagrams with manual editability.
- Prefer TikZ/PGFPlots for LaTeX-native figures and publication charts.
- Prefer SVG as the Office insertion asset when the figure is mostly vector.
- Use PNG when the figure contains generated bitmap imagery or complex effects.
- Deliver both source and rendered asset unless the user requests only one file.

## Resources

- `assets/styles/onij.png`: built-in style reference.
- `../config/office-skills.local.env.example`: shared local OpenAI-compatible image API configuration template.
- `assets/drawio-starter/`: editable draw.io starting point.
- `assets/drawio-templates/`: reusable editable draw.io templates.
- `assets/tikz-starter/transformer-detailed.tex`: detailed editable Transformer architecture TikZ template.
- `assets/node-image-starter/`: minimal style-guided image generation helper.
- `scripts/render-tikz.py`: compile TikZ with local Tectonic and render a PNG preview.
- `references/`: task-specific guidance.
- `examples/`: concrete figure briefs.
- `examples/showcase/`: showcase notes and rendered preview images.
