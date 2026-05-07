# Draw.io Figures

Use `.drawio` for Office-friendly diagrams that should remain editable outside
Word and PowerPoint.

## Good Fit

- Method pipelines
- Architecture diagrams
- Flowcharts
- Research framework figures
- Visual abstracts with labels and arrows
- Diagrams that need later manual edits

## Construction Rules

- Use one canvas and group related regions.
- Use short semantic labels.
- Keep arrows outside text boxes.
- Keep a consistent grid and spacing.
- Use SVG export for vector insertion into Word or PowerPoint.
- Use PNG export if the figure includes generated bitmap layers.

## Hybrid Image Layer

When combining generated imagery with draw.io:

1. Generate the bitmap as a background or panel image.
2. Insert the image into the `.drawio` file.
3. Add labels, arrows, callouts, and legends as draw.io text/shapes.
4. Export both `.drawio` and `.png` or `.svg`.

## Layout Patterns

| Pattern | Use |
| --- | --- |
| Left-to-right pipeline | Method steps, workflows |
| Layered stack | System architecture |
| Hub and spokes | Frameworks and dependencies |
| Before/after comparison | Ablations, redesigns, experiments |
| Loop | Feedback, iterative optimization |
| Soft roadmap | Chinese thesis routes, research plans, project task breakdowns |

## Built-In Templates

Use `assets/drawio-templates/` when the task matches an existing structure:

| Template | Use |
| --- | --- |
| `soft-roadmap-3col.drawio` | Compact problem-method-output diagrams |
| `soft-research-roadmap-4col.drawio` | Project vision, core challenges, implementation path, stage outputs |
| `soft-roadmap-5col.drawio` | Background, difficulties, tasks, validation, outputs |

For this template family, read `references/soft-roadmap-style.zh.md`.

## Office Export

- SVG is preferred for clean vector insertion.
- PNG is preferred when the diagram includes generated imagery.
- Keep the `.drawio` source beside the rendered asset.
