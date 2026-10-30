from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClassroomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: str = Field(..., min_length=1, max_length=50)
    series: str | None = None
    academic_year: str = Field(..., min_length=4, max_length=20)


class ClassroomCreate(ClassroomBase):
    school_id: UUID


class ClassroomRead(ClassroomBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime
