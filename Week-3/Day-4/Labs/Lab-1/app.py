"""
Lab 1 — Self-healing pipeline framework: detect, diagnose, remediate, verify, alert.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS_DIR = ROOT / "logs"
WORKFLOWS_DIR = ROOT / "workflows"
ALERTS_DIR = ROOT / "alerts"
REMEDIATION_DIR = ROOT / "remediation"


def read_latest_error() -> str:
    log_path = LOGS_DIR / "pipeline.log"
    if not log_path.exists():
        return "unknown failure"
    for line in reversed(log_path.read_text(encoding="utf-8").splitlines()):
        if "ERROR" in line:
            return line.split("ERROR", 1)[1].strip()
    return "unknown failure"


def detect_failure(pipeline_status: str) -> bool:
    if pipeline_status == "FAILED":
        print("Pipeline failure detected")
        return True
    print("Pipeline healthy")
    return False


def diagnose_failure(error: str) -> str:
    lowered = error.lower()
    if "schema" in lowered:
        return "Schema Drift"
    if "timeout" in lowered:
        return "Timeout"
    if "null" in lowered:
        return "Null Spike"
    return "Unknown Error"


def select_fix(issue: str) -> str:
    fixes = {
        "Schema Drift": "Update Schema Mapping",
        "Timeout": "Increase Timeout and Retry",
        "Null Spike": "Apply Null Imputation Rule",
        "Unknown Error": "Escalate to On-Call",
    }
    return fixes.get(issue, "Escalate to On-Call")


def apply_fix(action: str) -> None:
    print(f"Applying fix: {action}")
    REMEDIATION_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "status": "applied",
    }
    (REMEDIATION_DIR / "last_fix.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )


def rerun_workflow() -> str:
    print("Re-running workflow...")
    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    (WORKFLOWS_DIR / "last_run.json").write_text(
        json.dumps({"status": "SUCCESS", "rerun": True}, indent=2),
        encoding="utf-8",
    )
    return "SUCCESS"


def generate_alert(message: str) -> Path:
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    alert_path = ALERTS_DIR / "recovery_alert.txt"
    alert_path.write_text(message + "\n", encoding="utf-8")
    print(message)
    return alert_path


def main() -> None:
    pipeline_status = "FAILED"
    if not detect_failure(pipeline_status):
        return

    error = read_latest_error()
    issue = diagnose_failure(error)
    print(f"Diagnosis completed: {issue}")

    action = select_fix(issue)
    apply_fix(action)

    pipeline_status = rerun_workflow()
    if pipeline_status == "SUCCESS":
        print("Pipeline recovered")
        generate_alert("Alert: Pipeline recovered successfully")


if __name__ == "__main__":
    main()
