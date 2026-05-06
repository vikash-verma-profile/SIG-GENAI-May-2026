from pathlib import Path

import pandas as pd

import pipeline as healthcare_pipeline


LAB_ROOT = Path(__file__).resolve().parent.parent


def test_patients_csv_exists():
    assert (LAB_ROOT / "data" / "patients.csv").is_file()


def test_modular_pipeline_writes_expected_outputs(tmp_path, monkeypatch):
    monkeypatch.setattr(healthcare_pipeline, "OUT_DIR", tmp_path)
    monkeypatch.setattr(healthcare_pipeline, "DATA_PATH", LAB_ROOT / "data" / "patients.csv")

    healthcare_pipeline.run_pipeline()

    billing = pd.read_csv(tmp_path / "billing.csv")
    daily = pd.read_csv(tmp_path / "daily.csv")

    billing_totals = dict(zip(billing["diagnosis"], billing["billing_amount"]))
    assert billing_totals["Diabetes"] == 500
    assert billing_totals["Cardiac"] == 500

    daily_counts = dict(zip(daily["visit_date"].astype(str), daily["patient_count"]))
    assert daily_counts["2024-01-01"] == 2
    assert daily_counts["2024-01-02"] == 1
    assert daily_counts["2024-01-03"] == 1


def test_incremental_pattern_example_filter():
    df = pd.read_csv(LAB_ROOT / "data" / "patients.csv")
    incremental = df[df["visit_date"] > "2024-01-01"]
    assert set(incremental["visit_date"].astype(str).tolist()) == {"2024-01-02", "2024-01-03"}
