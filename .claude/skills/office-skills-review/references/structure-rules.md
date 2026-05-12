# Structure Rules

These are the hard checks for the `office-skills` repository.

## Skill Directories

Top-level reusable skills live at:

```text
office-docx/
office-pdf/
office-ppt/
office-figure/
office-motion/
```

Each skill directory must include:

- `SKILL.md`
- `agents/openai.yaml`
- task-specific `references/`
- task-specific `examples/`
- `assets/` or `scripts/` only when the skill actually needs them

## Root Package

The repository root includes a `package.json` that serves as the npm
distribution and task-runner wrapper. It must not absorb skill-specific content.

Required root package fields:

- `name`: `office-skills`
- `version`
- `license`
- `bin.office-skills`
- `files` (allowlist)
- `scripts.validate`
- `scripts.smoke`
- `scripts.pack:check`

Root `scripts/` contains only cross-cutting CLI/task-runner code.

## Shared Utilities

`scripts/shared/` contains cross-skill utility functions (env loading, common
helpers). No skill-specific logic belongs here.

## SKILL.md Frontmatter

`SKILL.md` must start with YAML frontmatter enclosed by `---`.

Required fields:

| Field | Rule |
| --- | --- |
| `name` | Must match the directory name |
| `description` | Must be non-empty and include trigger/use context |

Do not require `license` or `metadata` for the three production Codex skills;
Codex only requires `name` and `description`.

## Secret Handling

Real local configuration must not be committed:

```text
config/office-skills.local.env
```

Only the placeholder example `config/office-skills.local.env.example` is
committed. Do not add per-skill env examples under `assets/env/`.

The validator blocks high-confidence secret patterns such as:

- OpenAI-style `sk-...` keys
- AWS access key IDs
- long bearer tokens

Manual review should still check API key handling in scripts and docs.

## Publication Safety

The npm package uses a `files` allowlist and `.npmignore` for defense-in-depth.
Before publishing, run:

```bash
npm run pack:check
npm pack --dry-run
```

Nested starter `package.json` files must remain `"private": true`.

## Examples vs Assets

Use this boundary:

- `examples/`: prompts, briefs, showcases, rendered previews, expected outputs,
  community cases, and validation notes.
- `assets/`: reusable templates, style references, starter projects, and support
  resources used to create future outputs.

Rendered previews must not live under `assets/previews/`.

## Community Cases

Each skill must include:

```text
examples/community/
├─ README.md
├─ good/
├─ corrections/
└─ anti-patterns/
```
