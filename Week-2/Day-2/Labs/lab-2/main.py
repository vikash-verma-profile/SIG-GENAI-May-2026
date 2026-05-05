import json

from sql_review import review_sql

print("Lab 2 — SQL review agent (Ollama). Paste SQL, then a blank line to submit.\n")

while True:
    print("SQL (end with empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    sql = "\n".join(lines).strip()
    if not sql:
        continue
    result = review_sql(sql)
    print(json.dumps(result, indent=2))
    print()
