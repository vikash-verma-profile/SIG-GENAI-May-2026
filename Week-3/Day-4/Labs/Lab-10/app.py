"""
Lab 10 — LangGraph self-healing workflow with detect, diagnose, and fix nodes.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"


class State(TypedDict):
    issue: str
    fix: str
    status: str
    retries: int


def detect(state: State) -> State:
    state["issue"] = "Schema Drift"
    state["status"] = "detected"
    return state


def diagnose(state: State) -> State:
    if state["issue"] == "Schema Drift":
        state["fix"] = "Update schema mapping"
    else:
        state["fix"] = "Escalate to on-call"
    state["status"] = "diagnosed"
    return state


def apply_fix(state: State) -> State:
    print(f"Fix applied: {state['fix']}")
    state["status"] = "fixed"
    return state


def verify(state: State) -> State:
    state["status"] = "success"
    return state


def should_retry(state: State) -> str:
    if state["status"] != "success" and state["retries"] < 2:
        return "retry"
    return "done"


def increment_retry(state: State) -> State:
    state["retries"] += 1
    state["status"] = "retrying"
    return state


def build_workflow():
    workflow = StateGraph(State)
    workflow.add_node("detect", detect)
    workflow.add_node("diagnose", diagnose)
    workflow.add_node("apply_fix", apply_fix)
    workflow.add_node("verify", verify)
    workflow.add_node("increment_retry", increment_retry)

    workflow.add_edge(START, "detect")
    workflow.add_edge("detect", "diagnose")
    workflow.add_edge("diagnose", "apply_fix")
    workflow.add_edge("apply_fix", "verify")
    workflow.add_conditional_edges("verify", should_retry, {"retry": "increment_retry", "done": END})
    workflow.add_edge("increment_retry", "detect")
    return workflow.compile()


def main() -> None:
    graph = build_workflow()
    initial_state: State = {"issue": "", "fix": "", "status": "new", "retries": 0}
    final_state = graph.invoke(initial_state)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "workflow_state.json"
    out_path.write_text(json.dumps(final_state, indent=2), encoding="utf-8")
    print("Final workflow state:", final_state)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
