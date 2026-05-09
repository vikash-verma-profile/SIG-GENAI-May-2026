"""Print the Lab 6 review checklist (use while reviewing a peer repo)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    path = ROOT / "review_checklist.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    print(data["title"], "\n")
    for cat in data["categories"]:
        print(f"## {cat['name']}")
        for item in cat["items"]:
            print(f"  - [ ] {item}")
        print()


if __name__ == "__main__":
    main()
