from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


async def get_user_or_404(user_id: int, db: AsyncSession):
    user_qs = await db.execute(select(User).where(User.id == user_id))
    user = user_qs.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    return user
