"""Render a neofetch-style terminal card from live GitHub data.

The kernel and router lines come from the latest releases of the repositories that
build them, so the card shows what the home lab actually runs today. Writes
terminal-light.svg and terminal-dark.svg. Reads GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from xml.sax.saxutils import escape

from common import CardError, Palette, post_json, write_cards

W, H = 1012, 320
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
KERNEL_REPO = "asus-nuc16pro-cachyos-server-edge-kernel"
ROUTER_REPO = "gl-inet-mt6000-auto-snapshot"
# Opacity of the 6 x 6 block "logo", the same contribution-square motif as the header.
LOGO = [
    [1.0, 0.7, 0.45, 0.25, 0.45, 0.7],
    [0.7, 1.0, 0.7, 0.45, 0.25, 0.45],
    [0.45, 0.7, 1.0, 0.7, 0.45, 0.25],
    [0.25, 0.45, 0.7, 1.0, 0.7, 0.45],
    [0.45, 0.25, 0.45, 0.7, 1.0, 0.7],
    [0.7, 0.45, 0.25, 0.45, 0.7, 1.0],
]

QUERY = """
query($login: String!, $kernel: String!, $router: String!) {
  user(login: $login) {
    login createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount nodes { stargazerCount }
    }
    kernel: repository(name: $kernel) { latestRelease { name tagName } }
    router: repository(name: $router) { latestRelease { name tagName } }
  }
  merged: search(query: "is:pr is:merged", type: ISSUE, first: 0) { issueCount }
}
"""


def fetch(login: str, token: str) -> dict:
    if not token:
        raise CardError("GITHUB_TOKEN is required for the GraphQL API")
    query = QUERY.replace(
        '"is:pr is:merged"', f'"is:pr is:merged author:{login} -user:{login}"'
    )
    response = post_json(
        "https://api.github.com/graphql",
        {
            "query": query,
            "variables": {"login": login, "kernel": KERNEL_REPO, "router": ROUTER_REPO},
        },
        {"Authorization": f"Bearer {token}"},
    )
    if response.get("errors"):
        raise CardError(f"GraphQL error: {response['errors'][0].get('message')}")
    return response["data"]


def release(repo: dict | None, pattern: str, fallback: str) -> str:
    rel = (repo or {}).get("latestRelease") or {}
    match = re.search(pattern, rel.get("name") or "")
    return match.group(0) if match else fallback


def account_age(created: str, now: datetime) -> str:
    start = datetime.fromisoformat(created)
    months = (now.year - start.year) * 12 + now.month - start.month
    return f"{months // 12} years, {months % 12} months"


def summarise(data: dict, now: datetime) -> list[tuple[str, str]]:
    user = data["user"]
    stars = sum(n["stargazerCount"] for n in user["repositories"]["nodes"])
    kernel = release(user["kernel"], r"Linux [\d.]+", "Linux (CachyOS server)")
    router = release(user["router"], r"Snapshot [\d.]+", "OpenWrt snapshot")
    return [
        ("OS", "CachyOS (Arch Linux) x86_64"),
        ("Host", "ASUS NUC 16 Pro, home lab"),
        ("Kernel", f"{kernel} CachyOS ServerMax, sched-ext"),
        ("Router", f"GL.iNet Flint 2 (GL-MT6000), {router}"),
        ("Shell", "bash, POSIX sh, PowerShell"),
        ("Uptime", f"{account_age(user['createdAt'], now)} on GitHub"),
        (
            "Repos",
            (
                f"{user['repositories']['totalCount']} public source, {stars:,} stars, "
                f"{user['followers']['totalCount']:,} followers"
            ),
        ),
        ("Upstream", f"{data['merged']['issueCount']} pull requests merged"),
        ("Stack", "Docker, GitHub Actions, OpenWrt, Cloudflare"),
        ("Locale", "Auckland, New Zealand (Pacific/Auckland)"),
    ]


def render(login: str, rows: list[tuple[str, str]], p: Palette) -> str:
    green = "#1a7f37" if p.name == "light" else "#3fb950"
    parts = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{p.bg}" stroke="{p.border}"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="30" rx="6" fill="{p.track}"/>',
        f'<rect x="0.5" y="24" width="{W - 1}" height="7" fill="{p.track}"/>',
    ]
    for i, colour in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        parts.append(f'<circle cx="{20 + i * 18}" cy="15.5" r="5.5" fill="{colour}"/>')
    parts.append(
        f'<text x="{W / 2}" y="20" font-size="12" fill="{p.muted}" text-anchor="middle">'
        f"{escape(login.lower())}@github: ~</text>"
    )
    prompt = (
        f'<text x="24" y="58" font-size="13"><tspan fill="{green}">{escape(login.lower())}@github</tspan>'
        f'<tspan fill="{p.muted}">:</tspan><tspan fill="{p.accent}">~</tspan>'
        f'<tspan fill="{p.muted}">$ </tspan><tspan fill="{p.fg}">neofetch</tspan></text>'
    )
    parts.append(f'<g class="type">{prompt}</g>')
    for r, line in enumerate(LOGO):
        for c, opacity in enumerate(line):
            delay = 0.5 + (r * 6 + c) * 0.025
            parts.append(
                f'<rect class="sq" style="animation-delay:{delay:.2f}s" x="{40 + c * 26}" y="{82 + r * 26}" '
                f'width="22" height="22" rx="4" fill="{p.accent}" fill-opacity="{opacity}"/>'
            )
    x = 250
    head = f"{login.lower()}@github"
    parts.append(
        f'<g class="line" style="animation-delay:.6s"><text x="{x}" y="88" font-size="14" font-weight="700" '
        f'fill="{green}">{escape(head)}</text><text x="{x}" y="104" font-size="13" fill="{p.muted}">'
        f"{'-' * len(head)}</text></g>"
    )
    for i, (key, value) in enumerate(rows):
        y = 124 + i * 17
        parts.append(
            f'<g class="line" style="animation-delay:{0.7 + i * 0.12:.2f}s"><text x="{x}" y="{y}" font-size="13">'
            f'<tspan fill="{p.accent}" font-weight="700">{escape(key)}</tspan>'
            f'<tspan fill="{p.muted}">: </tspan><tspan fill="{p.fg}">{escape(value)}</tspan></text></g>'
        )
    palette = (
        "#cf222e",
        "#bf8700",
        "#1a7f37",
        "#0969da",
        "#8250df",
        "#1b7c83",
        p.muted,
        p.fg,
    )
    for i, colour in enumerate(palette):
        parts.append(
            f'<rect class="line" style="animation-delay:{0.8 + len(rows) * 0.12:.2f}s" '
            f'x="{x + i * 26}" y="{H - 22}" width="22" height="12" fill="{colour}"/>'
        )
    label = "neofetch for " + login + ": " + "; ".join(f"{k} {v}" for k, v in rows)
    css = (
        "<style>.line,.type{opacity:0;animation:fade .35s ease-out forwards}"
        ".type{animation-delay:.1s}"
        ".sq{opacity:0;animation:fade .3s ease-out forwards}"
        "@keyframes fade{to{opacity:1}}"
        "@media (prefers-reduced-motion:reduce){.line,.type,.sq{animation:none;opacity:1}}</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>{css}'
        f'<g font-family="{MONO}">{"".join(parts)}</g></svg>\n'
    )


def main() -> None:
    login = os.environ.get("GITHUB_REPOSITORY_OWNER", "AmirulAndalib")
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    rows = summarise(
        fetch(login, os.environ.get("GITHUB_TOKEN", "")), datetime.now(UTC)
    )
    write_cards("terminal", lambda p: render(login, rows, p), out)


if __name__ == "__main__":
    try:
        main()
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
