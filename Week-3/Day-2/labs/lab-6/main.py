"""
Lab 6: Configurable threshold monitoring for null rates.
"""
from __future__ import annotations

import pandas as pd

NULL_THRESHOLD_PERCENT = 5.0


def main() -> None:
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5],
            "revenue": [100.0, None, None, 400.0, 500.0],
        }
    )
    null_rate = (df.isnull().sum() / len(df)) * 100
    print("Null rate (% per column):\n", null_rate)

    if null_rate["revenue"] > NULL_THRESHOLD_PERCENT:
        print(
            f"ALERT: revenue null rate {null_rate['revenue']:.1f}% "
            f"exceeds threshold {NULL_THRESHOLD_PERCENT}%"
        )
    else:
        print("revenue null rate within threshold.")


if __name__ == "__main__":
    main()
