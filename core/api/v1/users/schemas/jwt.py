from datetime import datetime
from typing import Optional
from ninja import Schema


class TokenSchema(Schema):
    access_token: str
    refresh_token: str
    token_type: str= "Bearer"


class TokenPayload(Schema):
    sub: Optional[int] = None
    exp: Optional[datetime] = None


class AuthInSchema(Schema):
    email: str
    password: str


class AuthOutSchema(Schema):
    message: str


class UserCreate(AuthInSchema):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(Schema):
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime