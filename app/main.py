from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import text
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.youtube import router as youtube_router

app = FastAPI(
    title="PDF RAG Agent",
    description="AI-powered PDF Question Answering using LangGraph",
    version="1.0.0",
)

# -------------------------------
# Enable CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include Routers
# -------------------------------
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(text.router)
app.include_router(youtube_router)
# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def root():
    return {
        "message": "PDF RAG Agent is running 🚀"
    }