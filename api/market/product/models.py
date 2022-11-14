import uuid
from django.db import models
from django.dispatch import receiver

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    ean = models.PositiveIntegerField(blank=False, null=False)
    image = models.CharField(max_length=250, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=False, null=False)
    min_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    max_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(min_cost__gte=0), name="min_cost__gte_0"),
            models.CheckConstraint(check=models.Q(max_cost__gte=0), name="max_cost__gte_0"),
            models.CheckConstraint(check=models.Q(min_cost__lte=models.F('max_cost')), name="min_cost__lte_max_cost")
        ]
