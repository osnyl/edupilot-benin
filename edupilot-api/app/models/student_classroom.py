from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class StudentClassroom(Base):
    __tablename__ = "student_classrooms"
    __table_args__ = (
        Index("idx_student_classrooms_student", "school_id", "student_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    classroom_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
