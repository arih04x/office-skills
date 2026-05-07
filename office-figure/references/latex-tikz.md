# LaTeX TikZ and PGFPlots

Use TikZ or PGFPlots when the figure belongs in a LaTeX manuscript or when the
user wants editable LaTeX source.

## Good Fit

- Publication diagrams
- Mathematical figures
- Algorithm pipelines
- PGFPlots charts
- Simple architecture diagrams with precise layout

## Starter

For the built-in editable TikZ example, use
`assets/tikz-starter/transformer-detailed.tex`. Adapt it when the user asks for
Transformer, attention, encoder-decoder, or ML architecture figures.

Compile with:

```powershell
pdflatex figure.tex
```

Use `xelatex` if the figure requires CJK text and the TeX environment supports
it.

## PNG Preview Pipeline

TikZ renders through TeX. The usual preview chain is:

```powershell
pdflatex figure.tex
pdftoppm -png -r 300 figure.pdf figure
```

This creates a PDF and then a PNG preview such as `figure-1.png`. `xelatex` can
replace `pdflatex` when CJK/fontspec is required. If Poppler is not installed,
use Inkscape or ImageMagick to convert the PDF:

```powershell
inkscape figure.pdf --export-type=png --export-filename=figure.png
magick -density 300 figure.pdf figure.png
```

If TeX or PDF conversion tools are missing, still create the `.tex` source and
state which tool is needed for rendering.

For this skill, prefer the lightweight route in
`references/local-rendering-env.zh.md` when Tectonic is available:

```powershell
python office-figure\scripts\render-tikz.py figure.tex --outdir out --png out\figure.png
```

## Rules

- Keep labels as LaTeX text.
- Use named styles for repeated nodes.
- Keep coordinates readable and grouped by region.
- Use PGFPlots for data charts instead of drawing bars or lines manually.
- Store data in a table or inline coordinates so it remains editable.
- For large data, use `\pgfplotstableread` with a nearby `.csv` rather than
  embedding long coordinate lists in drawing code.
- Avoid large bitmap-only figures unless the user requests illustration.
- For publication styling, read `references/publication-consistency.zh.md`.
- For neural-network and scientific pattern choices, read
  `references/tikz-pattern-library.zh.md`.

## Hybrid Image Layer

TikZ can include generated images:

```latex
\node[anchor=south west, inner sep=0] at (0,0)
  {\includegraphics[width=12cm]{generated/background.png}};
```

Place editable labels, arrows, axes, formulas, and annotations above the image.
