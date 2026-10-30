from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Subject
from app.schemas.subject import SubjectCreate, SubjectRead

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("", response_model=list[SubjectRead])
async def list_subjects(
    school_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Liste les matières d'une école."""
    result = await db.execute(
        select(Subject).where(Subject.school_id == school_id).order_by(Subject.name)
    )
    return result.scalars().all()


@router.post("", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
async def create_subject(
    payload: SubjectCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée une matière."""
    subject = Subject(**payload.model_dump())
    db.add(subject)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette matière existe déjà dans cette école.",
        )
    await db.refresh(subject)
    return subject
