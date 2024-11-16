from abc import ABC, abstractmethod

from core.apps.users.entities import UserEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, user: UserEntity, code: str) -> None:
        ... 


class DummySenderService(BaseSenderService):
    def send_code(self, user: UserEntity, code: str) -> None:
        print(f"Sending code {code} to {user}")