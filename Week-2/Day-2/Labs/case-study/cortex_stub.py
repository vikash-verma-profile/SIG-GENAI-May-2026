"""
Snowflake Cortex Analyst maps natural language to SQL using semantic views
and governance metadata in the warehouse — analogous flow to nl2sql.py but
hosted inside Snowflake with entitlement-aware planners.

This module only documents the pattern for the case study; wire-up happens in SQL:

-- Example Snowflake-side pattern (run in worksheet):
-- CREATE SEMANTIC VIEW orders_sv AS ...
-- SELECT ANALYZE_SEMANTIC_VIEW(...) or Cortex Analyst REST/Warehouse APIs per account setup.
"""


def describe_cortex_flow() -> str:
    return (
        "1) Model curated semantic views on top of marts.\n"
        "2) Register descriptions, metrics, and dimensions Cortex can ground on.\n"
        "3) Route analyst prompts through Cortex instead of a local LLM when governance matters.\n"
        "4) Keep generated SQL compatible with your dbt contracts (Lab 3)."
    )
