from pathlib import Path

from nl2sql import natural_language_to_sql

LAB_DIR = Path(__file__).resolve().parent
DBT_MARTS_DIR = LAB_DIR / "retail_dw" / "models" / "marts"

print("Lab 1 — NL→dbt model SQL (Ollama). Ctrl+C to exit.\n")

while True:
    try:
        question = input("Question: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if not question:
        continue

    model_name = input("dbt model name (e.g. mart_revenue_by_customer): ").strip()
    if not model_name:
        model_name = "mart_generated"
    try:
        sql = natural_language_to_sql(question)
    except RuntimeError as exc:
        print(f"\nError: {exc}\n")
        continue

    DBT_MARTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DBT_MARTS_DIR / f"{model_name}.sql"
    out_path.write_text(sql.strip() + "\n", encoding="utf-8")

    print(f"\nSaved dbt model to:\n{out_path}\n")
    print("Generated SQL:\n")
    print(sql)
    print()
