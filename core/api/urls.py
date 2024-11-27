from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI
from ninja.security import (
    HttpBasicAuth,
    HttpBearer,
)

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api = NinjaAPI(csrf=True)


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == "admin" and password == "secret":
            return username


@api.get("/basic", auth=BasicAuth())
def basic(request):
    return {"httpuser": request.auth}


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "ZsKJQZ5oRTA9dUFz507GhbukpJpVf60O":
            return token


@api.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}


@api.get("/ping", response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(result=True)


api.add_router('v1/', v1_router)


urlpatterns = [
    path("", api.urls),
    

]
