from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("school_id", "matricule", name="students_school_id_matricule_key"),
        Index("idx_students_school", "school_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    matricule: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(Text, nullable=True)
    guardian_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    guardian_phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    guardian_email: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Student id={self.id} matricule={self.matricule!r}>"
