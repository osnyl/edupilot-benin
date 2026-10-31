from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Grade, GradeHistory
from app.schemas.grade import (
    GradeCreate,
    GradeHistoryRead,
    GradeRead,
    GradeUpdate,
)

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("", response_model=list[GradeRead])
async def list_grades(
    school_id: UUID,
    student_id: UUID | None = None,
    assessment_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Liste les notes d'une école (filtrable par élève ou évaluation)."""
    stmt = select(Grade).where(Grade.school_id == school_id)
    if student_id is not None:
        stmt = stmt.where(Grade.student_id == student_id)
    if assessment_id is not None:
        stmt = stmt.where(Grade.assessment_id == assessment_id)
    stmt = stmt.order_by(Grade.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=GradeRead, status_code=status.HTTP_201_CREATED)
async def create_grade(
    payload: GradeCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée une note (version 1, status draft par défaut)."""
    grade = Grade(**payload.model_dump())
    db.add(grade)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cette note existe déjà (conflit d'intégrité).",
        )
    await db.refresh(grade)
    return grade


@router.patch("/{grade_id}", response_model=GradeRead)
async def update_grade(
    grade_id: UUID,
    payload: GradeUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Modifie une note : incrémente la version et journalise l'ancienne valeur."""
    result = await db.execute(select(Grade).where(Grade.id == grade_id))
    grade = result.scalar_one_or_none()
    if grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note introuvable.",
        )

    # Journalise l'ancienne valeur dans grade_history AVANT de modifier
    history = GradeHistory(
        school_id=grade.school_id,
        grade_id=grade.id,
        old_value=grade.value,
        new_value=payload.value,
        old_status=grade.status,
        new_status=payload.status,
        reason=payload.reason,
        changed_by_id=payload.changed_by_id,
    )
    db.add(history)

    # Applique la modification + incrémente la version
    grade.value = payload.value
    grade.status = payload.status
    grade.version = grade.version + 1
    if payload.status == "validated":
        grade.validated_by_id = payload.changed_by_id
        from datetime import datetime, timezone
        grade.validated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(grade)
    return grade


@router.get("/{grade_id}/history", response_model=list[GradeHistoryRead])
async def get_grade_history(
    grade_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Retourne l'historique complet d'une note."""
    result = await db.execute(
        select(GradeHistory)
        .where(GradeHistory.grade_id == grade_id)
        .order_by(GradeHistory.changed_at.desc())
    )
    return result.scalars().all()
