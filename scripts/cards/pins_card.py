"""Render one pin card per featured repository: pin-<name>-light.svg and pin-<name>-dark.svg.

Reads GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER.
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from common import CardError, Palette, card, post_json, row, text, truncate, write_cards
from repos_card import LANGUAGE_COLOURS, ago

PINNED = (
    "gl-inet-mt6000-auto-snapshot",
    "asus-nuc16pro-cachyos-server-edge-kernel",
    "nvpi-r-auto",
    "mvolt-scoop",
    "TL-GD",
    "Tor-Toolkit",
    "GdriveTools",
    "MLTB-ALPINE-DOCKER",
)
QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name description stargazerCount forkCount pushedAt isArchived
    primaryLanguage { name }
    latestRelease { tagName }
  }
}
"""
HEIGHT = 120


def fetch(owner: str, token: str) -> list[dict]:
    if not token:
        raise CardError("GITHUB_TOKEN is required for the GraphQL API")
    repos = []
    for name in PINNED:
        response = post_json(
            "https://api.github.com/graphql",
            {"query": QUERY, "variables": {"owner": owner, "name": name}},
            {"Authorization": f"Bearer {token}"},
        )
        if response.get("errors") or not response.get("data", {}).get("repository"):
            raise CardError(f"could not read {owner}/{name}: {response.get('errors')}")
        repos.append(response["data"]["repository"])
    return repos


def render(repo: dict, now: datetime, palette: Palette) -> str:
    title = truncate(repo["name"], 44)
    status = (
        "Archived" if repo["isArchived"] else f"Updated {ago(repo['pushedAt'], now)}"
    )
    lines = [
        text(24, 34, title, size=14, weight=600, fill=palette.accent),
        text(471, 34, status, size=11, fill=palette.muted, anchor="end"),
        text(
            24,
            60,
            truncate(repo.get("description") or "", 70),
            size=12,
            fill=palette.muted,
        ),
    ]
    x = 24
    language = (repo.get("primaryLanguage") or {}).get("name")
    if language:
        lines.append(
            f'<circle cx="{x + 5}" cy="{91}" r="5" fill="{LANGUAGE_COLOURS.get(language, palette.muted)}"/>'
        )
        lines.append(text(x + 15, 95, language, size=12, fill=palette.muted))
        x += 15 + len(language) * 7 + 18
    for label, value in (
        ("stars", repo["stargazerCount"]),
        ("forks", repo["forkCount"]),
    ):
        lines.append(text(x, 95, f"{value:,} {label}", size=12, fill=palette.muted))
        x += len(f"{value:,} {label}") * 7 + 18
    if repo.get("latestRelease"):
        lines.append(
            text(
                x,
                95,
                truncate(repo["latestRelease"]["tagName"], 28),
                size=12,
                fill=palette.muted,
            )
        )
    return card(HEIGHT, f"{repo['name']} repository", row("".join(lines), 0), palette)


def main() -> int:
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "").strip()
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    try:
        repos = fetch(owner, os.environ.get("GITHUB_TOKEN", "").strip())
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    now = datetime.now(UTC)
    for repo in repos:
        write_cards(
            f"pin-{repo['name']}",
            lambda palette, repo=repo: render(repo, now, palette),
            out_dir,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
