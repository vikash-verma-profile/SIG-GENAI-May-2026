# Lab 5 - Multi-Agent SQL Pipeline using CrewAI

## Objective
Build collaborative SQL agents for generation, review, and execution.

## Agents

- SQL Generator Agent: creates SQL.
- Reviewer Agent: optimizes and validates SQL.
- Execution Agent: runs queries.

## Detailed Steps

1. Install CrewAI if extending the starter.

   ```bash
   pip install -r requirements.txt
   ```

2. Run the local multi-agent pipeline.

   ```bash
   python crew_pipeline.py
   ```

3. Ask: `Show total revenue by region`.

4. Review each agent handoff in the output.

## Exercises

- Add a validation agent.
- Add governance checks.
- Add retry mechanism.
- Convert the local classes to CrewAI agents and tasks.
