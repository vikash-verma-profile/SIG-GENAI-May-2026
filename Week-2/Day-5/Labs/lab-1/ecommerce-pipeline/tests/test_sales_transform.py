import pandas as pd

from pipeline.sales_transform import clean_sales_data


def test_clean_sales_data():
    data = {
        "customer_id": [1, None],
        "sales_amount": [100, None],
    }
    df = pd.DataFrame(data)
    result = clean_sales_data(df)
    assert len(result) == 1


def test_positive_keeps_valid_rows():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "sales_amount": [10.5, 20.0, 30.0],
        }
    )
    result = clean_sales_data(df)
    assert len(result) == 3
    assert result["sales_amount"].tolist() == [10.5, 20.0, 30.0]


def test_null_customer_rows_removed():
    df = pd.DataFrame(
        {
            "customer_id": [1, None, 2],
            "sales_amount": [100, 200, 300],
        }
    )
    result = clean_sales_data(df)
    assert len(result) == 2
    assert result["customer_id"].notna().all()


def test_null_sales_amount_filled_with_zero():
    df = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "sales_amount": [None, 50.0],
        }
    )
    result = clean_sales_data(df)
    assert result.loc[result["customer_id"] == 1, "sales_amount"].iloc[0] == 0
    assert result.loc[result["customer_id"] == 2, "sales_amount"].iloc[0] == 50.0


def test_empty_dataframe():
    df = pd.DataFrame(columns=["customer_id", "sales_amount"])
    result = clean_sales_data(df)
    assert len(result) == 0


def test_all_customer_ids_null_returns_empty():
    df = pd.DataFrame(
        {
            "customer_id": [None, None],
            "sales_amount": [1.0, 2.0],
        }
    )
    result = clean_sales_data(df)
    assert len(result) == 0


def test_single_valid_row():
    df = pd.DataFrame({"customer_id": [42], "sales_amount": [99.99]})
    result = clean_sales_data(df)
    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == 42
