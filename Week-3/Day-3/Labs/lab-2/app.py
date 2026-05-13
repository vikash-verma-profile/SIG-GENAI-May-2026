"""
Lab 2 — Automated dbt lineage: scan model SQL, extract ref('...') dependencies, build DAG.
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
OUTPUT_DIR = ROOT / "outputs"


def list_model_files() -> list[str]:
    return sorted(p.name for p in MODELS_DIR.glob("*.sql"))


def extract_ref_dependencies(sql_text: str) -> list[str]:
    return re.findall(r"\{\{\s*ref\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}", sql_text, flags=re.I)


def build_dependency_edges() -> list[tuple[str, str]]:
    """Return edges (upstream, downstream) where downstream is the model file stem."""
    edges: list[tuple[str, str]] = []
    for path in MODELS_DIR.glob("*.sql"):
        downstream = path.stem
        text = path.read_text(encoding="utf-8")
        for upstream in extract_ref_dependencies(text):
            edges.append((upstream, downstream))
    return edges


def draw_dag(edges: list[tuple[str, str]]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    g = nx.DiGraph()
    for u, v in edges:
        g.add_edge(u, v)
    plt.figure(figsize=(7, 4))
    pos = nx.spring_layout(g, seed=1)
    nx.draw(
        g,
        pos,
        with_labels=True,
        node_color="#d9ead3",
        edge_color="#555",
        arrows=True,
        arrowsize=16,
    )
    out = OUTPUT_DIR / "dbt_dag.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    return out


def main() -> None:
    files = list_model_files()
    print("Models directory listing:", files)
    edges = build_dependency_edges()
    print("Dependency edges (upstream -> model):", edges)
    png = draw_dag(edges)
    print("DAG image written to:", png)


if __name__ == "__main__":
    main()
