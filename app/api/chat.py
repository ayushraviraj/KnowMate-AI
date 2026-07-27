from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.core.workflow_manager import workflow_manager

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    workflow = workflow_manager.get_workflow(
        request.document_id
    )

    result = workflow.invoke(request.question)

    return ChatResponse(
        question=request.question,
        answer=result["answer"]
    )