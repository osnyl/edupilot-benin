from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Student
from app.schemas.student import StudentCreate, StudentRead

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentRead])
async def list_students(
    school_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Liste les élèves d'une école."""
    result = await db.execute(
        select(Student).where(Student.school_id == school_id).order_by(Student.last_name)
    )
    return result.scalars().all()


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée un élève dans une école."""
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un élève avec ce matricule existe déjà dans cette école.",
        )
    await db.refresh(student)
    return student
