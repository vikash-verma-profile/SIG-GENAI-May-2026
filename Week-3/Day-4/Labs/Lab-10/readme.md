# Lab 10 — LangGraph Self-Healing Workflow

Orchestrate detect, diagnose, fix, and verify steps as a stateful LangGraph workflow with a simple retry branch.

## Setup

```bash
cd Labs/Lab-10
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Steps

1. Read `app.py` and note the `State` fields and graph nodes.
2. Run `python app.py`.
3. Confirm fix application and final workflow state in the console.
4. Open `outputs/workflow_state.json`.

## Exercises

- Add a human-approval node before applying fixes.
- Persist workflow memory between runs.
- Connect detection input to real pipeline logs from Lab 1.
