from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = (
        Index("idx_grades_school", "school_id", "student_id"),
        Index("idx_grades_assessment", "school_id", "assessment_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    assessment_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="draft")
    author_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    validated_by_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Grade id={self.id} value={self.value} v{self.version}>"
