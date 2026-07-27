from pathlib import Path

import requests
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.dependencies import create_workflow
from app.core.workflow_manager import workflow_manager

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class URLUploadRequest(BaseModel):
    url: str


# --------------------------------------------------
# Upload Local PDF
# --------------------------------------------------

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    workflow = create_workflow(str(file_path))

    workflow_manager.add_workflow(
        file.filename,
        workflow,
    )

    return {
        "message": "PDF uploaded successfully.",
        "filename": file.filename,
    }


# --------------------------------------------------
# Upload PDF From URL
# --------------------------------------------------

@router.post("/url")
async def upload_pdf_url(request: URLUploadRequest):

    try:
        response = requests.get(request.url, timeout=30)

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="Unable to download PDF."
            )

        filename = request.url.split("/")[-1]

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(response.content)

        workflow = create_workflow(str(file_path))

        workflow_manager.add_workflow(
            filename,
            workflow,
        )

        return {
            "message": "PDF downloaded successfully.",
            "filename": filename,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )