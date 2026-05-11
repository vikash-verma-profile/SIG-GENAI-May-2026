# Lab 8 — AI-Assisted Remediation Engine

Detect invalid emails, print human-style remediation suggestions, and apply safe deterministic transforms.

## Learning outcomes

- Separate **detection**, **suggestion**, and **apply** phases.
- Use string normalization (`strip`, `lower`) as an automatic fix where appropriate.
- Leave hooks for an LLM (`suggest_fix`) without sending data until you configure keys.

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-8
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Run the remediation demo

```bash
python main.py
```

Flow:

1. Build a tiny dataframe with one valid-looking email with odd casing and one invalid value.
2. List invalid emails and print `suggest_fix()` text for each (stub for LLM output).
3. Lowercase and strip all emails.
4. Replace a known bad token with a placeholder domain for manual review.

## Step 3 — Expected output

- Invalid email listing and suggestion strings.
- Before/after dataframes printed after normalization and placeholder replacement.

## Exercises

1. Call OpenAI (or another provider) inside `suggest_fix` using an API key from an environment variable; **review** model output before applying.
2. Add a `confidence` float column when using a model (parse structured JSON from the model).
3. Implement approval: only write remediated CSV if `APPROVE_REMEDIATION=1` in the environment.

## Files

- `main.py` — detection + suggestions + simple corrections.
