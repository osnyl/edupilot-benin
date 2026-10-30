import enum
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, Text
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class AssessmentType(str, enum.Enum):
    DEVOIR = "devoir"
    COMPOSITION = "composition"
    INTERROGATION = "interrogation"
    EXAMEN = "examen"


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        Index("idx_assessments_school", "school_id", "classroom_id", "period"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    classroom_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False
    )
    teacher_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[AssessmentType] = mapped_column(
        PGEnum(AssessmentType, name="assessment_type", create_type=False,
               values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    period: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    max_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, server_default="20")
    coefficient: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False, server_default="1")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Assessment id={self.id} title={self.title!r} period={self.period!r}>"
