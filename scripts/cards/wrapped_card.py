"""Render a "year in review" card, a GitHub Wrapped built from the GraphQL API.

Counts the owner's contributions from 1 January of the current year (UTC) to now:
totals, busiest day, longest streak, contributions per month and per weekday, and the
repositories that took the most commits. Writes wrapped-light.svg and wrapped-dark.svg.
Reads GITHUB_TOKEN and GITHUB_REPOSITORY_OWNER.
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

from common import (
    ANIMATION_CSS,
    FONT,
    CardError,
    Palette,
    bar,
    post_json,
    row,
    text,
    truncate,
    write_cards,
)

W = 1012
PAD = 28
H = 330
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      totalRepositoriesWithContributedCommits
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
      commitContributionsByRepository(maxRepositories: 5) {
        repository { nameWithOwner isPrivate }
        contributions { totalCount }
      }
    }
  }
}
"""


def fetch(owner: str, token: str, now: datetime) -> dict:
    if not token:
        raise CardError("GITHUB_TOKEN is required for the GraphQL API")
    start = datetime(now.year, 1, 1, tzinfo=UTC)
    response = post_json(
        "https://api.github.com/graphql",
        {
            "query": QUERY,
            "variables": {
                "login": owner,
                "from": start.isoformat(),
                "to": now.isoformat(),
            },
        },
        {"Authorization": f"Bearer {token}"},
    )
    if response.get("errors"):
        raise CardError(f"GraphQL error: {response['errors'][0].get('message')}")
    return response["data"]["user"]["contributionsCollection"]


def summarise(raw: dict, today: date) -> dict:
    days = [
        (date.fromisoformat(d["date"]), d["contributionCount"])
        for week in raw["contributionCalendar"]["weeks"]
        for d in week["contributionDays"]
    ]
    days = [(d, n) for d, n in days if d.year == today.year and d <= today]
    if not days:
        raise CardError("contribution calendar is empty")
    months = [0] * 12
    weekdays = [0] * 7
    longest = current = 0
    for d, n in days:
        months[d.month - 1] += n
        weekdays[d.weekday()] += n
        current = current + 1 if n else 0
        longest = max(longest, current)
    busiest_day, busiest_count = max(days, key=lambda item: item[1])
    repos = [
        (
            "private repository"
            if item["repository"]["isPrivate"]
            else item["repository"]["nameWithOwner"],
            item["contributions"]["totalCount"],
        )
        for item in raw["commitContributionsByRepository"]
    ]
    return {
        "year": today.year,
        "total": raw["contributionCalendar"]["totalContributions"],
        "commits": raw["totalCommitContributions"]
        + raw["restrictedContributionsCount"],
        "prs": raw["totalPullRequestContributions"],
        "issues": raw["totalIssueContributions"],
        "reviews": raw["totalPullRequestReviewContributions"],
        "repos_touched": raw["totalRepositoriesWithContributedCommits"],
        "active_days": sum(1 for _, n in days if n),
        "days_so_far": len(days),
        "longest": longest,
        "busiest_day": busiest_day,
        "busiest_count": busiest_count,
        "months": months,
        "weekdays": weekdays,
        "repos": repos,
        "current_month": today.month,
    }


def tile(x: float, label: str, value: str, palette: Palette, index: int) -> str:
    return row(
        text(x, 104, value, size=26, weight=600, fill=palette.fg)
        + text(x, 126, label, size=12, fill=palette.muted),
        index,
    )


