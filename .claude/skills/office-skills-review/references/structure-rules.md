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
