# core\api\v1\urls.py
from ninja import Router

from core.api.v1.posts.handlers import router as post_router
from core.api.v1.users.handlers import router as user_router


router = Router(tags=['v1'])
router.add_router('posts/', post_router)
router.add_router('users/', user_router)
