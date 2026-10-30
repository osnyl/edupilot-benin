from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchoolBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    active_year: str | None = None
    languages: list[str] = ["fr"]


class SchoolCreate(SchoolBase):
    """Payload pour POST /schools."""
    pass


class SchoolRead(SchoolBase):
    """Réponse d'une école."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
