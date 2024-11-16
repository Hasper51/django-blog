import pytest

from core.apps.posts.services.posts import (
    BasePostService,
    ORMPostService,
)


@pytest.fixture
def post_service() -> BasePostService:
    return ORMPostService()
