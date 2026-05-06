"""Cleaning and aggregation."""
import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and handle missing amounts."""
    df = df.drop_duplicates().copy()
    df["amount"] = df["amount"].fillna(0)
    return df


def aggregate_by_account(df: pd.DataFrame) -> pd.DataFrame:
    """Total transaction amount per account."""
    return df.groupby("account_id")["amount"].sum().reset_index()

