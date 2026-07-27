from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.documents import Document

from app.core.dependencies import create_workflow
from app.core.workflow_manager import workflow_manager

router = APIRouter(
    prefix="/text",
    tags=["Text"],
)


class TextRequest(BaseModel):
    text: str


@router.post("/process")
async def process_text(request: TextRequest):

    if not request.text.strip():
        return {
            "message": "Text cannot be empty."
        }

    # Convert text to LangChain Document
    documents = [
        Document(
            page_content=request.text,
            metadata={
                "source": "Pasted Text"
            }
        )
    ]

    # Create workflow
    workflow = create_workflow(documents)

    # Generate unique document ID
    document_id = f"text_{uuid4().hex[:8]}"

    # Store workflow
    workflow_manager.add_workflow(
        document_id,
        workflow,
    )

    return {
        "message": "Text processed successfully.",
        "document_id": document_id,
    }