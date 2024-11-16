from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.users.services.codes import BaseCodeService
from core.apps.users.services.senders import BaseSenderService
from core.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class BaseAuthService(ABC):
    user_service: BaseUserService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, email: str):
        ...
    
    @abstractmethod
    def confirm(self, code: str, email: str):
        ...


class AuthService(BaseAuthService):
    def authorize(self, email: str):
        user = self.user_service.get_or_create(email)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def confirm(self, code: str, email: str):
        user = self.user_service.get(email)
        self.codes_service.validate_code(code, user)
        return self.user_service.generate_token(user)    
