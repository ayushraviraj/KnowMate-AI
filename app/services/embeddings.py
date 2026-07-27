from typing import List

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class LocalEmbeddings(Embeddings):
    """
    Local SentenceTransformer Embedding Wrapper for LangChain.
    """

    def __init__(
        self,
        model: str = "all-MiniLM-L6-v2",
    ):
        print("=" * 60)
        print("Loading SentenceTransformer Model...")
        print(f"Model Name : {model}")
        print("=" * 60)

        self.model = SentenceTransformer(model)

        print("=" * 60)
        print("✅ SentenceTransformer Loaded Successfully!")
        print("=" * 60)

    def embed_documents(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        print("=" * 60)
        print(f"Embedding {len(texts)} document chunks...")
        print("=" * 60)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        print("=" * 60)
        print("✅ Document Embeddings Created Successfully!")
        print("=" * 60)

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> List[float]:

        print("=" * 60)
        print("Embedding User Query...")
        print("=" * 60)

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        print("=" * 60)
        print("✅ Query Embedding Created Successfully!")
        print("=" * 60)

        return embedding.tolist()