from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=False)
class FollowingException(ServiceException):
    @property
    def message(self):
        return "Following exception occurred"


@dataclass(eq=False)
class FollowingExistsException(FollowingException):
    @property
    def message(self):
        return "Already following this user"


@dataclass(eq=False)
class FollowingNotExistException(FollowingException):
    @property
    def message(self):
        return "Not following this user"
