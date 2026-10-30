from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class GradeHistory(Base):
    """Trace immuable des corrections de notes (qui, quand, pourquoi)."""

    __tablename__ = "grade_history"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
    )
    grade_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("grades.id", ondelete="CASCADE"), nullable=False
    )
    old_value: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    new_value: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    old_status: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_status: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_by_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
