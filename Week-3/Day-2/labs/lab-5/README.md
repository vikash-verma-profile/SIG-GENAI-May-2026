# Lab 5 — Anomaly Detection Agent

Use an Isolation Forest to label obvious outliers in a numeric series and visualize them.

## Learning outcomes

- Fit `IsolationForest` on a single feature (extend to many later).
- Interpret `anomaly` labels (`1` inlier, `-1` outlier in scikit-learn).
- Optionally plot results for communication.

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-5
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Run the detector

```bash
python main.py
```

The sample series includes `5000` among small hundreds values; with `contamination=0.2` it should often be flagged as an outlier (exact labels can vary slightly with hyperparameters).

## Step 3 — Expected output

- Printed dataframe with `anomaly` column.
- Printed subset where `anomaly == -1`.
- `plots/anomalies.png` scatter plot.

## Exercises

1. Add Z-score based detection (`scipy.stats.zscore` or manual) and compare to Isolation Forest.
2. Raise an “alert” when any outlier exists (print or stub function).
3. Send email or Slack: implement a stub `send_alert(message: str)` and call it from `main()`.

## Files

- `main.py` — model + print + optional plot.
- `plots/` — PNG output after run.
