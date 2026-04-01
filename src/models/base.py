from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlmodel import SQLModel, Column, DateTime, Field

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        sa_column_kwargs={"nullable": False}
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True), 
            nullable=False, 
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )

    is_deleted: bool = Field(default=False, index=True)

