"""Render the coding-time card from the WakaTime API.

Reads the API key from WAKATIME_API_KEY and writes wakatime-light.svg and wakatime-dark.svg.
Editors are listed as WakaTime reports them, so time sent by the Claude Code plugin shows
up next to the regular editors.
"""

from __future__ import annotations

import base64
import os
import sys
import time
from pathlib import Path

from common import (
    PAD,
    WIDTH,
    CardError,
    Palette,
    bar,
    card,
    divider,
    fmt_duration,
    get_json,
    text,
    truncate,
    write_cards,
)

API = "https://wakatime.com/api/v1/users/current"
# Free WakaTime accounts may not expose 30 days of history; fall back instead of failing.
RANGES = (("last_30_days", "Last 30 days"), ("last_7_days", "Last 7 days"))
ROW = 24
LANGUAGE_ROWS = 6
EDITOR_ROWS = 4


def fetch(api_key: str) -> tuple[dict, str, dict]:
    token = base64.b64encode(api_key.encode()).decode()
    headers = {"Authorization": f"Basic {token}"}
    for slug, label in RANGES:
        try:
            stats = _stats_when_ready(f"{API}/stats/{slug}", headers)
        except CardError as exc:
            if "HTTP 402" in str(exc) or "HTTP 403" in str(exc):
                print(
                    f"note: {slug} is not available on this plan, trying a shorter range"
                )
                continue
            raise
        all_time = get_json(f"{API}/all_time_since_today", headers)["data"]
        return stats, label, all_time
    raise CardError("WakaTime returned no usable stats range")


def _stats_when_ready(url: str, headers: dict[str, str]) -> dict:
    # WakaTime computes stats in the background and answers with is_up_to_date=false meanwhile.
    for _ in range(6):
        data = get_json(url, headers)["data"]
        if data.get("is_up_to_date", True):
            return data
        time.sleep(10)
    raise CardError("WakaTime stats were still being computed after 60 seconds")


def _section(
    title: str, rows: list[dict], total: float, top: float, palette: Palette
) -> tuple[str, float]:
    parts = [text(PAD, top, title, size=12, weight=600, fill=palette.muted)]
    y = top + 24
    for row in rows:
        parts.append(text(PAD, y, truncate(row["name"], 18), fill=palette.fg))
        parts.append(bar(170, y - 9, 205, row["total_seconds"] / total, palette))
        parts.append(
            text(
                WIDTH - PAD,
                y,
                fmt_duration(row["total_seconds"]),
                size=12,
                fill=palette.muted,
                anchor="end",
            )
        )
        y += ROW
    return "".join(parts), y


def render(stats: dict, range_label: str, all_time: dict, palette: Palette) -> str:
    total = stats.get("total_seconds", 0) or 0
    daily = stats.get("daily_average", 0) or 0
    body = [
        text(PAD, 34, "Coding time", size=15, weight=600, fill=palette.fg),
        text(WIDTH - PAD, 34, range_label, size=12, fill=palette.muted, anchor="end"),
    ]
    columns = (
        (fmt_duration(total), "Total"),
        (fmt_duration(daily), "Daily average"),
        (fmt_duration(all_time.get("total_seconds", 0) or 0), "Since tracking began"),
    )
    for index, (value, label) in enumerate(columns):
        x = PAD + index * 152
        body.append(text(x, 70, value, size=18, weight=600, fill=palette.fg))
        body.append(text(x, 88, label, size=12, fill=palette.muted))
    body.append(divider(106, palette))

    languages = [row for row in stats.get("languages", []) if row.get("total_seconds")][
        :LANGUAGE_ROWS
    ]
    editors = [row for row in stats.get("editors", []) if row.get("total_seconds")][
        :EDITOR_ROWS
    ]
    if not total or not languages:
        body.append(
            text(
                PAD,
                136,
                "No coding activity recorded in this range.",
                fill=palette.muted,
            )
        )
        return card(160, "WakaTime coding time", "".join(body), palette)

    section, y = _section("Languages", languages, total, 134, palette)
    body.append(section)
    if editors:
        section, y = _section("Editors", editors, total, y + 6, palette)
        body.append(section)
    return card(y + 6, "WakaTime coding time", "".join(body), palette)


def main() -> int:
    api_key = os.environ.get("WAKATIME_API_KEY", "").strip()
    if not api_key:
        print("error: WAKATIME_API_KEY is not set", file=sys.stderr)
        return 1
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    try:
        stats, label, all_time = fetch(api_key)
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_cards(
        "wakatime", lambda palette: render(stats, label, all_time, palette), out_dir
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
