from pydantic import BaseModel, Field
from typing import Dict, Any

class Chunk(BaseModel):
    source_document: str = Field(..., description="The source document from which the chunk was created")
    content: str = Field(..., description="The content of the chunk")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the chunk")