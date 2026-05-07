# 本地渲染环境

用于把 TikZ/PGFPlots 源文件渲染成 PDF 和 PNG 预览。

## 当前轻量路径

优先使用 PATH 中的 `tectonic`：

```powershell
tectonic --version
tectonic -X compile --print --outdir out figure.tex
```

如果使用 portable Tectonic，不要把私有工具路径写进 skill；用环境变量
或命令参数显式指定：

```powershell
$env:OFFICE_SKILLS_TECTONIC="C:\path\to\tectonic.exe"
python office-figure\scripts\render-tikz.py figure.tex --outdir out --png out\figure.png
```

macOS / Linux:

```bash
OFFICE_SKILLS_TECTONIC=/path/to/tectonic python office-figure/scripts/render-tikz.py figure.tex --outdir out --png out/figure.png
```

已验证版本：

```text
Tectonic 0.16.9
```

Tectonic 第一次编译会下载 LaTeX bundle 和 TikZ/PGF 资源。首次运行可能较慢；缓存完成后，同类图编译会明显变快。若命令长时间无输出，加入 `--print` 查看下载和编译日志。

Windows 上可能出现：

```text
Fontconfig error: Cannot load default config file: No such file: (null)
```

当前简单 TikZ 模板仍可正常输出 PDF/PNG。若后续需要系统字体或 CJK 字体，再安装/配置 fontconfig 或改用完整 TeX Live。

macOS 可用 Homebrew 安装：

```bash
brew install tectonic
python -m pip install PyMuPDF
```

Linux 可用发行版包管理器或 GitHub release 安装 `tectonic`，并安装 `PyMuPDF`：

```bash
python -m pip install PyMuPDF
```

## 依赖

Tectonic 可从系统包管理器、Homebrew、发行版仓库或官方 release 安装。
`PyMuPDF` 的 Python import 名为 `fitz`，已包含在
`environment.office_envs.yml`。

## 可替代工具

若系统安装了 Poppler、Inkscape 或 ImageMagick，也可以使用：

```powershell
pdftoppm -png -r 300 figure.pdf figure
inkscape figure.pdf --export-type=png --export-filename=figure.png
magick -density 300 figure.pdf figure.png
```

本地未检测到这些命令时，继续使用 Tectonic + PyMuPDF。

## 已生成预览

当前已验证的 TikZ PNG 样例：

- `examples/showcase/previews/transformer-detailed.preview.png`
