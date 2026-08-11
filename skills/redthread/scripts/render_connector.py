#!/usr/bin/env python3
"""Render a bundled organic connector template between two canvas anchors."""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from pathlib import Path


NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
TOKEN_RE = re.compile(rf"[MC]|{NUMBER}")


def load_python_image_backend() -> None:
    global Image, ImageChops, ImageDraw, ImageFilter
    try:
        from PIL import Image as pillow_image
        from PIL import ImageChops as pillow_chops
        from PIL import ImageDraw as pillow_draw
        from PIL import ImageFilter as pillow_filter
    except ImportError as exc:  # pragma: no cover - depends on selected backend
        raise SystemExit("Selected Python image backend is unavailable") from exc
    Image = pillow_image
    ImageChops = pillow_chops
    ImageDraw = pillow_draw
    ImageFilter = pillow_filter


def parse_pair(value: str) -> tuple[float, float]:
    try:
        left, right = value.split(",", 1)
        return float(left), float(right)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("expected X,Y") from exc


def parse_color(value: str) -> tuple[int, int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) not in (6, 8):
        raise argparse.ArgumentTypeError("color must be #RRGGBB or #RRGGBBAA")
    try:
        values = tuple(int(text[index : index + 2], 16) for index in range(0, len(text), 2))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid hexadecimal color") from exc
    return values + (255,) if len(values) == 3 else values


def parse_path(path_text: str) -> tuple[tuple[float, float], list[tuple[float, ...]]]:
    tokens = TOKEN_RE.findall(path_text)
    if len(tokens) < 10 or tokens[0] != "M":
        raise ValueError("template path must start with M and contain C segments")
    cursor = 1
    start = (float(tokens[cursor]), float(tokens[cursor + 1]))
    cursor += 2
    segments: list[tuple[float, ...]] = []
    while cursor < len(tokens):
        if tokens[cursor] != "C" or cursor + 6 >= len(tokens):
            raise ValueError("only absolute M and C SVG commands are supported")
        cursor += 1
        segment = tuple(float(tokens[cursor + offset]) for offset in range(6))
        segments.append(segment)
        cursor += 6
    return start, segments


def cubic_point(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    t: float,
) -> tuple[float, float]:
    u = 1.0 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def sample_path(path_text: str, steps_per_segment: int = 42) -> list[tuple[float, float]]:
    start, segments = parse_path(path_text)
    points = [start]
    current = start
    for segment in segments:
        control1 = (segment[0], segment[1])
        control2 = (segment[2], segment[3])
        endpoint = (segment[4], segment[5])
        for step in range(1, steps_per_segment + 1):
            points.append(cubic_point(current, control1, control2, endpoint, step / steps_per_segment))
        current = endpoint
    if len(points) < 20:
        raise ValueError("template path is too short")
    return points


