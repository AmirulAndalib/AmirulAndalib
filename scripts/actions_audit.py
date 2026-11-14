"""Audit every repository the account owns and disable GitHub Actions where it is not wanted.

A repository keeps Actions when it is a non-fork pushed within KEEP_DAYS, or a fork the
owner committed to within KEEP_DAYS, or it is listed in KEEP_ALWAYS. Everything else that
contains workflows gets Actions disabled. Archived repositories never run workflows and
are left alone.

Usage:
    python actions_audit.py plan   OUT_DIR   # inventory + decisions, changes nothing
    python actions_audit.py apply  OUT_DIR   # disable Actions per plan.json, resumable
    python actions_audit.py restore OUT_DIR  # re-enable everything this script disabled

Reads the token from GH_TOKEN. The state file (changes.jsonl) records each repository's
previous setting before it is changed, so restore puts back exactly what was there.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path

API = "https://api.github.com"
KEEP_DAYS = 365
# "owner/name" entries that must never be disabled.
KEEP_ALWAYS: set[str] = {"AmirulAndalib/fork"}

INVENTORY_QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositories(first: 100, after: $after, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        nameWithOwner isFork isPrivate isArchived pushedAt
        parent { nameWithOwner }
        workflows: object(expression: "HEAD:.github/workflows") {
          ... on Tree { entries { name } }
        }
      }
    }
  }
}
"""

