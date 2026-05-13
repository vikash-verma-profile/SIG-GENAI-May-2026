"""
Lab 9 — Drift detection agent with distribution checks and pipeline adjustment.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from scipy.stats import ks_2samp

ROOT = Path(__file__).resolve().parent
BASELINE_PATH = ROOT / "data" / "baseline.csv"
CURRENT_PATH = ROOT / "data" / "current.csv"
OUT_DIR = ROOT / "outputs"


def load_series(path: Path) -> pd.Series:
    return pd.read_csv(path)["value"]


def mean_drift(baseline: pd.Series, current: pd.Series, tolerance: float = 20.0) -> bool:
    return abs(float(current.mean()) - float(baseline.mean())) > tolerance


def psi_score(baseline: pd.Series, current: pd.Series, bins: int = 5) -> float:
    breakpoints = pd.qcut(baseline, q=bins, duplicates="drop", retbins=True)[1]
    baseline_counts = pd.cut(baseline, bins=breakpoints, include_lowest=True).value_counts(normalize=True)
    current_counts = pd.cut(current, bins=breakpoints, include_lowest=True).value_counts(normalize=True)
    aligned = pd.concat([baseline_counts, current_counts], axis=1, keys=["base", "curr"]).fillna(0.0001)
    diff = aligned["curr"] - aligned["base"]
    ratio = aligned["curr"] / aligned["base"]
    return float(((diff * ratio.map(lambda x: 0 if x <= 0 else __import__("math").log(x))).sum()))


def adjust_pipeline(drift_detected: bool, baseline_mean: float) -> dict:
    if not drift_detected:
        return {"threshold": baseline_mean + 20, "action": "no_change"}
    return {"threshold": baseline_mean + 50, "action": "increase_validation_threshold"}


def main() -> None:
    baseline = load_series(BASELINE_PATH)
    current = load_series(CURRENT_PATH)
    baseline_mean = float(baseline.mean())
    current_mean = float(current.mean())

    drift = mean_drift(baseline, current)
    ks_stat, ks_pvalue = ks_2samp(baseline, current)
    psi = psi_score(baseline, current)
    adjustment = adjust_pipeline(drift, baseline_mean)

    if drift:
        print("Drift detected")
    else:
        print("No significant mean drift")

    print(f"Baseline mean={baseline_mean:.2f}, current mean={current_mean:.2f}")
    print(f"KS stat={ks_stat:.4f}, p-value={ks_pvalue:.4f}, PSI={psi:.4f}")
    print("Pipeline adjustment:", adjustment)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "drift_report.json"
    out_path.write_text(
        json.dumps(
            {
                "baseline_mean": baseline_mean,
                "current_mean": current_mean,
                "drift_detected": drift,
                "ks_stat": round(float(ks_stat), 4),
                "ks_pvalue": round(float(ks_pvalue), 4),
                "psi": round(psi, 4),
                "adjustment": adjustment,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
