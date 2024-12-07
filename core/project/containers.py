from functools import lru_cache

import punq

from core.apps.notifications.services.notification import (
    BaseNotificationService,
    ORMNotificationService,
)
from core.apps.posts.services.comment_likes import (
    BaseCommentLikeService,
    ORMCommentLikeService,
)
from core.apps.posts.services.comments import (
    BaseCommentService,
    ORMCommentService,
)
from core.apps.posts.services.post_likes import (
    BasePostLikeService,
    ORMPostLikeService,
)
from core.apps.posts.services.posts import (
    BasePostService,
    ORMPostService,
)
from core.apps.posts.use_cases.comments.create import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
)
from core.apps.posts.use_cases.posts.create import CreatePostUseCase
from core.apps.users.services.auth import (
    AuthService,
    BaseAuthService,
)
from core.apps.users.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.users.services.follow import (
    BaseFollowUserService,
    ORMFollowUserService,
)
from core.apps.users.services.senders import (
    BaseSenderService,
    ComposedSenderService,
    EmailSenderService,
)
from core.apps.users.services.users import (
    BaseUserService,
    ORMUserService,
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # initialize posts
    container.register(CreatePostUseCase)
    container.register(BasePostService, ORMPostService)

    container.register(BasePostLikeService, ORMPostLikeService)

    # initialize users
    container.register(BaseUserService, ORMUserService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(
        BaseSenderService,
        ComposedSenderService,
        sender_services=(
            # PushSenderService(),
            EmailSenderService(),
        ),
    )
    container.register(BaseAuthService, AuthService)

    container.register(BaseFollowUserService, ORMFollowUserService)

    container.register(BaseCommentService, ORMCommentService)
    container.register(CreateCommentUseCase)
    container.register(DeleteCommentUseCase)
    container.register(BaseCommentLikeService, ORMCommentLikeService)
    
    container.register(BaseNotificationService, ORMNotificationService)
    return container
