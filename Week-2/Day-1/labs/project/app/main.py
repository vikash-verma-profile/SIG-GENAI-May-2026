import sys
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

from agent import process_query

print("AI Clinical Assistant Ready...\n")

while True:
    query = input("Ask: ")
    result = process_query(query)
    print("\nAnswer:\n", result)