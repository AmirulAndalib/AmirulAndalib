"""Fail the publish step when any card is missing, broken, or shows an error message.

The old metrics setup passed CI for months while its SVG was full of error boxes. A green
run has to mean the cards actually render.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

STEMS = (
    "stats",
    "languages",
    "streak",
    "productive-time",
    "repos-per-language",
    "commit-language",
    "contributions-3d",
    "snake",
    "repos",
    "trophy",
    "activity",
    "star-history",
    "wakatime",
    "steam",
)
# Cards whose API keys only exist as GitHub secrets. A local publish may skip them with
# --allow-missing; CI never passes that flag, so they stay required there.
SECRET_STEMS = {"wakatime", "steam"}
MIN_BYTES = 300
ERROR_TEXT = re.compile(
    r"something went wrong|could not|rate limit|bad credentials|not found|unknown error|error",
    re.IGNORECASE,
)


def problems_in(path: Path) -> list[str]:
    if not path.is_file():
        return ["missing"]
    if path.stat().st_size < MIN_BYTES:
        return [f"only {path.stat().st_size} bytes"]
    raw = path.read_bytes()
    # No card needs a DTD; refusing entity declarations keeps the stdlib parser safe.
    if b"<!ENTITY" in raw:
        return ["contains an XML entity declaration"]
    # Some cards come from code installed without a lockfile; refuse anything active.
    lowered = raw.lower()
    for marker in (b"<script", b"javascript:", b"<foreignobject"):
        if marker in lowered:
            return [f"contains {marker.decode()}"]
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"not valid XML ({exc})"]
    if not root.tag.endswith("svg"):
        return [f"root element is {root.tag}, not svg"]
    words = " ".join(
        " ".join(node.itertext())
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] in {"text", "tspan"}
    )
    match = ERROR_TEXT.search(words)
    return (
        [
            f"contains error text near '{words[max(0, match.start() - 30) : match.end() + 30].strip()}'"
        ]
        if match
        else []
    )


def main() -> int:
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    allow_missing = "--allow-missing" in sys.argv
    if "--list" in sys.argv:
        # The exact file names the publish step may copy; anything else stays behind.
        for stem in STEMS:
            print(f"{stem}-light.svg\n{stem}-dark.svg")
        return 0
    out_dir = Path(args[0] if args else "dist")
    failures = checked = 0
    for stem in STEMS:
        for variant in ("light", "dark"):
            path = out_dir / f"{stem}-{variant}.svg"
            if allow_missing and stem in SECRET_STEMS and not path.exists():
                print(f"{path.name:32} skipped (needs a GitHub secret)")
                continue
            issues = problems_in(path)
            status = "ok" if not issues else "FAIL " + "; ".join(issues)
            print(f"{path.name:32} {status}")
            failures += bool(issues)
            checked += 1
    if failures:
        print(f"{failures} card(s) failed validation", file=sys.stderr)
        return 1
    print(f"all {checked} cards valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
