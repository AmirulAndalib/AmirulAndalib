"""Keep Dependabot only on repositories that are actively used.

Uses the plan.json written by actions_audit.py: "keep" repositories get Dependabot alerts
and security updates switched on, "disable" repositories get both switched off. Results
are appended to dependabot.jsonl in the same directory so a run can resume.

    python dependabot_audit.py OUT_DIR
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from actions_audit import Api


def main() -> int:
    out = Path(sys.argv[1])
    token = os.environ.get("GH_TOKEN", "").strip()
    if not token:
        print("error: GH_TOKEN is not set", file=sys.stderr)
        return 1
    api = Api(token)
    plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
    log_path = out / "dependabot.jsonl"
    done = set()
    if log_path.exists():
        done = {
            json.loads(line)["repo"]
            for line in log_path.read_text(encoding="utf-8").splitlines()
            if line
        }
    rows = [
        r for r in plan if r["action"] in {"keep", "disable"} and r["repo"] not in done
    ]
    print(f"{len(rows)} repositories to process", flush=True)
    with log_path.open("a", encoding="utf-8") as log:
        for index, item in enumerate(rows, 1):
            repo, enable = item["repo"], item["action"] == "keep"
            method = "PUT" if enable else "DELETE"
            if enable:
                alerts, _ = api.request("PUT", f"/repos/{repo}/vulnerability-alerts")
                fixes, _ = api.request("PUT", f"/repos/{repo}/automated-security-fixes")
            else:
                fixes, _ = api.request(
                    "DELETE", f"/repos/{repo}/automated-security-fixes"
                )
                alerts, _ = api.request("DELETE", f"/repos/{repo}/vulnerability-alerts")
            record = {"repo": repo, "action": method, "alerts": alerts, "fixes": fixes}
            log.write(json.dumps(record) + "\n")
            log.flush()
            if index % 100 == 0 or alerts >= 400:
                print(
                    f"[{index}/{len(rows)}] {repo} {method} alerts={alerts} fixes={fixes}",
                    flush=True,
                )
    return 0


if __name__ == "__main__":
    sys.exit(main())
