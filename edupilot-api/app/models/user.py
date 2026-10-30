import enum
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    DIRECTOR = "director"
    SECRETARY = "secretary"
    CENSOR = "censor"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("school_id", "email", name="users_school_id_email_key"),
        Index("idx_users_school", "school_id"),
        Index("idx_users_role", "school_id", "role"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        PGEnum(UserRole, name="user_role", create_type=False,
               values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    status: Mapped[UserStatus] = mapped_column(
        PGEnum(UserStatus, name="user_status", create_type=False,
               values_callable=lambda x: [e.value for e in x]),
        nullable=False, server_default="pending",
    )
    firebase_uid: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role.value!r}>"
