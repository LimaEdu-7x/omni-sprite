#!/usr/bin/env python3
"""Convert an ASCII grid into a JSON list of pixels for the draw_pixels tool."""
import argparse, json, sys


def convert(rows, legend, ox=0, oy=0, mirror_x=False):
    if mirror_x:
        rows = [r + r[::-1] for r in rows]
    pixels = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if ch not in legend:
                raise ValueError(f"char {ch!r} at ({x},{y}) not in legend")
            pixels.append({"x": x + ox, "y": y + oy, "color": legend[ch]})
    return pixels


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("grid")
    p.add_argument("--legend", required=True, help="JSON file: char -> #rrggbb")
    p.add_argument("--ox", type=int, default=0)
    p.add_argument("--oy", type=int, default=0)
    p.add_argument("--mirror-x", action="store_true", help="append mirrored copy of each row")
    a = p.parse_args()
    with open(a.grid, encoding="utf-8") as f:
        rows = [l.rstrip("\n") for l in f if l.strip()]
    with open(a.legend, encoding="utf-8") as f:
        legend = json.load(f)
    json.dump(convert(rows, legend, a.ox, a.oy, a.mirror_x), sys.stdout)


if __name__ == "__main__":
    # self-check
    assert convert(["a."], {"a": "#fff"}) == [{"x": 0, "y": 0, "color": "#fff"}]
    assert len(convert(["a"], {"a": "#fff"}, mirror_x=True)) == 2
    main()
