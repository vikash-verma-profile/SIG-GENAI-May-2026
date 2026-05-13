# Lab 10 — OpenMetadata + AI integration

Build an **OpenMetadata-ready** description and tag patch, save it as JSON, and optionally **`PATCH`** a table entity if you have a running server and entity id.

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`
- Optional: [OpenMetadata](https://open-metadata.org/) Docker deployment on **`http://localhost:8585`**

## Setup

```bash
cd Labs/lab-10
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Connect OpenMetadata (conceptual)

The course doc sets `url = "http://localhost:8585"`. This lab uses the environment variable **`OPENMETADATA_BASE_URL`** for real calls, but always prints that default as a **hint** for local installs.

### Step 2 — Generate AI description

`app.py` embeds an example description: *Sales dataset containing transaction details.* In your own project, replace this string with output from Labs 3–4 / your LLM pipeline.

### Step 3 — Update metadata (artifact)

```bash
python app.py
```

This writes **`outputs/openmetadata_patch.json`** containing `description` and `tags`.

### Step 4 — (Optional) Live PATCH

Create a JWT or personal token in OpenMetadata (per your deployment docs), discover a table’s UUID from the API, then:

```powershell
$env:OPENMETADATA_BASE_URL = "http://localhost:8585"
$env:OPENMETADATA_TOKEN = "eyJ..."
$env:OPENMETADATA_TABLE_ID = "<uuid-from-api>"
python app.py
```

The exact JSON body fields may vary slightly by OpenMetadata version—adjust after reading the official OpenAPI docs for your server.

## Exercises

1. Push **AI-generated tags** from Lab 3 instead of static strings.
2. Add **glossary term** links using the glossary APIs.
3. Attach **lineage** from Lab 1 JSON to OpenMetadata lineage endpoints.

## Learning outcomes

- Treat the catalog as an **API-driven** system of record.
- Keep **generated text** in version-controlled artifacts before applying to production metadata.
