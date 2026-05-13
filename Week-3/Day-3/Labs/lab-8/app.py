"""
Lab 8 — GDPR compliance monitoring agent (PII signals + retention check).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "compliance_report.json"

EMAIL_RE = re.compile(r"\S+@\S+")


def has_pii(df: pd.DataFrame) -> bool:
    for col in df.columns:
        for val in df[col].dropna().astype(str).head(50):
            if EMAIL_RE.search(val):
                return True
    return False


def evaluate_retention(max_age_days: int, retention_limit_days: int) -> bool:
    return max_age_days <= retention_limit_days


def run_check(df: pd.DataFrame, retention_days: int, max_record_age_days: int) -> dict:
    pii = has_pii(df)
    ok = evaluate_retention(max_record_age_days, retention_days)
    alerts: list[str] = []
    if pii:
        alerts.append("PII columns detected - verify lawful basis and minimization.")
    if not ok:
        alerts.append(
            f"Retention risk: oldest records exceed policy ({max_record_age_days} > {retention_days})."
        )
    if not alerts:
        alerts.append("GDPR compliance check completed — no blocking issues in this synthetic scan.")
    return {
        "pii_detected": pii,
        "retention_policy_days": retention_days,
        "max_record_age_days": max_record_age_days,
        "retention_ok": ok,
        "alerts": alerts,
    }


def main() -> None:
    df = pd.DataFrame({"customer_email": ["a@gmail.com"]})
    retention_days = 365
    max_record_age_days = 400  # trigger retention alert for demo
    report = run_check(df, retention_days, max_record_age_days)
    print(json.dumps(report, indent=2))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote:", OUT_PATH)


if __name__ == "__main__":
    main()
