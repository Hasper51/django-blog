import pytest
from core.api.filters import PaginationIn
from core.api.v1.posts.filters import PostFilters
from core.apps.posts.services.posts import BasePostService
from tests.factories.posts import PostModelFactory


@pytest.mark.django_db
def test_get_post_count_zero(post_service: BasePostService):
    """
    Test post count zero without post in database
    """
    post_count = post_service.get_post_count(PostFilters())
    assert post_count == 0, f'{post_count=}'


@pytest.mark.django_db
def test_get_post_count_exist(post_service: BasePostService):
    """
    Test post count with post in database
    """
    # TODO: Add a post to the database and assert the count
    expected_count = 5
    PostModelFactory.create_batch(size=expected_count)

    post_count = post_service.get_post_count(PostFilters())
    assert post_count > 0, f'{post_count=}'


@pytest.mark.django_db
def test_get_post_all(post_service: BasePostService):
    """
    Test get all posts with pagination
    """
    expected_count = 5
    posts = PostModelFactory.create_batch(size=expected_count)
    posts_captions = {post.caption for post in posts}

    fetched_posts = post_service.get_post_list(PostFilters(), PaginationIn())
    fetched_posts_captions = {post.caption for post in fetched_posts}

    assert len(fetched_posts_captions) == expected_count, f'{fetched_posts_captions=}'
    assert posts_captions == fetched_posts_captions, f'{posts_captions=}'