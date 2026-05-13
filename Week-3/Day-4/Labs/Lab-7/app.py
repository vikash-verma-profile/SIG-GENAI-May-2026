"""
Lab 7 — AI-generated narrative reporting from KPI metrics.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "kpi_metrics.json"
OUT_DIR = ROOT / "outputs"


def load_metrics() -> dict[str, float | int]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def build_prompt(metrics: dict[str, float | int]) -> str:
    return (
        "Generate executive business summary using these metrics: "
        + json.dumps(metrics)
    )


def generate_narrative(metrics: dict[str, float | int]) -> str:
    return (
        "Revenue declined primarily due to increased churn in the North region. "
        f"Revenue dropped {metrics['revenue_drop_pct']}% while churn rose "
        f"{metrics['churn_increase_pct']}%. Support tickets improved by "
        f"{abs(metrics['support_tickets_change_pct'])}%, indicating better onboarding."
    )


def classify_sentiment(metrics: dict[str, float | int]) -> str:
    if metrics["revenue_drop_pct"] > 5 or metrics["churn_increase_pct"] > 10:
        return "negative"
    return "neutral"


def main() -> None:
    metrics = load_metrics()
    prompt = build_prompt(metrics)
    narrative = generate_narrative(metrics)
    sentiment = classify_sentiment(metrics)

    print("Prompt:\n", prompt)
    print("\nExecutive narrative:\n", narrative)
    print("\nSentiment:", sentiment)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "executive_report.json"
    out_path.write_text(
        json.dumps(
            {"metrics": metrics, "prompt": prompt, "narrative": narrative, "sentiment": sentiment},
            indent=2,
        ),
        encoding="utf-8",
    )
    text_path = OUT_DIR / "executive_report.txt"
    text_path.write_text(narrative + "\n", encoding="utf-8")
    print(f"\nWrote {out_path} and {text_path}")


if __name__ == "__main__":
    main()
