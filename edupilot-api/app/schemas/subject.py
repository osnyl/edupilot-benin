from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    coefficient: Decimal = Field(default=Decimal("1"), ge=0, le=99.99)


class SubjectCreate(SubjectBase):
    school_id: UUID


class SubjectRead(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime
