from pydantic import BaseModel


class GetTokenResponseSchema(BaseModel):
    access: str
    claims: dict


class GetTokenRequestSchema(BaseModel):
    username: str
    password: str


class VerifyTokenRequestSchema(BaseModel):
    token: str


class VerifyTokenResponseSchema(BaseModel):
    pass
