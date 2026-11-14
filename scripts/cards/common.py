"""Shared pieces for the profile card generators: palettes, HTTP, and SVG output.

Only the standard library is used so the workflow needs no dependency install.
"""

from __future__ import annotations

import base64
import json
import re
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape


@dataclass(frozen=True)
class Palette:
    name: str
    bg: str
    border: str
    fg: str
    muted: str
    accent: str
    track: str


# GitHub Primer default light and dark themes, so the cards sit on the profile page
# without looking like third-party widgets.
LIGHT = Palette(
    "light", "#ffffff", "#d1d9e0", "#1f2328", "#59636e", "#0969da", "#eff2f5"
)
DARK = Palette("dark", "#0d1117", "#3d444d", "#f0f6fc", "#9198a1", "#4493f8", "#262c36")
PALETTES = (LIGHT, DARK)

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
WIDTH = 495
PAD = 24
USER_AGENT = (
    "AmirulAndalib-profile-cards/1.0 (+https://github.com/AmirulAndalib/AmirulAndalib)"
)
RETRYABLE = {429, 500, 502, 503, 504}


class CardError(RuntimeError):
    """A card cannot be rendered truthfully. The workflow must fail rather than publish it."""


def _redact(url: str) -> str:
    return re.sub(r"(key=)[^&]+", r"\1***", url)


def http_get(
    url: str,
    headers: dict[str, str] | None = None,
    *,
    timeout: float = 20,
    attempts: int = 3,
    data: bytes | None = None,
) -> bytes:
    method = "POST" if data is not None else "GET"
    request = urllib.request.Request(
        url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})}
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code in RETRYABLE and attempt < attempts:
                time.sleep(2**attempt)
                continue
            raise CardError(
                f"{method} {_redact(url)} failed with HTTP {exc.code}"
            ) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < attempts:
                time.sleep(2**attempt)
                continue
            raise CardError(f"{method} {_redact(url)} failed: {exc}") from exc
    raise AssertionError("unreachable")


def get_json(url: str, headers: dict[str, str] | None = None) -> dict:
    return json.loads(http_get(url, headers))


def post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    body = json.dumps(payload).encode()
    merged = {"Content-Type": "application/json", **(headers or {})}
    return json.loads(http_get(url, merged, data=body))


def data_uri(url: str, mime: str = "image/jpeg") -> str | None:
    """Inline a remote image. GitHub shows SVGs through <img>, which never loads external URLs."""
    try:
        payload = http_get(url, timeout=15, attempts=2)
    except CardError as exc:
        print(f"warning: image skipped, {exc}")
        return None
    return f"data:{mime};base64,{base64.b64encode(payload).decode('ascii')}"


def truncate(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def fmt_duration(seconds: float) -> str:
    minutes = round(seconds / 60)
    hours, minutes = divmod(minutes, 60)
    if hours and minutes:
        return f"{hours:,}h {minutes}m"
    if hours:
        return f"{hours:,}h"
    return f"{minutes}m"


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 13,
    fill: str,
    weight: int = 400,
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x:g}" y="{y:g}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def bar(
    x: float,
    y: float,
    width: float,
    fraction: float,
    palette: Palette,
    delay: float = 0,
) -> str:
    fill = max(0.0, min(1.0, fraction)) * width
    parts = [
        f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="8" rx="4" fill="{palette.track}"/>'
    ]
    if fill >= 1:
        parts.append(
            f'<rect class="grow" style="animation-delay:{delay:.2f}s" x="{x:g}" y="{y:g}" '
            f'width="{max(fill, 8):.1f}" height="8" rx="4" fill="{palette.accent}"/>'
        )
    return "".join(parts)


def row(content: str, index: int) -> str:
    """Wrap one list row so rows fade in one after another."""
    return f'<g class="row" style="animation-delay:{0.15 + index * 0.08:.2f}s">{content}</g>'


# Rows fade in and bars grow from the left. Viewers who ask for reduced motion get the
# finished card immediately.
ANIMATION_CSS = (
    "<style>"
    ".row{opacity:0;animation:fade .45s ease-out forwards}"
    ".grow{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);"
    "animation:grow .9s cubic-bezier(.2,.7,.2,1) forwards}"
    "@keyframes fade{to{opacity:1}}@keyframes grow{to{transform:scaleX(1)}}"
    "@media (prefers-reduced-motion:reduce){.row,.grow{animation:none;opacity:1;transform:none}}"
    "</style>"
)


def divider(y: float, palette: Palette) -> str:
    return f'<line x1="{PAD}" y1="{y:g}" x2="{WIDTH - PAD}" y2="{y:g}" stroke="{palette.border}" stroke-width="1"/>'


def card(height: float, label: str, body: str, palette: Palette, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height:g}" '
        f'viewBox="0 0 {WIDTH} {height:g}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>{ANIMATION_CSS}"
        f"{f'<defs>{defs}</defs>' if defs else ''}"
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1:g}" rx="6" '
        f'fill="{palette.bg}" stroke="{palette.border}"/>'
        f'<g font-family="{FONT}">{body}</g></svg>\n'
    )


def write_cards(stem: str, render: Callable[[Palette], str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for palette in PALETTES:
        path = out_dir / f"{stem}-{palette.name}.svg"
        path.write_text(render(palette), encoding="utf-8", newline="\n")
        print(f"wrote {path} ({path.stat().st_size:,} bytes)")
