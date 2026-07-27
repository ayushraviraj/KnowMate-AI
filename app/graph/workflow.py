from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.nodes import GraphNodes


class GraphWorkflow:

    def __init__(self, nodes: GraphNodes):

        graph = StateGraph(GraphState)

        graph.add_node("retrieve", nodes.retrieve)
        graph.add_node("generate", nodes.generate)

        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)

        self.app = graph.compile()

    def invoke(self, question: str):

        return self.app.invoke(
            {
                "question": question,
                "documents": [],
                "answer": "",
            }
        )