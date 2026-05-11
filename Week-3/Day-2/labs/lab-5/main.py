"""
Lab 5: Anomaly detection with Isolation Forest.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parent
PLOTS = ROOT / "plots"


def main() -> None:
    PLOTS.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"revenue": [100, 120, 110, 5000, 130]})
    model = IsolationForest(random_state=42, contamination=0.2)
    df["anomaly"] = model.fit_predict(df[["revenue"]])
    # sklearn: -1 anomaly, 1 inlier
    print(df)
    outliers = df[df["anomaly"] == -1]
    print("\nOutlier rows:\n", outliers)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.scatter(df.index, df["revenue"], c=df["anomaly"], cmap="coolwarm", s=80)
    ax.set_title("Revenue with anomaly labels (-1 = anomaly)")
    ax.set_xlabel("index")
    ax.set_ylabel("revenue")
    fig.tight_layout()
    fig.savefig(PLOTS / "anomalies.png", dpi=120)
    print(f"\nPlot saved to {PLOTS / 'anomalies.png'}")


if __name__ == "__main__":
    main()
