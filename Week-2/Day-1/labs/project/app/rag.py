from pathlib import Path

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

_GUIDELINES = Path(__file__).resolve().parent.parent / "data" / "guidelines.txt"
with open(_GUIDELINES, encoding="utf-8") as f:
    docs = f.read().split("\n\n")

embeddings = model.encode(docs)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.asarray(embeddings, dtype=np.float32))

def retrieve(query):
    q_emb = model.encode([query])
    _, I = index.search(np.asarray(q_emb, dtype=np.float32), k=1)
    return docs[I[0][0]]