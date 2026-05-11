"""
Lab 10: Self-healing pipeline skeleton with LangGraph (detect -> diagnose -> fix -> alert).
"""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    error: str
    fix: str
    recovered: bool


def detect_failure(state: State) -> dict:
    return {"error": "Null spike detected"}


def diagnose(state: State) -> dict:
    return {"fix": "Apply null filtering"}


def apply_fix(state: State) -> dict:
    print("Fix applied:", state.get("fix"))
    return {"recovered": True}


def alert(state: State) -> dict:
    if state.get("recovered"):
        print("Pipeline recovered. Alert: OK")
    else:
        print("Pipeline not recovered. Alert: ESCALATE")
    return {}


def build_graph():
    g = StateGraph(State)
    g.add_node("detect", detect_failure)
    g.add_node("diagnose", diagnose)
    g.add_node("fix", apply_fix)
    g.add_node("alert", alert)
    g.add_edge(START, "detect")
    g.add_edge("detect", "diagnose")
    g.add_edge("diagnose", "fix")
    g.add_edge("fix", "alert")
    g.add_edge("alert", END)
    return g.compile()


def main() -> None:
    app = build_graph()
    result = app.invoke({"error": "", "fix": "", "recovered": False})
    print("\nFinal state:", result)


if __name__ == "__main__":
    main()
