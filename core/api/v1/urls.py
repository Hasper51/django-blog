#core\api\v1\urls.py
from ninja import Router
from core.api.v1.posts.handlers import router as post_router
router = Router(tags=['v1'])
router.add_router('posts/', post_router)