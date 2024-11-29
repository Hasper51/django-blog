from django.http import HttpRequest
from ninja.security import HttpBearer
from core.apps.users.services.auth import BaseAuthService
from core.project.containers import get_container

class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        container = get_container()
        service: BaseAuthService = container.resolve(BaseAuthService)
        user_id = service.verify_token(token)
        if user_id:
            request.user_id = user_id
            return token