from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.assessment import AssessmentType


class AssessmentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    type: AssessmentType
    period: str = Field(..., min_length=1, max_length=50)
    date: date
    max_score: Decimal = Field(default=Decimal("20"), gt=0)
    coefficient: Decimal = Field(default=Decimal("1"), gt=0)


class AssessmentCreate(AssessmentBase):
    school_id: UUID
    subject_id: UUID
    classroom_id: UUID
    teacher_id: UUID | None = None


class AssessmentRead(AssessmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    subject_id: UUID
    classroom_id: UUID
    teacher_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
