"""
RAG over operational logs (Lab 7).

Uses LangChain + ChromaDB. Set OPENAI_API_KEY for full LLM answers; otherwise
retrieval-only output demonstrates embeddings + vector search.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def load_documents(logs_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(logs_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": path.name}))
    return docs


def main() -> None:
    root = Path(__file__).resolve().parent
    logs_dir = root / "logs"
    documents = load_documents(logs_dir)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Set OPENAI_API_KEY to run embeddings and chat. Example:\n"
            "  set OPENAI_API_KEY=sk-...\n"
            "  python rag_chatbot.py"
        )

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=str(root / "chroma_db"))
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a DataOps assistant. Answer using only the retrieved context. "
                "If unsure, say what is missing.",
            ),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    def format_docs(docs_list):
        return "\n\n".join(d.page_content for d in docs_list)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    question = "Explain why the airline booking pipeline failed yesterday."
    answer = chain.invoke(question)
    print(answer)


if __name__ == "__main__":
    main()
