"""
Lab 1 — Automated SQL lineage extraction (parse SQL → tables → graph → JSON).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import sqlparse

ROOT = Path(__file__).resolve().parent
SQL_PATH = ROOT / "sql" / "query.sql"
OUT_DIR = ROOT / "outputs"
LINEAGE_DIR = ROOT / "lineage"
TARGET_NODE = "output_table"


def read_sql() -> str:
    with open(SQL_PATH, encoding="utf-8") as f:
        return f.read()


def extract_tables(sql_query: str) -> list[str]:
    """Heuristic extraction of physical table names after FROM / JOIN."""
    normalized = sqlparse.format(sql_query, strip_comments=True).lower()
    # Remove quoted identifiers noise for this lab-level heuristic
    seen: list[str] = []
    for m in re.finditer(
        r"\b(from|join)\s+([`\"]?)([a-z_][a-z0-9_]*)\2",
        normalized,
        flags=re.IGNORECASE,
    ):
        name = m.group(3)
        if name not in ("select", "where", "on", "and", "or", "as"):
            if name not in seen:
                seen.append(name)
    return seen


def build_lineage_map(sources: list[str], target: str = TARGET_NODE) -> dict[str, str]:
    return {s: target for s in sources}


def save_lineage_json(mapping: dict[str, str]) -> Path:
    LINEAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = LINEAGE_DIR / "lineage.json"
    payload = {"edges": [{"from": k, "to": v} for k, v in mapping.items()]}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def draw_graph(mapping: dict[str, str]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g = nx.DiGraph()
    for src, dst in mapping.items():
        g.add_edge(src, dst)
    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(g, seed=42)
    nx.draw(g, pos, with_labels=True, node_color="#cfe2f3", edge_color="#666", arrows=True)
    png = OUT_DIR / "lineage_graph.png"
    plt.savefig(png, dpi=150, bbox_inches="tight")
    plt.close()
    return png


def main() -> None:
    sql_query = read_sql()
    print("--- SQL ---")
    print(sql_query)
    parsed = sqlparse.parse(sql_query)
    print("\n--- sqlparse.parse (statement count) ---")
    print(len(parsed), "statement(s)")

    tables = extract_tables(sql_query)
    print("\n--- Extracted tables ---")
    print(tables)

    lineage = build_lineage_map(tables)
    print("\n--- Lineage mapping (source -> target) ---")
    print(lineage)

    json_path = save_lineage_json(lineage)
    png_path = draw_graph(lineage)
    print("\n--- Written ---")
    print(json_path)
    print(png_path)


if __name__ == "__main__":
    main()