def render(s: dict, palette: Palette) -> str:
    body = [
        text(PAD, 44, f"{s['year']} in review", size=18, weight=600, fill=palette.fg),
        text(
            W - PAD,
            44,
            f"{s['active_days']} active days of {s['days_so_far']} so far · busiest "
            f"{s['busiest_day']:%a %d %b} ({s['busiest_count']})",
            size=12,
            fill=palette.muted,
            anchor="end",
        ),
    ]
    tiles = [
        ("contributions", f"{s['total']:,}"),
        ("commits", f"{s['commits']:,}"),
        ("pull requests", f"{s['prs']:,}"),
        ("issues", f"{s['issues']:,}"),
        ("reviews", f"{s['reviews']:,}"),
        ("repos committed to", f"{s['repos_touched']:,}"),
        ("longest streak", f"{s['longest']}d"),
    ]
    step = (W - 2 * PAD) / len(tiles)
    body += [
        tile(PAD + i * step, label, value, palette, i)
        for i, (label, value) in enumerate(tiles)
    ]
    body.append(
        f'<line x1="{PAD}" y1="148" x2="{W - PAD}" y2="148" stroke="{palette.border}"/>'
    )

    # Left column: contributions per month as vertical bars.
    body.append(text(PAD, 176, "By month", size=13, weight=600, fill=palette.fg))
    peak = max(s["months"]) or 1
    col_w, gap, base = 26, 10, 290
    for i, count in enumerate(s["months"]):
        x = PAD + i * (col_w + gap)
        height = max(2, 80 * count / peak) if count else 0
        future = i + 1 > s["current_month"]
        body.append(
            f'<rect x="{x}" y="{base - 80}" width="{col_w}" height="80" rx="3" fill="{palette.track}"/>'
        )
        if height:
            body.append(
                f'<rect class="rise" style="animation-delay:{0.2 + i * 0.05:.2f}s" x="{x}" '
                f'y="{base - height:.1f}" width="{col_w}" height="{height:.1f}" rx="3" fill="{palette.accent}">'
                f"<title>{MONTHS[i]}: {count:,}</title></rect>"
            )
        body.append(
            text(
                x + col_w / 2,
                base + 16,
                MONTHS[i],
                size=11,
                fill=palette.muted if not future else palette.border,
                anchor="middle",
            )
        )

    # Middle column: weekday split.
    mid = 470
    body.append(text(mid, 176, "By weekday", size=13, weight=600, fill=palette.fg))
    wpeak = max(s["weekdays"]) or 1
    for i, count in enumerate(s["weekdays"]):
        y = 194 + i * 15
        body.append(
            row(
                text(mid, y + 8, WEEKDAYS[i], size=11, fill=palette.muted)
                + bar(mid + 34, y, 150, count / wpeak, palette, 0.2 + i * 0.05)
                + text(mid + 192, y + 8, f"{count:,}", size=11, fill=palette.muted),
                i,
            )
        )

    # Right column: repositories that took the most commits.
    right = 720
    body.append(text(right, 176, "Most commits", size=13, weight=600, fill=palette.fg))
    rpeak = max((n for _, n in s["repos"]), default=1) or 1
    for i, (name, count) in enumerate(s["repos"][:5]):
        y = 198 + i * 22
        short = name.split("/", 1)[1] if name.startswith("AmirulAndalib/") else name
        body.append(
            row(
                text(right, y, truncate(short, 26), size=11, fill=palette.fg)
                + text(
                    W - PAD, y, f"{count:,}", size=11, fill=palette.muted, anchor="end"
                )
                + bar(
                    right,
                    y + 4,
                    W - PAD - right,
                    count / rpeak,
                    palette,
                    0.3 + i * 0.06,
                ),
                i,
            )
        )

    label = (
        f"{s['year']} in review: {s['total']:,} contributions, {s['commits']:,} commits, "
        f"{s['prs']:,} pull requests, longest streak {s['longest']} days"
    )
    css = ANIMATION_CSS.replace(
        "</style>",
        ".rise{transform-box:fill-box;transform-origin:bottom center;transform:scaleY(0);"
        "animation:rise .8s cubic-bezier(.2,.7,.2,1) forwards}"
        "@keyframes rise{to{transform:scaleY(1)}}"
        "@media (prefers-reduced-motion:reduce){.rise{animation:none;transform:none}}</style>",
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>{css}'
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{palette.bg}" '
        f'stroke="{palette.border}"/><g font-family="{FONT}">{"".join(body)}</g></svg>\n'
    )


def main() -> None:
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "AmirulAndalib")
    token = os.environ.get("GITHUB_TOKEN", "")
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    now = datetime.now(UTC)
    stats = summarise(fetch(owner, token, now), now.date())
    write_cards("wrapped", lambda p: render(stats, p), out)


if __name__ == "__main__":
    try:
        main()
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
