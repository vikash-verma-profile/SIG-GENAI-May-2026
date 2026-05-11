import sqlite3
from dataclasses import dataclass
from pathlib import Path

DB_PATH = Path(__file__).with_name('crew_sales.db')


@dataclass
class ReviewResult:
    approved: bool
    notes: str
    sql_query: str


class SQLGeneratorAgent:
    role = 'SQL Generator'

    def run(self, question: str) -> str:
        if 'region' in question.lower():
            return 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
        return 'SELECT id, region, revenue FROM sales;'


class ReviewerAgent:
    role = 'Reviewer'

    def run(self, sql_query: str) -> ReviewResult:
        lowered = sql_query.lower().strip()
        if not lowered.startswith('select'):
            return ReviewResult(False, 'Rejected: only SELECT is allowed.', sql_query)
        if 'select *' in lowered:
            optimized = 'SELECT id, region, revenue FROM sales;'
            return ReviewResult(True, 'Approved after replacing SELECT * with explicit columns.', optimized)
        return ReviewResult(True, 'Approved.', sql_query)


class ExecutionAgent:
    role = 'Execution'

    def run(self, sql_query: str) -> list[tuple]:
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute(sql_query).fetchall()


def prepare_database() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DROP TABLE IF EXISTS sales')
        conn.execute('CREATE TABLE sales(id INTEGER PRIMARY KEY, region TEXT, revenue INTEGER)')
        conn.executemany(
            'INSERT INTO sales(region, revenue) VALUES (?, ?)',
            [('North', 1000), ('South', 2000), ('East', 3000), ('West', 1500)],
        )


def main() -> None:
    prepare_database()
    question = input('Question: ')
    generator = SQLGeneratorAgent()
    reviewer = ReviewerAgent()
    executor = ExecutionAgent()
    sql_query = generator.run(question)
    review = reviewer.run(sql_query)
    print(f'{generator.role}: {sql_query}')
    print(f'{reviewer.role}: {review.notes}')
    if not review.approved:
        raise SystemExit('Pipeline stopped by reviewer.')
    print(f'{executor.role}: {executor.run(review.sql_query)}')


if __name__ == '__main__':
    main()
