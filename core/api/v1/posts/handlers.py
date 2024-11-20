# core\api\v1\posts\handlers.py
from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.schemas import (
    ApiResponce,
    ListPaginatedResponce,
    PaginationOut,
)
from core.api.v1.posts.filters import PostFilters
from core.api.v1.posts.schemas import PostInSchema, PostOutSchema, PostSchema
from core.apps.posts.filters.posts import PostFilters as PostFiltersEntity
from core.apps.posts.services.posts import BasePostService
from core.project.containers import get_container

from ninja.security import django_auth

router = Router(tags=['Posts'])


@router.get('', response=ApiResponce[ListPaginatedResponce[PostSchema]])
def get_post_list_handler(
    request: HttpRequest,
    filters: Query[PostFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponce[ListPaginatedResponce[PostSchema]]:
    container = get_container()
    service: BasePostService = container.resolve(BasePostService)
    post_list = service.get_post_list(filters=PostFiltersEntity(search=filters.search), pagination=pagination_in)
    post_count = service.get_post_count(filters=filters)
    items = [PostSchema.from_entity(obj) for obj in post_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=post_count,
    )
    return ApiResponce(
        data=ListPaginatedResponce(items=items, pagination=pagination_out),
    )


@router.post('{post_id}/delete', response=ApiResponce[PostOutSchema], operation_id='deletePost', auth=django_auth)
def del_post_handler(request: HttpRequest, schema: Query[PostInSchema]) -> ApiResponce[PostOutSchema]:
    container = get_container()
    service: BasePostService = container.resolve(BasePostService)
    service.delete_post(post_id=schema.post_id, user_id=schema.user_id)
    return ApiResponce(
        data=PostOutSchema(
            message=f'User {schema.user_id} deleted post {schema.post_id}')
    )
