from fastapi import HTTPException, status
from passlib.hash import pbkdf2_sha256

from models.users import User


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(secret=password, hash=hash)


def authenticate_user_or_403(user: User, password: str):
    user_is_authencitated = verify_password(password=password, hash=user.password)
    if not user_is_authencitated:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuário/Senha inválido(s)")
