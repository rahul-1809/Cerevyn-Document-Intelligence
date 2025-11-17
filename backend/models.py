from pydantic import BaseModel
from typing import List, Optional


class SourceReference(BaseModel):
    """A reference to a specific page in a document."""
    doc: str  # Document filename (e.g., "tech_spec.pdf")
    page: int  # Page number


class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for the chat endpoint."""
    answer: str
    sources: List[SourceReference]


class UploadResponse(BaseModel):
    """Response model for the upload endpoint."""
    status: str
    files_processed: int
    message: Optional[str] = None
