# Lab 6 - LangGraph Stateful Workflow

## Objective
Build a stateful AI workflow with graph-style orchestration.

## Learning Outcomes

- Create graph-based orchestration.
- Maintain workflow state.
- Add branching logic.

## Detailed Steps

1. Install dependencies if implementing with LangGraph.

   ```bash
   pip install -r requirements.txt
   ```

2. Run the local graph-style workflow.

   ```bash
   python stateful_workflow.py
   ```

3. Enter a question and inspect the final state.

## Exercises

- Add a retry edge.
- Add an execution node.
- Add an error node.
- Convert the local runner to LangGraph `StateGraph`.
