import json
from django.db import models
from product.models import BaseModel
from django.dispatch import receiver
from market import signals
from utils.json_encoder import CustomJSONEncoder


class Event(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    user_email = models.CharField(max_length=250, blank=False, null=False)
    entity_id = models.UUIDField()
    data = models.JSONField(encoder=CustomJSONEncoder, null=False)


@receiver(signals.user_interaction)
def save_user_event(sender, name, user_email, entity_id, data, **kwargs):
    Event.objects.create(
        name=name,
        user_email=user_email,
        entity_id=entity_id,
        data=data
    )
