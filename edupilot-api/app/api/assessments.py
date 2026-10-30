from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentRead

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("", response_model=list[AssessmentRead])
async def list_assessments(
    school_id: UUID,
    classroom_id: UUID | None = None,
    period: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Liste les évaluations d'une école, filtrables par classe et période."""
    stmt = select(Assessment).where(Assessment.school_id == school_id)
    if classroom_id is not None:
        stmt = stmt.where(Assessment.classroom_id == classroom_id)
    if period is not None:
        stmt = stmt.where(Assessment.period == period)
    stmt = stmt.order_by(Assessment.date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    payload: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée une évaluation."""
    assessment = Assessment(**payload.model_dump())
    db.add(assessment)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Référence invalide (école, matière ou classe).",
        )
    await db.refresh(assessment)
    return assessment
