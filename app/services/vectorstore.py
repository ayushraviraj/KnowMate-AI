from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.services.embeddings import LocalEmbeddings


class VectorStore:

    def __init__(self):
        self.embeddings = LocalEmbeddings()
        self.vectorstore = None

    def create(self, documents: list[Document]):

        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )

        return self.vectorstore

    def similarity_search(
        self,
        query: str,
        k: int = 8,
    ):

        if self.vectorstore is None:
            raise ValueError("Vector store has not been created.")

        # Pure similarity search
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
        )