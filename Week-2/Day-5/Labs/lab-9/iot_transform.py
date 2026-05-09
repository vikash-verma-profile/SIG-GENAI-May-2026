"""Manufacturing IoT ETL stub for Azure DevOps pipeline."""

import pandas as pd


def filter_sensor_noise(df: pd.DataFrame, column: str = "reading") -> pd.DataFrame:
    return df[df[column].notna()].copy()
