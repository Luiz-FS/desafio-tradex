from rest_framework.views import exception_handler as handler
from django.db.utils import IntegrityError
from http import HTTPStatus
from rest_framework.response import Response

def exception_handler(exc, context):
    response = handler(exc, context)

    if isinstance(exc, IntegrityError):
        error_message = str(exc).split("\n")[0]
        response = Response(data={"detail": error_message}, status=HTTPStatus.BAD_REQUEST)

    return response