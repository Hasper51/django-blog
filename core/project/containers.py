from functools import lru_cache

import punq

from core.apps.posts.services.comments import (
    BaseCommentService,
    ORMCommentService,
)
from core.apps.posts.services.posts import (
    BasePostService,
    ORMPostService,
)
from core.apps.posts.use_cases.comments.create import CreateCommentUseCase, DeleteCommentUseCase
from core.apps.users.services.auth import (
    AuthService,
    BaseAuthService,
)
from core.apps.users.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.users.services.senders import (
    BaseSenderService,
    ComposedSenderService,
    EmailSenderService,
    PushSenderService,
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
    container.register(BasePostService, ORMPostService)

    # initialize users
    container.register(BaseUserService, ORMUserService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(
        BaseSenderService,
        ComposedSenderService,
        sender_services=(
            PushSenderService(),
            EmailSenderService(),
        ),
    )
    container.register(BaseAuthService, AuthService)
    container.register(BaseCommentService, ORMCommentService)
    container.register(CreateCommentUseCase)
    container.register(DeleteCommentUseCase)
    return container
