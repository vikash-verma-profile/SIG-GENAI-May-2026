"""
Smart city traffic metrics — anomaly detection for small samples.

Uses median absolute deviation style rule: flag latency more than 3x the median
(which catches the 900 vs ~200 spike in metrics.csv). Lab 10 also expects
qualitative AI analysis in your LLM tool.
"""

from pathlib import Path

import pandas as pd


def main() -> None:
    path = Path(__file__).resolve().parent / "metrics.csv"
    df = pd.read_csv(path)
    lat = df["latency"]
    median = lat.median()
    anomalies = df[lat > median * 3]
    print("Median latency:", median)
    print("Rows flagged (latency > 3 * median):")
    print(anomalies.to_string(index=False))
    print("")
    print(
        "Interpretation: 10:02 latency spike (900 vs ~200) suggests investigating "
        "Kafka consumer scaling and Spark executor sizing."
    )


if __name__ == "__main__":
    main()
