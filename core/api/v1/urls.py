# core\api\v1\urls.py
from ninja import Router

from core.api.v1.comments.handlers import router as comment_router
from core.api.v1.posts.handlers import router as post_router
from core.api.v1.users.follow_handlers import router as follow_router
from core.api.v1.users.handlers import router as user_router
from core.api.v1.users.login import router as auth_router


router = Router(tags=['v1'])

post_router.add_router('', comment_router)

router.add_router('posts/', post_router)
router.add_router('users/', user_router)
router.add_router('', auth_router)
router.add_router('', follow_router)
