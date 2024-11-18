from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.users.services.codes import BaseCodeService
from core.apps.users.services.senders import BaseSenderService
from core.apps.users.services.users import BaseUserService


# TODO: выпилить бизнес логику и перенести в use case

@dataclass(eq=False)
class BaseAuthService(ABC):
    user_service: BaseUserService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, email: str):
        ...

    @abstractmethod
    def register(self, email: str, username: str, password: str):
        ...

    @abstractmethod
    def confirm(self, code: str, email: str):
        ...

    @abstractmethod
    def send_verification_code(self, email: str):
        ...


class AuthService(BaseAuthService):
    def register(self, email: str, username: str, password: str):
        user = self.user_service.create_user(email, username, password)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def authorize(self, email: str):
        user = self.user_service.get(email)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def send_verification_code(self, email: str):
        user = self.user_service.get(email)
        code = self.codes_service.generate_code(user)
        self.sender_service.send_code(user, code)

    def confirm(self, code: str, email: str):
        user = self.user_service.get(email)
        self.codes_service.validate_code(code, user)
        self.user_service.verify_email(email)
        return self.user_service.generate_token(user)
