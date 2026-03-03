# app/schemas/documents.py

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = Field(min_length=10, max_length=100_000)

class DocumentOut(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime
