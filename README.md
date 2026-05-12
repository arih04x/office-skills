# Office Skills

Open-source Codex skills for serious Office automation: DOCX, PDF, PPTX,
editable research figures, SVG/TikZ/draw.io assets, and promotional GIF
workflows.

Author: `ARIHOAX`
License: `MIT`

## What This Is

Office Skills is a collection of independent, reusable agent skills for
document production and review. It focuses on workflows where format fidelity,
editability, validation, and repeatability matter.

The package currently includes:

| Skill | Purpose | Main route |
| --- | --- | --- |
| `office-docx` | Create, edit, template, inspect, and validate Word documents | `.NET + OpenXML SDK` |
| `office-pdf` | Create, inspect, render, extract, fill, merge, and QA PDFs | Python PDF tooling |
| `office-ppt` | Build styled editable PowerPoint decks and image-backed slides | `Node.js + PptxGenJS` |
| `office-figure` | Create editable research figures, diagrams, charts, SVG/TikZ/draw.io assets | draw.io, TikZ, Python, SVG/PNG |
| `office-motion` | Create promotional GIFs, PPT-ready animated assets, short loops, and GIF/video conversions | Python + Pillow + FFmpeg |

Each skill has its own `SKILL.md`, UI metadata, references, examples, scripts,
and reusable assets where needed. Skills are parallel modules; shared runtime
setup is documented at the repository root.

## Quick Start

Install and link with npx (Node 20+):

```bash
npx office-skills install
```

Or clone the repository for development:

```bash
git clone git@github.com:arih04x/office-skills.git
cd office-skills
npm run smoke
```

Create the shared local Python environment:

```bash
conda env create -f environment.office_envs.yml
conda activate office_envs
```

Update an existing environment:

```bash
conda env update -n office_envs -f environment.office_envs.yml --prune
```

The shared environment is used for PDF, XLSX, image inspection, TikZ preview
conversion, GIF/video conversion, and helper scripts. DOCX and PPT workflows
also use external runtimes such as `.NET SDK`, `Node.js`, PowerPoint,
Tectonic, or LibreOffice when the task requires them.

## Local Configuration

Private API keys and local gateways are configured in one local-only file:

```text
config/office-skills.local.env
```

Start from the public example:

```bash
cp config/office-skills.local.env.example config/office-skills.local.env
```

Windows PowerShell:

```powershell
Copy-Item config\office-skills.local.env.example config\office-skills.local.env
```

The real `config/office-skills.local.env` file is ignored by Git. PPT, figure,
SVG, and style-guided image helper scripts should read this shared config by
default, while still allowing `OFFICE_SKILLS_ENV` or `--env` overrides.

## Repository Layout

```text
office-skills
├─ office-docx
├─ office-pdf
├─ office-ppt
├─ office-figure
├─ office-motion
├─ config
│  └─ office-skills.local.env.example
├─ docs
├─ .codex
│  └─ INSTALL.md
├─ .claude
│  └─ skills
├─ .claude-plugin
├─ environment.office_envs.yml
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ CODE_OF_CONDUCT.md
├─ LICENSE
└─ README.md
```

## Examples vs Assets

The boundary is intentional:

- `examples/`: prompts, briefs, showcases, rendered previews, expected outputs,
  community cases, and validation notes.
- `assets/`: reusable templates, style references, starter projects, and support
  resources used to create future outputs.

Do not put one-off previews or community case outputs in `assets/`.

## Community Cases

Every skill has a dedicated area for community PRs:

```text
office-*/examples/community/
├─ good/
├─ corrections/
└─ anti-patterns/
```

Use it to contribute:

- strong examples that others can reproduce;
- bad-output correction cases with diagnosis and improved workflow;
- anti-patterns that help the skills avoid common failure modes.

See `CONTRIBUTING.md` and `docs/CASE_GUIDE.md` before opening a case PR.

## Validation

Run the repository validation before opening a PR:

```bash
npm run validate
npm run smoke
```

Or without npm:

```bash
python .claude/skills/office-skills-review/scripts/validate_skills.py
python -m py_compile office-pdf/scripts/pdf_toolkit.py office-figure/scripts/render-tikz.py office-motion/scripts/motion_toolkit.py
node --check office-ppt/assets/node-starter/create-onij-slide.mjs
node --check office-figure/assets/node-image-starter/generate-style-image.mjs
```

GitHub Actions also runs these checks on pull requests.

## Publishing Safety

Before publishing to npm:

```bash
npm run validate
npm run smoke
npm run pack:check
npm pack --dry-run
```

The package uses a `files` allowlist and `.npmignore` to exclude local secrets,
generated output, caches, and private config.

## Installation Details

Codex installation notes are in:

```text
.codex/INSTALL.md
```

The install guide covers skill discovery, local environment setup, macOS/Linux
notes, Windows notes, and smoke tests.

## Project Metadata

Recommended GitHub repository description:

```text
Open-source Codex office automation skills for DOCX, PDF, PPTX, editable figures, SVG/TikZ/draw.io assets, and promotional GIF workflows.
```

Recommended topics are listed in `docs/REPOSITORY_METADATA.md`.
