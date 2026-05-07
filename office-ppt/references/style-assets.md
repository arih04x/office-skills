# Style Assets

Style assets live in `assets/styles/` and are part of the skill.

## Built-In Styles

| Style | File | Use |
| --- | --- | --- |
| `onij` | `assets/styles/onij.png` | Stylized image-backed PPT visuals |

## Usage

When a user names a style:

1. Resolve the style name to a file in `assets/styles/`.
2. Use the image as visual reference for GPT image generation.
3. Extract presentation-level choices from the reference: palette, contrast,
   density, texture, and composition.
4. Keep slide title and labels native in PPT.
5. Record which style file was used in the task notes or final response.

## Adding Styles

Add future styles as image files under `assets/styles/`. Use short lowercase
names without spaces for the style identifier.
