"""
Lab 3: Automated data profiling with ydata-profiling.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5],
            "revenue": [100, 200, None, 400, 10_000],
            "region": ["A", "A", "B", "B", "B"],
        }
    )
    df.to_csv(DATA_DIR / "customers.csv", index=False)

    profile = ProfileReport(df, title="Lab 3 Profiling Report", minimal=True)
    out_html = REPORTS_DIR / "profile.html"
    profile.to_file(out_html)
    print(f"Report written to {out_html}")
    print("\nQuick stats — null counts:\n", df.isnull().sum())


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    main()
