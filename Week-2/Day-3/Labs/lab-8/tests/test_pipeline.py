from pathlib import Path

import pandas as pd

import pipeline as logistics_pipeline


LAB_ROOT = Path(__file__).resolve().parent.parent


def test_shipments_csv_exists():
    assert (LAB_ROOT / "data" / "shipments.csv").is_file()


def test_avg_delivery_by_destination_matches_expected():
    df = pd.read_csv(LAB_ROOT / "data" / "shipments.csv")
    cleaned = logistics_pipeline.clean_shipments(df)
    out = logistics_pipeline.avg_delivery_by_destination(cleaned)

    means = dict(zip(out["destination"], out["delivery_time"]))
    assert means == {"Chennai": 1.0, "Kolkata": 0.0, "Mumbai": 2.0, "Pune": 1.0}


def test_clean_fills_missing_delivery_times():
    df = pd.DataFrame({"destination": ["X"], "delivery_time": [float("nan")]})
    cleaned = logistics_pipeline.clean_shipments(df)
    assert cleaned["delivery_time"].tolist() == [0.0]
