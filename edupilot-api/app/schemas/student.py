from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    """Champs communs à la création et à la lecture."""
    matricule: str = Field(..., min_length=2, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    birth_date: date | None = None
    gender: str | None = None
    guardian_name: str | None = None
    guardian_phone: str | None = None
    guardian_email: EmailStr | None = None


class StudentCreate(StudentBase):
    """Payload pour POST /students (school_id sera déduit côté serveur plus tard)."""
    pass


class StudentRead(StudentBase):
    """Réponse d'un élève."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    created_at: datetime
    updated_at: datetime
