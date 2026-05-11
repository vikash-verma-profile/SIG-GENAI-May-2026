import json
import logging
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).with_name('observability.db')
LOG_PATH = Path(__file__).with_name('agent.log')

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(message)s')


def prepare_database() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DROP TABLE IF EXISTS sales')
        conn.execute('CREATE TABLE sales(region TEXT, revenue INTEGER)')
        conn.executemany(
            'INSERT INTO sales(region, revenue) VALUES (?, ?)',
            [('North', 1000), ('South', 2000), ('East', 3000), ('West', 1500)],
        )


def generate_sql(question: str) -> tuple[str, str]:
    reasoning = 'The question asks for revenue aggregation by region.'
    sql_query = 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    return reasoning, sql_query


def main() -> None:
    prepare_database()
    question = input('Question: ')
    reasoning, sql_query = generate_sql(question)
    start = time.perf_counter()
    status = 'success'
    error = None
    try:
        with sqlite3.connect(DB_PATH) as conn:
            results = conn.execute(sql_query).fetchall()
    except Exception as exc:
        status = 'failure'
        error = str(exc)
        results = []
    execution_time_ms = (time.perf_counter() - start) * 1000
    event = {
        'user_prompt': question,
        'reasoning': reasoning,
        'generated_sql': sql_query,
        'execution_time_ms': round(execution_time_ms, 3),
        'status': status,
        'error': error,
    }
    logging.info(json.dumps(event))
    print('Results:', results)
    print(f'Log written to {LOG_PATH}')


if __name__ == '__main__':
    main()
