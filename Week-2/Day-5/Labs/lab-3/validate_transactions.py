"""
Banking transactions schema validation (Great Expectations).

Lab steps also cover CLI: `great_expectations init`, suite/checkpoint setup,
and `great_expectations checkpoint run transactions_checkpoint`.
This script runs the same expectation (`customer_id` not null) programmatically.
"""

from pathlib import Path

import pandas as pd
import great_expectations as gx
from great_expectations.expectations import ExpectColumnValuesToNotBeNull


def main() -> None:
    root = Path(__file__).resolve().parent
    csv_path = root / "data" / "transactions.csv"
    df = pd.read_csv(csv_path)

    context = gx.get_context(mode="ephemeral")
    datasource = context.data_sources.add_pandas("banking_transactions")
    asset = datasource.add_dataframe_asset(name="transactions_batch")
    batch_def = asset.add_batch_definition_whole_dataframe("whole")
    batch = batch_def.get_batch(batch_parameters={"dataframe": df})

    expectation = ExpectColumnValuesToNotBeNull(column="customer_id")
    result = batch.validate(expectation)

    print("Validation result:", "PASS" if result.success else "FAIL (expected: bad rows)")
    print(result)


if __name__ == "__main__":
    main()
