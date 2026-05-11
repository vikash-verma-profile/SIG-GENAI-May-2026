# Lab 7 - Snowflake MCP Integration

## Objective
Connect AI agents with Snowflake-style execution while protecting credentials and query safety.

## Learning Outcomes

- Execute AI-generated SQL safely.
- Access metadata.
- Secure credentials.

## Detailed Steps

1. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

2. Set Snowflake credentials when available.

   ```bash
   set SNOWFLAKE_USER=your_user
   set SNOWFLAKE_PASSWORD=your_password
   set SNOWFLAKE_ACCOUNT=your_account
   ```

3. Run the agent.

   ```bash
   python snowflake_agent.py
   ```

4. Without credentials, the script runs in dry-run mode.

## Exercises

- Add RBAC validation.
- Add unsafe query detection.
- Add schema discovery.
- Connect to Snowflake MCP when available.