CONTRIBUTIONS_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 100) {
        repository { nameWithOwner }
        contributions { totalCount }
      }
    }
  }
}
"""


class Api:
    def __init__(self, token: str) -> None:
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "actions-audit",
        }

    def request(
        self, method: str, path: str, body: dict | None = None
    ) -> tuple[int, dict]:
        url = path if path.startswith("http") else f"{API}{path}"
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(1, 7):
            req = urllib.request.Request(
                url, data=data, method=method, headers=self.headers
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    self._pace(resp.headers)
                    raw = resp.read()
                    return resp.status, (json.loads(raw) if raw else {})
            except urllib.error.HTTPError as exc:
                raw = exc.read()
                payload = (
                    json.loads(raw)
                    if raw.startswith(b"{")
                    else {"message": raw[:200].decode(errors="replace")}
                )
                if exc.code in (403, 429) and self._rate_limited(exc.headers, payload):
                    continue
                if exc.code >= 500 and attempt < 6:
                    time.sleep(5 * attempt)
                    continue
                return exc.code, payload
            except (urllib.error.URLError, TimeoutError):
                if attempt < 6:
                    time.sleep(5 * attempt)
                    continue
                raise
        raise RuntimeError(f"{method} {path} kept failing")

    def graphql(self, query: str, variables: dict) -> dict:
        status, payload = self.request(
            "POST", "/graphql", {"query": query, "variables": variables}
        )
        if status != 200 or payload.get("errors"):
            raise RuntimeError(
                f"GraphQL failed ({status}): {payload.get('errors') or payload}"
            )
        return payload["data"]

    @staticmethod
    def _pace(headers) -> None:
        remaining = int(headers.get("X-RateLimit-Remaining", "1000"))
        if remaining < 50:
            reset = int(headers.get("X-RateLimit-Reset", "0"))
            wait = max(0, reset - int(time.time())) + 5
            print(f"rate limit low ({remaining}); sleeping {wait}s", flush=True)
            time.sleep(wait)

    @staticmethod
    def _rate_limited(headers, payload: dict) -> bool:
        message = str(payload.get("message", "")).lower()
        if "rate limit" not in message:
            return False
        retry_after = headers.get("Retry-After")
        if retry_after:
            wait = int(retry_after) + 1
        else:
            reset = int(headers.get("X-RateLimit-Reset", "0"))
            wait = max(60, reset - int(time.time()) + 5)
        print(f"rate limited; sleeping {wait}s", flush=True)
        time.sleep(wait)
        return True


def inventory(api: Api, login: str) -> list[dict]:
    repos, after = [], None
    while True:
        data = api.graphql(INVENTORY_QUERY, {"login": login, "after": after})["user"][
            "repositories"
        ]
        for node in data["nodes"]:
            entries = (node.get("workflows") or {}).get("entries") or []
            node["workflow_files"] = [
                e["name"] for e in entries if e["name"].endswith((".yml", ".yaml"))
            ]
            node.pop("workflows", None)
            repos.append(node)
        print(f"inventoried {len(repos)} repositories", flush=True)
        if not data["pageInfo"]["hasNextPage"]:
            return repos
        after = data["pageInfo"]["endCursor"]


def committed_repos(api: Api, login: str) -> dict[str, int]:
    now = datetime.now(UTC)
    variables = {
        "login": login,
        "from": (now - timedelta(days=KEEP_DAYS)).isoformat(),
        "to": now.isoformat(),
    }
    rows = api.graphql(CONTRIBUTIONS_QUERY, variables)["user"][
        "contributionsCollection"
    ]
    return {
        row["repository"]["nameWithOwner"].lower(): row["contributions"]["totalCount"]
        for row in rows["commitContributionsByRepository"]
    }


def decide(repos: list[dict], commits: dict[str, int]) -> list[dict]:
    cutoff = datetime.now(UTC) - timedelta(days=KEEP_DAYS)
    plan = []
    for repo in repos:
        name = repo["nameWithOwner"]
        pushed = (
            datetime.fromisoformat(repo["pushedAt"]) if repo.get("pushedAt") else None
        )
        if repo["isArchived"]:
            action, reason = "skip", "archived"
        elif not repo["workflow_files"]:
            action, reason = "skip", "no workflows"
        elif name in KEEP_ALWAYS:
            action, reason = "keep", "allowlisted"
        elif not repo["isFork"] and pushed and pushed >= cutoff:
            action, reason = "keep", f"own repository pushed {pushed.date()}"
        elif repo["isFork"] and commits.get(name.lower()):
            action, reason = (
                "keep",
                f"fork with {commits[name.lower()]} of your commits in the last year",
            )
        elif repo["isFork"]:
            action, reason = (
                "disable",
                f"fork of {(repo.get('parent') or {}).get('nameWithOwner')}, none of your commits in a year",
            )
        else:
            action, reason = (
                "disable",
                f"own repository, last pushed {pushed.date() if pushed else 'never'}",
            )
        plan.append(
            {
                "repo": name,
                "fork": repo["isFork"],
                "private": repo["isPrivate"],
                "action": action,
                "reason": reason,
                "workflows": len(repo["workflow_files"]),
            }
        )
    return plan


def cmd_plan(api: Api, login: str, out: Path) -> None:
    repos = inventory(api, login)
    (out / "inventory.json").write_text(json.dumps(repos, indent=1), encoding="utf-8")
    plan = decide(repos, committed_repos(api, login))
    (out / "plan.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    counts: dict[str, int] = {}
    for row in plan:
        counts[row["action"]] = counts.get(row["action"], 0) + 1
    print("plan:", counts)
    for row in plan:
        if row["action"] == "keep":
            print(f"  keep    {row['repo']}  ({row['reason']})")


def _done(out: Path) -> dict[str, dict]:
    path = out / "changes.jsonl"
    if not path.exists():
        return {}
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return {row["repo"]: row for row in rows}


def cmd_apply(api: Api, out: Path) -> None:
    plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
    done = _done(out)
    targets = [
        row["repo"]
        for row in plan
        if row["action"] == "disable" and row["repo"] not in done
    ]
    print(
        f"{len(targets)} repositories to process ({len(done)} already done)", flush=True
    )
    with (out / "changes.jsonl").open("a", encoding="utf-8") as log:
        for index, repo in enumerate(targets, 1):
            status, before = api.request("GET", f"/repos/{repo}/actions/permissions")
            record = {"repo": repo, "time": datetime.now(UTC).isoformat()}
            if status != 200:
                record.update(
                    result="error", detail=f"read {status}: {before.get('message')}"
                )
            elif not before.get("enabled"):
                record.update(result="already-disabled", before=before)
            else:
                status, body = api.request(
                    "PUT", f"/repos/{repo}/actions/permissions", {"enabled": False}
                )
                record.update(
                    before=before,
                    result="disabled" if status == 204 else "error",
                    detail=None
                    if status == 204
                    else f"write {status}: {body.get('message')}",
                )
            log.write(json.dumps(record) + "\n")
            log.flush()
            if index % 50 == 0 or record["result"] == "error":
                print(
                    f"[{index}/{len(targets)}] {repo}: {record['result']} {record.get('detail') or ''}",
                    flush=True,
                )
    summary: dict[str, int] = {}
    for row in _done(out).values():
        summary[row["result"]] = summary.get(row["result"], 0) + 1
    print("result:", summary)


def cmd_restore(api: Api, out: Path) -> None:
    for repo, row in _done(out).items():
        if row.get("result") != "disabled":
            continue
        before = row["before"]
        body = {
            "enabled": True,
            "allowed_actions": before.get("allowed_actions", "all"),
        }
        status, payload = api.request("PUT", f"/repos/{repo}/actions/permissions", body)
        outcome = (
            "restored" if status == 204 else f"error {status} {payload.get('message')}"
        )
        print(f"{repo}: {outcome}")


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"plan", "apply", "restore"}:
        print(__doc__)
        return 2
    token = os.environ.get("GH_TOKEN", "").strip()
    login = os.environ.get("GH_LOGIN", "AmirulAndalib").strip()
    if not token:
        print("error: GH_TOKEN is not set", file=sys.stderr)
        return 1
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    api = Api(token)
    {
        "plan": lambda: cmd_plan(api, login, out),
        "apply": lambda: cmd_apply(api, out),
        "restore": lambda: cmd_restore(api, out),
    }[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
