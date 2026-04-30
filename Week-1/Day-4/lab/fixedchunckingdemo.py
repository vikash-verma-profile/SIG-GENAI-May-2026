## Fixed Chunking Demo

from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = CSVLoader(file_path="catalog.csv")
documents = loader.load()
# print(documents[0])


### Semantic   Chunking Demo

splitter = RecursiveCharacterTextSplitter(chunk_size=300)
chunks = splitter.split_documents(documents)
# print(chunks[1])
# print(chunks[1].page_content)
# print(chunks[2].page_content)
# print(chunks[3].page_content)


print("--------------------------------")
#Hierarchical Chunking 
for doc in chunks:
    doc.metadata = {"source": "data_catalog"}
    # print(doc.page_content)
    # print(doc.metadata)


# from langchain_openai import OpenAIEmbeddings
# import os

# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     print(
#         "OPENAI_API_KEY is not set. Set it in your environment to run embeddings, "
#         "or comment out the embedding section."
#     )
# else:
#     embedding_model = OpenAIEmbeddings(api_key=api_key)
#     print(embedding_model.embed_query("Hello, world!"))
#     print(embedding_model.embed_query("Hello, world!"))
#     print(embedding_model.embed_query("Hello, world!"))

from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# print(embed("Hello, world!"))
# print(embed("Hello, world!"))


from langchain_community.vectorstores import FAISS

vector_db = FAISS.from_documents(chunks, embedding_model)
print(vector_db.index.ntotal)

results = vector_db.similarity_search("customer PII", k=3)


from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()

query = "Which tables contain customer PII?"

results = vector_db.similarity_search(query, k=3)

context = "\n".join([r.page_content for r in results])

response = llm.predict(f"Answer:\n{context}\nQuestion:{query}")
print(response)
