import json
from pathlib import Path

from cortex_stub import describe_cortex_flow
from nl2sql import natural_language_to_sql
from sql_review import review_sql

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def run(question: str) -> dict:
    sql = natural_language_to_sql(question)
    verdict = review_sql(sql)
    return {"question": question, "sql": sql, "review": verdict}


print("Case study — NL2SQL → SQL review → optional artifact save.")
print("Cortex Analyst recap:\n", describe_cortex_flow(), "\n")

while True:
    question = input("Business question (blank to exit): ").strip()
    if not question:
        break
    bundle = run(question)
    print("\n--- Generated SQL ---\n")
    print(bundle["sql"])
    print("\n--- Review ---\n")
    print(json.dumps(bundle["review"], indent=2))

    save = input("\nSave last SQL to case-study/output? [y/N]: ").strip().lower()
    if save == "y":
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / "last_query.sql"
        path.write_text(bundle["sql"], encoding="utf-8")
        print(f"Wrote {path}")
