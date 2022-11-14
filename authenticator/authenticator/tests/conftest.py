import pytest
from django.contrib.auth.models import User


@pytest.fixture
def make_user():
    user = User.objects.create(**{
        "username": "jNFS9XqKZSyd",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string"
    })

    user.set_password("mYpAss3rd")
    user.save()

    return user
