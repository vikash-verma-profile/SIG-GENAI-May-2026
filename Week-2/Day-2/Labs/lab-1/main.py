from nl2sql import natural_language_to_sql

print("Lab 1 — NL2SQL (Ollama). Ctrl+C to exit.\n")

while True:
    try:
        question = input("Question: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if not question:
        continue
    try:
        sql = natural_language_to_sql(question)
    except RuntimeError as exc:
        print(f"\nError: {exc}\n")
        continue
    print("\nGenerated SQL:\n")
    print(sql)
    print()
