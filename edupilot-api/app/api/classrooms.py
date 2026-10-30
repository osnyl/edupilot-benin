from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomRead

router = APIRouter(prefix="/classrooms", tags=["classrooms"])


@router.get("", response_model=list[ClassroomRead])
async def list_classrooms(
    school_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Liste les classes d'une école."""
    result = await db.execute(
        select(Classroom).where(Classroom.school_id == school_id).order_by(Classroom.name)
    )
    return result.scalars().all()


@router.post("", response_model=ClassroomRead, status_code=status.HTTP_201_CREATED)
async def create_classroom(
    payload: ClassroomCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée une classe."""
    classroom = Classroom(**payload.model_dump())
    db.add(classroom)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette classe existe déjà pour cette année scolaire.",
        )
    await db.refresh(classroom)
    return classroom
