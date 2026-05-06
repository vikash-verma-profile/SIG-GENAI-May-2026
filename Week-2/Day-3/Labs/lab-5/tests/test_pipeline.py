from pathlib import Path

import pandas as pd

import pipeline as telecom_pipeline


LAB_ROOT = Path(__file__).resolve().parent.parent


def test_cdr_files_exist():
    assert (LAB_ROOT / "data" / "cdr_day1.csv").is_file()
    assert (LAB_ROOT / "data" / "cdr_day2.csv").is_file()


def test_pipeline_writes_outputs_and_updates_watermark(tmp_path, monkeypatch):
    out_dir = tmp_path / "output"
    watermark_path = tmp_path / "watermark.txt"

    monkeypatch.setattr(telecom_pipeline, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(telecom_pipeline, "STATE_PATH", watermark_path)

    telecom_pipeline.run_pipeline()

    duration = pd.read_csv(out_dir / "duration_by_user.csv")
    totals = dict(zip(duration["user_id"], duration["call_duration"]))
    assert totals[1001] == 210
    assert totals[1002] == 450
    assert totals[1003] == 200

    assert watermark_path.read_text(encoding="utf-8").strip() == "2024-01-02"


def test_incremental_slice_filters_day2_by_watermark():
    day2 = pd.read_csv(LAB_ROOT / "data" / "cdr_day2.csv")
    incremental = telecom_pipeline.incremental_load(day2, "2024-01-01")
    assert incremental.shape[0] == 3


def test_cdc_keeps_latest_call_id():
    old_df = pd.read_csv(LAB_ROOT / "data" / "cdr_day1.csv")
    new_df = pd.read_csv(LAB_ROOT / "data" / "cdr_day2.csv")
    merged = telecom_pipeline.apply_cdc(old_df, new_df[new_df["last_updated"] > "2024-01-01"])
    row = merged.loc[merged["call_id"] == 3].iloc[0]
    assert int(row["call_duration"]) == 90
