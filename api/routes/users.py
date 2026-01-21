from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.users import (
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserPasswordUpdateRequestSchema,
    UserListResponseSchema,
)
from models.users import User
import logging

from utils.security import get_password_hash, get_user_or_404, authenticate_user_or_403


user_router = APIRouter(prefix="/api")


@user_router.post(
    "/users/",
    response_model=UserCreateResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreateRequestSchema, db: AsyncSession = Depends(get_db)
):
    new_user = User(**payload.model_dump())
    qs = await db.execute(select(User).where(User.username == new_user.username))
    user_exists = qs.scalar_one_or_none()
    if user_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Usuário já existe")

    new_user.password = get_password_hash(new_user.password)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception:
        await db.rollback()
        logging.error("Erro ao criar usuário", exc_info=True)
        raise


@user_router.put("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user_id: int,
    payload: UserPasswordUpdateRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_or_404(user_id=user_id, db=db)
    authenticate_user_or_403(user=user, password=payload.current_password)
    user.password = get_password_hash(password=payload.new_password)

    try:
        db.add(user)
        await db.commit()
    except Exception:
        logging.error("Falha ao atualizar senha do usuário")
        await db.rollback()
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.get(
    "/users/",
    response_model=list[UserListResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def list_users(db: AsyncSession = Depends(get_db)):
    qs = await db.execute(select(User))
    users = qs.scalars().all()
    return users


@user_router.delete("/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_or_404(user_id=user_id, db=db)
    try:
        await db.delete(user)
        await db.commit()
    except Exception:
        await db.rollback()
        logging.error("Erro ao deletar usuário")
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)
