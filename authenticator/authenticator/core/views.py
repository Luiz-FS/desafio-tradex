
from http import HTTPStatus

from core.serializers import (CustomAuthTokenSerializer,
                              UserRegisterSerializer, UserSerializer)
from django.contrib.auth.models import User
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, parsers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class CustomAuthToken(ObtainAuthToken):
    """Authorizes the user and retrieve
    a json with the token and basic user infos.
    """

    parser_classes = (parsers.JSONParser,)
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class VerifyTokenView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("token", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
        responses=UserSerializer
    )
    def get(self, request, *args, **kwargs):
        token = request.query_params["token"]

        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user

            return Response(UserSerializer(user).data)
        except Token.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
