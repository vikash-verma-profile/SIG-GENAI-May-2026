# Capstone Architecture Notes

## Components

- Gateway API: receives user requests and validates payloads.
- SQL Generator Agent: converts natural language into SQL.
- Review Agent: checks safety, governance, and optimization opportunities.
- Execution Agent: runs approved SQL against Snowflake or a local database.
- Memory Store: saves prior questions and generated SQL.
- Observability Layer: records reasoning, SQL, timings, and failures.

## Production Extensions

- Replace the local runner with LangGraph.
- Replace local memory with ChromaDB.
- Replace SQLite execution with Snowflake MCP or the Snowflake connector.
- Add a human approval queue for high-risk queries.
- Send failures and high-cost queries to Slack.
