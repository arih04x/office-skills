# Community Case Guide

Community cases turn real usage into reusable skill knowledge. A good case
should let maintainers understand the request, reproduce the workflow, and see
what quality bar was met.

## Case Template

```markdown
# Case: concise title

## Context

- Skill:
- User goal:
- Target format:
- Platform:

## Inputs

List public inputs, source files, style references, or synthetic fixtures.

## Workflow

List the commands, scripts, or manual review steps.

## Result

Link outputs or describe the expected artifact.

## Validation

Explain how the output was checked.

## Notes

Mention limitations, tradeoffs, or follow-up improvements.
```

## Correction Case Template

```markdown
# Correction: concise title

## Bad Output

Describe the failure and why it matters.

## Diagnosis

Name the specific issue: layout, editability, hallucinated text, wrong tool,
broken environment, missing validation, or another cause.

## Fix

Show the corrected workflow or changed instruction.

## Better Result

Describe or link the corrected artifact and validation.
```
