from dataclasses import dataclass

from core.apps.posts.entities.comments import Comment as CommentEntity
from core.apps.posts.services.comments import BaseCommentService
from core.apps.posts.services.posts import BasePostService
from core.apps.users.services.users import BaseUserService


@dataclass
class CreateCommentUseCase:
    comment_service: BaseCommentService
    user_service: BaseUserService
    post_service: BasePostService
    # validator_service: BaseCommentValidatorService

    def execute(
        self,
        post_id: int,
        user_token: str,
        comment: CommentEntity,
    ) -> CommentEntity:
        user = self.user_service.get_by_token(token=user_token)
        post = self.post_service.get_by_id(post_id=post_id)
        saved_comment = self.comment_service.save_comment(post=post, user=user, comment=comment)
        
        return saved_comment
