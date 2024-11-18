from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from core.apps.users.entities import User


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, user: User, code: str) -> None:
        ...


class PushSenderService(BaseSenderService):
    def send_code(self, user: User, code: str) -> None:
        print(f"Sending push notification with token fcm_token to {user}")


class EmailSenderService(BaseSenderService):
    def send_code(self, user: User, code: str) -> None:
        print(f"Sending code {code} to {user} email")


@dataclass
class ComposedSenderService(BaseSenderService):
    sender_services: Iterable[BaseSenderService]

    def send_code(self, user: User, code: str) -> None:
        for service in self.sender_services:
            service.send_code(user, code)
