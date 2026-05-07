# Data Charts

Use this reference for charts and plots.

## Source First

Keep the source data or data-generation code beside the rendered chart. A chart
without data source is not considered editable.

## Format Choice

| Target | Preferred source |
| --- | --- |
| LaTeX | PGFPlots `.tex` |
| Word | SVG plus source data/code |
| PowerPoint | SVG or PPT native chart when live editing in PowerPoint is required |
| Exploratory chart | Python script plus SVG/PNG output |

## Chart Rules

- Use real axis labels and units.
- Avoid decorative 3D chart effects.
- Keep legends short or label series directly.
- Use color only when it adds grouping or comparison value.
- Keep fonts, sizes, and colors aligned with the manuscript or slide style; use
  `references/publication-consistency.zh.md` for final plotting settings.
- Keep generated imagery out of data marks unless it is a visual abstract, not a
  quantitative chart.

## PGFPlots

Use PGFPlots for LaTeX-native charts. Keep coordinates or table data in the
`.tex` file or a nearby `.csv`.

For large tables:

```latex
\pgfplotstableread[col sep=comma]{data.csv}\datatable
\addplot table[x=x, y=y] {\datatable};
```

## Office Charts

For Word and PowerPoint, use SVG for high-quality insertion. If the user needs
PowerPoint-native chart editing, create the chart directly in PPT with
PptxGenJS or use the PPT skill.
