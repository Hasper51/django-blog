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


class SignInSchema(Schema):
    email: str
    password: str


class SignOutSchema(Schema):
    message: str


class SignUpSchema(Schema):
    email: str
    username: str
    password: str
