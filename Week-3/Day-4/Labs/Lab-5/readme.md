# Lab 5 — RAG-Powered Analytics System

Index analytics snippets in ChromaDB, retrieve relevant context for a natural-language question, and draft an answer.

## Setup

```bash
cd Labs/Lab-5
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

First run downloads the `all-MiniLM-L6-v2` embedding model.

## Steps

1. Review `data/analytics_corpus.txt`.
2. Run `python app.py`.
3. Confirm retrieved context and draft answer for the revenue query.
4. Open `outputs/rag_response.json`.

## Exercises

- Add more datasets and metadata filters for governance.
- Swap the stitched answer for an LLM completion.
- Build a simple CLI or dashboard on top of the retriever.
