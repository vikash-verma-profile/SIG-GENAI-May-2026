import os
import re
import sqlite3
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

DB_PATH = Path(__file__).with_name('database.db')
TABLE_SCHEMA = 'sales(id, region, revenue)'
BLOCKED_KEYWORDS = {'delete', 'drop', 'insert', 'update', 'alter', 'truncate'}


def fallback_sql(question: str) -> str:
    text = question.lower()
    if 'total' in text and 'region' in text:
        return 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    if 'highest' in text or 'top' in text or 'max' in text:
        return 'SELECT region, revenue FROM sales ORDER BY revenue DESC LIMIT 1;'
    return 'SELECT id, region, revenue FROM sales;'


def generate_sql(question: str) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or OpenAI is None:
        return fallback_sql(question)

    client = OpenAI(api_key=api_key)
    prompt = f'''
Convert the following question into one SQLite SELECT query.
Return only SQL and no markdown.

Question: {question}
Table: {TABLE_SCHEMA}
'''
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.choices[0].message.content.strip()


def validate_sql(sql_query: str) -> None:
    normalized = re.sub(r'\s+', ' ', sql_query.strip().lower())
    if not normalized.startswith('select'):
        raise ValueError('Only SELECT statements are allowed.')
    if any(keyword in normalized for keyword in BLOCKED_KEYWORDS):
        raise ValueError('Unsafe SQL keyword detected.')


def execute_sql(sql_query: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit('Run setup_db.py before running app.py')

    question = input('Ask your question: ')
    sql_query = generate_sql(question)
    validate_sql(sql_query)
    results = execute_sql(sql_query)

    print('\nGenerated SQL:')
    print(sql_query)
    print('\nResults:')
    for row in results:
        print(row)


if __name__ == '__main__':
    main()
