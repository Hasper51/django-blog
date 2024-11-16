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
from core.api.v1.posts.schemas import PostSchema
from core.apps.posts.services.posts import (
    BasePostService,
    ORMPostService,
)


router = Router(tags=['Posts'])


@router.get('', response=ApiResponce[ListPaginatedResponce[PostSchema]])
def get_post_list_handler(
    request: HttpRequest,
    filters: Query[PostFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponce[ListPaginatedResponce[PostSchema]]:
    service: BasePostService = ORMPostService()
    post_list = service.get_post_list(filters=filters, pagination=pagination_in)
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
