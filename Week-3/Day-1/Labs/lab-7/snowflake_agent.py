import os

try:
    import snowflake.connector
except ImportError:
    snowflake = None

BLOCKED = {'delete', 'drop', 'insert', 'update', 'alter', 'truncate'}


def validate_sql(sql_query: str) -> None:
    lowered = sql_query.lower().strip()
    if not lowered.startswith('select'):
        raise ValueError('Only SELECT statements are allowed.')
    if any(keyword in lowered for keyword in BLOCKED):
        raise ValueError('Unsafe SQL keyword detected.')


def build_sql(question: str) -> str:
    if 'metadata' in question.lower() or 'tables' in question.lower():
        return 'SHOW TABLES;'
    return 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'


def connect_snowflake():
    if snowflake is None:
        return None
    required = ['SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD', 'SNOWFLAKE_ACCOUNT']
    if not all(os.getenv(name) for name in required):
        return None
    return snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        account=os.environ['SNOWFLAKE_ACCOUNT'],
    )


def main() -> None:
    question = input('Question: ')
    sql_query = build_sql(question)
    if sql_query.lower().startswith('select'):
        validate_sql(sql_query)
    conn = connect_snowflake()
    if conn is None:
        print('Dry-run mode. Configure Snowflake credentials to execute.')
        print(sql_query)
        return
    cursor = conn.cursor()
    cursor.execute(sql_query)
    print(cursor.fetchall())
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
