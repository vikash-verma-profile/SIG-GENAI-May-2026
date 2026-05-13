"""
Lab 4 — AI-assisted runbook lookup and remediation recommendations.
"""
from __future__ import annotations

import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "runbooks.json"
OUT_DIR = ROOT / "outputs"


def load_runbooks() -> dict[str, str]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def retrieve_runbook(issue: str, runbooks: dict[str, str]) -> str:
    return runbooks.get(issue, runbooks["Unknown Error"])


def similarity_match(query: str, runbooks: dict[str, str]) -> tuple[str, float]:
    labels = list(runbooks.keys())
    corpus = [f"{label}. {runbooks[label]}" for label in labels]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    best_idx = int(scores.argmax())
    return labels[best_idx], float(round(scores[best_idx], 3))


def action_summary(issue: str, steps: str) -> str:
    return f"Issue: {issue}\nRecommended fix: {steps}\nStatus: ready to apply"


def main() -> None:
    runbooks = load_runbooks()
    issue = "Schema Drift"
    steps = retrieve_runbook(issue, runbooks)
    print(steps)

    matched_issue, score = similarity_match("column type changed in orders feed", runbooks)
    print(f"Similarity match: {matched_issue} (score={score})")

    summary = action_summary(issue, steps)
    print(summary)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "runbook_recommendation.json"
    out_path.write_text(
        json.dumps(
            {
                "issue": issue,
                "steps": steps,
                "similarity_match": {"issue": matched_issue, "score": score},
                "summary": summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
