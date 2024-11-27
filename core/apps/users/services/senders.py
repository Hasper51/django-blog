from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from django.conf import settings

from core.apps.users.entities import User
from core.apps.users.tasks import send_email_yandex


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, user: User, code: str) -> None:
        ...


class PushSenderService(BaseSenderService):
    def send_code(self, user: User, code: str) -> None:
        print(f"Sending push notification with token fcm_token to {user}")


class EmailSenderService(BaseSenderService):
    def send_code(self, user: User, code: str) -> None:
        send_email_yandex.delay(
            smtp_server='smtp.yandex.ru',
            smtp_port=465,
            user_email=settings.YANDEX_MAIL,
            recipient_email=user.email,
            user_password=settings.YANDEX_MAIL_PASSWORD,
            subject='Verification Code',
            body=code,
        )
        print(f"Sending code {code} to {user.email}")


@dataclass
class ComposedSenderService(BaseSenderService):
    sender_services: Iterable[BaseSenderService]

    def send_code(self, user: User, code: str) -> None:
        for service in self.sender_services:
            service.send_code(user, code)
