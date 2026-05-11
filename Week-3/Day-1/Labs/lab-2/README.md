# Lab 2 - ReAct Pattern Agent

## Objective
Implement ReAct reasoning for a SQL agent.

## Learning Outcomes

- Implement reasoning loops.
- Use observation feedback.
- Improve SQL generation quality.
- Store reasoning logs.

## Architecture

```text
Thought -> Action -> Observation -> Reflection
```

## Detailed Steps

1. Run the lab.

   ```bash
   python react_agent.py
   ```

2. Enter this prompt.

   ```text
   Show total revenue by region
   ```

3. Review the printed trace: Thought, Action, SQL, Observation, and Reflection.

4. Open `reasoning.log` to inspect the saved reasoning trace.

## Exercises

- Add a retry loop.
- Add SQL validation.
- Store reasoning logs as JSON.
