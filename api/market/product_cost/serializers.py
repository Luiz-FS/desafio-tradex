from product_cost import models
from rest_framework import serializers
from market import signals


class ProductCostSerializer(serializers.ModelSerializer):
    def __send_user_signal(self, name, entity_id, data):
        if self.context.get("request"):
            user = self.context["request"].user

            signals.user_interaction.send(
                sender=self.__class__,
                name=name,
                user_email=user.email,
                entity_id=entity_id,
                data=data
            )


    def create(self, validated_data):
        obj = super().create(validated_data)

        if self.is_valid():
            self.__send_user_signal(
                name="create_product_cost",
                entity_id=obj.id,
                data=validated_data
            )

        return obj

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)

        if self.is_valid():
            self.__send_user_signal(
                name="update_product_cost",
                entity_id=obj.id,
                data=validated_data
            )

        return obj


    class Meta:
        model = models.ProductCost
        fields = '__all__'