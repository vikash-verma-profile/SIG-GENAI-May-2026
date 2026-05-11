# Lab 8 - AI Observability and Logging

## Objective
Track reasoning and execution for auditability.

## Learning Outcomes

- Capture AI reasoning.
- Build audit logs.
- Track failures.

## Logging Schema

| Field | Description |
| --- | --- |
| `user_prompt` | User question |
| `reasoning` | Agent thoughts |
| `generated_sql` | SQL created |
| `execution_time_ms` | Query duration |
| `status` | Success or failure |

## Detailed Steps

1. Run the observability agent.

   ```bash
   python observability_agent.py
   ```

2. Ask a question.

3. Open `agent.log` and inspect the JSON record.

## Exercises

- Add structured JSON logging.
- Add a monitoring dashboard.
- Add error tracking.
- Add token and cost tracking.
