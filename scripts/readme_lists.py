"""Refresh the auto-updated lists in README.md: recent releases and merged upstream PRs.

Each list lives between <!-- NAME:START --> and <!-- NAME:END --> markers. Reads
GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER. Run from anywhere:
    python scripts/readme_lists.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
LIMIT = 6

RELEASES = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 50, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes { name url releases(first: 1, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes { name tagName url publishedAt isPrerelease } } }
    }
  }
}
"""

MERGED = """
query($q: String!) {
  search(query: $q, type: ISSUE, first: 30) {
    nodes { ... on PullRequest { title url mergedAt additions deletions repository { nameWithOwner } } }
  }
}
"""


def graphql(query: str, variables: dict, token: str) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors'][0].get('message')}")
    return payload["data"]


def clean(value: str) -> str:
    """Keep titles from breaking the Markdown list."""
    return re.sub(r"[\[\]\|<>`*_]", "", value).strip()


def releases(login: str, token: str) -> list[str]:
    rows = []
    for repo in graphql(RELEASES, {"login": login}, token)["user"]["repositories"][
        "nodes"
    ]:
        for rel in repo["releases"]["nodes"]:
            rows.append((rel["publishedAt"], repo, rel))
    rows.sort(key=lambda item: item[0], reverse=True)
    lines = []
    for published, repo, rel in rows[:LIMIT]:
        label = clean(rel["name"] or rel["tagName"])
        pre = " (pre-release)" if rel["isPrerelease"] else ""
        lines.append(
            f"- [{repo['name']}]({repo['url']}): [{label}]({rel['url']}){pre}, {published[:10]}"
        )
    return lines


def merged(login: str, token: str) -> list[str]:
    query = f"author:{login} is:pr is:merged -user:{login} sort:updated-desc"
    nodes = graphql(MERGED, {"q": query}, token)["search"]["nodes"]
    nodes = sorted((n for n in nodes if n), key=lambda n: n["mergedAt"], reverse=True)
    return [
        f"- {n['repository']['nameWithOwner']}: [{clean(n['title'])}]({n['url']}), "
        f"`+{n['additions']} -{n['deletions']}`, {n['mergedAt'][:10]}"
        for n in nodes[:LIMIT]
    ]


def replace(text: str, name: str, lines: list[str]) -> str:
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    if start not in text or end not in text:
        raise SystemExit(f"README.md has no {name} markers")
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    body = "\n".join(lines) if lines else "- Nothing yet."
    return f"{head}{start}\n{body}\n{end}{tail}"


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    login = os.environ.get("GITHUB_REPOSITORY_OWNER", "AmirulAndalib")
    text = README.read_text(encoding="utf-8")
    text = replace(text, "RELEASES", releases(login, token))
    text = replace(text, "MERGED", merged(login, token))
    README.write_text(text, encoding="utf-8", newline="\n")
    print("README lists refreshed")


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
