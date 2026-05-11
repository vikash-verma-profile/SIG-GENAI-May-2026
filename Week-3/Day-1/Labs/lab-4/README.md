# Lab 4 - Long-Term Memory Agent

## Objective
Store historical interactions and retrieve similar questions to support long-term memory.

## Learning Outcomes

- Implement memory persistence.
- Understand embeddings and retrieval workflows.
- Build a simple RAG-style pattern.
- Persist memory to disk.

## Detailed Steps

1. Install optional vector dependencies.

   ```bash
   pip install -r requirements.txt
   ```

2. Run the memory agent.

   ```bash
   python memory_agent.py
   ```

3. Ask a question, then run again with a similar question.

4. Review the retrieved similar memories.

## Exercises

- Replace token matching with ChromaDB embeddings.
- Add user history.
- Add semantic search.
- Persist vector memory to disk.
