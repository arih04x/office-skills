# Detailed Transformer Example

Request:

Create a detailed editable Transformer architecture figure that shows encoder
and decoder stacks, embedding plus positional encoding, multi-head attention
internals, residual add/norm paths, feed-forward layers, causal masking,
encoder memory, cross-attention, linear projection, and softmax.

Use:

- `assets/tikz-starter/transformer-detailed.tex`
- `references/tikz-pattern-library.zh.md`
- `references/local-rendering-env.zh.md`

Render:

```powershell
python office-figure/scripts/render-tikz.py office-figure/assets/tikz-starter/transformer-detailed.tex --outdir Work/figure-tests/transformer-detailed --png office-figure/examples/showcase/previews/transformer-detailed.preview.png
```
