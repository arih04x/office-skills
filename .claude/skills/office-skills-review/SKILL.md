---
name: office-skills-review
description: >
  Review pull requests and local changes for the office-skills repository. Use
  when validating Office skills, checking SKILL.md frontmatter, reviewing
  repository structure, or scanning for hardcoded secrets before commit/push.
license: MIT
metadata:
  version: "0.1.0"
  category: tooling
---

# Office Skills Review

Review changes against this repository's skill packaging rules.

## Phase 1: Automated Validation

Run the validator from the repository root:

```bash
python .claude/skills/office-skills-review/scripts/validate_skills.py
```

The script checks:

- every top-level `office-*` skill has `SKILL.md`
- `SKILL.md` frontmatter is parseable
- required fields are present: `name`, `description`
- `name` matches the skill directory
- high-confidence hardcoded secrets are not present in tracked-style text files
- each skill exposes `examples/community/{good,corrections,anti-patterns}`
- rendered previews stay under `examples/`, not `assets/previews/`
- local secret files such as `config/office-skills.local.env` are skipped

All `ERROR` findings must be fixed before publishing.

## Phase 2: Manual Review

After automated checks pass, review the changed files:

1. Skill boundary: each skill should remain independently usable.
2. Secret handling: real API keys stay in ignored local files; examples use placeholders.
3. Cross-platform behavior: Windows paths must have macOS/Linux equivalents when practical.
4. Asset purpose: examples/previews belong in `examples/`; only reusable templates, styles, starters, and support resources belong in `assets/`.
5. Documentation: `.codex/INSTALL.md`, `README.md`, and relevant references should stay in sync.

Read `references/structure-rules.md` and `references/quality-guidelines.md` for details.