def normalize_template(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Make both authored endpoints land exactly on the normalized anchor axis."""
    start_x, start_y = points[0]
    end_x, end_y = points[-1]
    span_y = end_y - start_y
    if abs(span_y) < 1e-8:
        raise ValueError("template endpoints must have different y coordinates")
    normalized = []
    for x, y in points:
        along = (y - start_y) / span_y
        axis_x = start_x + (end_x - start_x) * along
        normalized.append((x - axis_x, along))
    return normalized


def map_to_anchors(
    points: list[tuple[float, float]],
    start: tuple[float, float],
    end: tuple[float, float],
    spread: float,
    mirror: bool,
) -> list[tuple[float, float]]:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.hypot(dx, dy)
    if distance < 24:
        raise ValueError("connector anchors must be at least 24 pixels apart")
    along = (dx / distance, dy / distance)
    perpendicular = (-along[1], along[0])
    direction = -1.0 if mirror else 1.0
    mapped = []
    for x, y in points:
        cross = x * spread * direction * distance
        mapped.append(
            (
                start[0] + along[0] * y * distance + perpendicular[0] * cross,
                start[1] + along[1] * y * distance + perpendicular[1] * cross,
            )
        )
    mapped[0] = start
    mapped[-1] = end
    return mapped


def cumulative_lengths(points: list[tuple[float, float]]) -> tuple[list[float], float]:
    lengths = [0.0]
    for first, second in zip(points, points[1:]):
        lengths.append(lengths[-1] + math.hypot(second[0] - first[0], second[1] - first[1]))
    return lengths, lengths[-1]


def offset_path(
    points: list[tuple[float, float]], amplitude: float, phase: float
) -> list[tuple[float, float]]:
    """Create one faint, slowly wandering pencil fiber beside the centerline."""
    lengths, total_length = cumulative_lengths(points)
    if total_length <= 0:
        return points
    offset = []
    last = len(points) - 1
    for index, (x, y) in enumerate(points):
        before = points[max(0, index - 2)]
        after = points[min(last, index + 2)]
        dx = after[0] - before[0]
        dy = after[1] - before[1]
        magnitude = math.hypot(dx, dy) or 1.0
        normal = (-dy / magnitude, dx / magnitude)
        t = lengths[index] / total_length
        wander = 0.62 * math.sin(2 * math.pi * (2.35 * t + phase))
        wander += 0.38 * math.sin(2 * math.pi * (7.1 * t + phase * 0.43))
        endpoint_fade = math.sin(math.pi * t) ** 0.45
        distance = amplitude * wander * endpoint_fade
        offset.append((x + normal[0] * distance, y + normal[1] * distance))
    offset[0] = points[0]
    offset[-1] = points[-1]
    return offset


def draw_variable_stroke(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    stroke_width: float,
    scale: int,
    fill: int,
    width_scale: float,
    pressure_phase: float,
) -> None:
    lengths, total_length = cumulative_lengths(points)
    if total_length <= 0:
        raise ValueError("connector path has zero length")
    scaled = [(x * scale, y * scale) for x, y in points]
    start_radius = stroke_width * width_scale * scale * 0.68 * 0.5
    draw.ellipse(
        (
            scaled[0][0] - start_radius,
            scaled[0][1] - start_radius,
            scaled[0][0] + start_radius,
            scaled[0][1] + start_radius,
        ),
        fill=fill,
    )
    for index in range(len(scaled) - 1):
        t = ((lengths[index] + lengths[index + 1]) * 0.5) / total_length
        pressure = 1.0 + 0.090 * math.sin(2 * math.pi * (1.30 * t + pressure_phase))
        pressure += 0.042 * math.sin(2 * math.pi * (3.70 * t + pressure_phase * 0.61))
        pressure += 0.020 * math.sin(2 * math.pi * (17.0 * t + pressure_phase * 1.37))
        endpoint_taper = min(1.0, 0.68 + min(t, 1.0 - t) / 0.026 * 0.32)
        radius = max(
            0.70,
            stroke_width * width_scale * scale * pressure * endpoint_taper * 0.5,
        )
        line_width = max(1, int(round(radius * 2)))
        first = scaled[index]
        second = scaled[index + 1]
        draw.line((first, second), fill=fill, width=line_width)
        draw.ellipse(
            (second[0] - radius, second[1] - radius, second[0] + radius, second[1] + radius),
            fill=fill,
        )


def random_bytes(rng: random.Random, count: int) -> bytes:
    if hasattr(rng, "randbytes"):
        return rng.randbytes(count)
    return bytes(rng.getrandbits(8) for _ in range(count))


def apply_pencil_grain(
    alpha: Image.Image, seed: int, texture_strength: float
) -> Image.Image:
    if texture_strength <= 0:
        return alpha
    width, height = alpha.size
    rng = random.Random(f"pencil-grain:{seed}:{width}x{height}")

    micro = Image.frombytes("L", alpha.size, random_bytes(rng, width * height))
    micro = micro.filter(ImageFilter.GaussianBlur(0.22))
    micro_floor = round(255 - 88 * texture_strength)
    micro = micro.point(
        lambda value: micro_floor + round((255 - micro_floor) * value / 255)
    )

    coarse_size = (max(2, width // 12), max(2, height // 12))
    coarse = Image.frombytes(
        "L", coarse_size, random_bytes(rng, coarse_size[0] * coarse_size[1])
    ).resize(alpha.size, Image.Resampling.BICUBIC)
    coarse_floor = round(255 - 34 * texture_strength)
    coarse = coarse.point(
        lambda value: coarse_floor + round((255 - coarse_floor) * value / 255)
    )

    grain = ImageChops.multiply(micro, coarse)
    speckles = Image.frombytes("L", alpha.size, random_bytes(rng, width * height))
    threshold = round(4 + 12 * texture_strength)
    speckles = speckles.point(lambda value: 135 if value < threshold else 255)
    grain = ImageChops.multiply(grain, speckles)
    return ImageChops.multiply(alpha, grain)


def load_protected_mask(path: Path, size: tuple[int, int], stroke_width: float) -> Image.Image:
    with Image.open(path) as source:
        if source.size != size:
            raise ValueError(f"avoid mask must be {size[0]}x{size[1]}, got {source.width}x{source.height}")
        rgba = source.convert("RGBA")
    luminance = rgba.convert("L")
    alpha = rgba.getchannel("A")
    protected = ImageChops.multiply(luminance, alpha)
    radius = max(1, int(math.ceil(stroke_width * 1.5)))
    kernel = min(51, radius * 2 + 1)
    if kernel % 2 == 0:
        kernel += 1
    return protected.filter(ImageFilter.MaxFilter(kernel))


def candidate_score(
    points: list[tuple[float, float]],
    canvas: tuple[int, int],
    margin: float,
    protected: Image.Image | None,
) -> tuple[float, float]:
    width, height = canvas
    outside = 0.0
    collision = 0.0
    total = max(1, len(points) - 1)
    pixels = protected.load() if protected is not None else None
    for index, (x, y) in enumerate(points):
        outside += max(0.0, margin - x, x - (width - margin), margin - y, y - (height - margin))
        fraction = index / total
        if pixels is not None and 0.035 < fraction < 0.965:
            px = min(width - 1, max(0, int(round(x))))
            py = min(height - 1, max(0, int(round(y))))
            collision += pixels[px, py] / 255.0
    return outside, collision


def choose_candidate(
    templates: list[dict],
    requested_template: str,
    mirror_mode: str,
    start: tuple[float, float],
    end: tuple[float, float],
    spread: float,
    canvas: tuple[int, int],
    stroke_width: float,
    protected: Image.Image | None,
    seed: int,
) -> tuple[dict, bool, list[tuple[float, float]], tuple[float, float]]:
    if requested_template != "auto":
        templates = [template for template in templates if template["id"] == requested_template]
        if not templates:
            raise ValueError(f"unknown template: {requested_template}")
    mirror_values = {"auto": (False, True), "no": (False,), "yes": (True,)}[mirror_mode]
    candidates = []
    margin = max(stroke_width * 2.0, min(canvas) * 0.012)
    for template in templates:
        normalized = normalize_template(sample_path(template["path"]))
        for mirrored in mirror_values:
            mapped = map_to_anchors(normalized, start, end, spread, mirrored)
            outside, collision = candidate_score(mapped, canvas, margin, protected)
            tie_break = random.Random(f"{seed}:{template['id']}:{int(mirrored)}").random()
            candidates.append((outside, collision, tie_break, template, mirrored, mapped))
    candidates.sort(key=lambda item: (item[0] > 0, item[0], item[1], item[2]))
    best = candidates[0]
    return best[3], best[4], best[5], (best[0], best[1])


def render_mask(
    points: list[tuple[float, float]],
    canvas: tuple[int, int],
    stroke_width: float,
    supersample: int,
    seed: int,
    texture_strength: float,
) -> Image.Image:
    scale = supersample
    high_size = (canvas[0] * scale, canvas[1] * scale)
    mask = Image.new("L", high_size, 0)
    draw = ImageDraw.Draw(mask)
    phase = random.Random(f"pressure:{seed}").random()

    fiber_a = offset_path(points, stroke_width * 0.46, phase + 0.17)
    fiber_b = offset_path(points, -stroke_width * 0.39, phase + 0.63)
    draw_variable_stroke(draw, fiber_a, stroke_width, scale, 105, 0.28, phase + 0.23)
    draw_variable_stroke(draw, fiber_b, stroke_width, scale, 82, 0.22, phase + 0.71)
    draw_variable_stroke(draw, points, stroke_width, scale, 232, 1.0, phase)

    alpha = mask.resize(canvas, Image.Resampling.LANCZOS)
    return apply_pencil_grain(alpha, seed, texture_strength)


def load_templates(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    templates = payload.get("templates")
    if payload.get("version") != 1 or not isinstance(templates, list) or len(templates) < 12:
        raise ValueError("connector template library is incomplete")
    identifiers = set()
    for template in templates:
        identifier = template.get("id")
        if not isinstance(identifier, str) or identifier in identifiers or "path" not in template:
            raise ValueError("connector template library contains an invalid entry")
        identifiers.add(identifier)
        normalize_template(sample_path(template["path"], steps_per_segment=6))
    return templates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="transparent RGBA PNG output")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--start", type=parse_pair, required=True, metavar="X,Y")
    parser.add_argument("--end", type=parse_pair, required=True, metavar="X,Y")
    parser.add_argument("--color", type=parse_color, required=True, metavar="#RRGGBB")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--template", default="auto", help="auto or a bundled template id")
    parser.add_argument("--mirror", choices=("auto", "yes", "no"), default="auto")
    parser.add_argument("--spread", type=float, default=1.0, help="cross-axis template scale")
    parser.add_argument("--stroke-width", type=float, default=None, help="final pixels")
    parser.add_argument(
        "--texture-strength",
        type=float,
        default=0.58,
        help="colored-pencil grain from 0 to 1; keep the default for this style",
    )
    parser.add_argument("--avoid-mask", type=Path)
    parser.add_argument("--supersample", type=int, default=6, choices=range(3, 9))
    parser.add_argument(
        "--templates",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "connectors" / "templates.json",
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    load_python_image_backend()
    if args.width < 64 or args.height < 64:
        raise SystemExit("canvas dimensions must be at least 64 pixels")
    if not 0.55 <= args.spread <= 1.45:
        raise SystemExit("--spread must be between 0.55 and 1.45")
    if not 0.0 <= args.texture_strength <= 1.0:
        raise SystemExit("--texture-strength must be between 0 and 1")
    canvas = (args.width, args.height)
    stroke_width = args.stroke_width or max(2.4, min(canvas) * 0.0052)
    try:
        templates = load_templates(args.templates)
        protected = (
            load_protected_mask(args.avoid_mask, canvas, stroke_width) if args.avoid_mask else None
        )
        template, mirrored, points, score = choose_candidate(
            templates,
            args.template,
            args.mirror,
            args.start,
            args.end,
            args.spread,
            canvas,
            stroke_width,
            protected,
            args.seed,
        )
        texture_seed = random.Random(f"texture:{args.seed}:{template['id']}").randrange(2**31)
        alpha = render_mask(
            points,
            canvas,
            stroke_width,
            args.supersample,
            texture_seed,
            args.texture_strength,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc

    red, green, blue, opacity = args.color
    if opacity != 255:
        alpha = alpha.point(lambda value: value * opacity // 255)
    output = Image.new("RGBA", canvas, (red, green, blue, 0))
    output.putalpha(alpha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output, format="PNG", optimize=True)
    print(
        json.dumps(
            {
                "template": template["id"],
                "mirrored": mirrored,
                "outside_score": round(score[0], 3),
                "avoid_score": round(score[1], 3),
                "stroke_style": "colored-pencil",
                "stroke_width": round(stroke_width, 3),
                "texture_strength": args.texture_strength,
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
