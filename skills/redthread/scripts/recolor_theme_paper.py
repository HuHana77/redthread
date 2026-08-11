from __future__ import annotations

import argparse
import math
from pathlib import Path


PAPER = (
    Path(__file__).resolve().parent.parent
    / "assets/paper/theme-fiber-paper.jpg"
)


def load_python_image_backend() -> None:
    global Image, ImageStat
    try:
        from PIL import Image as pillow_image
        from PIL import ImageStat as pillow_stat
    except ImportError as exc:  # pragma: no cover - depends on selected backend
        raise SystemExit("Selected Python image backend is unavailable") from exc
    Image = pillow_image
    ImageStat = pillow_stat


def parse_color(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) != 6:
        raise argparse.ArgumentTypeError("color must use #RRGGBB")
    try:
        return tuple(int(text[index:index + 2], 16) for index in range(0, 6, 2))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color must use hexadecimal digits") from exc


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (math.ceil(image.width * scale), math.ceil(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def recolor(image: Image.Image, target_rgb: tuple[int, int, int]) -> Image.Image:
    """Map the fixed paper to the theme without requiring NumPy."""
    source = image.convert("RGB")
    source_mean = ImageStat.Stat(source).mean
    mean_luminance = (
        0.2126 * source_mean[0]
        + 0.7152 * source_mean[1]
        + 0.0722 * source_mean[2]
    )
    channel_corrections = tuple(
        -(channel_mean - mean_luminance) * 0.08 for channel_mean in source_mean
    )
    raw = source.tobytes()
    output = bytearray(len(raw))
    for offset in range(0, len(raw), 3):
        red, green, blue = raw[offset], raw[offset + 1], raw[offset + 2]
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        detail = (luminance - mean_luminance) * 0.72
        for channel, value in enumerate((red, green, blue)):
            mapped = (
                target_rgb[channel]
                + detail
                + (value - luminance) * 0.08
                + channel_corrections[channel]
            )
            output[offset + channel] = max(0, min(255, int(mapped)))
    return Image.frombytes("RGB", source.size, bytes(output))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recolor the Skill's mandatory lower-panel paper to a theme color."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument("--color", type=parse_color, required=True)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    args = parser.parse_args()
    load_python_image_backend()
    if args.width <= 0 or args.height <= 0:
        parser.error("width and height must be positive")
    if not PAPER.is_file():
        raise FileNotFoundError(f"Required fixed paper asset is missing: {PAPER}")

    result = recolor(cover_crop(Image.open(PAPER), args.width, args.height), args.color)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output)
    mean = ImageStat.Stat(result).mean
    print(
        f"paper={PAPER} output={args.output} size={result.width}x{result.height} "
        f"mean={tuple(round(float(value), 2) for value in mean)}"
    )


if __name__ == "__main__":
    main()
