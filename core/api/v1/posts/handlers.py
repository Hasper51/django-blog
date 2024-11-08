#core\api\v1\posts\handlers.py
from django.http import HttpRequest
from ninja import Router
from core.api.v1.posts.schemas import PostListSchema, PostSchema
from core.apps.posts.services.posts import BasePostService, ORMPostService



router = Router(tags=['Posts'])

@router.get('', response=PostListSchema)
def get_post_list(request: HttpRequest) -> PostListSchema:
    service: BasePostService = ORMPostService()
    post_list  = service.get_post_list()
    return [PostSchema.from_entity(obj) for obj in post_list]