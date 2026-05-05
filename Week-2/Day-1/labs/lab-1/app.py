from fastapi import FastAPI
import snowflake.connector

app = FastAPI()

def run_query(query):
    conn = snowflake.connector.connect(
        user='ERVIKASHVERMA551',
        password='VikashTest@123',
        account='AMWBDHB-UL94640',
        warehouse='Compute_WH',
        database='SALESDB',
        schema='PUBLIC'
    )

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

@app.post("/run_sql")
def run_sql(payload: dict):
    query = payload.get("query")
    result = run_query(query)
    return {"query": query, "result": result}
