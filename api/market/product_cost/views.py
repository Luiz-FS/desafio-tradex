from product_cost import models, serializers
from rest_framework.permissions import IsAuthenticated
from middlewares.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from market import signals
from rest_framework import viewsets


class ProductCostViewSet(viewsets.ModelViewSet):
    queryset = models.ProductCost.objects.all().order_by('date')
    serializer_class = serializers.ProductCostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'product', 'date']

    def destroy(self, request, *args, **kwargs):
        user = request.user
        product_cost = self.get_object()

        signals.user_interaction.send(
            sender=self.__class__,
            name="delete_product_cost",
            user_email=user.email,
            entity_id=product_cost.id,
            data={}
        )

        return super().destroy(request, *args, **kwargs)
