import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from models.users import User
from utils.security import (
    authenticate_user_or_401,
    generate_token,
    validate_token,
)
from schemas.token import (
    GetTokenResponseSchema,
    GetTokenRequestSchema,
    VerifyTokenRequestSchema,
    VerifyTokenResponseSchema,
)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os


token_router = APIRouter(prefix="/api/token")


def get_time_zone_env() -> str:
    tz = os.getenv("TIMEZONE_INFO")
    if not tz:
        logging.error("Erro ao buscar variável de ambiente TIMEZONE_INFO")
        raise
    return tz


def get_token_expire_time() -> dict:
    access = os.getenv("TOKEN_ACCESS_EXPIRES")
    refresh = os.getenv("TOKEN_REFRESH_EXPIRES")
    if not all([access, refresh]):
        logging.error(
            "Erro ao buscar variável de ambiente TOKEN_ACCESS_EXPIRES/TOKEN_REFRESH_EXPIRES"
        )
        raise
    return {"access": access, "refresh": refresh}


@token_router.post("/", response_model=GetTokenResponseSchema)
async def get_token(payload: GetTokenRequestSchema, db: AsyncSession = Depends(get_db)):
    qs = await db.execute(select(User).where(User.username == payload.username))
    user = qs.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuário não encontrado")
    authenticate_user_or_401(user=user, password=payload.password)

    claims = {}
    claims["sub"] = str(user.id)
    claims["exp"] = datetime.now(ZoneInfo(get_time_zone_env())) + timedelta(
        minutes=int(get_token_expire_time()["access"])
    )
    return {"access": generate_token(payload=claims), "claims": claims}


@token_router.post("/verify/", response_model=VerifyTokenResponseSchema)
async def verify_token(payload: VerifyTokenRequestSchema):
    validate_token(token=payload.token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
