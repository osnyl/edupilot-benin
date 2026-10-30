from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import School
from app.schemas.school import SchoolCreate, SchoolRead

router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("", response_model=list[SchoolRead])
async def list_schools(db: AsyncSession = Depends(get_db)):
    """Liste tous les établissements."""
    result = await db.execute(select(School).order_by(School.name))
    return result.scalars().all()


@router.post("", response_model=SchoolRead, status_code=status.HTTP_201_CREATED)
async def create_school(
    payload: SchoolCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée un nouvel établissement."""
    school = School(**payload.model_dump())
    db.add(school)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une école avec ce slug existe déjà.",
        )
    await db.refresh(school)
    return school
