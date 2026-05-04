import re

import requests

from llm import ask_llm
from rag import retrieve


def _sql_from_llm_output(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:sql)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text

SYSTEM_CONTEXT = """
You are a clinical data assistant.

Tables:
patients(patient_id, name, age, gender, diagnosis)
admissions(admission_id, patient_id, admission_date, discharge_date, department)
vitals(patient_id, bp, heart_rate, recorded_at)

Rules:
- Generate ONLY SQL for data queries
- Use correct joins
"""

def process_query(user_input):

    # STEP 1: RAG
    knowledge = retrieve(user_input)

    # STEP 2: Generate SQL
    sql_prompt = f"""
    {SYSTEM_CONTEXT}

    Question: {user_input}

    Generate SQL query:
    """

    sql_query = _sql_from_llm_output(ask_llm(sql_prompt))

    print("Generated SQL:", sql_query)

    # STEP 3: MCP CALL
    db_result = requests.post(
        "http://127.0.0.1:8000/run_sql",
        json={"query": sql_query}
    ).json()

    # STEP 4: FINAL ANSWER
    final_prompt = f"""
    Question: {user_input}

    Medical Knowledge:
    {knowledge}

    Database Result:
    {db_result}

    Give final answer in simple terms.
    """

    final_answer = ask_llm(final_prompt)

    return final_answer