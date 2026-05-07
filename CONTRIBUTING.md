# Contributing

Office Skills is intended to grow through practical pull requests: better
workflows, better examples, sharper validation, and documented failure modes.

## Contribution Lanes

- Case PRs: add examples under `<skill>/examples/community/`.
- Skill PRs: improve `SKILL.md`, `references/`, `scripts/`, or reusable `assets/`.
- Validation PRs: improve checks, showcase QA, rendering, or secret scanning.
- Documentation PRs: clarify setup, local config, contribution standards, or
  cross-platform behavior.

## Community Cases

Each skill owns a community case area:

```text
office-*/examples/community/
├─ good/
├─ corrections/
└─ anti-patterns/
```

Use these lanes consistently:

- `good`: high-quality reproducible cases with prompt, inputs, commands,
  outputs, and validation notes.
- `corrections`: before/after cases where a bad output is diagnosed and fixed.
- `anti-patterns`: examples of workflows or outputs that should be avoided,
  with a concise explanation and a better direction.

Case files should be small, public, and reproducible. Use Markdown for the case
brief and place large binary artifacts only when they materially improve review.

## Examples vs Assets

Keep this boundary strict:

- `examples/`: briefs, showcases, rendered previews, good/bad/correction cases,
  expected output snapshots, and review notes.
- `assets/`: reusable templates, style references, starter projects, scripts'
  support files, fonts, and other resources used to create future outputs.

Do not put one-off previews or community case outputs in `assets/`.

## Local Configuration

Private keys and gateways are local-only. Use:

```text
config/office-skills.local.env
```

Start from:

```text
config/office-skills.local.env.example
```

Never commit real keys, private endpoints, credentials, or customer data. Helper
scripts should accept `OFFICE_SKILLS_ENV` or `--env` for private external config.

## Pull Request Checklist

- Keep changes scoped to one skill or one cross-cutting concern.
- Update examples or references when changing behavior.
- Add a community case for new user-facing workflows when possible.
- Run the repository validation before submitting.
- Confirm no private env file, key, certificate, token, or local path is staged.

Recommended checks:

```bash
python .claude/skills/office-skills-review/scripts/validate_skills.py
python -m py_compile office-pdf/scripts/pdf_toolkit.py office-figure/scripts/render-tikz.py office-motion/scripts/motion_toolkit.py
node --check office-ppt/assets/node-starter/create-onij-slide.mjs
node --check office-figure/assets/node-image-starter/generate-style-image.mjs
```
