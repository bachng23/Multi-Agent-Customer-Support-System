from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum

class DocumentStatus(str, Enum):
    processing = 'processing'
    ready = 'ready'
    error = 'error'

class UploadResponse(BaseModel):
    file_id: UUID4 = Field(..., description="Unique identifier for the uploaded file (Already stored in the database)")
    file_name: str = Field(..., description="Original name of the uploaded file")
    status: DocumentStatus

class ChatRequest(BaseModel):
    user_id: UUID4 = Field(..., description="Unique identifier for the user")
    session_id: Optional[UUID4] = Field(None, description="Unique identifier for the chat session")
    content: str = Field(..., description="The content of the chat message")
    file_ids: list[UUID4] = Field(default_factory=list, description="List of file ID references associated with the message")

class ChatResponse(BaseModel):
    message_id: UUID4 = Field(..., description="Unique identifier for the chat message")
    session_id: UUID4 = Field(..., description="Unique identifier for the chat session")
    content: str = Field(..., description="The content of the chat message")
    agent_handle: str = Field(..., description="Identifier for the agent handling the message")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the message was created")
