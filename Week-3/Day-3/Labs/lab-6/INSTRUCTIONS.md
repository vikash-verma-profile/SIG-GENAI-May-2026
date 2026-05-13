# Lab 6 — AI-based governance policy generation

Turn a short **governance context** block into a **policy draft** using an LLM, with a **safe offline template** if no API key is set.

## Prerequisites

- Python 3.11+
- Optional: `OPENAI_API_KEY`, `OPENAI_MODEL`

## Setup

```bash
cd Labs/lab-6
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

### Step 1 — Define governance context

Open `app.py` and read the `context` triple-quoted string (PII, encryption, access roles). Replace with your own scenario for exercises.

### Step 2 — Create the prompt

`draft_policy()` wraps that context in instructions for a concise bullet-list policy.

### Step 3 — Generate the policy

```bash
python app.py
```

- **With API key**: model-generated draft.
- **Without**: deterministic template echoing the context with standard bullets.

### Step 4 — Review output

Open `outputs/policy_draft.txt`. In real workflows, this file would feed **legal review**, not production enforcement directly.

## Exercises

1. **Retention**: add a second function `draft_retention_policy(years: int)`.
2. **HIPAA / GDPR**: parameterize regime name and adjust prompt constraints.
3. **Versioning**: append timestamp and hash of context to the filename.

## Learning outcomes

- Practice **policy-as-text** generation under guardrails.
- Separate **model output** from **human approval**.
