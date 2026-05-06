"""Part A: Traditional ETL (minimal, as in lab)."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(ROOT / "data" / "patients.csv")
df = df.drop_duplicates()
df["age"] = df["age"].fillna(df["age"].mean())
df["billing_amount"] = df["billing_amount"].fillna(0)

billing = df.groupby("diagnosis")["billing_amount"].sum()
daily = df.groupby("visit_date")["patient_id"].count()

billing.to_csv(OUT_DIR / "billing.csv")
daily.to_csv(OUT_DIR / "daily.csv")
