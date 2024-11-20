from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=False)
class CommentNotFound(ServiceException):
    comment_id: int
    
    @property
    def message(self):
        return "Comment not found"
