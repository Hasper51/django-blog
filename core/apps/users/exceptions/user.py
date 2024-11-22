from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=False)
class UserTokenInvalid(ServiceException):
    token: str
    
    @property
    def message(self):
        return "A user with provided token is not found"
