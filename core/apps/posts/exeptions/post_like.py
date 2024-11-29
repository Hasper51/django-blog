from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=False)
class LikeAlreadyExists(ServiceException):
    post_id: int
    user_id: int

    @property
    def message(self):
        return f"User with ID {self.user_id} has already liked post with ID {self.post_id}."


@dataclass(eq=False)
class LikeDoesNotExist(ServiceException):
    post_id: int
    user_id: int

    @property
    def message(self):
        return f"Like from user with ID {self.user_id} on post with ID {self.post_id} does not exist."
