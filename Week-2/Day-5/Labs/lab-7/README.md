# Lab 7 — RAG chatbot for DataOps logs (airline reservation system)

**Domain:** Airline reservations  
**Goal:** Build a small **RAG** (retrieval-augmented generation) flow over **pipeline logs** and ops notes using **LangChain**, **ChromaDB**, and **OpenAI** embeddings/chat.

**Tools:** LangChain · OpenAI · ChromaDB.

---

## What’s in this folder

| Path | Purpose |
|------|---------|
| `logs/incident1.txt` | Sample incident narrative for retrieval. |
| `rag_chatbot.py` | Loads `.txt` logs, builds a **Chroma** store, answers a fixed question via OpenAI. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Ignores local `chroma_db/` embedding store. |

---

## Prerequisites

- Python **3.10+**.
- An **OpenAI API key** with access to chat + embedding models used in the script (`gpt-4o-mini` is the default chat model in code—adjust if your org requires another model).

---

## Step-by-step

### 1. Install packages

```bash
cd lab-7
pip install -r requirements.txt
```

### 2. Set your API key

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

**Windows CMD:**

```cmd
set OPENAI_API_KEY=sk-...
```

**macOS / Linux:**

```bash
export OPENAI_API_KEY="sk-..."
```

Never commit keys to Git.

### 3. Add more log files (optional)

Drop additional `.txt` files under `logs/`. The loader reads **all** `*.txt` files in that folder.

### 4. Run the chatbot script

```bash
python rag_chatbot.py
```

The script asks:

> Explain why the airline booking pipeline failed yesterday.

It retrieves from `logs/` and generates an answer grounded in those documents.

### 5. Experiment with prompts

Edit `rag_chatbot.py`:

- Change `question = "..."` to operational questions you care about.
- Tune `search_kwargs={"k": 3}` for more/fewer chunks.

### 6. Clean up vector store (optional)

Delete the `chroma_db/` folder if embeddings get stale after large log changes.

---

## Expected results

- Chroma persists under `chroma_db/` (gitignored).
- Answers cite themes from `incident1.txt` (schema change, stale APIs, etc.—exact wording will vary by model).

---

## Troubleshooting

| Issue | What to try |
|-------|----------------|
| `OPENAI_API_KEY` errors | Confirm env var in the **same terminal session** you use to run Python. |
| Rate limits / quota | Retry later; reduce calls; use org-approved model. |
| Empty retrieval | Ensure logs are non-empty UTF-8 text and question overlaps vocabulary. |

---

## Learning outcomes

- Minimal **RAG** loop: **chunk → embed → retrieve → generate**.
- Operational docs as **first-class** knowledge, not only metrics.
