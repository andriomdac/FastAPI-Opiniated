from pydantic import BaseModel


class UserCreateRequestSchema(BaseModel):
    username: str
    password: str


class UserCreateResponseSchema(BaseModel):
    id: int
    username: str


class UserPasswordUpdateRequestSchema(BaseModel):
    current_password: str
    new_password: str


class UserPasswordUpdateResponseSchema(BaseModel):
    pass


class UserListResponseSchema(BaseModel):
    id: int
    username: str
