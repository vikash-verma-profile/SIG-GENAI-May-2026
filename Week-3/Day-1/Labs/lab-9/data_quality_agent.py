from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).with_name('sales.csv')
REPORT_PATH = Path(__file__).with_name('quality_report.md')
REQUIRED_COLUMNS = {'id', 'region', 'revenue'}


def severity(issue_count: int) -> str:
    if issue_count == 0:
        return 'low'
    if issue_count <= 2:
        return 'medium'
    return 'high'


def run_checks(df: pd.DataFrame) -> dict[str, object]:
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    null_counts = df.isnull().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())
    invalid_revenue = 0
    if 'revenue' in df.columns:
        invalid_revenue = int(pd.to_numeric(df['revenue'], errors='coerce').isnull().sum())
    return {
        'missing_columns': missing_columns,
        'null_counts': null_counts,
        'duplicate_rows': duplicate_rows,
        'invalid_revenue_values': invalid_revenue,
    }


def build_report(checks: dict[str, object]) -> str:
    issue_count = len(checks['missing_columns']) + checks['duplicate_rows'] + checks['invalid_revenue_values']
    issue_count += sum(1 for value in checks['null_counts'].values() if value)
    level = severity(issue_count)
    return f'''# Data Quality Report

## Summary

Severity: {level}

## Issues Found

- Missing columns: {checks['missing_columns']}
- Null counts: {checks['null_counts']}
- Duplicate rows: {checks['duplicate_rows']}
- Invalid revenue values: {checks['invalid_revenue_values']}

## Recommendations

- Fill or remove rows with missing required values.
- Remove duplicate records or define a deduplication rule.
- Enforce numeric validation on revenue before loading data.
'''


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    checks = run_checks(df)
    report = build_report(checks)
    REPORT_PATH.write_text(report, encoding='utf-8')
    print(report)
    print(f'Report written to {REPORT_PATH}')


if __name__ == '__main__':
    main()
