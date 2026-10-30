import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# --- Notre projet ---
from app.config import settings
from app.database import Base
# Import de tous les modèles pour qu'Alembic puisse les voir
from app.models import (  # noqa: F401
    Assessment,
    AuditEvent,
    Classroom,
    Grade,
    GradeHistory,
    School,
    Student,
    StudentClassroom,
    Subject,
    User,
)

# --- Config Alembic ---
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# On injecte l'URL de connexion lue depuis le .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Les métadonnées que Alembic doit comparer à la base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Mode 'offline' : génère le SQL sans se connecter à la base."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Mode 'online' : se connecte réellement à PostgreSQL."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
