# GPT Image Style

Use this reference when a slide needs GPT-generated visuals or a stored style.

## Required Workflow For Styled Decks

For polished style-guided PowerPoint work, generate image assets before building
the deck:

1. Resolve the style image, such as `assets/styles/onij.png`.
2. Generate one or more PNG layers for cover backgrounds, chapter dividers,
   local illustrations, or figure backplates.
3. Save generated files under the task folder, usually
   `assets/generated/*.png`.
4. In the PptxGenJS deck script, insert generated images first.
5. Add all exact text, labels, arrows, numbers, legends, and tables as native
   PowerPoint objects.

If the sibling `office-figure` skill is available, its
`assets/node-image-starter/generate-style-image.mjs` is the preferred starting
point for image-only asset generation. Copy or adapt it into the PPT task
folder so the deck remains reproducible without writing dependencies into the
skill directory.

## Environment

Load key-value pairs from the shared repository config:

```text
config/office-skills.local.env
```

The file uses OpenAI-compatible environment names through a gateway. Do not
print secret values. Scripts should also accept `OFFICE_SKILLS_ENV` or `--env`
so contributors can keep private config outside the repository.

Common mapping:

| Config key | SDK use |
| --- | --- |
| `OPENAI_API_KEY` | `apiKey` |
| `OPENAI_BASE_URL` | `baseURL` |
| `ANTHROPIC_API_KEY` | fallback `apiKey` for the local gateway |
| `ANTHROPIC_API_BASE_URL` | fallback `baseURL` for the local gateway |

Model selection:

- Use `PPT_IMAGE_MODEL` when present.
- Use the user's requested image model when specified.
- Otherwise use `gpt-image-2` or the local gateway's available GPT image model.

## Style Reference

For `onij`, use:

```text
assets/styles/onij.png
```

Use the style image as an input/reference image when the API supports image
editing or style-guided generation. Preserve style-level features such as:

- palette and contrast
- texture
- lighting
- line density
- composition rhythm
- visual mood

Do not place final slide text inside the generated image. Add exact text in
PowerPoint.

## Prompt Pattern

Write prompts with:

- subject
- slide role
- style reference instruction
- aspect ratio
- explicit negative space for native PPT overlays
- clear negative constraints for embedded text

Example:

```text
Create a 16:9 presentation background about disciplined office automation.
Use the supplied style reference for palette, texture, visual rhythm, and
illustrative density. Leave clean negative space on the left for native
PowerPoint title text. No readable words, no logo, no UI screenshots.
```

For a local figure layer:

```text
Create a wide scientific visual layer for a research method slide. Use the
supplied style reference for palette, paper texture, density, and lighting.
Show an abstract process with soft blocks and connecting strokes. Leave open
space for editable PowerPoint labels and arrows. No readable words, no numbers,
no logos, no screenshots, no watermark.
```

## File Handling

Save generated images under the task folder, for example:

```text
assets/generated/onij-background.png
```

Record the final generated paths in the task README if one exists, otherwise in
the final response. Do not leave project-used images only inside a temporary or
skill directory.
