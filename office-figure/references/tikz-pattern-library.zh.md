# TikZ 模板经验

本 reference 只保留对当前 skill 有用的模板经验。外部仓库作为结构参考，不作为运行依赖。

来源：

- `https://github.com/fraserlove/nntikz`，MIT License。
- `https://github.com/janosh/diagrams`，MIT License，并提供 Zenodo citation。

内置 TikZ 模板：

- `assets/tikz-starter/transformer-detailed.tex`
- `examples/showcase/previews/transformer-detailed.preview.png`

## 使用方式

- Transformer、attention、encoder-decoder、ML architecture：从 `transformer-detailed.tex` 开始改。
- 只需要局部 attention 图时，从模板中的 attention 节点抽取，并把 Q/K/V 作为节点内短标签或旁注。
- 只需要 encoder-decoder 图时，保留左右两栏和 encoder memory 连接，删除不相关层。
- 用于论文时保留 TikZ 源和 PDF；用于 Word/PPT 时额外导出 PNG 或 SVG。

## 写图原则

- 精确文字、公式、箭头、数据和标签保留为 TikZ 可编辑对象。
- 用命名样式管理节点、线条、颜色，不在正文里散写样式。
- 复杂图分成 2-3 个清楚区域：主流程、关键内部结构、输出或数据面板。
- 不用多条长箭头承载细节。优先用节点内短标签、色带、浅色分区和少量语义箭头表达结构。
- 借鉴公开模板的结构和命名，不直接复制整张图；明显基于外部模板时保留来源 URL 和 license/citation note。
