from pydantic import BaseModel, Field
from typing import Dict, Any

class Document(BaseModel):
    title: str = Field(..., description="The title of the document")
    content: str = Field(..., description="The content of the document")
    metatdata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the document")