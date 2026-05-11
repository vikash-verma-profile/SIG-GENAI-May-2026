# Lab 9 — AI-Based PII Detection (Regex Foundations)

Classify sensitive-looking fields using regular expressions and attach governance-style labels.

## Learning outcomes

- Match common **patterns** for email and phone (teaching heuristics only).
- Extend with Aadhaar-like and credit-card-like **format** checks (not cryptographic validity).
- Add a coarse `classification` column for downstream policy engines.

## Prerequisites

- Python 3.11+

## Important disclaimer

Regex matching is **not** sufficient for legal/compliance-grade PII discovery. Use dedicated DLP tools and legal review for production.

## Step 1 — Environment

```bash
cd labs/lab-9
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Review patterns

Open `main.py` and read `EMAIL_PATTERN`, `PHONE_PATTERN`, `AADHAAR_PATTERN`, and `CARD_PATTERN`.

## Step 3 — Run detection

```bash
python main.py
```

Each original column gets a companion `*_tags` column with comma-separated labels.

## Step 4 — Expected output

- A single printed dataframe showing tags per cell value and `classification = Confidential`.

## Exercises

1. Tighten phone rules for your locale.
2. Implement Luhn for card-like strings before tagging `PII_CARD_FORMAT`.
3. Integrate a vendor DLP SDK or scanner and compare results to regex tags.

## Files

- `main.py` — regex detectors and tagging.
