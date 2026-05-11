import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).with_name('optimizer.db')


def prepare_database() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DROP TABLE IF EXISTS sales')
        conn.execute('CREATE TABLE sales(region TEXT, revenue INTEGER)')
        conn.executemany(
            'INSERT INTO sales(region, revenue) VALUES (?, ?)',
            [('North', 1000), ('South', 2000), ('East', 3000), ('West', 1500)],
        )


def standard_sql(question: str) -> str:
    return 'SELECT * FROM sales;'


def cot_sql(question: str) -> tuple[str, str]:
    reasoning = (
        '1. The question asks for total revenue.\n'
        '2. Revenue must be aggregated with SUM.\n'
        '3. Region is the grouping column.'
    )
    sql_query = 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    return reasoning, sql_query


def complexity_score(sql_query: str) -> int:
    keywords = ['join', 'group by', 'order by', 'where', 'having', 'limit']
    lowered = sql_query.lower()
    return 1 + sum(1 for keyword in keywords if keyword in lowered)


def benchmark(sql_query: str) -> tuple[list[tuple], float]:
    start = time.perf_counter()
    with sqlite3.connect(DB_PATH) as conn:
        results = conn.execute(sql_query).fetchall()
    duration_ms = (time.perf_counter() - start) * 1000
    return results, duration_ms


def main() -> None:
    prepare_database()
    question = input('Question: ')
    direct = standard_sql(question)
    reasoning, optimized = cot_sql(question)
    results, duration_ms = benchmark(optimized)

    print('\nStandard SQL:')
    print(direct)
    print('\nReasoning:')
    print(reasoning)
    print('\nCoT SQL:')
    print(optimized)
    print(f'Complexity score: {complexity_score(optimized)}')
    print(f'Benchmark: {duration_ms:.3f} ms')
    print('Results:', results)


if __name__ == '__main__':
    main()
