---
name: postcard-maker
description: Generate stylized photo postcards with a blurred backdrop, centered foreground image, black caption bar, and custom title text using Python Pillow. Use when the user asks to turn a photo into a postcard, create a blurred-background photo card, add a caption bar and title text to an image, or replicate the b11413076 postcard style.
---
# postcard-maker

Create stylized 800x600 photo postcards from any input image using Python Pillow. The layout pairs a Gaussian-blurred full-bleed backdrop with a centered sharp foreground image, a black bottom caption bar, custom title text, and a subtle soft-focus finish.

## When to Use

- The user wants to convert an image or photo into a stylized postcard.
- The user asks for a blurred-background photo card with a bottom caption bar and title text.
- The user wants to batch-generate or customize postcards with different titles, text colors, or dimensions.

## Steps

1. Confirm the input image path, desired caption text, and output file path (default output: `postcard.jpg`).
2. Run `scripts/make_postcard.py` with the target parameters:

   ```bash
   python3 scripts/make_postcard.py \
     --input path/to/input.png \
     --output path/to/postcard.jpg \
     --text "Your Title" \
     --color violet
   ```

3. Verify the generated output image exists and check its dimensions and text placement.
4. Adjust optional flags if needed:
   - `--width` and `--height` (defaults: `800` and `600`)
   - `--bar-height` (default: `100`, leaving `500` px for the image area)
   - `--blur-bg` (default: `15`) and `--blur-final` (default: `0.5`)
   - `--font` and `--font-size` (default: `45`)
   - `--text-x` and `--text-y` (defaults: centered horizontally or `200`, `520`)

## Gotchas

- **Font availability across OSes**: `arial.ttf` is standard on Windows, but Linux environments often lack it. The bundled script automatically falls back to `DejaVuSans.ttf` or Pillow's default font if the requested font file is missing.
- **RGB conversion**: Always convert input images (especially PNGs with transparency) to `RGB` before pasting or saving as `.jpg`, otherwise Pillow raises an `OSError: cannot write mode RGBA as JPEG`.
- **Text centering**: Fixed `x` coordinates like `200` only center short titles. Pass `--center-text` when generating postcards with varying title lengths.
