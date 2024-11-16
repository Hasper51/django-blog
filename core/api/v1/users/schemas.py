from ninja import Schema


class AuthInSchema(Schema):
    email: str


class AuthOutSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    token: str


class TokenInSchema(Schema):
    email: str
    code: str
