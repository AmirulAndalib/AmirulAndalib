"""Render the coding-time card from the WakaTime API.

Reads a personal OAuth token from WAKATIME_TOKEN, or falls back to the public stats of
WAKATIME_USER, and writes wakatime-light.svg and wakatime-dark.svg.
Editors are listed as WakaTime reports them, so time sent by the Claude Code plugin shows
up next to the regular editors.
"""

from __future__ import annotations

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
    row,
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


def fetch(token: str, username: str) -> tuple[dict, str, dict]:
    # WakaTime no longer accepts plugin API keys for reads. Use a personal OAuth token
    # (https://wakatime.com/oauth) when given; otherwise read the user's public stats.
    if token:
        base, headers = API, {"Authorization": f"Bearer {token}"}
    elif username:
        base, headers = f"https://wakatime.com/api/v1/users/{username}", {}
    else:
        raise CardError("set WAKATIME_TOKEN (OAuth) or WAKATIME_USER (public stats)")
    for slug, label in RANGES:
        try:
            stats = _stats_when_ready(f"{base}/stats/{slug}", headers)
        except CardError as exc:
            if "HTTP 402" in str(exc) or "HTTP 403" in str(exc):
                print(f"note: {slug} refused ({exc}), trying a shorter range")
                continue
            raise
        all_time = get_json(f"{base}/all_time_since_today", headers)["data"]
        return stats, label, all_time
    raise CardError(
        "WakaTime refused every range; use an OAuth token or make stats public"
    )


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
    for index, item in enumerate(rows):
        delay = 0.15 + index * 0.08
        content = (
            text(PAD, y, truncate(item["name"], 18), fill=palette.fg)
            + bar(170, y - 9, 205, item["total_seconds"] / total, palette, delay)
            + text(
                WIDTH - PAD,
                y,
                fmt_duration(item["total_seconds"]),
                size=12,
                fill=palette.muted,
                anchor="end",
            )
        )
        parts.append(row(content, index))
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
    token = os.environ.get("WAKATIME_TOKEN", "").strip()
    username = os.environ.get("WAKATIME_USER", "").strip()
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    try:
        stats, label, all_time = fetch(token, username)
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_cards(
        "wakatime", lambda palette: render(stats, label, all_time, palette), out_dir
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
