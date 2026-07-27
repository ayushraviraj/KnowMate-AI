from urllib.parse import parse_qs, urlparse

from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document
from pydantic import BaseModel

from app.core.dependencies import create_workflow
from app.core.workflow_manager import workflow_manager
from app.mcp.youtube_client import youtube_client

router = APIRouter(prefix="/youtube", tags=["YouTube"])


class YouTubeRequest(BaseModel):
    url: str


@router.post("/upload")
async def upload_youtube(request: YouTubeRequest):
    try:
        # -------------------------------
        # Get transcript using MCP
        # -------------------------------
        transcript = await youtube_client.get_transcript(request.url)

        # -------------------------------
        # Convert transcript to Document
        # -------------------------------
        documents = [
            Document(
                page_content=transcript,
                metadata={
                    "source": request.url,
                    "type": "youtube",
                },
            )
        ]

        # -------------------------------
        # Create workflow
        # -------------------------------
        workflow = create_workflow(documents)

        # -------------------------------
        # Extract YouTube Video ID
        # -------------------------------
        parsed_url = urlparse(request.url)
        query = parse_qs(parsed_url.query)

        if "v" not in query:
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL."
            )

        document_id = query["v"][0]

        # -------------------------------
        # Store workflow
        # -------------------------------
        workflow_manager.add_workflow(
            document_id,
            workflow,
        )

        return {
            "message": "YouTube transcript indexed successfully.",
            "document_id": document_id,
            "source": request.url,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )