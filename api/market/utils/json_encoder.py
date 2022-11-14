import json
import decimal
import datetime
from django.db import models

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, models.Model):
            return str(o.id)

        return super(CustomJSONEncoder, self).default(o)  # pragma nocover