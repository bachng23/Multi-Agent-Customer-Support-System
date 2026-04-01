from __future__ import annotations
from src.models.base import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from src.models.business import Customer

class SupportTicket(BaseModel, table=True):
    subject: str = Field(..., description="The subject of the support ticket", min_length=5)
    content: str = Field(..., description="The content of the support ticket")
    status: str = Field(..., description="The status of the support ticket", default="open")
    priority: str = Field(..., description="The priority of the support ticket", default="medium")
    customer_id: Optional[uuid.UUID] = Field(foreign_key="customer.id")

    customer: Optional[Customer] = Relationship(back_populates="tickets")
    comments: list["TicketComment"] = Relationship(back_populates="ticket")

class TicketComment(BaseModel, table=True):
    ticket_id: uuid.UUID = Field(foreign_key="supportticket.id")
    author_role: str = Field(..., description="The role of the comment author (user or agent)")
    content: str = Field(..., description="The content of the comment")
    
    ticket: SupportTicket = Relationship(back_populates="comment")
