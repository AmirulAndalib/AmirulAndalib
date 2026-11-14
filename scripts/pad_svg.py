"""Grow an SVG card to a target height so paired cards in the README line up exactly.

    python scripts/pad_svg.py HEIGHT file.svg [file.svg ...]

Only the outer height and viewBox change; cards drawn with percentage backgrounds (as the
stats card is) stretch to fill, and the extra space lands at the bottom.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def pad(path: Path, height: int) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', text)
    if not match:
        raise SystemExit(f"{path}: no viewBox to adjust")
    width, current = match.group(1), float(match.group(2))
    if current >= height:
        print(f"{path.name}: already {current:g}px")
        return
    text = text.replace(match.group(0), f'viewBox="0 0 {width} {height}"', 1)
    text = re.sub(
        r'(<svg[^>]*?\sheight=")[\d.]+(")', rf"\g<1>{height}\2", text, count=1
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"{path.name}: {current:g}px -> {height}px")


def main() -> None:
    height = int(sys.argv[1])
    for name in sys.argv[2:]:
        pad(Path(name), height)


if __name__ == "__main__":
    main()
