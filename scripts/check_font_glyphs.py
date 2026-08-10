#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import struct


DEFAULT_FONT = (
    Path(__file__).resolve().parent.parent
    / "assets/fonts/asobi-memogaki/AsobiMemogaki-Regular-1-02.ttf"
)


def u16(data: bytes, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def unicode_cmaps(font: Path) -> list[tuple[int, bytes]]:
    data = font.read_bytes()
    table_count = u16(data, 4)
    cmap_offset = None
    for index in range(table_count):
        record = 12 + index * 16
        if data[record : record + 4] == b"cmap":
            cmap_offset = u32(data, record + 8)
            break
    if cmap_offset is None:
        raise SystemExit("font has no cmap table")
    subtables = []
    count = u16(data, cmap_offset + 2)
    for index in range(count):
        record = cmap_offset + 4 + index * 8
        platform = u16(data, record)
        encoding = u16(data, record + 2)
        offset = cmap_offset + u32(data, record + 4)
        if platform == 0 or (platform == 3 and encoding in (1, 10)):
            subtables.append((u16(data, offset), data[offset:]))
    if not subtables:
        raise SystemExit("font has no Unicode cmap subtable")
    return subtables


def glyph4(table: bytes, codepoint: int) -> int:
    if codepoint > 0xFFFF:
        return 0
    table = table[: u16(table, 2)]
    count = u16(table, 6) // 2
    end_offset = 14
    start_offset = end_offset + count * 2 + 2
    delta_offset = start_offset + count * 2
    range_offset = delta_offset + count * 2
    for index in range(count):
        start = u16(table, start_offset + index * 2)
        end = u16(table, end_offset + index * 2)
        if start <= codepoint <= end:
            delta = u16(table, delta_offset + index * 2)
            range_value_offset = range_offset + index * 2
            range_value = u16(table, range_value_offset)
            if range_value == 0:
                return (codepoint + delta) & 0xFFFF
            glyph_offset = range_value_offset + range_value + (codepoint - start) * 2
            if glyph_offset + 2 > len(table):
                return 0
            glyph = u16(table, glyph_offset)
            return 0 if glyph == 0 else (glyph + delta) & 0xFFFF
        if codepoint < start:
            break
    return 0


def glyph12(table: bytes, codepoint: int) -> int:
    count = u32(table, 12)
    offset = 16
    for _ in range(count):
        start = u32(table, offset)
        end = u32(table, offset + 4)
        if start <= codepoint <= end:
            return u32(table, offset + 8) + codepoint - start
        if codepoint < start:
            break
        offset += 12
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Check AsobiMemogaki glyph coverage.")
    parser.add_argument("texts", nargs="+")
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT)
    args = parser.parse_args()
    cmaps = unicode_cmaps(args.font)
    missing = []
    for character in "".join(args.texts):
        if character.isspace():
            continue
        present = any(
            (fmt == 4 and glyph4(table, ord(character)))
            or (fmt == 12 and glyph12(table, ord(character)))
            for fmt, table in cmaps
        )
        if not present:
            missing.append(character)
    if missing:
        unique = "".join(dict.fromkeys(missing))
        raise SystemExit(f"missing glyphs: {unique}")
    print(f"font={args.font}")
    print("glyph coverage=ok")


if __name__ == "__main__":
    main()
