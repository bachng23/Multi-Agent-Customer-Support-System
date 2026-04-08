import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, String, Text, DateTime, Boolean, Integer, LargeBinary, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    "Base Class for SQLAlchemy models"
    pass

class User(Base):
    __tablename__='users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)

    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True ,index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    sessions: Mapped[list["ChatSession"]] = relationship(back_populates="user")  

class ChatSession(Base):
    __tablename__='chat_sessions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True) # Auto-delete messages when a session is deleted
    status: Mapped[str] = mapped_column(String(50), default='active')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    user: Mapped[User] = relationship(back_populates="sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="session")
    documents: Mapped[list["Document"]] = relationship(back_populates="session")

class ChatMessage(Base):
    __tablename__='chat_messages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chat_sessions.id'), index=True)
    sender: Mapped[str] = mapped_column(String(50))  # 'customer', 'agent', 'system', 'manager'
    content: Mapped[str] = mapped_column(Text)
    
    is_security_threat: Mapped[bool] = mapped_column(Boolean, default=False)
    thread_details: Mapped[Optional[str]] = mapped_column(Text)  

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    session: Mapped[ChatSession] = relationship(back_populates="messages")

class AuditLog(Base):
    __tablename__='audit_logs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True)) # ID Manager/System
    action: Mapped[str] = mapped_column(String(100)) # DECRYPT_PII, ACCESS_VAULT
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # Message or User's ID
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

class Document(Base):
    __tablename__='documents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('chat_sessions.id', ondelete='CASCADE'), index=True)

    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(512))
    file_type: Mapped[Optional[str]] = mapped_column(String(50))

    # OCR/Vision metadata
    status: Mapped[str] = mapped_column(String(50), default='pending')  # 'pending', 'processed', 'failed'

    # Summary of document content for quick reference
    summary: Mapped[Optional[str]] = mapped_column(Text)  

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    session: Mapped[ChatSession] = relationship(back_populates="documents")
    elements: Mapped[list["DocumentElement"]] = relationship(back_populates="document")

class DocumentElement(Base):
    __tablename__='document_elements'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('documents.id', ondelete='CASCADE'), index=True)

    element_type: Mapped[str] = mapped_column(String(50)) # 'text', 'table', 'image'
    page_number: Mapped[Optional[int]] = mapped_column(Integer)  # For multi-page documents
    content: Mapped[Optional[str]] = mapped_column(Text)  # For text and table data

    json_data: Mapped[Optional[dict]] = mapped_column(JSONB)  # For structured data like tables or OCR metadata

    image_path: Mapped[Optional[str]] = mapped_column(String(512))  # For extracted images

    summary: Mapped[Optional[str]] = mapped_column(Text)  # Summary of this element for quick reference

    anchor_id: Mapped[Optional[str]] = mapped_column(String(255))  # For linking back to original document position

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    document: Mapped[Document] = relationship(back_populates="elements")