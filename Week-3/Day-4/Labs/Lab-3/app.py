"""
Lab 3 — Root cause analysis agent for pipeline incidents.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "incident.log"
OUT_DIR = ROOT / "outputs"

FAILURE_TYPES = ["Schema Drift", "Null Spike", "Timeout", "Unknown"]


def diagnose(log: str) -> str:
    lowered = log.lower()
    if "schema" in lowered:
        return "Schema Drift"
    if "null" in lowered:
        return "Null Spike"
    if "timeout" in lowered:
        return "Timeout"
    return "Unknown"


def confidence_score(log: str, issue: str) -> float:
    keywords = {
        "Schema Drift": ["schema", "drift", "column"],
        "Null Spike": ["null", "missing"],
        "Timeout": ["timeout", "deadline"],
    }
    hits = sum(1 for word in keywords.get(issue, []) if word in log.lower())
    return round(min(0.95, 0.45 + hits * 0.2), 2)


def build_summary(issue: str, log: str) -> str:
    if issue == "Schema Drift":
        return "Failure caused by schema drift in customer_orders table."
    if issue == "Null Spike":
        return "Failure caused by a sudden null spike in revenue_amount."
    if issue == "Timeout":
        return "Failure caused by a warehouse write timeout."
    return f"Failure requires manual review. Evidence: {log}"


def main() -> None:
    logs = [line.strip() for line in DATA_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    incidents = []
    for log in logs:
        issue = diagnose(log)
        incidents.append(
            {
                "log": log,
                "issue": issue,
                "confidence": confidence_score(log, issue),
                "summary": build_summary(issue, log),
            }
        )
        print(f"{issue} ({incidents[-1]['confidence']}): {incidents[-1]['summary']}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "rca_report.json"
    out_path.write_text(json.dumps({"failure_types": FAILURE_TYPES, "incidents": incidents}, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
