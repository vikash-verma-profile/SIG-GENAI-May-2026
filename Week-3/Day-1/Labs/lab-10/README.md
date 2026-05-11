# Lab 10 - Enterprise Capstone Project

## Objective
Build a complete Agentic AI Data Engineering Platform.

## System Requirements

The platform must:

- Accept natural language requests.
- Generate SQL.
- Review SQL.
- Execute against Snowflake or a local placeholder.
- Log reasoning.
- Store memory.
- Validate governance.

## Architecture

```text
User -> Gateway API -> Stateful Workflow -> SQL Generator Agent -> Review Agent -> Execution Agent -> Observability Dashboard
```

## Detailed Steps

1. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

2. Run the capstone starter.

   ```bash
   python capstone_platform.py
   ```

3. Enter a natural language request.

4. Review the final workflow state.

5. Open `capstone.log` and `memory.jsonl`.

## Core Features

- Multi-agent workflow.
- Stateful orchestration.
- RAG memory.
- Logging.
- Retry handling.

## Advanced Features

- Human approval workflow.
- Cost tracking.
- Query optimization.
- Slack notifications.
- Dashboard visualization.

## Deliverables

- Source code.
- Architecture diagram.
- Logs.
- Demo video.
- README documentation.
