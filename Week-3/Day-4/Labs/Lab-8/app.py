"""
Lab 8 — AI-assisted MLOps monitoring with MLflow logging.
"""
from __future__ import annotations

import json
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"
MLFLOW_DIR = ROOT / "mlruns"
THRESHOLD = 0.80


def train_and_log() -> float:
    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment("lab8_monitoring")

    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.3, random_state=42
    )
    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)
    accuracy = float(accuracy_score(y_test, model.predict(x_test)))

    with mlflow.start_run(run_name="iris_classifier"):
        mlflow.log_param("model", "logistic_regression")
        mlflow.log_metric("accuracy", accuracy)
    return accuracy


def detect_performance_drop(accuracy: float) -> bool:
    if accuracy < THRESHOLD:
        print("Retraining required")
        return True
    print("Model within threshold")
    return False


def trigger_retraining() -> dict:
    print("Model retraining started")
    return {"status": "retraining_triggered", "strategy": "full_refit"}


def main() -> None:
    accuracy = train_and_log()
    needs_retrain = detect_performance_drop(accuracy)
    action = trigger_retraining() if needs_retrain else {"status": "monitoring_only"}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "accuracy": round(accuracy, 4),
        "threshold": THRESHOLD,
        "needs_retrain": needs_retrain,
        "action": action,
        "history": pd.DataFrame({"accuracy": [accuracy]}).to_dict(orient="records"),
    }
    out_path = OUT_DIR / "mlops_report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
