import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('memory.db')


def init_memory() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                sql_query TEXT NOT NULL
            )
            '''
        )


def tokens(text: str) -> set[str]:
    return {part.strip(',.?').lower() for part in text.split() if part.strip(',.?')}


def similarity_score(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def retrieve_similar(question: str, limit: int = 2) -> list[tuple[float, str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute('SELECT question, sql_query FROM memories').fetchall()
    ranked = [(similarity_score(question, row[0]), row[0], row[1]) for row in rows]
    return [item for item in sorted(ranked, reverse=True)[:limit] if item[0] > 0]


def store_memory(question: str, sql_query: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO memories(question, sql_query) VALUES (?, ?)', (question, sql_query))


def generate_sql(question: str) -> str:
    if 'region' in question.lower():
        return 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    return 'SELECT * FROM sales;'


def main() -> None:
    init_memory()
    question = input('Question: ')
    similar = retrieve_similar(question)
    print('\nSimilar memories:')
    if not similar:
        print('No similar memories found.')
    for score, past_question, sql_query in similar:
        print(f'- score={score:.2f} question={past_question} sql={sql_query}')
    sql_query = generate_sql(question)
    store_memory(question, sql_query)
    print('\nGenerated SQL:')
    print(sql_query)


if __name__ == '__main__':
    main()
