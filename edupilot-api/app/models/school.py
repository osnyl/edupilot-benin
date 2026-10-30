from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class School(Base):
    """Établissement scolaire. Racine du modèle multi-tenant."""

    __tablename__ = "schools"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    active_year: Mapped[str | None] = mapped_column(Text, nullable=True)
    languages: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default="{fr}",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<School id={self.id} name={self.name!r} slug={self.slug!r}>"
