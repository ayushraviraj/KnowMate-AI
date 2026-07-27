from pydantic import BaseModel


class URLUploadRequest(BaseModel):
    url: str