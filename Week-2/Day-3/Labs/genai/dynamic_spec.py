"""
Runtime pipeline tuning via Ollama — returns validated JSON only.

Design goals:
- AI-enabled: parameters can change run-to-run based on model + intent.
- Safe: never `exec` model output; only whitelisted keys apply.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd

from genai.json_extract import extract_json_object
from genai.ollama_client import chat

SYSTEM_JSON_ONLY = (
    "You are a careful data pipeline planner. Reply with ONE JSON object only. "
    "No markdown fences, no commentary outside JSON."
)


def dataframe_summary(df: pd.DataFrame, max_rows_sample: int = 3) -> str:
    lines = [
        f"rows={len(df)} cols={len(df.columns)}",
        "columns: " + ", ".join(df.columns.astype(str).tolist()),
        "dtypes:\n" + df.dtypes.astype(str).to_string(),
        "null_counts:\n" + df.isnull().sum().astype(str).to_string(),
        "head:\n" + df.head(max_rows_sample).to_string(index=False),
    ]
    return "\n".join(lines)


def healthcare_cleaning_spec(
    summary: str,
    user_intent: str | None,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    defaults = {"age_missing_strategy": "mean", "billing_missing_fill": 0.0}
    intent = user_intent or os.environ.get(
        "PIPELINE_AI_INTENT",
        "Healthcare billing aggregates; handle missing age and billing safely.",
    )
    user = f"""Lab: healthcare patients CSV.

Dataset summary:
{summary}

User intent:
{intent}

Return JSON with exactly these keys:
- age_missing_strategy: string, one of "mean" or "median"
- billing_missing_fill: number (use 0 if unsure)

Suggested defaults: {defaults}
"""
    raw = chat(
        [{"role": "system", "content": SYSTEM_JSON_ONLY}, {"role": "user", "content": user}],
        model=model,
    )
    spec = extract_json_object(raw)

    strat = spec.get("age_missing_strategy", defaults["age_missing_strategy"])
    if strat not in ("mean", "median"):
        strat = defaults["age_missing_strategy"]

    fill = spec.get("billing_missing_fill", defaults["billing_missing_fill"])
    try:
        fill_f = float(fill)
    except (TypeError, ValueError):
        fill_f = float(defaults["billing_missing_fill"])

    return {"age_missing_strategy": strat, "billing_missing_fill": fill_f}


def retail_cleaning_spec(
    summary: str,
    user_intent: str | None,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    defaults = {"quantity_missing_fill": 1.0, "price_missing_fill": 0.0, "filter_non_positive_price": True}
    intent = user_intent or os.environ.get(
        "PIPELINE_AI_INTENT",
        "Retail revenue by category and daily order counts.",
    )
    user = f"""Lab: retail orders CSV.

Dataset summary:
{summary}

User intent:
{intent}

Return JSON with exactly these keys:
- quantity_missing_fill: number (typically 1)
- price_missing_fill: number (typically 0)
- filter_non_positive_price: boolean

Suggested defaults: {defaults}
"""
    raw = chat(
        [{"role": "system", "content": SYSTEM_JSON_ONLY}, {"role": "user", "content": user}],
        model=model,
    )
    spec = extract_json_object(raw)

    q = spec.get("quantity_missing_fill", defaults["quantity_missing_fill"])
    p = spec.get("price_missing_fill", defaults["price_missing_fill"])
    f = spec.get("filter_non_positive_price", defaults["filter_non_positive_price"])

    try:
        q_f = float(q)
    except (TypeError, ValueError):
        q_f = float(defaults["quantity_missing_fill"])
    try:
        p_f = float(p)
    except (TypeError, ValueError):
        p_f = float(defaults["price_missing_fill"])
    if not isinstance(f, bool):
        f = bool(f)

    return {"quantity_missing_fill": q_f, "price_missing_fill": p_f, "filter_non_positive_price": f}


def read_csv_header_line(csv_path: Path) -> str:
    with open(csv_path, encoding="utf-8") as f:
        return f.readline().strip()


def lab2_watermark_spec(
    csv_header_line: str,
    current_last_run_date: str,
    user_intent: str | None,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    intent = user_intent or os.environ.get(
        "PIPELINE_AI_INTENT",
        "Incremental bronze ingest: filter rows where visit_date > last_run_date.",
    )
    user = f"""PySpark medallion lab (bronze incremental filter).

CSV header line:
{csv_header_line}

Current YAML last_run_date:
{current_last_run_date}

Intent:
{intent}

Return JSON with exactly one key:
- last_run_date: string YYYY-MM-DD

If unsure, use "{current_last_run_date}".
"""
    raw = chat(
        [{"role": "system", "content": SYSTEM_JSON_ONLY}, {"role": "user", "content": user}],
        model=model,
    )
    spec = extract_json_object(raw)
    val = spec.get("last_run_date", current_last_run_date)
    if not isinstance(val, str):
        val = current_last_run_date
    parts = val.split("-")
    if len(parts) != 3 or len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        val = current_last_run_date
    return {"last_run_date": val}
