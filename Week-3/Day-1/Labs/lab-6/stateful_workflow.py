from typing import TypedDict


class AgentState(TypedDict, total=False):
    user_query: str
    sql_query: str
    review_notes: str
    approved: bool
    result: str


def generate_sql(state: AgentState) -> AgentState:
    question = state['user_query'].lower()
    if 'region' in question:
        state['sql_query'] = 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    else:
        state['sql_query'] = 'SELECT id, region, revenue FROM sales;'
    return state


def review_sql(state: AgentState) -> AgentState:
    sql_query = state['sql_query'].lower().strip()
    state['approved'] = sql_query.startswith('select') and 'sales' in sql_query
    state['review_notes'] = 'Approved read-only sales query.' if state['approved'] else 'Rejected SQL.'
    return state


def execute_sql(state: AgentState) -> AgentState:
    state['result'] = 'Execution node placeholder: connect this to SQLite or Snowflake.'
    return state


def error_node(state: AgentState) -> AgentState:
    state['result'] = 'Workflow stopped because SQL review failed.'
    return state


def run_workflow(user_query: str) -> AgentState:
    state: AgentState = {'user_query': user_query}
    state = generate_sql(state)
    state = review_sql(state)
    if state['approved']:
        return execute_sql(state)
    return error_node(state)


def main() -> None:
    question = input('Question: ')
    final_state = run_workflow(question)
    print('\nFinal state:')
    for key, value in final_state.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
