"""
Lab 2 — AI-based failure detection from operational logs.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sample_logs.txt"
OUT_DIR = ROOT / "outputs"


def load_logs() -> list[str]:
    return [line.strip() for line in DATA_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def logs_to_features(logs: list[str]) -> pd.DataFrame:
    return pd.DataFrame(logs, columns=["message"])


def detect_failures(logs: list[str]) -> list[dict]:
    failures: list[dict] = []
    for log in logs:
        if "ERROR" in log:
            failures.append({"message": log, "severity": "high"})
            print("Failure detected:", log)
    return failures


def severity_score(log: str) -> int:
    score = 1
    if "ERROR" in log:
        score += 3
    if "timeout" in log.lower():
        score += 2
    if "schema" in log.lower():
        score += 2
    return score


def cluster_logs(logs: list[str], k: int = 2) -> list[int]:
    if len(logs) < k:
        return list(range(len(logs)))
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(logs)
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    return model.fit_predict(matrix).tolist()


def summarize_root_cause(failures: list[dict]) -> str:
  if not failures:
      return "No failures detected in the current log window."
  messages = " ".join(item["message"] for item in failures).lower()
  if "schema" in messages:
      return "Root cause: schema mismatch between source and target tables."
  if "timeout" in messages:
      return "Root cause: downstream write timeout under load."
  return "Root cause: review ERROR lines and correlate with upstream job changes."


def main() -> None:
    logs = load_logs()
    df = logs_to_features(logs)
    print("--- Log features ---")
    print(df)

    failures = detect_failures(logs)
    scored = [{"message": log, "score": severity_score(log)} for log in logs]
    clusters = cluster_logs(logs)

    summary = summarize_root_cause(failures)
    print("\n--- AI-style summary ---")
    print(summary)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "failures": failures,
        "severity": scored,
        "clusters": clusters,
        "summary": summary,
    }
    out_path = OUT_DIR / "failure_report.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
