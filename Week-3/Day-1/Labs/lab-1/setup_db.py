import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('database.db')

rows = [
    ('North', 1000),
    ('South', 2000),
    ('East', 3000),
    ('West', 1500),
]

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS sales')
    cursor.execute(
        '''
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            revenue INTEGER NOT NULL
        )
        '''
    )
    cursor.executemany('INSERT INTO sales(region, revenue) VALUES (?, ?)', rows)
    conn.commit()

print(f'Created sample database at {DB_PATH}')
