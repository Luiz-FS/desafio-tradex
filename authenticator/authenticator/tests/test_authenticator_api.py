from http import HTTPStatus
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core import serializers


@pytest.mark.django_db
class TestUserRegisterView:
    def test_create(self, client):
        response = client.post("/auth/register", {
                "username": "jNFS9XqKZSyd",
                "password": "mYpAss3rd",
                "confirm_pswd": "mYpAss3rd",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string"
            },
            content_type="application/json"
        )

        data = response.json()
        user = User.objects.get(username=data["username"])
        user_raw = serializers.UserRegisterSerializer(user).data

        assert data == user_raw
    
    def test_create_password_not_match(self, client):
        expected = {"password": ["Password fields didn't match."]}
        response = client.post("/auth/register", {
                "username": "jNFS9XqKZSyd",
                "password": "mYpAss3rd",
                "confirm_pswd": "dasdasdsda",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string"
            },
            content_type="application/json"
        )

        data = response.json()

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data == expected
    
    def test_create_required_field(self, client):
        expected = {"email": ['This field is required.']}
        response = client.post("/auth/register", {
                "username": "jNFS9XqKZSyd",
                "password": "mYpAss3rd",
                "confirm_pswd": "dasdasdsda",
                "first_name": "string",
                "last_name": "string"
            },
            content_type="application/json"
        )

        data = response.json()

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data == expected


@pytest.mark.django_db
class TestCustomAuthToken:
    def test_get_token(self, client, make_user):

        response = client.post("/auth/api-token-auth/", {
                "username": "jNFS9XqKZSyd",
                "password": "mYpAss3rd"
            },
            content_type="application/json"
        )
        data = response.json()

        token = Token.objects.get(user_id=make_user.id)
        expected = {
            "token": token.key,
            "first_name": make_user.first_name,
            "last_name": make_user.last_name,
            "email": make_user.email,
            "user_id": make_user.pk,
            "is_admin": make_user.is_staff
        }

        assert data == expected
    
    @pytest.mark.parametrize(
        "request_data,expected",
        [
           (
                {
                    "username": "test",
                    "password": "mYpAss3rd"
                },
                {
                    "non_field_errors": [
                        "Unable to log in with provided credentials."
                    ]
                }
           ),
           (
                {
                    "username": "jNFS9XqKZSyd",
                    "password": "test"
                },
                {
                    "non_field_errors": [
                        "Unable to log in with provided credentials."
                    ]
                }
           ),
           (
                {},
                {
                    "username": ["This field is required."],
                    "password": ["This field is required."]
                }

           )
        ]
    )
    def test_get_token_invalid_credentials(self, client, make_user, request_data, expected):
        response = client.post("/auth/api-token-auth/", request_data,
            content_type="application/json"
        )
        data = response.json()

        assert data == expected
        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
class TestVerifyTokenView:
    def test_retrieve_user(self, client, make_user):
        token = Token.objects.create(user=make_user)
        expected = serializers.UserSerializer(make_user).data

        response = client.get(f"/auth/verify?token={token.key}")
        data = response.json()

        assert data == expected
    
    def test_retrieve_user_token_not_found(self, client):

        response = client.get("/auth/verify?token=fdsfdsfdsfdsf")

        assert response.status_code == HTTPStatus.NOT_FOUND