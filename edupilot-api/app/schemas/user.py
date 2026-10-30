from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=200)
    role: UserRole


class UserCreate(UserBase):
    """Payload pour POST /users. school_id temporaire (avant auth)."""
    school_id: UUID
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    """Réponse d'un utilisateur."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    school_id: UUID
    status: UserStatus
    created_at: datetime
    updated_at: datetime
