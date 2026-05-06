"""Fraud / high-value flags."""
import pandas as pd


def detect_fraud(df: pd.DataFrame, threshold: float = 800) -> pd.DataFrame:
    """Flag high-value transactions."""
    out = df.copy()
    out["is_fraud"] = out["amount"] > threshold
    return out

