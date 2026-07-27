from langchain_core.documents import Document

from app.graph.nodes import GraphNodes
from app.graph.workflow import GraphWorkflow

from app.services.llm import GroqLLM
from app.services.pdf_loader import PDFLoader
from app.services.retriever import Retriever
from app.services.splitter import TextSplitter
from app.services.vectorstore import VectorStore


def create_workflow(
    source: str | list[Document],
) -> GraphWorkflow:

    # -------------------------------
    # Load Documents
    # -------------------------------
    if isinstance(source, str):

        # PDF Path
        loader = PDFLoader()
        documents = loader.load(source)

    else:

        # Already loaded Documents
        documents = source

    # -------------------------------
    # Split into Chunks
    # -------------------------------
    splitter = TextSplitter()
    chunks = splitter.split_documents(documents)

    # -------------------------------
    # Create Vector Store
    # -------------------------------
    vector_store = VectorStore()
    vector_store.create(chunks)

    # -------------------------------
    # Create Retriever
    # -------------------------------
    retriever = Retriever(vector_store)

    # -------------------------------
    # Initialize LLM
    # -------------------------------
    llm = GroqLLM()

    # -------------------------------
    # Create Graph Nodes
    # -------------------------------
    nodes = GraphNodes(
        retriever=retriever,
        llm=llm,
    )

    # -------------------------------
    # Return Workflow
    # -------------------------------
    return GraphWorkflow(nodes)