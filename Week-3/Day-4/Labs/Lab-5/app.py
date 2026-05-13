"""
Lab 5 — RAG-powered analytics assistant over a small metrics corpus.
"""
from __future__ import annotations

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "analytics_corpus.txt"
OUT_DIR = ROOT / "outputs"
MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents() -> list[str]:
    return [line.strip() for line in DATA_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_collection(documents: list[str]):
    client = chromadb.Client()
    collection = client.get_or_create_collection("analytics_lab5")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(documents).tolist()
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[str(i + 1) for i in range(len(documents))],
    )
    return collection, model


def answer_query(collection, model, query: str) -> dict:
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=2)
    context = results["documents"][0]
    answer = " ".join(context)
    return {"query": query, "context": context, "answer": answer}


def main() -> None:
    documents = load_documents()
    collection, model = build_collection(documents)
    query = "Revenue trend"
    response = answer_query(collection, model, query)

    print("--- Retrieved context ---")
    for line in response["context"]:
        print("-", line)
    print("\n--- Draft answer ---")
    print(response["answer"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "rag_response.json"
    out_path.write_text(json.dumps(response, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
