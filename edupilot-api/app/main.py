from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.assessments import router as assessments_router
from app.api.classrooms import router as classrooms_router
from app.api.schools import router as schools_router
from app.api.students import router as students_router
from app.api.subjects import router as subjects_router
from app.api.users import router as users_router
from app.config import settings
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Vérifie la connexion à la base au démarrage."""
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="API d'EduPilot Bénin — SaaS scolaire multi-rôles",
    lifespan=lifespan,
)

app.include_router(students_router)
app.include_router(schools_router)
app.include_router(users_router)
app.include_router(classrooms_router)
app.include_router(subjects_router)
app.include_router(assessments_router)


@app.get("/health", tags=["system"])
async def health_check():
    """Vérifie que l'API et la base sont opérationnelles."""
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version();"))
        pg_version = result.scalar()
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "database": pg_version,
    }
