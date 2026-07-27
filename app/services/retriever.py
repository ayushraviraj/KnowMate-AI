from langchain_core.documents import Document

from app.services.vectorstore import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
    ) -> list[Document]:

        query_lower = query.lower()

        summary_keywords = [
            "summary",
            "summarize",
            "overview",
            "brief",
            "abstract",
            "explain",
            "describe",
            "paper",
        ]

        k = 20 if any(keyword in query_lower for keyword in summary_keywords) else 10

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )