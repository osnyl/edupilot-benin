from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Moteur asynchrone vers PostgreSQL
# pool_pre_ping=True : vérifie que la connexion est vivante avant chaque usage
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),  # log SQL en dev
    pool_pre_ping=True,
)

# Fabrique de sessions (une session = une "conversation" avec la base)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Classe mère de tous les modèles ORM (School, Student, Grade, ...)
class Base(DeclarativeBase):
    pass


# Dépendance FastAPI : fournit une session par requête, la ferme à la fin
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
