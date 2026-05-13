"""
Lab 10 — OpenMetadata + AI integration (build PATCH body; optional API call).

OpenMetadata typically runs at http://localhost:8585 for local trials.
This script writes a JSON request body you can apply via the UI or REST.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "outputs" / "openmetadata_patch.json"


def build_description_patch(description: str, tags: list[str]) -> dict[str, Any]:
    return {
        "description": description,
        "tags": [{"tagFQN": t} for t in tags],
    }


def maybe_patch(base_url: str, token: str | None, entity_id: str | None, body: dict) -> None:
    if not base_url or not entity_id:
        print("OPENMETADATA_BASE_URL / OPENMETADATA_TABLE_ID not set - skipping PATCH.")
        return
    url = f"{base_url.rstrip('/')}/api/v1/tables/{entity_id}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.patch(url, headers=headers, json=body, timeout=30)
    print("PATCH status:", resp.status_code, resp.text[:500])


def main() -> None:
    base_url = os.environ.get("OPENMETADATA_BASE_URL", "http://localhost:8585")
    description = "Sales dataset containing transaction details (AI-enriched lab text)."
    body = build_description_patch(description, tags=["Finance", "lab-demo"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(body, indent=2), encoding="utf-8")
    print("Default UI URL hint:", base_url)
    print("Wrote:", OUT_PATH)
    print(json.dumps(body, indent=2))

    om_url = os.environ.get("OPENMETADATA_BASE_URL")
    token = os.environ.get("OPENMETADATA_TOKEN")
    table_id = os.environ.get("OPENMETADATA_TABLE_ID")
    maybe_patch(om_url or "", token, table_id, body)


if __name__ == "__main__":
    main()
