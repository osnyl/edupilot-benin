from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("", response_model=list[UserRead])
async def list_users(
    school_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Liste les utilisateurs d'une école."""
    result = await db.execute(
        select(User).where(User.school_id == school_id).order_by(User.full_name)
    )
    return result.scalars().all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crée un utilisateur (mot de passe hashé)."""
    data = payload.model_dump()
    password = data.pop("password")
    data["password_hash"] = pwd_context.hash(password)
    user = User(**data)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un utilisateur avec cet email existe déjà dans cette école.",
        )
    await db.refresh(user)
    return user
