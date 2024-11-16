import factory
from factory.django import DjangoModelFactory

from core.apps.posts.models import Post


class PostModelFactory(DjangoModelFactory):
    image = factory.Faker("image_url")
    caption = factory.Faker("text")
    user = factory.SubFactory("tests.factories.users.UserModelFactory")

    class Meta:
        model = Post
