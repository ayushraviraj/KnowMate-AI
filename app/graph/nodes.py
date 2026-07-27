from app.graph.state import GraphState
from app.services.retriever import Retriever
from app.services.llm import GroqLLM
from app.prompts.rag_prompt import RAG_PROMPT


class GraphNodes:

    def __init__(
        self,
        retriever: Retriever,
        llm: GroqLLM,
    ):
        self.retriever = retriever
        self.llm = llm

    def retrieve(self, state: GraphState) -> GraphState:

        documents = self.retriever.retrieve(
            state["question"]
        )

        print("\n" + "=" * 60)
        print("QUESTION:", state["question"])
        print(f"RETRIEVED DOCUMENTS: {len(documents)}")

        if len(documents) == 0:
            print("❌ No documents retrieved!")
        else:
            for i, doc in enumerate(documents, start=1):
                print(f"\n------ Document {i} ------")
                print(f"Source: {doc.metadata.get('source')}")
                print(f"Page: {doc.metadata.get('page')}")
                print(doc.page_content[:500])
                print("--------------------------")

        print("=" * 60 + "\n")

        return {
            **state,
            "documents": documents,
        }

    def generate(self, state: GraphState) -> GraphState:

        documents = state["documents"]

        # Include page numbers in context
        context = "\n\n".join(
            f"[Page {doc.metadata.get('page')}]\n{doc.page_content}"
            for doc in documents
        )

        print("\n" + "=" * 60)
        print("CONTEXT SENT TO LLM:")
        print(context[:1500])
        print("=" * 60 + "\n")

        prompt = RAG_PROMPT.format(
            context=context,
            question=state["question"],
        )

        answer = self.llm.generate(prompt)

        # ===========================
        # Build Source Citations
        # ===========================

        pages = sorted(
            {
                doc.metadata.get("page")
                for doc in documents
                if doc.metadata.get("page") is not None
            }
        )

        if pages:
            answer += "\n\n📚 Retrieved Pages: "
            answer += ", ".join(str(page) for page in pages)

        print("\nLLM ANSWER:")
        print(answer)
        print("=" * 60 + "\n")

        return {
            **state,
            "answer": answer,
        }