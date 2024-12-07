# core\api\v1\urls.py
from ninja import Router

from core.api.v1.comments.handlers import router as comment_router
from core.api.v1.posts.handlers import router as post_router
from core.api.v1.users.handlers.following import router as follow_router
from core.api.v1.users.handlers.handlers import router as user_router
from core.api.v1.notifications.handlers import router as notification_router

router = Router(tags=['v1'])

post_router.add_router('posts/', comment_router)

router.add_router('posts/', post_router)
router.add_router('', user_router)
router.add_router('users/', follow_router)
router.add_router('notifications/', notification_router)
