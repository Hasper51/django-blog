from dataclasses import dataclass

from core.apps.common.exception import ServiceException


@dataclass(eq=False)
class PostNotFound(ServiceException):
    post_id: int
    
    @property
    def message(self):
        return "Product not found"
