import pandas as pd

from pipeline.claims_transform import normalize_claim_amount


def test_normalize_claim_amount_non_negative():
    df = pd.DataFrame({"claim_amount": [-10, 100]})
    result = normalize_claim_amount(df)
    assert result["claim_amount"].min() >= 0
