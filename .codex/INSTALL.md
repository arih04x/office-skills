# Installing Office Skills for Codex

Enable these Office skills in Codex through native skill discovery. Clone the
repository, link the skill collection, then restart Codex.

## Prerequisites

- Git
- Codex CLI
- For full runtime support:
  - `.NET SDK 8+` for `office-docx`
  - `Node.js 20+` for `office-ppt` image/PPT helpers
  - Conda or `Python 3.11+` for PDF, figure, motion, and helper scripts
  - PowerPoint desktop app for PPTX PNG review when available
  - Tectonic or another TeX toolchain for TikZ rendering
  - FFmpeg for video-to-GIF conversion in `office-motion`

Shared Conda environment, recommended:

```bash
conda env create -f environment.office_envs.yml
conda activate office_envs
```

Update an existing environment after pulling new changes:

```bash
conda env update -n office_envs -f environment.office_envs.yml --prune
```

The environment spec installs:

- Conda packages: `python=3.11`, `ffmpeg`, `pip`
- pip packages: `python-docx`, `pypdf`, `reportlab`, `pandas`, `openpyxl`,
  `matplotlib`, `pdfplumber`, `pillow`, `PyMuPDF`, `pyyaml`
- Windows-only pip marker: `pywin32; platform_system == 'Windows'`

`environment.office_envs.yml` is the public runtime dependency contract. It does
not store private keys or gateway URLs. Keep local secrets in
`config/office-skills.local.env`.

macOS quick setup without Conda:

```bash
brew install git dotnet node tectonic ffmpeg
python3 -m pip install python-docx pypdf reportlab pandas openpyxl matplotlib pdfplumber pillow PyMuPDF pyyaml
```

Linux quick setup without Conda varies by distribution. The common minimum is:

```bash
sudo apt-get update
sudo apt-get install -y git nodejs npm python3 python3-pip ffmpeg
python3 -m pip install python-docx pypdf reportlab pandas openpyxl matplotlib pdfplumber pillow PyMuPDF pyyaml
```

Install `.NET SDK 8+` and `tectonic` from the official packages or release
archives if they are not available in your distribution repository.

## Installation

### Option A: Install with npx

```bash
npx office-skills install
```

Supports `--target <path>`, `--dry-run`, and `--force`. Default target is
`~/.agents/skills/office-skills`.

### Option B: Clone and link manually

1. Clone the repository:

   ```bash
   git clone git@github.com:arih04x/office-skills.git ~/.codex/office-skills
   ```

2. Link the skill collection:

   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/office-skills ~/.agents/skills/office-skills
   ```

   Windows PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\office-skills" "$env:USERPROFILE\.codex\office-skills"
   ```

3. Restart Codex so the skills are discovered.

## Available Skills

- `office-docx` - Create, edit, template, inspect, and validate Word `.docx`
  files with `.NET` and OpenXML SDK.
- `office-pdf` - Create, inspect, render, extract, fill, merge, and validate
  PDF files with a cross-platform Python workflow.
- `office-ppt` - Create styled editable PowerPoint `.pptx` slides/decks with
  PptxGenJS and optional image generation.
- `office-figure` - Create editable research figures, diagrams, charts,
  TikZ/draw.io sources, and Word/PPT/LaTeX insertion assets.
- `office-motion` - Create promotional GIFs, PPT-ready animated assets,
  stickers, short loops, and GIF/video conversions.

## Local Configuration

Image-generation helpers for PPT, figure, SVG, and style-guided visual assets
use one shared local file:

```text
config/office-skills.local.env
```

This file is intentionally ignored by Git. Start from the checked-in example:

```bash
cp config/office-skills.local.env.example config/office-skills.local.env
```

Then fill in your local API key, gateway URL, and optional image model
overrides. You can also set `OFFICE_SKILLS_ENV=/path/to/private.env` or pass
`--env /path/to/private.env` to helper scripts.

Windows PowerShell:

```powershell
Copy-Item config\office-skills.local.env.example config\office-skills.local.env
```

## Verify

Check that the collection link exists:

```bash
ls -la ~/.agents/skills/office-skills
```

Run the unified smoke test from the clone:

```bash
cd ~/.codex/office-skills
npm run smoke
```

Or validate individual components:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/office-skills/office-docx
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/office-skills/office-pdf
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/office-skills/office-ppt
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/office-skills/office-figure
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/office-skills/office-motion
```

Smoke-test the cross-platform helpers:

```bash
dotnet run --project ~/.codex/office-skills/office-docx/assets/dotnet-starter/OfficeDocxTask.csproj -- /tmp/office-docx-starter.docx
python ~/.codex/office-skills/office-pdf/scripts/pdf_toolkit.py create-demo --out /tmp/office-pdf-demo.pdf
python ~/.codex/office-skills/office-pdf/scripts/pdf_toolkit.py render --input /tmp/office-pdf-demo.pdf --outdir /tmp/office-pdf-rendered
node --check ~/.codex/office-skills/office-ppt/assets/node-starter/create-onij-slide.mjs
python ~/.codex/office-skills/office-figure/scripts/render-tikz.py --help
python ~/.codex/office-skills/office-motion/scripts/motion_toolkit.py promo-gif --title "Office Motion" --subtitle "Promotional GIFs for decks" --cta "Preview" --out /tmp/office-motion.gif
```

## Updating

```bash
cd ~/.codex/office-skills
git pull
```

Skills update through the symlink/junction after Codex restarts.

## Uninstalling

```bash
rm ~/.agents/skills/office-skills
```

Windows PowerShell:

```powershell
Remove-Item "$env:USERPROFILE\.agents\skills\office-skills" -Force
```

Optionally delete the clone after removing the link.
