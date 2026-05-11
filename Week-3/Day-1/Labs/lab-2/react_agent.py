from dataclasses import dataclass
from pathlib import Path

LOG_PATH = Path(__file__).with_name('reasoning.log')


@dataclass
class ReactStep:
    thought: str
    action: str
    observation: str
    reflection: str
    sql_query: str


def generate_sql(question: str) -> str:
    text = question.lower()
    if 'total' in text and 'region' in text:
        return 'SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region;'
    if 'average' in text:
        return 'SELECT AVG(revenue) AS average_revenue FROM sales;'
    return 'SELECT id, region, revenue FROM sales;'


def validate_sql(sql_query: str) -> str:
    if not sql_query.lower().strip().startswith('select'):
        return 'Query failed validation because it is not read-only.'
    if ' from sales' not in sql_query.lower():
        return 'Query failed validation because it does not use the sales table.'
    return 'Query passed validation.'


def run_react(question: str) -> ReactStep:
    thought = 'Identify the requested metric and target table.'
    action = 'Generate a read-only SQL query.'
    sql_query = generate_sql(question)
    observation = validate_sql(sql_query)
    reflection = 'The query is ready to execute.' if 'passed' in observation else 'The query needs revision.'
    return ReactStep(thought, action, observation, reflection, sql_query)


def main() -> None:
    question = input('Question: ')
    step = run_react(question)
    trace = f'''Thought: {step.thought}
Action: {step.action}
SQL: {step.sql_query}
Observation: {step.observation}
Reflection: {step.reflection}
'''
    print(trace)
    LOG_PATH.write_text(trace, encoding='utf-8')
    print(f'Reasoning trace saved to {LOG_PATH}')


if __name__ == '__main__':
    main()
