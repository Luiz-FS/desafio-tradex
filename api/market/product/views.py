import uuid
from datetime import datetime
from http import HTTPStatus
from product import models, serializers
from rest_framework.permissions import IsAuthenticated
from middlewares.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from market import signals, settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser
from utils.verify_process_area import verify_process_area


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all().order_by('name')
    serializer_class = serializers.ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    @action(detail=True, methods=["POST"], parser_classes=(MultiPartParser, ))
    def upload_image(self, request: Request, pk: str=None) -> Response:
        user = request.user
        product = self.get_object()
        file = request.data.get('file')

        if not file:
            return Response(data={"detail": "File field is required"}, status=HTTPStatus.BAD_REQUEST)
        elif not file.content_type.startswith("image/"):
            return Response(data={"detail": "Only images are accepted"}, status=HTTPStatus.BAD_REQUEST)

        mime_type = file.content_type.split("/")[1]
        filename = f"{uuid.uuid4()}-{datetime.now().timestamp()}.{mime_type}"

        verify_process_area()
        
        with open(f"{settings.PROCESS_AREA}/{filename}", 'wb') as f:
            f.write(file.read())
        
        product.image = filename
        product.save()

        signals.user_interaction.send(
            sender=self.__class__,
            name="update_product",
            user_email=user.email,
            entity_id=product.id,
            data={"image": filename}
        )

        return Response(data=self.serializer_class(product).data, status=HTTPStatus.CREATED)


    def destroy(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()

        signals.user_interaction.send(
            sender=self.__class__,
            name="delete_product",
            user_email=user.email,
            entity_id=product.id,
            data={}
        )

        return super().destroy(request, *args, **kwargs)
