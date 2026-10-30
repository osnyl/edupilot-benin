from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Text, text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (
        Index("idx_audit_school", "school_id", text("created_at DESC")),
        Index("idx_audit_actor", "actor_id", text("created_at DESC")),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    school_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("schools.id", ondelete="SET NULL"), nullable=True
    )
    actor_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(Text, nullable=False)
    resource_type: Mapped[str] = mapped_column(Text, nullable=False)
    resource_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    old_value: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
