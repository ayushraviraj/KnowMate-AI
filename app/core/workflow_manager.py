from app.graph.workflow import GraphWorkflow


class WorkflowManager:

    def __init__(self):
        self.workflows: dict[str, GraphWorkflow] = {}

    def add_workflow(
        self,
        document_id: str,
        workflow: GraphWorkflow,
    ):
        self.workflows[document_id] = workflow

    def get_workflow(
        self,
        document_id: str,
    ) -> GraphWorkflow:

        if document_id not in self.workflows:
            raise ValueError(
                f"No workflow found for '{document_id}'."
            )

        return self.workflows[document_id]

    def list_documents(self):
        return list(self.workflows.keys())

    def remove_workflow(self, document_id: str):

        if document_id in self.workflows:
            del self.workflows[document_id]


workflow_manager = WorkflowManager()