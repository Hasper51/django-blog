from typing import Optional
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI, Schema

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api = NinjaAPI()

class UserSchema(Schema):
    username: str
    email: str
    first_name: str
    last_name: str

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {"message": "Please sign in first"}
    return request.user 

@api.get("/ping", response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(result=True)



class HelloResponseSchema(Schema):
    message: str = 'world'

@api.post("/hello")
def hello(request, data: HelloResponseSchema):
    return f'Hello {data.message}'

api.add_router('v1/', v1_router)

urlpatterns = [
    path("", api.urls),
]