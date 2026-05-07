# 出版一致性

用于论文、学位论文、正式 Word 文档、PPT/Keynote 讲稿和 Overleaf 项目中的图。目标是让图内文字、线条、颜色、导出格式与正文系统一致。

## 字体

- 图中文字优先跟随正文。LaTeX 论文默认使用 Computer Modern；Word 常用 Times New Roman；中文正文按文档模板选择宋体、黑体或等线。
- 不要在同一组图里混用多套西文字体。若正文是 Times New Roman，图中英文、坐标轴、图例也使用 Times New Roman。
- TikZ/PGFPlots 默认继承 LaTeX 字体。除非任务需要幻灯片风格，不要在 TikZ starter 中强制 `\sffamily`。
- Matplotlib 图用于 LaTeX 时，优先开启 LaTeX text backend 或 PGF backend，使标题、标签、图例与正文一致。
- Keynote 使用论文同款字体时，先在系统中安装 Computer Modern Unicode / CMU Serif，必要时导入 CMUrm 字体后再设为图表文本字体。

## 字号

- 图内正文标签通常使用正文小一号或同号。正文 10-12 pt 时，图内标签常用 8-10 pt。
- 坐标轴、图例、节点标签使用同一字号层级。标题若已有图题，不在图内重复放大标题。
- 多张子图使用统一字号，避免某一张因缩放导致文字明显变小。

## 颜色

Matplotlib 默认离散色板适合科研图和 Office 图复用：

```text
1F77B4, FF7F0E, 2CA02C, D62728, 9467BD,
8C564B, E377C2, 7F7F7F, BCBD22, 17BECF
```

Overleaf / TikZ 可直接定义：

```latex
\definecolor{mplBlue}{HTML}{1F77B4}
\definecolor{mplOrange}{HTML}{FF7F0E}
\definecolor{mplGreen}{HTML}{2CA02C}
\definecolor{mplRed}{HTML}{D62728}
\definecolor{mplPurple}{HTML}{9467BD}
\definecolor{mplBrown}{HTML}{8C564B}
\definecolor{mplPink}{HTML}{E377C2}
\definecolor{mplGray}{HTML}{7F7F7F}
\definecolor{mplOlive}{HTML}{BCBD22}
\definecolor{mplCyan}{HTML}{17BECF}
```

Keynote / PowerPoint 中建立同一组色板。图、正文强调色和 Overleaf 宏保持同名或同顺序。

## Matplotlib 设置

LaTeX 已安装时使用：

```python
import os
import matplotlib as mpl

# Add TeX/Poppler paths here only when the tools are installed outside PATH.
# os.environ["PATH"] = r"C:\texlive\2026\bin\windows;" + os.environ["PATH"]

mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman"],
    "axes.labelsize": 9,
    "font.size": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})
```

LaTeX 不可用时，仍使用 serif 字体、固定字号和矢量导出；不要为了预览改成另一套最终不会使用的风格。

## 矢量导出

- Matplotlib：优先 `fig.savefig("figure.pdf", bbox_inches="tight")`，Office 需要时同时导出 SVG 或 300-600 dpi PNG。
- TikZ/PGFPlots：输出 PDF 作为论文主资产；需要 Office 插入时再转 SVG/PNG。
- Keynote / PowerPoint：优先导出 PDF 保留矢量。复杂位图或透明效果需要 PNG 时，另存一份源文件。
- Inkscape 可作为 Adobe Illustrator 的免费替代，用于检查和微调 SVG/PDF。改动后保留编辑源和导出资产。

## 数据量较大时

PGFPlots 数据较多时不要把几千行坐标直接写进绘图逻辑。使用外部 CSV 或表格读取：

```latex
\pgfplotstableread[col sep=comma]{data.csv}\datatable
\addplot table[x=x, y=y] {\datatable};
```

大型数据图应保留 `data.csv` 或生成脚本，保证图可以复现。
