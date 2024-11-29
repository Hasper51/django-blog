from datetime import datetime
from typing import List

from ninja import Schema

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    username: str


class FollowCreateSchema(Schema):
    following_id: int


class FollowOutSchema(Schema):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime


class UnfollowOutSchema(Schema):
    message: str


class UserFollowersOut(Schema):
    total_followers: int
    followers: List[FollowOutSchema]


class FollowErrorSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    token: str


class TokenInSchema(Schema):
    email: str
    code: str


class SignInSchema(Schema):
    email: str
    password: str


class SignOutSchema(Schema):
    message: str


class SignUpSchema(Schema):
    email: str
    username: str
    password: str
