# Lab 1 - Building Your First AI Agent for Data Engineering

## Objective
Create a basic AI agent that accepts a natural language question, generates a SQL query, and executes it against a sample SQLite database.

## Learning Outcomes

- Understand basic AI agent structure.
- Connect LLMs with Python.
- Build prompt-based SQL generation.
- Execute generated SQL safely.

## Architecture

```text
User Prompt -> AI Agent -> SQL Generator -> SQLite Database
```

## Files

- `setup_db.py`: Creates the sample `sales` table.
- `app.py`: Generates, validates, and executes SQL.
- `requirements.txt`: Python packages for the lab.

## Detailed Steps

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install packages.

   ```bash
   pip install -r requirements.txt
   ```

3. Create the sample database.

   ```bash
   python setup_db.py
   ```

4. Run the agent.

   ```bash
   python app.py
   ```

5. Ask a question.

   ```text
   Show total revenue by region
   ```

6. Confirm that the output resembles this SQL.

   ```sql
   SELECT region, SUM(revenue) AS total_revenue
   FROM sales
   GROUP BY region;
   ```

## Exercises

- Add filtering support.
- Add sorting support.
- Prevent DELETE queries.
- Add error handling for invalid SQL.
