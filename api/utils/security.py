from fastapi import HTTPException, status
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(secret=password, hash=hash)


async def get_user_or_404(user_id: int, db: AsyncSession):
    user_qs = await db.execute(select(User).where(User.id == user_id))
    user = user_qs.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    return user


def authenticate_user_or_403(user: User, password: str):
    user_is_authencitated = verify_password(password=password, hash=user.password)
    if not user_is_authencitated:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Recurso não autorizado")
