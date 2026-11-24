#!/usr/bin/env python3
"""Generate a stylized photo postcard with a blurred backdrop and caption bar."""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


def load_font(font_path: str, size: int) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    candidates = [
        font_path,
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_postcard(
    input_path: str,
    output_path: str,
    text: str = "Aespa Winter",
    color: str = "violet",
    width: int = 800,
    height: int = 600,
    bar_height: int = 100,
    blur_bg: float = 15.0,
    blur_final: float = 0.5,
    font_path: str = "arial.ttf",
    font_size: int = 45,
    text_x: int | None = None,
    text_y: int | None = None,
    center_text: bool = False,
) -> Path:
    img = Image.open(input_path).convert("RGB")
    panel_height = height - bar_height

    # Blurred background
    bg = ImageOps.fit(img, (width, panel_height))
    bg = bg.filter(ImageFilter.GaussianBlur(blur_bg))

    # Scaled foreground centered on the blurred backdrop
    fg = img.copy()
    fg.thumbnail((width - 40, panel_height - 10))
    bg.paste(fg, ((width - fg.width) // 2, (panel_height - fg.height) // 2))

    # Composite onto black canvas
    result = Image.new("RGB", (width, height), "black")
    result.paste(bg, (0, 0))

    # Draw caption text
    draw = ImageDraw.Draw(result)
    font = load_font(font_path, font_size)
    y = text_y if text_y is not None else panel_height + 20

    if center_text or text_x is None:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
    else:
        x = text_x

    draw.text((x, y), text, fill=color, font=font)

    # Subtle overall soft-focus finish
    if blur_final > 0:
        result = result.filter(ImageFilter.GaussianBlur(blur_final))

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.save(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a stylized photo postcard.")
    parser.add_argument("--input", required=True, help="Path to the source image.")
    parser.add_argument("--output", default="postcard.jpg", help="Output image path.")
    parser.add_argument("--text", default="Aespa Winter", help="Caption text.")
    parser.add_argument("--color", default="violet", help="Caption text color.")
    parser.add_argument("--width", type=int, default=800, help="Canvas width in pixels.")
    parser.add_argument("--height", type=int, default=600, help="Canvas height in pixels.")
    parser.add_argument("--bar-height", type=int, default=100, help="Bottom black bar height.")
    parser.add_argument("--blur-bg", type=float, default=15.0, help="Background Gaussian blur radius.")
    parser.add_argument("--blur-final", type=float, default=0.5, help="Final Gaussian blur radius.")
    parser.add_argument("--font", default="arial.ttf", help="Path or name of TrueType font.")
    parser.add_argument("--font-size", type=int, default=45, help="Caption font size.")
    parser.add_argument("--text-x", type=int, default=None, help="Caption X coordinate (auto-centered if omitted).")
    parser.add_argument("--text-y", type=int, default=None, help="Caption Y coordinate.")
    parser.add_argument("--center-text", action="store_true", help="Center caption horizontally.")
    args = parser.parse_args()

    out = create_postcard(
        input_path=args.input,
        output_path=args.output,
        text=args.text,
        color=args.color,
        width=args.width,
        height=args.height,
        bar_height=args.bar_height,
        blur_bg=args.blur_bg,
        blur_final=args.blur_final,
        font_path=args.font,
        font_size=args.font_size,
        text_x=args.text_x,
        text_y=args.text_y,
        center_text=args.center_text,
    )
    print(f"Postcard saved to: {out}")


if __name__ == "__main__":
    main()
