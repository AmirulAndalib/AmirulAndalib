"""Render the "Recently updated" card from the GitHub REST API.

Lists the owner's most recently pushed source repositories (no forks, no archives) and
writes repos-light.svg and repos-dark.svg. Reads GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER.
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from common import (
    PAD,
    WIDTH,
    CardError,
    Palette,
    card,
    divider,
    post_json,
    row,
    text,
    truncate,
    write_cards,
)

ROWS = 6
ROW = 46
# Linguist colours for the languages that appear in these repositories.
LANGUAGE_COLOURS = {
    "Python": "#3572a5",
    "Shell": "#89e051",
    "PowerShell": "#4a7ee0",
    "Dockerfile": "#5e8696",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Go": "#00add8",
    "Rust": "#dea584",
    "C": "#555555",
    "C++": "#f34b7d",
    "HTML": "#e34c26",
    "Makefile": "#427819",
}


QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 20, ownerAffiliations: OWNER, isFork: false, isArchived: false,
                 privacy: PUBLIC, orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes { name description pushedAt primaryLanguage { name } }
    }
  }
}
"""


def fetch(owner: str, token: str) -> list[dict]:
    # GraphQL filters forks on the server; the REST listing returns forks first for an
    # account with thousands of them.
    if not token:
        raise CardError("GITHUB_TOKEN is required for the GraphQL API")
    response = post_json(
        "https://api.github.com/graphql",
        {"query": QUERY, "variables": {"login": owner}},
        {"Authorization": f"Bearer {token}"},
    )
    if response.get("errors"):
        raise CardError(f"GraphQL error: {response['errors'][0].get('message')}")
    nodes = response["data"]["user"]["repositories"]["nodes"]
    picked = [
        {
            "name": node["name"],
            "description": node["description"],
            "pushed_at": node["pushedAt"],
            "language": (node["primaryLanguage"] or {}).get("name"),
        }
        for node in nodes
        if node["name"].lower() != owner.lower()
    ][:ROWS]
    if not picked:
        raise CardError(f"no source repositories found for {owner}")
    return picked


def ago(timestamp: str, now: datetime) -> str:
    then = datetime.fromisoformat(timestamp)
    days = (now - then).days
    if days < 1:
        hours = max(1, int((now - then).total_seconds() // 3600))
        return f"{hours}h ago"
    if days < 60:
        return f"{days}d ago"
    months = days // 30
    return f"{months} months ago" if months < 24 else f"{days // 365} years ago"


def render(repos: list[dict], now: datetime, palette: Palette) -> str:
    body = [
        text(PAD, 34, "Recently updated", size=15, weight=600, fill=palette.fg),
        divider(50, palette),
    ]
    for index, repo in enumerate(repos):
        top = 76 + index * ROW
        language = repo.get("language")
        line = [
            text(PAD, top, truncate(repo["name"], 44), weight=600, fill=palette.accent)
        ]
        line.append(
            text(
                WIDTH - PAD,
                top,
                ago(repo["pushed_at"], now),
                size=12,
                fill=palette.muted,
                anchor="end",
            )
        )
        description = repo.get("description") or ""
        x = PAD
        if language:
            colour = LANGUAGE_COLOURS.get(language, palette.muted)
            line.append(f'<circle cx="{x + 5}" cy="{top + 14}" r="5" fill="{colour}"/>')
            line.append(text(x + 15, top + 18, language, size=12, fill=palette.muted))
            x += 15 + len(language) * 7 + 12
        limit = int((WIDTH - PAD - x) / 6.4)
        line.append(
            text(x, top + 18, truncate(description, limit), size=12, fill=palette.muted)
        )
        body.append(row("".join(line), index))
    height = 76 + len(repos) * ROW - 12
    return card(height, "Recently updated repositories", "".join(body), palette)


def main() -> int:
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "").strip()
    if not owner:
        print("error: GITHUB_REPOSITORY_OWNER is not set", file=sys.stderr)
        return 1
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    try:
        repos = fetch(owner, os.environ.get("GITHUB_TOKEN", "").strip())
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    now = datetime.now(UTC)
    write_cards("repos", lambda palette: render(repos, now, palette), out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
