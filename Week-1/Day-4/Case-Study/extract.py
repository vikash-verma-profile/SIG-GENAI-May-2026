
#  RAG PIPELINE 


try:
    # LangChain modern split packages
    from langchain_text_splitters import CharacterTextSplitter
except Exception:
    from langchain.text_splitter import CharacterTextSplitter

try:
    from langchain_community.vectorstores import FAISS
except Exception:
    from langchain.vectorstores import FAISS

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
except Exception:
    from langchain.embeddings import HuggingFaceEmbeddings

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from pathlib import Path

try:
    # LangChain < 0.1
    from langchain.docstore.document import Document
except Exception:
    # LangChain >= 0.1
    from langchain_core.documents import Document

# 1. LOAD DATASET (FROM ./rag_dataset)

DATA_DIR = Path(__file__).parent / "rag_dataset"
if not DATA_DIR.exists():
    raise FileNotFoundError(
        f"Dataset folder not found at: {DATA_DIR}. "
        "Create it and add .txt files (e.g. hr_leave_policy.txt)."
    )

raw_docs = []
for fp in sorted(DATA_DIR.glob("*.txt")):
    content = fp.read_text(encoding="utf-8", errors="ignore").strip()
    if content:
        raw_docs.append(Document(page_content=content, metadata={"source": fp.name}))

if not raw_docs:
    raise RuntimeError(f"No non-empty .txt files found in: {DATA_DIR}")

print(f"Loaded {len(raw_docs)} documents from {DATA_DIR}", flush=True)


# 2. CHUNKING

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=300,
    chunk_overlap=50
)
docs = splitter.split_documents(raw_docs)


# 3. EMBEDDINGS (FREE)

print("Loading embedding model (first run may download)...", flush=True)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. VECTOR DATABASE (FAISS)

db = FAISS.from_documents(docs, embeddings)
print("Vector store ready.", flush=True)


# 5. LLM s

print("Loading LLM (first run may download)...", flush=True)
tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
mdl = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def llm(prompt: str) -> str:
    inputs = tok(prompt, return_tensors="pt", truncation=True)
    outputs = mdl.generate(**inputs, max_new_tokens=256)
    return tok.decode(outputs[0], skip_special_tokens=True).strip()


# 6. RAG QUERY FUNCTION

def ask_question(query):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    # LangChain retriever API differs by version:
    # - Newer: retriever.invoke(query)
    # - Older: retriever.get_relevant_documents(query)
    if hasattr(retriever, "invoke"):
        results = retriever.invoke(query)
    elif hasattr(retriever, "get_relevant_documents"):
        results = retriever.get_relevant_documents(query)
    else:
        results = retriever._get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
    Answer ONLY from the context below.
    If answer is not present, say "Not available".

    Context:
    {context}

    Question:
    {query}
    """

    response = llm(prompt)
    return response



# 7. INTERACTIVE CHAT LOOP

if __name__ == "__main__":
    print("RAG System Ready (type 'exit' to quit)\n")

    while True:
        query = input("Ask a question: ")

        if query.lower() == "exit":
            print("Exiting...")
            break

        answer = ask_question(query)
        print("\nAnswer:", answer, "\n")