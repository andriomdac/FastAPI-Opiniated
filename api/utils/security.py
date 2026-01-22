import logging
from fastapi import HTTPException, Request, status
from passlib.hash import pbkdf2_sha256

from models.users import User
import os
from jwt.exceptions import DecodeError, ExpiredSignatureError
import jwt


def get_password_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(secret=password, hash=hash)


def authenticate_user_or_401(user: User, password: str):
    user_is_authencitated = verify_password(password=password, hash=user.password)
    if not user_is_authencitated:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário/Senha inválido(s)")


def get_jwt_env_variables():
    secret = os.getenv("SECRET")
    algorithm = os.getenv("ALGORITHM")
    if not all([secret, algorithm]):
        logging.error("Erro ao buscar variável de ambiente SECRET e/ou ALGORITHM")
        raise
    return {"secret": secret, "algorithm": algorithm}


def generate_token(payload: dict) -> str:
    env = get_jwt_env_variables()
    return jwt.encode(
        payload=payload,
        key=env["secret"],
    )


def get_token_claims(token: str) -> dict:
    validate_token(token=token)
    return jwt.decode(token)


def validate_bearer(request: Request):
    authorization = request.headers.get("Authorization")
    token = ""
    if authorization:
        token = authorization.split(" ")[1]
        if not token:
            token = ""
    validate_token(token=token)


def validate_token(token: str):
    env = get_jwt_env_variables()
    try:
        jwt.decode(jwt=token, key=env["secret"], algorithms=env["algorithm"])
    except DecodeError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido")
    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expirado")
