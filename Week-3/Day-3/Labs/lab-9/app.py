"""
Lab 9 — Governance integration with DataHub (build MCP-style payload; optional HTTP post).

This lab avoids requiring a live DataHub instance. It writes a JSON payload you can
ingest later using the official DataHub CLI/SDK in your environment.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "datahub_dataset_payload.json"


def build_dataset_payload(urn: str, name: str, tags: list[str], description: str) -> dict[str, Any]:
    """Simplified structure for teaching — map fields to your DataHub version's MCP schema."""
    return {
        "entityType": "dataset",
        "entityUrn": urn,
        "aspects": {
            "globalTags": {"tags": [{"tag": t} for t in tags]},
            "editableDatasetProperties": {
                "description": description,
            },
        },
    }


def maybe_post(url: str, token: str | None, body: dict) -> None:
    if not url:
        print("DATAHUB_GMS_URL not set - skipping HTTP POST (artifact only).")
        return
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    # Real deployments use Metadata Service REST or Kafka; this is a placeholder hook.
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    print("POST status:", resp.status_code, resp.text[:500])


def main() -> None:
    metadata = {
        "table": "sales",
        "platform": "snowflake",
        "database": "analytics",
        "schema": "mart",
    }
    urn = (
        f"urn:li:dataset:(urn:li:dataPlatform:{metadata['platform']},"
        f"{metadata['table']},{metadata['schema']})"
    )
    body = build_dataset_payload(
        urn=urn,
        name=metadata["table"],
        tags=["finance", "lab-generated"],
        description="AI-enriched sales mart dataset (lab demo).",
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(body, indent=2), encoding="utf-8")
    print("Wrote payload:", OUT_PATH)
    print("Metadata payload preview:\n", json.dumps(body, indent=2)[:800], "...")

    gms = os.environ.get("DATAHUB_GMS_URL")
    token = os.environ.get("DATAHUB_TOKEN")
    maybe_post(gms or "", token, body)
    if not gms:
        print('Example: set DATAHUB_GMS_URL to your GMS "ingest" compatible endpoint for experiments.')


if __name__ == "__main__":
    main()
