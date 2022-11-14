import requests
from http import HTTPStatus
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from market import settings


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate_header(self, request):
        return HTTPStatus.UNAUTHORIZED

    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if token != None and request.session.get("token") == token:
            data = request.session.get("user")
            return (User(id=data["id"], email=data["email"]), token)
        elif not token:
            return None

        response = requests.get(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={token}")
        
        if response.status_code != HTTPStatus.OK:
            raise exceptions.AuthenticationFailed("Invalid auth token!")
        
        data = response.json()

        request.session["user"] = data
        request.session["token"] = token

        user = User(id=data["id"], email=data["email"])
        return (user, token)


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):  # pragma nocover
    target_class = 'middlewares.authentication.JWTAuthentication'
    name = 'JWTAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }