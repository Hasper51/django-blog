from datetime import datetime
from typing import List

from ninja import Schema

from pydantic import BaseModel

from core.apps.users.entities import (
    Following as FollowingEntity,
    User as UserEntity,
)


class FollowSchema(BaseModel):
    id: int # noqa
    follower_id: int
    following_id: int
    created_at: datetime

    @staticmethod
    def from_entity(entity: FollowingEntity) -> 'FollowSchema':
        return FollowSchema(
            id=entity.id,
            follower_id=entity.follower_id,
            following_id=entity.following_id,
            created_at=entity.created_at,
        )


class UserSchema(BaseModel):
    id: int # noqa
    username: str
    email: str
    created_at: datetime

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserSchema':
        return UserSchema(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            created_at=entity.date_joined,
        )


class FollowCreateSchema(Schema):
    following_id: int


class FollowOutSchema(Schema):
    id: int # noqa
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
