# Quickstart

## Create a draw.io diagram (XML source)
```bash
# Write a .drawio XML file with <mxfile><diagram><mxGraphModel>...</mxGraphModel></diagram></mxfile>
# See references/drawio-figures.md for node/edge patterns
```

## Render a TikZ figure to PDF and PNG
```bash
python office-figure/scripts/render-tikz.py input.tex --out out/figure.png --dpi 300
```

## Generate a style image with the node starter (mock or real API)
```bash
cd office-figure/assets/node-image-starter && node index.js --prompt "diagram background" --mock
```

## Validate a figure file (PNG, SVG, or .drawio)
```bash
python office-figure/scripts/check-figure.py out/figure.png
python office-figure/scripts/check-figure.py out/diagram.drawio
```
