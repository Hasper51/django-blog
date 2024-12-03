from dataclasses import dataclass

from core.apps.posts.entities.posts import Post as PostEntity
from core.apps.posts.services.posts import BasePostService
from core.apps.users.services.users import BaseUserService


@dataclass
class CreatePostUseCase:
    user_service: BaseUserService
    post_service: BasePostService

    def execute(
        self,
        user_id: int,
        post: PostEntity,
    ) -> PostEntity:
        user = self.user_service.get_by_id(user_id=user_id)
        saved_post = self.post_service.save_post(post=post, user=user)

        return saved_post


# @dataclass
# class DeleteCommentUseCase(CreateCommentUseCase):

#     def execute(self, comment_id: int, post_id: int, user_id: int) -> None:
#         user = self.user_service.get_by_id(user_id=user_id)
#         post = self.post_service.get_by_id(post_id=post_id)
#         comment = self.comment_service.get_by_id(comment_id=comment_id)
#         deleted_comment = self.comment_service.delete_comment(comment=comment, post=post, user=user)

#         return deleted_comment
