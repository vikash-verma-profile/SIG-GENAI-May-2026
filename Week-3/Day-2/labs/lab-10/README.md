# Lab 10 — Self-Healing Pipeline using LangGraph

Model a minimal **detect → diagnose → fix → alert** workflow as a stateful graph.

## Learning outcomes

- Define graph `State` with `TypedDict`.
- Wire nodes with `StateGraph`, `START`, and `END`.
- `invoke` a run and inspect final state (foundation for retries, memory, and external integrations).

## Prerequisites

- Python 3.11+

## Step 1 — Environment

```bash
cd labs/lab-10
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2 — Read the graph

Open `main.py`. Nodes return **partial** state updates (dictionaries) that LangGraph merges into `State`.

## Step 3 — Run the workflow

```bash
python main.py
```

You should see:

- `Fix applied: Apply null filtering`
- `Pipeline recovered. Alert: OK`
- Printed final state with `error`, `fix`, and `recovered=True`.

## Step 4 — Architecture (conceptual)

```text
Detect -> Diagnose -> Fix -> Re-run (exercise) -> Alert
```

This lab implements detect/diagnose/fix/alert only; add a real “re-run” node that calls your batch job or DAG task in exercises.

## Exercises

1. Add **retry** logic: route back to `detect` until `recovered` or max attempts.
2. On failure after max retries, print a Slack-style payload dict (no secrets in code).
3. Add **checkpointing** / persistence using LangGraph persistence APIs (see current LangGraph docs).
4. Integrate a warehouse-specific healing action (for example Snowflake Cortex) as a separate node behind an interface.

## Files

- `main.py` — graph definition and `main()` entrypoint.
- `requirements.txt` — `langgraph` and `langchain-core`.
