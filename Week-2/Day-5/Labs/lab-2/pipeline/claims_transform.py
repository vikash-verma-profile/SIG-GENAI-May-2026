"""Healthcare claims transformation stubs."""

import pandas as pd


def normalize_claim_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe with non-negative claim amounts."""
    out = df.copy()
    if "claim_amount" in out.columns:
        out["claim_amount"] = out["claim_amount"].clip(lower=0)
    return out
