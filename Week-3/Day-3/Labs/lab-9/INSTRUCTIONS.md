# Lab 9 — Governance integration with DataHub

Prepare a **dataset metadata payload** suitable for pushing into **[DataHub](https://datahubproject.io/)**, and optionally attempt an HTTP POST if your instructor provides a gateway URL.

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`
- Optional: running DataHub stack and credentials (advanced)

## Course doc vs this repo

The original material mentions:

```bash
pip install acryl-datahub
```

The full **`acryl-datahub`** SDK is powerful but heavy for a first exercise. This lab uses **`requests`** plus a **JSON artifact** so every student can finish locally. Your instructor can swap in the official emitter examples later.

## Setup

```bash
cd Labs/lab-9
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Inspect the metadata payload builder

Open `app.py` and read `build_dataset_payload`. It groups **URN**, **tags**, and **description** the way many ingestion tutorials do (simplified).

### Step 2 — Generate the JSON file

```bash
python app.py
```

This always writes **`outputs/datahub_dataset_payload.json`**.

### Step 3 — (Optional) Push metadata

If your environment exposes a compatible HTTP ingest endpoint, try:

```powershell
$env:DATAHUB_GMS_URL = "https://example-gms/..."   # instructor-supplied
$env:DATAHUB_TOKEN = "..."                         # if required
python app.py
```

Without these variables, the script **skips the network call** by design.

## Exercises

1. Add **lineage** edges to the payload structure (upstream datasets).
2. Attach **PII tags** derived from Lab 5 outputs.
3. Integrate **business glossary** terms from Lab 4 as glossaryTerm associations.

## Learning outcomes

- Understand **URNs** and **aspects** mentally before clicking UIs.
- Separate **payload construction** from **transport** (REST, Kafka, CLI).
