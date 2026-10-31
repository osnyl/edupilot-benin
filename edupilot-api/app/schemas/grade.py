from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GradeBase(BaseModel):
    value: Decimal = Field(..., ge=0)
    status: str = Field(default="draft", pattern=r"^(draft|validated)$")


class GradeCreate(GradeBase):
    """Payload pour POST /grades."""
    school_id: UUID
    assessment_id: UUID
    student_id: UUID
    author_id: UUID | None = None


class GradeUpdate(BaseModel):
    """Payload pour PATCH /grades/{id} — modification versionnée."""
    value: Decimal = Field(..., ge=0)
    status: str = Field(default="draft", pattern=r"^(draft|validated)$")
    reason: str = Field(..., min_length=3, max_length=500)
    changed_by_id: UUID | None = None


class GradeRead(GradeBase):
    """Réponse d'une note."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    assessment_id: UUID
    student_id: UUID
    version: int
    author_id: UUID | None = None
    validated_by_id: UUID | None = None
    validated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class GradeHistoryRead(BaseModel):
    """Réponse d'une entrée d'historique."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    grade_id: UUID
    old_value: Decimal | None = None
    new_value: Decimal | None = None
    old_status: str | None = None
    new_status: str | None = None
    reason: str | None = None
    changed_by_id: UUID | None = None
    changed_at: datetime
