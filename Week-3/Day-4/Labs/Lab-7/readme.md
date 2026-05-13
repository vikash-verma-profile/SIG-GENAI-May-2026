# Lab 7 — AI-Generated Narrative Reporting

Convert dashboard KPIs into an executive narrative, sentiment label, and exportable report files.

## Setup

```bash
cd Labs/Lab-7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Open `data/kpi_metrics.json`.
2. Run `python app.py`.
3. Review the generated prompt, narrative, and sentiment in the console.
4. Inspect `outputs/executive_report.json` and `outputs/executive_report.txt`.

## Exercises

- Add month-over-month trend paragraphs.
- Export PDF reports.
- Replace the template narrative with an LLM using the built prompt.
