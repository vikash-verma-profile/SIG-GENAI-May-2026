import json
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path

DB_PATH = Path(__file__).with_name('capstone.db')
LOG_PATH = Path(__file__).with_name('capstone.log')
MEMORY_PATH = Path(__file__).with_name('memory.jsonl')


@dataclass
class WorkflowState:
    user_request: str
    generated_sql: str = ''
    review_notes: str = ''
    approved: bool = False
    result: list[tuple] | None = None
    execution_time_ms: float = 0.0


def prepare_database() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DROP TABLE IF EXISTS sales')
        conn.execute('CREATE TABLE sales(region TEXT, revenue INTEGER)')
        conn.executemany(
            'INSERT INTO sales(region, revenue) VALUES (?, ?)',
            [('North', 1000), ('South', 2000), ('East', 3000), ('West', 1500)],
        )


def generate_sql(state: WorkflowState) -> WorkflowState:
    if 'region' in state.user_request.lower():
        state.generated_sql = 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    else:
        state.generated_sql = 'SELECT region, revenue FROM sales;'
    return state


def review_sql(state: WorkflowState) -> WorkflowState:
    lowered = state.generated_sql.lower().strip()
    blocked = ['delete', 'drop', 'insert', 'update', 'alter', 'truncate']
    state.approved = lowered.startswith('select') and not any(word in lowered for word in blocked)
    state.review_notes = 'Approved by governance review.' if state.approved else 'Rejected by governance review.'
    return state


def execute_sql(state: WorkflowState) -> WorkflowState:
    if not state.approved:
        return state
    start = time.perf_counter()
    with sqlite3.connect(DB_PATH) as conn:
        state.result = conn.execute(state.generated_sql).fetchall()
    state.execution_time_ms = round((time.perf_counter() - start) * 1000, 3)
    return state


def store_memory(state: WorkflowState) -> None:
    event = {'request': state.user_request, 'sql': state.generated_sql, 'approved': state.approved}
    with MEMORY_PATH.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(event) + '\n')


def log_state(state: WorkflowState) -> None:
    with LOG_PATH.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(asdict(state)) + '\n')


def run_platform(user_request: str) -> WorkflowState:
    state = WorkflowState(user_request=user_request)
    state = generate_sql(state)
    state = review_sql(state)
    state = execute_sql(state)
    store_memory(state)
    log_state(state)
    return state


def main() -> None:
    prepare_database()
    request = input('Natural language request: ')
    state = run_platform(request)
    print('\nFinal workflow state:')
    for key, value in asdict(state).items():
        print(f'{key}: {value}')
    print(f'Log written to {LOG_PATH}')
    print(f'Memory written to {MEMORY_PATH}')


if __name__ == '__main__':
    main()
