import pandas as pd


def clean_sales_data(df):
    df = df.dropna(subset=["customer_id"]).copy()
    df["sales_amount"] = df["sales_amount"].fillna(0)
    return df
