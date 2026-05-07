# Image Generation

Use generated images when the figure benefits from illustration, texture,
background, visual analogy, or style transfer.

## Environment

Load key-value pairs from the shared repository config:

```text
config/office-skills.local.env
```

The file may use OpenAI-compatible keys or local gateway keys. Do not print the
values. Scripts should also accept `OFFICE_SKILLS_ENV` or `--env` so private
config can live outside the repository.

Common mapping:

| Config key | SDK use |
| --- | --- |
| `OPENAI_API_KEY` | `apiKey` |
| `OPENAI_BASE_URL` | `baseURL` |
| `ANTHROPIC_API_KEY` | fallback `apiKey` |
| `ANTHROPIC_API_BASE_URL` | fallback `baseURL` |

## Style Assets

The built-in style is:

```text
assets/styles/onij.png
```

Use style images for palette, texture, density, and composition rhythm. Do not
copy logos or exact source content.

## Prompt Rules

- Specify the target figure role.
- Ask for clean negative space where editable labels will be placed.
- State that the image must contain no readable text.
- Generate in a wide aspect ratio for slides and reports unless another target
  is specified.

Example:

```text
Create a wide research figure background about multimodal office automation.
Use the supplied style reference for palette, texture, density, and lighting.
Leave clean space in the upper left and lower right for editable labels. No
readable words, no logos, no UI screenshots.
```

## Integration

Generated image files should be inserted under editable overlays:

- draw.io: image layer plus editable text, arrows, shapes.
- TikZ: `includegraphics` layer plus TikZ labels and annotations.
- Word/PPT: SVG/PNG background plus native Word/PPT text and shapes.
