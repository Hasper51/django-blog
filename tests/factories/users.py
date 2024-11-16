import factory
from factory.django import DjangoModelFactory

from core.apps.users.models import User


class UserModelFactory(DjangoModelFactory):
    username = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    bio = factory.Faker("name")

    class Meta:
        model = User
